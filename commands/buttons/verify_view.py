import nextcord

VIEW_NAME = "VerifyView"
VERIFY_ID = "942461296836759592"

class VerifyView(nextcord.ui.View):
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
    
    @nextcord.ui.button(label="Verify", emoji="✅", style=nextcord.ButtonStyle.primary, custom_id=custom_id(VIEW_NAME, VERIFY_ID))
    async def VERIFY_button(self, button, interaction):
        await self.handle_click(button, interaction)