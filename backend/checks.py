from discord.ext import commands
from discord.ext.commands import check

from backend.conn import cur
from backend.helpers import sql_query


class NoCharacter(commands.CheckFailure):
    """Exception raised when a command is used by user without a character"""
    pass


class HasCharacter(commands.CheckFailure):
    """Exception raised when a command is used by user with a character"""
    pass


class RequiredLevelNotMet(commands.CheckFailure):
    """Exception raised when a command is used but the user doesnt have the required level to use it."""


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


def has_level(skill, level):
    async def predicate(ctx):
        discord_id = ctx.author.id
        skill_request = f"{skill}_lvl"
        valid_skills = {"firemaking_lvl", "woodcutting_lvl"}
        if skill_request not in valid_skills:
            raise Exception
        query = f"SELECT {skill_request} FROM characters WHERE discord_id = ?"
        current_skill_level = (await sql_query(query, (discord_id,)))[0][0]
        if current_skill_level >= level:
            return True
        else:
            raise RequiredLevelNotMet
    return check(predicate)




