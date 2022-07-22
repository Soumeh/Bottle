from principality.cog import Cog
from nextcord import Embed
from random import seed, choice
from datetime import date

class Jester_Of_The_Day(Cog):

    @Cog.slash_command(guild_ids=[802577295960571907, 418105205100642315, 292703237755240448])
    async def jotd(self, ctx):
        """Shows the server's Jester of the Day, now point and laugh at them!"""
        jester = self.jester_of_the_day(ctx.guild)
        await ctx.send(Embed(description=f"**{ctx.guild.name}**'s Jester of the Day is {jester.mention}!"))
    
    def jester_of_the_day(self, server):
        today = date.today()
        seed(today)
        return choice(server.members)