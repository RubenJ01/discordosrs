import asyncio
from discord import message
from discord.ext.commands import Cog, command
from discord.ext import commands
import discord
from backend.conn import cur, conn, db
from backend.helpers import sql_query, sql_edit
from backend.checks import has_character, has_no_character


class CharacterHandling(Cog, name="Character Handling"):
    """A class containing the various commands using in handling characters.
    - character: Display important information about the users character
    - character create name: create a character using the users discord_id and the name provided
    - character delete: prompts the user to make sure they want to delete their character, times out after 15 seconds of not recieving a y/Y
    """

    def __init__(self, bot):
        self.bot = bot

    @has_character()
    @commands.group(name="character", invoke_without_command=True)
    async def character(self, ctx):
        discord_id = ctx.author.id
        # get the character matching the discord ID
        character = await sql_query("SELECT id, name, discord_id FROM characters WHERE discord_id = ?", (discord_id,))
        # send back some information on the character TODO: figure out what information we need to send to the user.
        print(character)
        message = discord.Embed(
            title=character[0][1],  # Character name
            description=str(
                f"You have created a character called")
        )
        return await ctx.send(embed=message)

    @has_no_character()
    @character.command(name="create")
    async def create_character(self, ctx, character_name):
        discord_id = ctx.author.id

        # create character with the name from the command and the discord id of the author
        await sql_edit("INSERT INTO characters (name, discord_id) VALUES(?, ?)", (character_name, discord_id,))

        message = discord.Embed(
            title="Character Created",
            description=str(
                "You have created a character called " + character_name)
        )
        return await ctx.send(embed=message)

    @has_character()
    @character.command(name="delete")
    async def delete_character(self, ctx):
        discord_id = ctx.author.id
        # ask to confirm that the auther wants to delete the character
        await ctx.send("Are you sure you want to delete your character? Y/N")

        try:
            def check(message):
                """check that the message is from the same author and in the same channel as the command was called."""
                return message.channel == ctx.channel and message.author == ctx.author

            msg = await self.bot.wait_for('message', timeout=15.0, check=check)
            if msg.content in 'Yy':
                # if the message from the author contains y or Y, delete the character bound to that discord_id
                await sql_edit("DELETE FROM Characters WHERE discord_id = ?", (discord_id,))
                await ctx.send('Character deleted')

            elif msg.content in 'Nn':
                await ctx.send('Character deletion stopped.')

        except asyncio.TimeoutError:
            return await ctx.send('No response. Character reset stopped.')


def setup(bot):
    bot.add_cog(CharacterHandling(bot))
