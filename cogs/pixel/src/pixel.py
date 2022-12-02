from cog import  Cog, SlashOption
from nextcord import Embed, Attachment, File
from io import BytesIO

try:
    from PIL import Image
except ImportError:
    pass

class Pixel(Cog):

    async def attachment_to_image(self, attachment: Attachment):
        return Image.open(BytesIO(await attachment.read(use_cached=True)))

    @Cog.slash_command()
    async def pixel(self, ctx):
        pass

    @pixel.subcommand()
    async def up(self, ctx,
        attachment: Attachment,
        scale: int = SlashOption(default=8, min_value=2, max_value=16)
    ):
        image = await self.attachment_to_image(attachment)
        if (sum(image.size)/2) * scale >= 1024: return await ctx.send("Image is too large", ephemeral=True)
        image = image.resize((image.width * scale, image.height * scale), Image.NEAREST)

        await self._post(ctx, image, attachment)

    @pixel.subcommand()
    async def tile(self, ctx,
        attachment: Attachment,
        times: int = SlashOption(default=3, min_value=2, max_value=9),
        scale: int = SlashOption(default=8, min_value=2, max_value=16)
    ):
        image = await self.attachment_to_image(attachment)
        if (sum(image.size)/2) * scale >= 1024: return await ctx.send("Image is too large", ephemeral=True)
        image = image.resize((image.width * scale, image.height * scale), Image.NEAREST)
        
        tiled_image = Image.new('RGBA', (image.width * times, image.height * times), (255, 0, 0, 0))
        for w in range(times):
            for h in range(times):
                tiled_image.paste(image, (image.width * w, image.height * h))
        
        await self._post(ctx, tiled_image, attachment)

    @Cog.message_command(name="Upscale Pixel Art")
    async def up_message(self, ctx, message):
        for attachment in message.attachments:
            await self.up(ctx, attachment, 8)

    @Cog.message_command(name="Tile Pixel Art")
    async def tile_message(self, ctx, message):
        for attachment in message.attachments:
            await self.tile(ctx, attachment, 3, 8)

    async def _post(self, ctx, image, attachment):
        file = BytesIO()
        image.save(file, 'png')
        file.seek(0)
        file = File(file, filename=attachment.filename)

        embed = Embed(title=f'``{attachment.filename}``')
        embed.set_thumbnail(url=attachment.proxy_url)
        embed.set_image(url='attachment://' + attachment.filename)

        await ctx.send(file=file, embed=embed)