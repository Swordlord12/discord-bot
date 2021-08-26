import discord
from discord.ext import commands
import tracemalloc

from discord.ext.commands.context import Context

tracemalloc.start()

mgk = ["Mgk", "mgk", "Machine Gun Kelly", "Machine gun kelly", "machine gun kelly"]

disses = ["He really did have a downfall, but it was long before the album.", "bro he sucks", "🤮"]

class Useful(commands.Cog, description='Commands that might come in handy once in a while.'):

    """Commands that serve a general useful purpose."""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='stalin', aliases=['purge', 'gulag'])
    @commands.has_permissions(manage_messages=True)
    async def stalin(self, ctx, amount):
        """does what Stalin does best"""
        if amount.isdigit():
            await ctx.channel.purge(limit=int(amount)+1)
            embed = discord.Embed(name="The Great Purge", color=0x000080)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/800039486339678250/870451513854672896/soviet_union_flag.png")
            embed.add_field(name="Great Success!", value=f"Stalin managed to purge {amount} messages successfully.")
            embed.set_footer(icon_url=ctx.author.avatar_url, text=f'{ctx.author.name} ordered the purge.')
        else:
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Value", value=f'Stalin does not deal in {amount}. Please write a number.')
            await ctx.send(embed=embed)

    @commands.command(aliases=["av", "avatar", "profilepic"])
    async def pfp(self, ctx, member : discord.Member):
        """sends a users pfp"""
        embed = discord.Embed(title = member.name, color=0x000080)
        embed.set_image(url = member.avatar_url)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Stalked by {ctx.author.name}')
        await ctx.send(embed=embed)

    @pfp.error
    async def pfp_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Argument", value='Please provide all required arguments.')
            await ctx.send(embed=embed)

    @stalin.error
    async def stalin_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Argument", value='Stalin must know how many messages to purge.')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Permissions", value="You can't just go around expecting the leader of the Soviet Union to obey you now can you?")
            await ctx.send(embed=embed)

    @commands.command(aliases=['version'])
    async def info(self, ctx):
        """states bots version"""
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))
        embed = discord.Embed(title="BlenderBot Info", color = 0x000080)
        embed.add_field(name="Version:",value="1.6.2 Beta")
        embed.add_field(name="‎‎‎‎‏‏‎ ‎", value=f"BlenderBot is in {serverCount} servers and serves {memberCount} members.", inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870688256524701706/BLENDAAAA.png')
        embed.set_footer(text="Created by Swordlord")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Useful(bot))