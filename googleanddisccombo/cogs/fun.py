import discord
from discord import client
from discord.ext import commands
import random
from discord import Embed
from discord import FFmpegPCMAudio
import asyncio

france = ["French", "France", "french", "france"]

andrew= ["schlafly", "Schlafly"]

random_fact_list = ["France's longest continuous border is with Brazil.", "The political left is usually signalled with red, but in the U.S. the parties got it flipped. https://tenor.com/view/ugh-donald-trump-head-shake-eye-roll-unbelievable-gif-14330090", "India and Bangladesh used to have an enclave within an enclave within an enclave. It has since been resolved.", "The 2021 Peruvian Presidential election second round involved both a communist and the daughter of the deposed dictator of the country.", "SCUBA and RADAR were originally acronyms."]

dares = ['Text the 3rd person in your phone "I know what you did".', "Blast Locationships - Cordae for 5 seconds.", "Instead of swearing, use derivatives of 'pog' for the next 24 hours.", "Confess to the 7th person on your dms of your most recent lie.", "Reccomend Mickey Mouse Clubhouse to the 2nd person on ur dms list.", "Make a rap about the most recent political argument on the server and send it here.", "End all of your messages with an emoji for the next 5 minutes.", "Blast Mining Away for 15 seconds out loud.", "Don't listen to Machine Gun Kelly or any form of his songs or any features for a week."]

truths = ['placeholder truth']

mgk = ["mgk", "Mgk", "Machine Gun Kelly", "Machine gun kelly", "machine gun kelly"]

ooc = ['https://cdn.discordapp.com/attachments/783881442622308382/870707941932671086/image0.jpg',
        'https://cdn.discordapp.com/attachments/850408868919509004/860955116752470026/image0.png',
        'https://cdn.discordapp.com/attachments/850408868919509004/857340084088733706/unknown.png',
        'https://cdn.discordapp.com/attachments/800039486339678250/870709835723853975/unknown.png',
        'https://cdn.discordapp.com/attachments/800039486339678250/870710600429363261/unknown.png',
        'https://cdn.discordapp.com/attachments/800039486339678250/870710970887057408/unknown.png',
        'https://cdn.discordapp.com/attachments/850408868919509004/869385234460848169/image0.png',
        'https://cdn.discordapp.com/attachments/800039486339678250/870711752910852127/unknown.png',
        'https://cdn.discordapp.com/attachments/795023687501611018/870715907612225557/IMG_3493.jpg',
        'https://cdn.discordapp.com/attachments/870073339224420393/870718276542541864/Liam_likes_very_special_things_there_I_guess.png',
        'https://cdn.discordapp.com/attachments/870073339224420393/870718173249425448/image0.png',
        'https://cdn.discordapp.com/attachments/870073339224420393/870718632735416370/LIAMWHATAREYOUHIDING.png',
        'https://cdn.discordapp.com/attachments/870073339224420393/870718627140206602/image0.png',
        'https://cdn.discordapp.com/attachments/850408868919509004/870719250275401768/Liamconfessed.png',
        'https://cdn.discordapp.com/attachments/850408868919509004/870720464434131005/ZEKEHASBEENLIKED.png',
        'https://cdn.discordapp.com/attachments/850408868919509004/870721555607453707/unknown.png',
        'https://cdn.discordapp.com/attachments/850408868919509004/870722287815516250/image0.png',
        'https://cdn.discordapp.com/attachments/850408868919509004/870723769604378634/image0.png',
        'https://cdn.discordapp.com/attachments/795023687501611018/871863915267620884/unknown.png',
        'https://cdn.discordapp.com/attachments/795023687501611018/871866601627066408/unknown.png',
        'https://cdn.discordapp.com/attachments/862025232336289810/869263494388793404/image0.png',
        'https://cdn.discordapp.com/attachments/850408868919509004/875148978864402463/unknown.png',
        'https://cdn.discordapp.com/attachments/850408868919509004/875372858992382062/unknown.png'
        ]

oocname = ["Do you have an explanation for this one...", "Oh no...", "Caught in 4K."]

ooctext = ["When you try your best but you don't succeed...", "Work smarter not harder buckaroo.", "Better luck next time..."]

