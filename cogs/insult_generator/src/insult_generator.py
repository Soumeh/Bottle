from random import choice
from principality.cog import  Cog, SlashOption

class Insult_Generator(Cog):

    patterns = [
        'well played (noun)', 'you are (adjct) (noun)', 'you are (adjct) (noun)', 'eat a (noun) (noun)',
        'eat a (noun)', '(verb)', 'i will (verb) you', 'who is this (adjct) (noun)', 'go to (location) (noun)',
        'you (adjct) (noun)', 'seek (noun)s', 'go to (location) and (verb)', '(adjct) (noun)'
    ]
    
    insults = {
        "noun": ['goober', 'chungus', 'chair', 'brat', 'swine', 'hog', 'nerd', 'weakling', 'dork', 'donkey', 'maggot', 'cretin', 'jerk', 'idiot', 'fool', 'butt', 'nerd', 'freak', 'buffoon', 'tool',
        'dunce', 'blockhead', 'pinhead', 'chump', 'donkey', 'muppet'],
        "verb": ['kiss', 'kick', 'punch', 'hate'],
        "adjct": ['big', 'french', 'stupid', 'weak', 'dumb', 'fat', 'ugly', 'thick', 'daft', 'long', 'tiny', 'bumbling', 'absolute', 'darn'],
        "location": ['church', 'heck', 'hole', 'toilet', 'basement']
    }
    
    unsafe_patterns = [
        'i will (verb) your mother','(verb) yourself', 'i (verb) you', '(verb) you', 'i (verb) in your room', 'choke on a (noun) and (verb)',
        'go (verb) an (adjct) (noun)', 'catch (disease) and (verb)', 'get (adjct) (disease)', '(verb) me', 
        'i suggest you (verb) your (noun)', 'i suggest you (verb) yourself', '(verb) me (noun)'
    ]

    unsafe_insults = {
        "noun": ['shitlips', 'whore', 'cunt', 'hoe', 'simp', 'harlot', 'slut', 'pussy', 'retard', 'fuck', 'shit', 'ass', 'imbecile', 'asshole', 'turd', 'sucker', 'piss', 'bitch', 'tard', 'fuckhead', 'dick', 'cock', 'wanker'],
        "verb": ['fuck', 'shit', 'kill', 'hang', 'pass', 'fist', 'piss', 'ram'],
        "adjct": ['retarded', 'motherfucking', 'girthy', 'slim', 'damn'],
        "disease": ['cancer', 'aids', 'gay', 'homo', 'syphilis', 'scurvy', 'the plague', 'ebola', 'tuberculosis', 'smallpox'],
        "location": ['hell']
    }

    unsafe_patterns.extend(patterns)
    for key, value in insults.items():
        unsafe_insults[key].extend(value)

    @Cog.slash_command(guild_ids=[802577295960571907, 418105205100642315, 964251827099033610, 292703237755240448])
    async def insult(self, ctx, 
        safe: bool = SlashOption(description="Whether or not to limit insult vocabulary to be PG-13.", default=True)
    ):
        insult = self.generate_insult(safe)
        await ctx.response.send_message(insult)

    def generate_insult(self, safe=False):

        if not safe:
            patterns, insults = self.unsafe_patterns, self.unsafe_insults
        else:
            patterns, insults = self.patterns, self.insults

        insult = choice(patterns)
        for key, choices in insults.items():
            key = f'({key})'
            while key in insult:
                insult = insult.replace(key, choice(choices), 1)
        remove_characters = choice(range(-2, 3))
        while remove_characters > 0:
            insult = insult.replace(insult[choice(range(len(insult)))], '', 1)
            remove_characters -= 1
        return insult