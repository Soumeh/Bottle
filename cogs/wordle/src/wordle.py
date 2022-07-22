import base64
from random import choice
from nextcord import ChannelType, Embed
from principality.cog import  Cog, ConfigOption, SlashOption
from principality.utils import url_to_json

class Wordle(Cog):

    class Config:
        words_url: str = ConfigOption('https://gist.githubusercontent.com/Soumeh/afea52493f79da710b79228e6ec7874e/raw/f10fa4d4f31a830005aa6101b38a3dfe994b99a9/wordle_words.json')

    emoji_map = {}
    game_map = {}

    tutorial_embed = Embed(
        description = """
Guess the **WORDL** in 6 tries using the `/wordle guess` command.

Each guess must be a valid 5 letter word.

After each guess, the color of the tiles will change to show how close your guess was to the word.
 ︀︀
"""
    )

    tutorial_embed.add_field(
        name = "Examples",
        #<:blank_v:941100390009700382><:blank_a:941100389237948466><:blank_g:941100389669957712><:gray_u:936597251608969236><:blank_e:941100389263110184>
        value = """
︀︀
<:green_w:936590522028544032><:blank_e:941100389263110184><:blank_a:941100389237948466><:blank_r:941100390005477477><:blank_y:941100389732847647>
The letter **W** is in the word and is in the correct spot.

<:blank_p:941100389518942311><:orange_i:936590890703663136><:blank_l:941100389774807040><:blank_l:941100389774807040><:blank_s:941100389984514110>
The letter **I** is in the word but is in the wrong spot.

<:blank_v:941100390009700382><:blank_a:941100389237948466><:blank_g:941100389669957712><:gray_u:936597251608969236><:blank_e:941100389263110184>
The letter **U** is not in the word in any spot.
"""
    )

    # utils

    def comp_word(self, word, final_word, private):
        e = ''
        for i in range(len(word)):
            if word[i] == final_word[i]: e += self.emoji_map['green_'+word[i]] if private else '🟩'
            elif word[i] in final_word: e += self.emoji_map['orange_'+word[i]] if private else '🟧'
            else: e += self.emoji_map['gray_'+word[i]] if private else self.emoji_map['gray_square']
        return e

    async def error(self, response, message):
        await response.send_message(embed=Embed(description=message, color=16711680), ephemeral=True)

    async def private_result(self, response, words, final_word, is_correct):
        title = f"{len(words)}/6"
        description = '\n' + '\n'.join([self.comp_word(word, final_word, True) for word in words])
        if is_correct: 
            description += f'\n\nThe word was `{final_word}`!'
        else:
            keys = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm']
            for i in ''.join(words):
                if i in keys:
                    keys[keys.index(i)] = " "
            description += '\n\n```\n' + ' '.join(keys[0:10]) + '\n ' + ' '.join(keys[10:19]) + '\n   ' + ' '.join(keys[19:26]) + '\n```'
        await response.send_message(embed=Embed(title=title, description=description), ephemeral=True)

    async def public_result(self, channel, user, words, final_word):
        await channel.send(embed=Embed(title=f"{user.name} finished in {len(words)}/6!", description='\n'.join([self.comp_word(word, final_word, False) for word in words])))

    def random_word(self, len):
        return choice(self.words['final'])

    def is_valid_word(self, word):
        return word in self.words['guess'] or word in self.words['final']

    def b64_decode(self, b64):
        base64_bytes = b64.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        return message_bytes.decode('ascii')
    
    def b64_encode(self, message):
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        return base64_bytes.decode('ascii')

    # utils end

    async def ready(self):
        if not hasattr(self, 'words'): self.words = url_to_json(self.config.words_url)

        for id in [936590443418898432, 936589817410629653, 936597076278665246]:
            server = await self.bot.fetch_guild(id)
            emojis = await server.fetch_emojis()
            for emoji in emojis:
                self.emoji_map[emoji.name] = str(emoji)

    @Cog.slash_command(guild_ids=[802577295960571907, 418105205100642315, 292703237755240448])
    async def wordle(self, ctx):
        pass

    @wordle.subcommand()
    async def guess(self, ctx,
        word: str = SlashOption(description="Guess the wordle word.")
    ):

        await ctx.channel.add_user(ctx.user)

        if ctx.channel.type != ChannelType.public_thread or not ctx.channel.name.startswith('wordl-'):
            return await self.error(ctx.response, "Command must be used in a Wordl Game Thread.")

        final_word = self.b64_decode(ctx.channel.name.split('wordl-')[1])

        if not ctx.channel.id in self.game_map: self.game_map[ctx.channel.id] = {}
        game = self.game_map[ctx.channel.id]

        if not ctx.user.id in game: game[ctx.user.id] = []
        guesses = game[ctx.user.id]

        if len(guesses) > 6:
            return await self.error(ctx.response, "You already finished all your guesses!")

        if word != final_word:
            if len(word) < len(final_word) or len(word) > len(final_word): 
                return await self.error(ctx.response, f'Word must be {len(final_word)} characters long.')
            if not word.isalpha():
                return await self.error(ctx.response, 'Word must be alphabetical.')
            if not self.is_valid_word(word):
                return await self.error(ctx.response, 'Unknown word.')

        guesses.append(word)

        if word == final_word or len(guesses) == 6:
            await self.private_result(ctx.response, guesses, final_word, True)
            await self.public_result(ctx.channel, ctx.user, guesses, final_word)
            guesses = ['' for i in range(6)]
        else:
            await self.private_result(ctx.response, guesses, final_word, False)


    @wordle.subcommand()
    async def new(self, ctx,
        word: str = SlashOption(description="What word to create the game with.", default=None),
        length: int = SlashOption(description="How many characters long should the word be? (Between 3 and 8)", min_value=3, max_value=8, default=5)
    ):
        """Create a new wordle game."""

        if word and len(word) != 5:
            return await self.error(ctx.response, 'Temporarily, custom words must be 5 characters long, sorry.')
        elif not word: word = self.random_word(length)
        thread = await ctx.channel.create_thread(name='wordl-'+self.b64_encode(word), type=ChannelType.public_thread, reason="New wordl game.")
        await thread.send(embed=self.tutorial_embed)
        #await thread.add_user(ctx.user)
        await ctx.response.send_message(f"Psst! Don't tell anyone, but the game's word is ||`{word}`||!", ephemeral=True)