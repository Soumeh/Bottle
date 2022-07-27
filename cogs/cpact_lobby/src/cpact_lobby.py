from nextcord import Embed
from principality.cog import  Cog, ConfigOption

from cpact_watcher import Counterpact_Lobby

class Counterpact_Status(Cog):

    class Config:
        lobby_ip: str = ConfigOption('', "The IP to fetch lobby data from. Currently, the Counterpact lobby's information is private, so you will have to ask the developer for help. (Unless you are the developer, in which case, you probably know what to do)")
        lobby_port: int = ConfigOption(0, "Refer to comment above.")

    async def ready(self):
        self.cpact_lobby = Counterpact_Lobby(self.config.lobby_ip, self.config.lobby_port)

    @Cog.slash_command()
    async def lobby(self, ctx):

        self.cpact_lobby.refresh()
        embed = Embed(
            title="Counterpact Lobby Status",
            color=0x6415ba,
            timestamp=self.cpact_lobby.last_check,
            url='http://discord.gg/gfKpVCv7Qd'
        )
        embed.set_footer(text="Last Updated")
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/964252632023703582/977969364823318558/icon.png')

        if self.cpact_lobby.total_players == 1: embed.description = f"There is **{self.cpact_lobby.total_players}** player online."
        else: embed.description = f"There are **{self.cpact_lobby.total_players}** players online."
        if ctx.user.id == 685507245777354877: embed.description = embed.description.replace('online', 'among us')

        for server in self.cpact_lobby.servers:
            embed.add_field(
                name = server.name,
                value = f"""```hs
Players: {server.players}/{server.max_players}
Map: {server.map_name}```""",
                inline = False,
            )

        await ctx.response.send_message(embed=embed)