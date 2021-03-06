import discord
from discord import message
from discord.ext.commands import Cog, command
from discord.ext import commands

from backend.conn import cur, conn, db
from backend.helpers import sql_query, sql_edit, gained_exp
from backend.checks import has_character, has_no_character


class SkillTraining(Cog, name="Skill Training"):
    """A class for containing commands regarding the training of ones skills."""

    @command(name="train")
    async def train_skill(selv, ctx, skillname, exp):
        print(skillname, exp)
        await gained_exp(ctx, skillname, exp, ctx.author.id)

        return await ctx.send('Calculating exp gaing')


def setup(bot):
    bot.add_cog(SkillTraining(bot))
