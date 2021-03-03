from discord import message
from discord.ext.commands import Cog, command
import discord
from backend.conn import cur, conn, db


class CharacterCreation(Cog, name="Character Creation"):
    def __init__(self, bot):
        self.bot = bot

    @command(name="create_character")
    async def create_character(self, ctx, character_name):
        discord_id = ctx.author.id
        print(character_name, discord_id)
        try:
            cur.execute("INSERT INTO characters (name, discord_id) VALUES(?, ?)",
                        (character_name, discord_id,))
        except db.Error as e:
            print(f"Maria DB Error: {e}")

        message = discord.Embed(
            title="Character Created",
            description=str(
                "You have created a character called " + character_name)
        )

        # get discord_id

        return await ctx.send(embed=message)

    @ command(name="characters")
    # show all the characters in the DB
    async def characters(self, ctx):
        cur.execute("SELECT id, name, discord_id FROM characters")
        for (id, name, discord_id) in cur:
            await ctx.send("id: " + id + ", name: " + name + ", discord_id: " + discord_id)


def setup(bot):
    bot.add_cog(CharacterCreation(bot))
