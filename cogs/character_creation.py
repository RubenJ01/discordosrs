import asyncio
from discord import message
from discord.ext.commands import Cog, command
from discord.ext import commands
import discord
from backend.conn import cur, conn, db
from backend.helpers import sql_query, sql_edit


class CharacterCreation(Cog, name="Character Creation"):

    def __init__(self, bot):
        self.bot = bot
    # create a group for character commands

    @commands.group(name="character", invoke_without_command=True)
    async def character(self, ctx):
        discord_id = ctx.author.id
        # get the character matching the discord ID
        character = await sql_query("SELECT id, name, discord_id FROM characters WHERE discord_id = ?", (discord_id,))
        # send back some information on the character TODO: figure out what information we need to send to the user.
        print(character)

    # command for creating a character
    @character.command(name="create")
    async def create_character(self, ctx, character_name):
        discord_id = ctx.author.id
        print(character_name, discord_id)
        # create character with the name from the command and the discord id of the author
        await sql_edit("INSERT INTO characters (name, discord_id) VALUES(?, ?)", (character_name, discord_id,))

        message = discord.Embed(
            title="Character Created",
            description=str(
                "You have created a character called " + character_name)
        )
        return await ctx.send(embed=message)
    # command for deleting a character

    @character.command(name="delete")
    async def delete_character(self, ctx):
        discord_id = ctx.author.id
        # ask to confirm that the auther wants to delete the character
        await ctx.send("Are you sure you want to delete your character? Y/N")

        # check that the message is from the same author and in the same channel as the command was called.
        try:
            def check(message):
                return message.channel == ctx.channel and message.author == ctx.author

            msg = await self.bot.wait_for('message', timeout=15.0, check=check)
            if(msg.content in 'Yy'):
                # if the message from the author contains y or Y, delete the character bound to that discord_id
                await sql_edit("DELETE FROM Characters WHERE discord_id = ?", (discord_id,))
        except asyncio.TimeoutError:
            return await ctx.send('No response. Character reset stopped.')


def setup(bot):
    bot.add_cog(CharacterCreation(bot))
