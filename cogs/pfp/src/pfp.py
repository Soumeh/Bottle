from principality.cog import  Cog, SlashOption
from nextcord import Embed, User

class Profile_Picture(Cog):

    @Cog.slash_command(guild_ids=[802577295960571907, 418105205100642315])
    async def pfp(self, ctx,
        member: User = SlashOption(description="What user to get the profile picture of", default='user'),
        private: bool = SlashOption(description="Whether or not to privately get the profile picture", default=False, required=False)
    ):
        if member == 'user': member = ctx.user
        embed = Embed(description=f"{member.mention}'s Profile Picture:")
        embed.set_image(url=member.display_avatar.url)
        await ctx.response.send_message(embed=embed, ephemeral=True)
    
    @Cog.user_command(name="Get Profile Picture", guild_ids=[802577295960571907, 418105205100642315])
    async def get_pfp(self, ctx, user):
        embed = Embed(description=f"{user.mention}'s Profile Picture:")
        embed.set_image(url=user.display_avatar.url)
        await ctx.response.send_message(embed=embed)

    @Cog.user_command(name="Get Profile Picture (Private)", guild_ids=[802577295960571907, 418105205100642315])
    async def get_pfp_private(self, ctx, user):
        embed = Embed(description=f"{user.mention}'s Profile Picture:")
        embed.set_image(url=user.display_avatar.url)
        await ctx.response.send_message(embed=embed, ephemeral=True)