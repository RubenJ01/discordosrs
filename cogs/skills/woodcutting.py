import discord
from discord import message
from discord.ext.commands import Cog, command
from discord.ext import commands

from backend.conn import cur, conn, db
from backend.helpers import sql_query, sql_edit, gained_exp
from backend.checks import has_character, has_no_character


class WoodcuttingTraining(Cog, name="Woodcutting Training"):
    def __init__(self, bot):
        self.bot = bot


    @has_character()
    @commands.group(name="woodcutting", invoke_without_command=True)
    async def woodcutting(self, ctx):
        pass


    @has_character()
    @woodcutting.command(name="stats")
    async def stats(self, ctx):
        pass


    @has_character()
    @woodcutting.command(name="cut")
    async def cut(self, ctx, log: str, requested_time: int):
        pass



def setup(bot):
    bot.add_cog(WoodcuttingTraining(bot))
