from principality.cog import  Cog, ConfigOption, SlashOption

class Example(Cog):

    # Built-in attributes:
    # self.bot - Returns the Bot object that loaded this cog
    # self.folder - Returns the Path object of the folder containing this cog

    class Config:
        is_true: bool = ConfigOption(True, "Whether or not this value is true")

    def load(self):
        print('Loaded!')

    async def ready(self):
        print('Async Loaded!')

    @Cog.slash_command()
    async def test(self, ctx):
        await ctx.response.send_message(f"This value is {str(self.config['is_true'])}")

    @Cog.listener()
    async def on_member_join(self, member):
        print(member)