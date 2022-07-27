from principality.cog import  Cog, SlashOption
from nextcord.abc import GuildChannel
from nextcord import Embed, ChannelType

from datetime import timedelta, datetime
from random import randint
from principality.utils import message_as_embed

class Random_Message(Cog):

    @Cog.slash_command()
    async def randmsg(self, ctx,
        channel: GuildChannel = SlashOption(description="What channel to get the message from.", channel_types=[ChannelType.text])
    ):
        if channel.nsfw and not ctx.channel.nsfw:
            return await ctx.response.send_message(embed=Embed(description="Messages from NSFW channels are exclusive."), ephemeral=True)
        message = await self.get_random_message(channel)
        embed = message_as_embed(message)
        await ctx.response.send_message(embed=embed)
    
    async def get_random_message(self, channel):

        date = self.random_date(datetime.now().astimezone(), channel.created_at)
        messages = channel.history(limit=32, oldest_first=True, after=date)
        if not messages:
            messages = channel.history(limit=32, oldest_first=True, before=date)
        if not messages: return None
        messages = await messages.flatten()
        return messages[randint(0, len(messages)-1)]
    
    def random_date(self, start, end):
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randint(int_delta, 0)
        return start + timedelta(seconds=random_second)