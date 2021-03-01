from discord.ext.commands import Cog, command


class CharacterCreation(Cog, name="Character Creation"):
    def __init__(self, bot):
        self.bot = bot

    @command(name="test")
    async def test(self, ctx):
        return await ctx.send("test")


def setup(bot):
    bot.add_cog(CharacterCreation(bot))
