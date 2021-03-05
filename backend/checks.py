from discord.ext import commands
from discord.ext.commands import check

from backend.conn import cur


class NoCharacter(commands.CheckFailure):
    """Exception raised when a command is used by user without a character"""
    pass


def has_character():
    async def predicate(ctx):
        user_id = ctx.author.id
        cur.execute("SELECT `name` FROM `characters` WHERE discord_id = ?", (user_id,))
        result = cur.fetchall()
        if result:
            # returns true because the users has a character
            return True
        else:
            raise NoCharacter
    return check(predicate)
