#imports
import discord
from discord.ext import commands

class LiamsExperiments(commands.Cog, description='Liams Creations, or whatever he puts in here'):

    #don't touch this statement
    def __init__(self, bot):
        self.bot = bot
    #put commands at this indentation below the init function

    @commands.command()
    async def LiamsTest(self, ctx):
        await ctx.send('Test!')
        
def setup(bot):
    bot.add_cog(LiamsExperiments(bot))