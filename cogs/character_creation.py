from discord import message
from discord.ext.commands import Cog, command
from discord.ext import commands
import discord

from backend.conn import cur, conn, db
from backend.helpers import sql_query, sql_edit


class CharacterCreation(Cog, name="Character Creation"):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="character", invoke_without_command=True)
    async def character(self, ctx):
        discord_id = ctx.author.id
        character = await sql_query("SELECT id, name, discord_id FROM characters WHERE discord_id = ?", (discord_id,))
        print(character)

    @character.command(name="create")
    async def create_character(self, ctx, character_name):
        discord_id = ctx.author.id
        print(character_name, discord_id)
        await sql_edit("INSERT INTO characters (name, discord_id) VALUES(?, ?)", (character_name, discord_id,))

        message = discord.Embed(
            title="Character Created",
            description=str(
                "You have created a character called " + character_name)
        )

        # get discord_id

        return await ctx.send(embed=message)


def setup(bot):
    bot.add_cog(CharacterCreation(bot))
