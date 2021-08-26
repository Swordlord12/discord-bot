from __future__ import annotations
from typing import TYPE_CHECKING
from discord_components.client import DiscordComponents
import discord
from discord.ext import commands, tasks
from discord.ext.commands import bot
from itertools import cycle
import asyncio
import os
import json
import random
import logging
from pathlib import Path
from discord_components import *
cwd = Path(__file__).parents[0]
cwd = str(cwd)

TOKEN = os.environ.get('BOT_TOKEN')

secret_file = json.load(open(cwd+'/bot_config/secrets.json'))

bigbadexceptions = ["essex", "wessex", "sussex", "asexual", "bisexual", "homosexual", "pansexual"]

kt = ["kt", "katie"]

ktid = 773262481208377406

filler = ["ah fun", "oh fun", "oh nice", "ah nice", "thats fun", "that's fun", "thats nice", "that's nice", "oh cool", "ah cool", "that's cool", "thats cool", "ah ok", "oh ok", "thats ok", "that's ok", "oh wow", "ah wow", "thats just wow", "that's just wow", "ah good", "oh good", "thats good", "that's good", "oh interesting", "ah interesting", "thats interesting", "that's interesting"]

weezer = "weezer"

bean = "bean"

roasts = ["You're as sharp as a marble", "Is your butt jealous of all the crap that comes out of your mouth?", "You're more pointless than a circle.", "You're so ugly you make onions cry.", "It is impossible to underesitmate you.", "Don't be dissappointed in yourself, that's your parents job."]

buddyholly = ["What's with these homies dissin' my girl?", 
            "Why do they gotta front?",
            "What did we ever do to these guys",
            "That made them so violent?",
            "Woo-hoo, but you know I'm yours",
            "Woo-hoo, and I know you're mine",
            "Woo-hoo, that's for all the time",
            "I look just like Buddy Holly",
            "And you're Mary Tyler Moore",
            "I don't care what they say about us anyway",
            "I don't care 'bout that",
            "Don't you ever fear, I'm always near",
            "I know that you need help",
            "Your tongue is twisted, your eyes are slit",
            "You need a guardian",
            "Woo-hoo, and you know I'm yours",
            "Woo-hoo, and I know you're mine",
            "Woo-hoo, that's for all the time",
            "I look just like Buddy Holly",
            "And you're Mary Tyler Moore",
            "I don't care what they say about us anyway",
            "I don't care 'bout that",
            "I don't care 'bout that",
            "Bang! Bang! Knock on the door",
            "Another big bang, get down on the floor",
            "Oh no! What do we do?",
            "Don't look now but I lost my shoe",
            "I can't run and I can't kick",
            "What's a matter, babe, are you feelin' sick?",
            "What's a matter, what's a matter, what's a matter you?",
            "What's a matter, babe, are you feelin' blue? Oh-oh!",
            "That's for all the time",
            "That's for all the time",
            "I look just like Buddy Holly",
            "And you're Mary Tyler Moore",
            "I don't care what they say about us anyway",
            "I don't care 'bout that",
            "I don't care 'bout that",
            "I don't care 'bout that",
            "I don't care 'bout that"]

bigbad = ["porn", "sex", "hentai", "cum", "cock", "retard"]
    
mgk = ["mgk", "Machine Gun Kelly","colson"]

disses = ["He really did have a downfall, but it was long before the album.", "bro he sucks", "🤮"]

labigail = ["Labigail", "labigail"]

blender = ["blender", "blenderbot", ""]

hangover = "hangover"

def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or("%")(bot, message)
        
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

status = cycle(["Map Game VI", "%help for help"])

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = get_prefix, help_command=None, intents = intents)



bot.config_token = secret_file['token']
bot.connection_url = secret_file['mongo']
logging.basicConfig(level=logging.INFO)

