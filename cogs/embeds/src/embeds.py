from nextcord import Embed, Interaction
from typing import List, Dict, Literal
from json import loads, dumps, JSONDecodeError

from principality.cog import Cog, ConfigOption, SlashOption
from principality.utils import url_to_json

class Embeds(Cog):

    class Config:
        embeds: Dict[str, Literal[Dict, List[Dict]]] = ConfigOption([{'embed_id': {"description": "This is an example embed."}}])
        channel_embeds: Dict[str, Literal[Dict, List[Dict]]] = ConfigOption([{'0000000000000000': {"description": "This is an example channel embed."}}])

    @Cog.message_command("Get Embed JSON", guild_ids=[802577295960571907])
    async def json_from_message(self, ctx, message):
        embeds = message.embeds or []
        for embed in embeds:
            json = dumps(embed.to_dict(), indent=2)
            message = f'```json\n{json}\n```'
            return await ctx.response.send_message(embed=Embed(description=""), ephemeral=True)

    @Cog.slash_command(guild_ids=[802577295960571907])
    async def embed(self, ctx):
        pass

    @embed.subcommand()
    async def get(self, ctx, id: str = SlashOption(description="The ID of the embed from the config file")):
        """Send an embed from locally stored embed data"""
        embed_data = self.config.embeds.get(id, None)
        if not embed_data: return await ctx.send(embed=Embed(description="This ID doesn't exist, give it embed data in the `embeds.toml` config file"), ephemeral=True)
        await self.send_embeds(ctx, embed_data)

    @embed.subcommand()
    async def new(self, ctx, json: str = SlashOption(description="A JSON sterilizable string with embed data")):
        await self.send_embeds(ctx, json)

    @embed.subcommand()
    async def url(self, ctx, url: str = SlashOption(description='A link to a website containing raw JSON embed data')):
        try:
            embed_data = url_to_json(url)
        except Exception as error:
            return await ctx.send(error, ephemeral=True)
        await self.send_embeds(ctx, embed_data)

    @embed.subcommand()
    async def channel(self, ctx):
        pass

    @channel.subcommand()
    async def update(self, ctx):
        """Update the channel's embed message(s)"""
        embed_data = self.config.channel_embeds.get(str(ctx.channel.id), None)
        if not embed_data: return await ctx.send(embed=Embed(description="This channel doesn't have an embed data, define its embed data in the `embeds.toml` config file"), ephemeral=True)
        await self.send_embeds(ctx, embed_data)

    async def send_embeds(self, ctx: Interaction, embed_data: Literal[str, dict, list]):
        try:
            embeds = self._data_to_embeds(embed_data)
        except JSONDecodeError as error:
            await ctx.send(error, ephemeral=True)
        await ctx.channel.send(embeds=embeds)
        await ctx.send('Done!', ephemeral=True)
    
    def _data_to_embeds(self, embed_data = Literal[str, dict, list]):
        if isinstance(embed_data, str): embed_data = loads(embed_data)
        if isinstance(embed_data, dict): embed_data = [embed_data]
        else: raise JSONDecodeError("Embed data must be a dictionary or a list of dictionaries.")

        for raw_embed in embed_data:
            if 'description' not in raw_embed: raw_embed['description'] = '\u200b'
            if 'fields' in raw_embed:
                for field in raw_embed['fields']:
                    if 'title' not in field: field['title'] = '\u200b'
                    if 'description' not in field: field['description'] = '\u200b'
            yield Embed.from_dict(raw_embed)