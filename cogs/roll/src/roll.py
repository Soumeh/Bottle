from typing import Optional
from principality.cog import  Cog, SlashOption
from nextcord import Embed
from random import choice

class Roll(Cog):

    @Cog.slash_command(guild_ids=[802577295960571907, 418105205100642315])
    async def roll(self, ctx,
        number: int = SlashOption(description="What number to roll.", min_value=1, max_value=1000),
        multiplier: Optional[int] = SlashOption(description="How many times to roll.", min_value=1, max_value=30, default=1)
    ):
        description = f"{ctx.user.mention} rolled "
        if multiplier == 1:
            num = choice(range(1, number+1))
            description += f"a D{number}, and it landed on **{num}**!"
        else:
            nums = [choice(range(1, number+1)) for i in range(multiplier)]
            description += f"{multiplier} D{number}s, and they landed on {', '.join([f'**{i}**' for i in nums])}! [{sum(nums)}]"

        await ctx.response.send_message(embed=Embed(description=description))
        return