@bot.command()
async def help(ctx, *, commandSent=None):
    found = False
    if commandSent != None:
        for command in bot.commands:
            cmmd = bot.get_command(command.name)
            for alias in cmmd.aliases:
                if alias == commandSent:
                    commandSent = cmmd.name


            if commandSent.lower() == command.name.lower():

                paramString = ''

                for param in command.clean_params:
                    paramString += param + ', '

                paramString = paramString[:-2]

                if len(command.clean_params) ==  0:
                    paramString ="None"

                aka = command.aliases

                if command.aliases == []:
                    aka = ["None"]

                embed=discord.Embed(title=f'Help - {command.name.capitalize()}', description=command.description, color = 0x000080)
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870688256524701706/BLENDAAAA.png')
                embed.add_field(name='Parameters:', value=f'`{paramString}`')
                embed.add_field(name="Aliases:", value="`"+f', '.join(aka)+"`", inline=False)
                await ctx.send(embed=embed)
                found = True

        for cog in bot.cogs:
            if commandSent.lower() == cog.lower():
                

                category = bot.get_cog(cog)
                cmds = category.get_commands()

                cmdlist = []
                for cmd in cmds:
                    cmd=cmd.name
                    cmdlist.append(cmd)
                

                embed=discord.Embed(title=f'Help - {cog}', description=category.description, color = 0x000080)
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870688256524701706/BLENDAAAA.png')
                embed.add_field(name='Commands:', value="`"+f', '.join(cmdlist)+"`")
                await ctx.send(embed=embed)
                found = True
        if found == False:
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Argument", value='Please enter a valid command name or category name.')
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='BlenderBot Help', description = "A list of all the commands that are on this bot.", color = 0x000080)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/871579655667351593/BLENDAAAA.png')
        embed.set_footer(text='You can get help for a specifc command or category by adding it after the help command.')
        
        for cog in bot.cogs:
            category = bot.get_cog(cog)
            cmds = category.get_commands()

            cmdlist = []
            for cmd in cmds:
                cmd=cmd.name
                cmdlist.append(cmd)
            embed.add_field(name=cog, value=category.description, inline=False)
        await ctx.send(
                embed=embed,
                components = [
                    Button(style=ButtonStyle.URL, label='Additonal Resources', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
                ]
            )
        interaction = await bot.wait_for("button_click", check=lambda i: i.component.label.startswith("Additonal"))
        await interaction.respond(content="You have claimed your reward!")

@bot.event
async def on_ready():
    change_status.start()
    print('Bot is online.')
    DiscordComponents(bot)

@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '%'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

@bot.event
async def on_guild_remove(guild):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent = 4)

@bot.command()
async def changeprefix(ctx, prefix):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent = 4)

        await ctx.send(f'Prefix changed to: {prefix}')
  
@tasks.loop(seconds=30)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

@bot.command(hidden=True)
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command(hidden=True)
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

@bot.command(hidden=True)
@commands.is_owner()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title='On Cooldown...', description='This command is on cooldown for {:.2f} seconds'.format(error.retry_after),color = 0xFF0000)
        await ctx.send(embed=embed)
@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return

    for word in mgk:
        if word.lower() in str(message.content).lower():
            await message.channel.send(f"Really. {message.author.mention} 😐")
    
    for word in labigail:
        if word in message.content:
            await message.channel.send(f'I agree with {message.author.mention}, its a great')
    
    if hangover.lower() in str(message.content).lower():
        await message.channel.send("is that seriously still ur favorite song...")
    await bot.process_commands(message)

    if weezer.lower() in str(message.content).lower():
        for line in buddyholly:
            await message.channel.send(line)
            await asyncio.sleep(2)

    for word in kt:
        if word in str(message.content).lower():
            await message.channel.send("🤫 Shhhh shes sleeping")

    if str(ktid) in str(message.content):
            await message.channel.send("🤫 Shhhh shes sleeping")

    if bean in str(message.content).lower():
        roasted = []
        for guild in bot.guilds:
            for member in guild.members:
                roasted.append(member)
        chosen = random.choice(roasted)
        embed = discord.Embed(title="YOU'VE BEAN ROASTED!", color=0xFFA500)
        embed.add_field(name=chosen.name, value=random.choice(roasts))
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/871853444212858960/PKFIRE.png')
        await message.channel.send(embed = embed)
    
    if message.guild == bot.get_guild(874298437481418752):
        completed = False
        for word in bigbad:
            for exception in bigbadexceptions:
                if exception in str(message.content).lower():
                    completed = True
                    return
            if word in str(message.content).lower() and completed == False:
                await message.delete()
                await message.channel.send("That message was big bad. Please do not send things such as ||" + str(message.content) + f"|| {message.author.mention}")
    
            



@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,asyncio.TimeoutError):
        embed=discord.Embed(title='Error', color=0xFF0000)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
        embed.add_field(name="Timeout Error", value='You must respond to the question in time.')
        await ctx.send(embed=embed)

bot.run(TOKEN)