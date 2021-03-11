from discord.ext import commands
from discord.ext.commands import check

from backend.conn import cur


class NoCharacter(commands.CheckFailure):
    """Exception raised when a command is used by user without a character"""
    pass


class HasCharacter(commands.CheckFailure):
    """Exception raised when a command is used by user with a character"""
    pass


def has_character():
    async def predicate(ctx):
        discord_id = ctx.author.id
        cur.execute(
            "SELECT `name` FROM `characters` WHERE discord_id = ?", (discord_id,))
        result = cur.fetchall()
        if result:
            # returns true because the users has a character
            return True
        else:
            raise NoCharacter
    return check(predicate)


def has_no_character():
    async def predicate(ctx):
        discord_id = ctx.author.id
        cur.execute(
            "SELECT `name` FROM `characters` WHERE discord_id = ?", (discord_id,))
        result = cur.fetchall()
        if result:
            raise HasCharacter
        else:
            return True
    return check(predicate)
