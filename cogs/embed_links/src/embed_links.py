from principality.cog import  Cog
from principality.utils import message_as_embed

class Embed_Links(Cog):

    @Cog.listener()
    async def on_message(self, message):
        args = message.content.lower()
        if 'https://' in args and 'discord' in args:
            for word in args.split():
                if 'https://' not in word:
                    continue
                domain = word.split('https://', 1)[1].split('.com/channels/', 1)[0]
                if 'discord' in domain and 'cdn' not in domain:
                    try:
                        linked_message = await self.url_to_message(word)
                    except:
                        linked_message = None
                    if linked_message:
                        result = message_as_embed(linked_message)
                        if isinstance(result, list):
                            return await message.reply(embeds=result)
                        await message.reply(embed=result)
    
    @Cog.message_command(name="Embed Message")
    async def embed_message(self, ctx, message):
        print(message)
        embed = message_as_embed(message)
        await ctx.response.send_message(embed=embed)

    async def url_to_message(self, url):
        try:
            data = url.split('/channels/')[1].split('/')
        except IndexError:
            return None
        channel = await self.bot.fetch_channel(int(data[1]))
        return await channel.fetch_message(int(data[2]))