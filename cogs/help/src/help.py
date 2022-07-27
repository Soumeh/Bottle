from principality.cog import  Cog, ConfigOption, SlashOption
from nextcord import Embed

class Help(Cog):

    class Config:
        information: str = ConfigOption('test', "Write your bot's basic information here.")
        modules_per_page: int = ConfigOption(6, "How many modules should be displayed per page?")

    async def ready(self):
        self.cog_pages = self._split_every(list(self.bot.cogs.keys()), self.config.modules_per_page)

    @Cog.slash_command()
    async def help(self, ctx,
        cog: str = SlashOption(description="What Cog to get help for")
    ):
        "Bring up... idk"
        cog = cog.replace(' ', '_')
        await ctx.send(embed=self.cog_menu(page), ephemeral=False)

    @Cog.slash_command()
    async def cogs(self, ctx, 
        page: int = SlashOption(description='What page of the modules to display', default=1)
    ):
        """List and explain Cogs"""
        await ctx.send(embed=self.cog_list(page), ephemeral=False)
    
    def cog_menu(self, cog: Cog) -> Embed:
        embed = {"title": f"{cog.metadata.name.replace('_', ' ')} Cog"}

        return Embed.from_dict(embed)

    def cog_list(self, page: int = 1) -> Embed:
        # title
        embed = {"title": f"Loaded Cogs: [{page}/{self.cog_pages}]"}

        # fields
        embed['fields'] = []
        cogs = list(self.bot.cogs.values())
        min_page = (page-1)*self.config.modules_per_page
        max_page = min_page+self.config.modules_per_page
        for cog in cogs[min_page:max_page]:
            name = cog.metadata.name.replace('_', ' ')
            description = cog.metadata.description
            author = self.metadata.author
            description += f'\n\n*by {", ".join([i["name"] for i in cog.metadata.authors])}*'
            embed['fields'].append({'name': name, 'value': description, 'inline': True})
        return Embed.from_dict(embed)

    def _split_every(self, list: list, count: int) -> int:
        return len([list[i::i+count] for i in range(0, len(list), count)])