def convert(time):
    pos = ["s","m","h","d"]

    time_dict = {"s":1, "m":60, "h":3600, "d":3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2


    return val * time_dict[unit]

nerd1_score_list = []
nerd2_score_list = []

class Fun(commands.Cog, description='These commands are random commands used for purely fun purposes.'):

    """These commands are purely for fun."""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=['8ball'])
    async def eightball(self, ctx, *, question):
        """The 8ball will try to predict the answer to a yes or no question."""
        responses = ["It is certain.",
                    "It is decidedly so.",
                    "Without a doubt.",
                    "Yes - definitely.",
                    "You may rely on it.",
                    "As I see it, yes.",
                    "Most likely.",
                    "Outlook good.",
                    "Yes.",
                    "Signs point to yes.",
                    "Reply hazy, try again.",
                    "Ask again later.",
                    "Better not tell you now.",
                    "Cannot predict now.",
                    "Concentrate and ask again.",
                    "Don't count on it.",
                    "My reply is no.",
                    "My sources say no.",
                    "Outlook not so good.",
                    "Very doubtful."]

        embed = Embed(title="8ball predicts that...", colour=0x000080)
        print("Question from 8ball: " + question)

        if any(word in question for word in france):
            embed.add_field(name=f"Question: {question}", value="France will always find a way to surrender, even in that circumstance.")
        elif any(word in question for word in andrew):
            embed.add_field(name=f'Question: {question}', value="Sorry, I don't answer questions for deceitful liberals.")
        else:
            embed.add_field(name=f'Question: {question}', value=f'{random.choice(responses)}')
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870409765728182352/8ball.png')
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Pondered by {ctx.author.name}')
        await ctx.send(embed=embed)
        
    @eightball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Question", value='The 8ball requires a question to answer.')
            await ctx.send(embed=embed)
        
    @commands.command()
    async def weirdfact(self, ctx):
        """Sends a weird fact about the world."""
        await ctx.send(random.choice(random_fact_list))

    @commands.command(aliases=['mitch','weirdo'])
    async def creep(self,ctx):
        """he rly is a creep"""
        await ctx.send('https://tenor.com/view/mitch-mc-connell-mitch-mcconnell-smile-awkward-gif-8010168')

    @commands.command(aliases=['ooc'])
    async def outofcontext(self,ctx):
        """You have done that yourself"""
        embed = discord.Embed(title='Interesting...', color=0x000080)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870717643315888168/bae_emoji.png')
        embed.set_image(url=random.choice(ooc))
        embed.add_field(name=random.choice(oocname), value=random.choice(ooctext))
        await ctx.send(embed=embed)

    """@commands.command()
    async def prank(self, ctx, joke):

        if not (ctx.voice_client):
            channel = ctx.message.author.voice.channel
            await channel.connect()
        
        if joke.lower() == 'rickroll':
            embed = Embed(title='Another One Bites the Dust...', color=0x000080)
            embed.add_field(name=f"+1 to {ctx.author.name}'s rickroll counter!", value="Good job, you're rising up in the world.")
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870765083406508092/rickmanhedobekindanice.jpg')
            await ctx.send(
                embed=embed,
                components = [
                    Button(style=ButtonStyle.URL, label='Claim Reward!', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
                ]
            )
            interaction = await self.bot.wait_for("button_click", check=lambda i: i.component.label.startswith("Claim"))
            await interaction.respond(content="You have claimed your reward!")

        elif joke.lower() == 'soviet':
            embed = Embed(title='Good Job Comrade!', color=0x000080)
            embed.add_field(name=f"{ctx.author.name} is really becoming a true Comrade.", value="One day you might become the leader of the Soviet Union.")
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870451513854672896/soviet_union_flag.png')
            await ctx.send(embed=embed)
        
        elif joke.lower() == 'crabrave':
            embed = Embed(title='CRAB RAVEEEE', color=0x000080)
            embed.add_field(name=f"{ctx.author.name} just why", value="Ig we have a crab rave now...")
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/795023687501611018/872228944827539466/DUNDUNDUNDANUN.jpg')
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="You must pick a valid option.", value='As of now its just Rick Astley and the Soviet Anthem.')
            await ctx.send(embed=embed)

        voice = ctx.guild.voice_client
        song = joke + '.mp3'
        source = FFmpegPCMAudio(song)
        voice.play(source)

    @prank.error
    async def prank_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Can't have both at once sadly", value='You must pick a prank to do.')
            await ctx.send(embed=embed)"""

    @commands.command()
    async def leavevc(self, ctx):

        if (ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
        else:
            embed = discord.Embed(title='Error', description='I am not in a voice channel.', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def pause(self, ctx):
        voice = discord.utils.get(client.voice_clients,guild=ctx.guild)

    @commands.command()
    async def mlg(self, ctx):
        embed = discord.Embed(title='Super Intense Minecraft Player Here', color=0x000080)
        embed.set_image(url='https://cdn.discordapp.com/attachments/783881442622308382/870725370456977498/image0.jpg')
        await ctx.send(embed=embed)

    @commands.command()
    async def tord(self, ctx, tord):
        if tord == 'dare':
            embed = discord.Embed(title='Dare!', color=0x000080)
            embed.add_field(name="Your dare is to...", value=random.choice(dares))
            await ctx.send(embed=embed)

        elif tord == 'truth':
            embed = discord.Embed(title='Truth!', color=0x000080)
            embed.add_field(name="Your truth is to...", value=random.choice(truths))
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title='Error', description='You must pick either truth or dare.', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            await ctx.send(embed=embed)

    @tord.error
    async def tord_error(self,ctx,error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="You must choose", value='You must select truth or dare in order to play.')
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def gstart(self, ctx):
        await ctx.send("Giveaway started. Answer the questions within 15 seconds.")

        questions = ["Which channel should it be hosted in?",
                    "What should be the duration of the giveaway? (s, m, h, d)",
                    "What is the prize?"]

        answers = []

        def check (m):
            return m.author == ctx.author and m.channel == ctx.channel

        for i in questions:
            await ctx.send(i)

            try:
                msg = await self.bot.wait_for(event='message', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send("You did not answer in time.")
                return
            else:
                answers.append(msg.content)
            

        try:
            c_id = int(answers[0][2:-1])
        except:
            await ctx.send(f"Please mention a channel correctly such as {ctx.channel.mention}")
            return

        channel = self.bot.get_channel(c_id)
        
        time = convert(answers[1])
        if time == -1:
            await ctx.send(f'You must use a correct unit.')
            return
        elif time == -2:
            await ctx.send(f"Time must be an integer.")
            return
        prize = answers[2]

        await ctx.send(f"Giveaway will be held in {channel.mention} and will last {answers[1]}!")


        embed = discord.Embed(title = "Giveaway", description = f"{prize}", color = 0x000080)

        embed.add_field(name="Hosted by:", value=ctx.author.mention)

        embed.set_footer(text=f"Ends {answers[1]} from now!")

        my_msg = await channel.send(embed = embed)


        await my_msg.add_reaction("🎉")


        await asyncio.sleep(time)


        new_msg = await channel.fetch_message(my_msg.id)


        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))

        winner = random.choice(users)

        await channel.send(f"Congrats! {winner.mention} has won {prize} from the giveaway!")

    @gstart.error
    async def gstarterror(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Permissions", value="You aren't qualified enough to just give things away.")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reroll(self,ctx, channel:discord.TextChannel, id_:int):
        try:
            new_msg = await channel.fetch_message(id_)
        except:
            await ctx.send("The id is invalid.")
            return
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))

        winner = random.choice(users)

        await channel.send(f"Congrats! {winner.mention} is the new winner of the giveaway.")

    @reroll.error
    async def gstarterror(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Permissions", value="You aren't qualified enough to just give things away.")
            await ctx.send(embed=embed)

    @commands.command(aliases=['nw'])
    async def nerdwars(self, ctx, nerd1:discord.User, nerd2:discord.User, *, prompt):
        embed = discord.Embed(title="Nerd Wars!", color=0x000080)
        embed.add_field(name="Prompt:", value=prompt)
        embed.set_footer(text=f"{nerd1.name} vs {nerd2.name}")
        await ctx.send(embed=embed)


        global nerd_1
        global nerd_2
        nerd_1 = nerd1
        nerd_2 = nerd2

        def check(m):
            return nerd1.author == m.author or nerd2.author == m.author
        time = 180
        await asyncio.sleep(time)

        await ctx.send(f'{nerd1.mention} and {nerd2.mention} times up!')
        embed = discord.Embed(title="Results!", color=0x000080)

        if nerd1_score_list != []:
            embed.add_field(name=f'{nerd1.name} got {len(nerd1_score_list)}', value=f', '.join(nerd1_score_list))
        if nerd1_score_list == []:
            embed.add_field(name=f'{nerd1.name} got {len(nerd1_score_list)}', value="None")
        if nerd2_score_list != []:
            embed.add_field(name=f'{nerd2.name} got {len(nerd2_score_list)}', value=f', '.join(nerd2_score_list))
        if nerd2_score_list == []:
            embed.add_field(name=f'{nerd2.name} got {len(nerd2_score_list)}', value="None")
        await ctx.send(embed=embed)
        nerd_1 = None
        nerd_2 = None
        nerd1_score_list.clear()
        nerd2_score_list.clear()

    @nerdwars.error
    async def nerdwarserror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Arguments", value='You must provide all required fields. Make sure they are correct as well.')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Argument", value='All arguments must be mentions except the prompt.')
            await ctx.send(embed=embed)

    @commands.command(description='Only true nerds can win at this.', aliases=['nwa', 'ans', 'answer', 'a'])
    async def nwanswer(self, ctx, *, answer:str):
        global nerd_1
        global nerd_2
        
        if ctx.author == nerd_1:
            if answer.title() not in nerd1_score_list or answer.title() not in nerd2_score_list:
                nerd1_score_list.append(answer.title())
                await ctx.send(f"+1 point to {ctx.author.mention}")
            elif answer.title() in nerd1_score_list or answer.title() not in nerd2_score_list:
                await ctx.send("Someone has already answered that.")

        elif ctx.author == nerd_2:
            if answer.title() not in nerd1_score_list or answer.title() not in nerd2_score_list:
                nerd2_score_list.append(answer.title())
                await ctx.send(f"+1 point to {ctx.author.mention}")
            elif answer.title() in nerd1_score_list or answer.title() not in nerd2_score_list:
                await ctx.send("Someone has already answered that.")

        else:
            await ctx.send("You are not currently playing a nerdwars.")

    @nwanswer.error
    async def nwanswererror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Arguments", value='You must provide all required fields. Make sure they are correct as well.')
            await ctx.send(embed=embed)

    @commands.command(description="Will send a question for you to answer.", aliases=["quiz"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def trivia(self, ctx):
        questions = [["What year did WW2 start? (History)", "C", 1, "A: 1936\nB: 1914\nC: 1939\nD: 1938"],
                     ["What was the precursor to the Republican Party? (Politics)", "A", 3, "A: Opposition Party\nB: Unconditional Union Party\nC: Whig Party\nD: Nullifier Party"],
                     ["What does SSD stand for? (Computer Science)", "D", 2, "A: Solid State Disk\nB: Static State Disk\nC: Static State Drive\nD: Solid State Drive"],
                     ["Which island in Indonesia has the most population? (Geography)", "B", 2, "A: Borneo\nB: Java\nC: Sumatra\nD: Timor"],
                     ["What is the territory that France ceded in the Franco-Prussian war? (History)","A", 2, "A: Alsace-Lorraine\nB: Savoy\nC: Maginot\nD: Calais"],
                     ["A communist or authoritarian state normally requires what system?", "C", 2, "A: Nonpartisan System\nB: Fascism\nC: One Party System\nD: Multiparty System"],
                     ["What was Coldplay's first album? (Music)","D", 2, "A: A Rush of Blood to the Head\nB: A Head Full of Dreams\nC: X&Y\nD: Parachutes" ],
                     ["What is the closest star to Earth other than the Sun? (Astronomy)", "B", 1, "A: Sirius A\nB: Alpha Centauri\nC: The North Star\nD: Bernard's Star"],
                     ["What is Sumerian, family and larger than a whale? (Kts suggestion)", "D", 1, "A: Chariots\nB: Mesopatamia\nC: Spears\nD: Ur mom"],
                     ["How many Pokémon were in the original games (Red/Blue)? (Gaming)", "B", 2, "A: 809\nB: 151\nC: 333\nD: 69"],
                     ["Which empire was the largest in history? (History)", "A", 1, "A: British Empire\nB: Mongol Empire\nC: Roman Empire\nD: Spanish Empire"],
                     ["Who was the president before Abraham Lincoln? (U.S. Politics)", "C", 3, "A: Taylor\n B: Polk\n C: Buchanan\n D: Jackson"],
                     ["What is the most spoken language in the world? (Language)", "B", 1, "A: Hindi\n B: Mandarin\n C: English\n D: Spanish"],
                     ["What is the most searched website in the US?(as of 2020) (General Trends)", "D", 2, "A: YouTube\n B: Facebook\n C: Twitter\n D: Google"]
                     ]

        answers = []
        def check (m):
            return m.author == ctx.author and m.channel == ctx.channel

        question_used = random.choice(questions)

        embed = discord.Embed(title="Question!", color=0xFFFF00)
        embed.add_field(name=question_used[0], value=question_used[3])
        embed.set_author(name=f"Difficuly Level {question_used[2]}")
        embed.set_footer(text="Type the letter of the answer, not the words.")
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/871723684816097370/questiones.png')
        await ctx.send(embed=embed)

        try:
            words = await self.bot.wait_for(event="message", check=check)
        except asyncio.TimeoutError:
            await ctx.send("You did not answer in time.")
            return
        else:
            answers.append(words.content)
            if str(answers[0]).lower() == str(question_used[1]).lower():
                embed = discord.Embed(title="Correct!", color=0x00FF00)
                embed.add_field(name=f'You have added another correct answer to your collection.',value=f'Difficulty Level: {question_used[2]}')
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/871435654049955860/CHECKMARKSTHESPOT.png')
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Incorrect!",color=0xFF0000)
                embed.add_field(name=f"The correct answer was {str(question_used[1])}",value=f"Difficulty Level: {question_used[2]}")
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
                await ctx.send(embed=embed)


    @commands.command()
    async def miniship(self, ctx, name1:str, name2:str):
        test1 = len(name1)
        test2 = len(name2)
        splicer1 = random.randint(1, test1)
        splicer2 = random.randint(0, test2)
        ship1 = name1[:splicer1]
        ship2 = name2[splicer2:]
        shipname = str(ship1)+str(ship2)
        ship_score = random.randint(0, 1000)
        if ship_score < 5:
            ship_statement = "You go worse than dinosaurs and comets and then some. Just say goodbye to that matchup."
        elif 5 <= ship_score < 25:
            ship_statement = "You go together like Kimmy and South Korea. Not well, as South Korea clearly doesn't exist. Its just The People's Democratic Republic of Korea. They just like to be rebellious..."
        elif 25 <= ship_score < 50:
            ship_statement = "Schlafly would be a better match than this for both of you."
        elif '69' in str(ship_score):
            ship_statement = "👀"
        elif 50 <= ship_score < 100:
            ship_statement = "You work about as well as Anakin and younglings."
        elif 100 <= ship_score < 150:
            ship_statement = "A website could treat u better than this. ||**Hint Hint** Wikipedia||"
        elif 150 <= ship_score < 200:
            ship_statement = "You all would work better than Gorbachev and the Soviet Union, but *dang* the Pizza Hut was good."
        elif 200 <= ship_score < 250:
            ship_statement = "Mike Pence would kiss the fly on his head before you both got along."
        elif 250 <= ship_score < 350:
            ship_statement = "This working out is as likely as Poland surviving in World War 2. Oh wait, that got split in half."
        elif 350 <= ship_score < 450:
            ship_statement = "Once Astatine works into a stable relationship, so might you two."
        elif 450 <= ship_score < 550:
            ship_statement = "Flip a coin. Thats about how likely it'll work."
        elif 550 <= ship_score < 650:
            ship_statement = "You might work out better than Israel and Palestine! Just maybe though..."
        elif 650 <= ship_score < 750:
            ship_statement = "Two Oxygen atoms look on with jealousy at how well you mesh."
        elif 750 <= ship_score < 850:
            ship_statement = "A binary star wouldn't have the same kind of positive gravity you two would have."
        elif 850 <= ship_score < 950:
            ship_statement = "Rick Astley wouldn't even mesh better with you than that. Thats just downright impressive."
        elif ship_score == 1000:
            ship_statement = "Best. Couple. To. Ever. Exist."
        else:
            ship_statement = "Y'all are **so** good, Schlafly wouldn't call it deceit."
        embed = discord.Embed(title="The Latest Ship is...", color=0xFF0000)
        embed.add_field(name="Ship Name:", value=shipname.capitalize())
        embed.add_field(name="Works like...", value=f'{ship_statement}', inline=False)
        embed.add_field(name="Ship Score:", value=f'{ship_score}',inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/850408868919509004/878825591875448922/awww.png')
        await ctx.send(embed = embed)

    @commands.command(description="The True Information, none of the liberal deceit.", aliases=['cp'])
    async def conservapedia(self, ctx, *, page:str):
        site = page.replace(' ', '_')
        await ctx.send(f"https://conservapedia.com/{site}")

    @conservapedia.error
    async def cperror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Arguments", value='You must provide a page for the link.')
            await ctx.send(embed=embed)

    @commands.command(description="Brings you to any desired page on Wikipedia.", aliases=['wikipedia', 'liamsbae'])
    async def wiki(self, ctx, *, page:str):
        site = page.replace(' ', '_')
        await ctx.send(f"https://en.wikipedia.org/wiki/{site}")

    @wiki.error
    async def wikierror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Arguments", value='You must provide a page for the link.')
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))