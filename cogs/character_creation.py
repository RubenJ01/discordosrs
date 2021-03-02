from discord import message
from discord.ext.commands import Cog, command
import discord
from backend.conn import conn


class CharacterCreation(Cog, name="Character Creation"):
    def __init__(self, bot):
        self.bot = bot

    @command(name="test")
    async def test(self, ctx, character_name):
        message = discord.Embed(
            title="donald",
            description="sdmfkjlsdmfk"
        )

        # get discord_id
        discord_id = ctx.author.id
        print(discord_id)

        return await ctx.send(embed=message)


def setup(bot):
    bot.add_cog(CharacterCreation(bot))
