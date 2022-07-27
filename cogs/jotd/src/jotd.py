from principality.cog import Cog
from nextcord import Embed
from random import seed, choice
from datetime import date

class Jester_Of_The_Day(Cog):

    @Cog.slash_command()
    async def jotd(self, ctx):
        """Shows the server's Jester of the Day, now point and laugh at them!"""
        jester = self.jester_of_the_day(ctx.guild)
        await ctx.send(embed=Embed(description=f"**{ctx.guild.name}**'s Jester of the Day is {jester.mention}!"))

    def jester_of_the_day(self, server):
        today = date.today()
        seed(today)
        return choice(server.members)