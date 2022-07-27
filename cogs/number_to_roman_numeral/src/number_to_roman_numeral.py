from principality.cog import  Cog, SlashOption
from nextcord import Embed, errors

class Number_To_RoNum(Cog):

    ronum_dict = {
    900: 'CM', 500: 'D', 400: 'CD', 100: 'C', 90: 'XC', 50: 'L', 
    40:  'XL',  10: 'X',   9: 'IX',   5: 'V',  4: 'IV',  1: 'I'
    }

    supertext_dict = {
    '1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉', '0': '₀'
    }

    @Cog.slash_command()
    async def ronum(self, ctx,
        number: int = SlashOption(description="What number will be converted to a roman numeral", min_value=1),
        full: bool = SlashOption(description="Whether or not to return a possibly lengthy roman numeral", default=False, required=False)
    ):
        if full: roman_number = self.int_to_full_ronum(number)
        else: roman_number = self.int_to_ronum(number)

        embed = Embed(description=f"{number} = \n{roman_number}")
        await ctx.response.send_message(embed=embed)
    
    def num_to_superscript(self, number: int = 0):
        result = str(number)
        for number, superscript in self.supertext_dict.items():
            result = result.replace(number, superscript)
        return result

    def int_to_full_ronum(self, number: int = 0):
        if not number:
            return 'N'
        result = ''
        thousand = int(number / 1000)
        if thousand:
            result = 'M' * thousand
            number -= 1000 * thousand
        for num, ronum in self.ronum_dict.items():
            while number >= num:
                result += ronum
                number -= num
        return result

    def int_to_ronum(self, number: int = 0):
        if not number:
            return 'N'
        result = ''
        thousand = int(number / 1000)
        if thousand:
            result = 'M'
            if thousand > 1: result += self.num_to_superscript(thousand)
            number -= 1000 * thousand
        for num, ronum in self.ronum_dict.items():
            while number >= num:
                result += ronum
                number -= num
        return result