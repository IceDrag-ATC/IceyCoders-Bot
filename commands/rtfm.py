import io
import os
import re
import zlib
from typing import Dict

import nextcord as discord
from nextcord.ext import commands, fuzzy

class SphinxObjectFileReader:
    # Inspired by Sphinx's InventoryFileReader
    BUFSIZE = 16 * 1024

    def __init__(self, buffer):
        self.stream = io.BytesIO(buffer)

    def readline(self):
        return self.stream.readline().decode("utf-8")

    def skipline(self):
        self.stream.readline()

    def read_compressed_chunks(self):
        decompressor = zlib.decompressobj()
        while True:
            chunk = self.stream.read(self.BUFSIZE)
            if len(chunk) == 0:
                break
            yield decompressor.decompress(chunk)
        yield decompressor.flush()

    def read_compressed_lines(self):
        buf = b""
        for chunk in self.read_compressed_chunks():
            buf += chunk
            pos = buf.find(b"\n")
            while pos != -1:
                yield buf[:pos].decode("utf-8")
                buf = buf[pos + 1 :]
                pos = buf.find(b"\n")


class Rtfm(commands.Cog):
    """Commands for fetching Python library documentation"""

    # full credit to https://github.com/Rapptz/RoboDanny
    def __init__(self, client):
        self.client = client

    def parse_object_inv(self, stream: SphinxObjectFileReader, url: str) -> Dict:
        result = {}
        inv_version = stream.readline().rstrip()

        if inv_version != "# Sphinx inventory version 2":
            raise RuntimeError("Invalid objects.inv file version.")

        projname = stream.readline().rstrip()[11:]
        stream.readline().rstrip()[11:]  # version line is not needed

        line = stream.readline()
        if "zlib" not in line:
            raise RuntimeError("Invalid objects.inv file, not z-lib compatible.")

        entry_regex = re.compile(r"(?x)(.+?)\s+(\S*:\S*)\s+(-?\d+)\s+(\S+)\s+(.*)")
        for line in stream.read_compressed_lines():
            match = entry_regex.match(line.rstrip())
            if not match:
                continue

            name, directive, prio, location, dispname = match.groups()
            domain, _, subdirective = directive.partition(":")
            if directive == "py:module" and name in result:
                continue

            if directive == "std:doc":
                subdirective = "label"

            if location.endswith("$"):
                location = location[:-1] + name

            key = name if dispname == "-" else dispname
            prefix = f"{subdirective}:" if domain == "std" else ""

            key = (
                key.replace("nextcord.ext.commands.", "")
                .replace("nextcord.ext.menus.", "")
                .replace("nextcord.ext.ipc.", "")
                .replace("nextcord.", "")
            )

            result[f"{prefix}{key}"] = os.path.join(url, location)

        return result

    async def build_rtfm_lookup_table(self, page_types):
        cache = {}
        for key, page in page_types.items():
            sub = cache[key] = {}
            async with self.client.session.get(page + "/objects.inv") as resp:
                if resp.status != 200:
                    raise RuntimeError(
                        "Cannot build rtfm lookup table, try again later."
                    )

                stream = SphinxObjectFileReader(await resp.read())
                cache[key] = self.parse_object_inv(stream, page)

        self._rtfm_cache = cache

    async def do_rtfm(self, ctx, key, obj):
        page_types = {
            "python": "https://docs.python.org/3",
            "nextcord": "https://nextcord.readthedocs.io/en/latest",
            "menus": "https://nextcord-ext-menus.readthedocs.io/en/latest",
            "ipc": "https://nextcord-ext-ipc.readthedocs.io/en/latest",
            "dpy": "https://discordpy.readthedocs.io/en/latest",
            "dpy2": "https://discordpy.readthedocs.io/en/master",
            "pycord": "https://docs.pycord.dev/en/master",
            "edpy": "https://enhanced-dpy.readthedocs.io/en/latest",
            "disnake": "https://disnake.readthedocs.io/en/latest",
        }

        if obj is None:
            await ctx.send(page_types[key])
            return

        if not hasattr(self, "_rtfm_cache"):
            await ctx.trigger_typing()
            await self.build_rtfm_lookup_table(page_types)

        obj = re.sub(r"^(?:discord\.(?:ext\.)?)?(?:commands\.)?(.+)", r"\1", obj)
        obj = re.sub(r"^(?:nextcord\.(?:ext\.)?)?(?:commands\.)?(.+)", r"\1", obj)

        if key.startswith("master"):
            # point the abc.Messageable types properly:
            q = obj.lower()
            for name in dir(discord.abc.Messageable):
                if name[0] == "_":
                    continue
                if q == name:
                    obj = f"abc.Messageable.{name}"
                    break

        cache = list(self._rtfm_cache[key].items())

        matches = fuzzy.finder(obj, cache, key=lambda t: t[0], lazy=False)[:8]

        e = discord.Embed(colour=discord.Colour.blurple())
        if len(matches) == 0:
            return await ctx.send("Could not find anything. Sorry.")

        e.description = "\n".join(f"[`{key}`]({url})" for key, url in matches)
        ref = ctx.message.reference
        refer = None
        if ref and isinstance(ref.resolved, discord.Message):
            refer = ref.resolved.to_reference()
        await ctx.send(embed=e, reference=refer)

    @commands.group(name="rtfm", aliases=["rtfd"], invoke_without_command=True)
    async def rtfm_group(self, ctx: commands.Context, *, obj: str = None):
        """Retrieve documentation on Python libraries"""
        await self.do_rtfm(ctx, "nextcord", obj)

    @rtfm_group.command(name="menus")
    async def rtfm_menus_cmd(self, ctx: commands.Context, *, obj: str = None):
        await self.do_rtfm(ctx, "menus", obj)

    @rtfm_group.command(name="ipc")
    async def rtfm_ipc_cmd(self, ctx: commands.Context, *, obj: str = None):
        await self.do_rtfm(ctx, "ipc", obj)

    @rtfm_group.command(name="python", aliases=["py"])
    async def rtfm_python_cmd(self, ctx: commands.Context, *, obj: str = None):
        await self.do_rtfm(ctx, "python", obj)

    @rtfm_group.command(name="discord.py", aliases=["dpy"])
    async def rtfm_dpy_cmd(self, ctx: commands.Context, *, obj: str = None):
        await self.do_rtfm(ctx, "dpy", obj)

    @rtfm_group.command(name="dpy2")
    async def rtfm_dpy2_cmd(self, ctx: commands.Context, *, obj: str = None):
        await self.do_rtfm(ctx, "dpy2", obj)

    @rtfm_group.command(name="pycord")
    async def rtfm_pycord_cmd(self, ctx: commands.Context, *, obj: str = None):
        await self.do_rtfm(ctx, "pycord", obj)

    @rtfm_group.command(name="edpy")
    async def rtfm_edpy_cmd(self, ctx: commands.Context, *, obj: str = None):
        await self.do_rtfm(ctx, "edpy", obj)

    @rtfm_group.command(name="disnake")
    async def rtfm_disnake_cmd(self, ctx: commands.Context, *, obj: str = None):
        await self.do_rtfm(ctx, "disnake", obj)

    @commands.command(help="delete cache of rtfm", aliases=["purge-rtfm", "delrtfm"])
    @commands.is_owner()
    async def rtfmcache(self, ctx: commands.Context):
        del self._rtfm_cache
        embed = discord.Embed(title="Purged rtfm cache.", color=discord.Color.blurple())
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Rtfm(client))