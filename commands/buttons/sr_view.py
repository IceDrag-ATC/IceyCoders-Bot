import nextcord

VIEW_NAME = "SRView"
HELPERNS_ID = "942882061751029780"
ALERTS_ID = "942882077303525377"
YTF_ID = "942882082055663637"

class SRView(nextcord.ui.Button):
    def __init__(self):
        super().__init__(timeout=None)

    async def handle_click(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        role_id=int(button.custom_id.split(":")[-1])
        role = interaction.guild.get_role(role_id)
        assert isinstance(role, nextcord.Role)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"Your {role.name} role has been removed.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have been given the {role.name} role.", ephemeral=True)

    def custom_id(view: str, id: int) -> str:
        return f"{view}:{id}"
    
    @nextcord.ui.button(label="Helpers (NOT STAFF)", style=nextcord.ButtonStyle.primary, custom_id='SRView:942882061751029780')
    async def HELPERSNS_button(self, button, interaction):
        await self.handle_click(button, interaction)
    
    @nextcord.ui.button(label="Announcements Ping", style=nextcord.ButtonStyle.secondary, custom_id='SRView:942882077303525377')
    async def ALERTS_button(self, button, interaction):
        await self.handle_click(button, interaction)
    
    @nextcord.ui.button(label="Youtube Notifications", style=nextcord.ButtonStyle.red, custom_id='SRView:942882082055663637')
    async def YTF_button(self, button, interaction):
        await self.handle_click(button, interaction)