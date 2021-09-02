#imports
import discord
from discord.ext import commands
import datetime
from datetime import datetime
import asyncio
import random
from googleapiclient.discovery import build
from google.oauth2 import service_account
import gspread
import pytz
import math
import matplotlib.pyplot as plt
#from osgeo import _gdal
#import fiona
#import geopandas as gpd





#holds API keys for the google service accounts
SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']

#Initializing the Spreadsheet
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

client = gspread.authorize(creds)

maptest = client.open("Map Game VI Database").worksheet("Territories")

SAMPLE_SPREADSHEET_ID = '1EodY2Cs1t1UfarRwF80pIcLLGsD2OfdiyIImRD02g8g'

service = build('sheets', 'v4', credentials=creds)

sheet = service.spreadsheets()


#makes a later variable global
retreat_flag = False


class MapGame(commands.Cog, name='Map Game', description='Commands for the Map Game, such as military, leaderboards and attacking.'):

    """Map-Game specific commands"""

    def __init__(self, bot):
        self.bot = bot

    #sends a link to the map
    @commands.command(aliases=['maplink'], description='Sends a link to the map for this current Map Game.')
    async def map(self, ctx):
        await ctx.send('https://www.google.com/maps/d/u/2/edit?mid=1cPVGM4rxJt4JrdlP6Ps2vaHMnFQCNmSr&ll=38.72418301870549%2C-26.391804523192732&z=5')

    def write(self, sheets, inputs):
        request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                            range=f"{sheets}!A1", valueInputOption="USER_ENTERED", body={"values":inputs}).execute()

    def log(self, ranges, inputs):
        request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                            range=f"Logging!{ranges}", valueInputOption="USER_ENTERED", body={"values":inputs}).execute()

    @commands.command(aliases=['startclaims'])
    async def claim(self, ctx, *, empire):
        questions = ["First Claim?", "Second Claim?", "Third Claim?", "Fourth Claim?", "Fifth Claim?", "Sixth Claim?", "Seventh Claim?", "Eighth Claim?", "Ninth Claim?", "Tenth Claim?", "Eleventh Claim?", "Twelveth Claim?", "Thirteenth Claim?", "Fourteenth Claim?", "Last Claim?"]
        
        answers = []

        def check (m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        for i in questions:
            await ctx.send(i)
            msg = await self.bot.wait_for('message', check=check)
            answers.append(msg.content)

        for territory in answers:
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Territories!A1:Q1400").execute()
            values = result.get('values')
            for row in values:
                if territory == row[1]:
                    maptest.update_cell(int(row[0]), 7, empire)
        initialize_empire = [['tbd', empire, ]]
        MapGame.write(self, 'General Stats', )


    #uses oil for travel
    @commands.command(aliases=['oil'], description='Uses oil to make either planes or naval units go faster.')
    async def use(self, ctx, distance:int, *, empire):
        amount = int(math.ceil(distance/200))
                
        eastern = pytz.timezone('US/Eastern')
        utc = pytz.utc
        time = datetime.now(tz=eastern)
        string_time = time.strftime("%m/%d/%Y %H:%M:%S")

        
        inputs = [[str(empire), '0', '-'+str(amount), str(string_time)]]
        request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                            range="Invoice!A1", valueInputOption="USER_ENTERED", body={"values":inputs}).execute()

        empire_result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Military Stats!A1:I150").execute()
        empire_values = empire_result.get('values')

        for row in empire_values:
            if row[0] == empire:
                check = int(row[1])
        if check - amount < 0:
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Argument", value='You cannot use more oil than you own.')
            await ctx.send(embed=embed)
            return

        log = [[empire, check]]
        MapGame.write(self, 'Logging', log)

        embed = discord.Embed(title=f'You have used {amount} oil barrels.', color=0x000080)
        await ctx.send(embed = embed)

    #error handling for use
    @use.error
    async def useerror(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Argument", value='You must provide an empire and an amount. Make sure they are correct as well.')
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BadArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Argument", value='The amount must be an integer.')
            await ctx.send(embed=embed)

    #manually adds a battle to the database
    @commands.command(aliases=['addbattlelog', 'addlog', 'battleadd'], description='Adds a battle manually to the database.')
    @commands.has_permissions(administrator=True) #makes the command admin only
    async def addbattle(self, ctx, winner, loser, territory, lost_winner, lost_loser):

        """adds a battle to the spreadsheet"""

        inputs = [winner, loser, territory, lost_winner, lost_loser]

        battles = [inputs, ['','','','','']]
        
        
        if lost_winner.isdigit() and lost_loser.isdigit():
            embed = discord.Embed(title=f'Battle of {territory} Added to Database.', color=0x000080)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870689026053664808/fighticon2.png')
            if int(lost_winner) > 9:
                embed.add_field(name="That was one costly battle.", value=f'You did win, but hopefully it does not cost you later {winner}...')
            if int(lost_loser) > 9:
                embed.add_field(name="That was one rough defeat.", value=f'Hopefully you can rebuild from here {loser}.')
            request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                range="Battle Record!A1", valueInputOption="USER_ENTERED", body={"values":battles}).execute()
            await ctx.send(embed=embed)

        else:
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Value", value=f'You must use numbers for losses on arguments 4 and 5.')
            await ctx.send(embed=embed)
        
    #error handling for addbattle
    @addbattle.error
    async def addbattle_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Argument", value='You must provide all values for the battle. Make sure they are correct as well.')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.TooManyArguments):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Too Many Arguments", value='You must provide only values for the battle. Make sure they are correct as well. (if u got this because of spaces do not use spaces use underscores instead.)')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Permissions", value="Alas, this is a manual override command reserved for naval battles or errors. It is done automatically by %attack otherwise.")
            await ctx.send(embed=embed)


    #shows the top empires for different non military stats
    @commands.command(aliases=['lb', 'top', 'rank', 'rankings', 'ranking'], description='Shows the top 5 Empires for any stat entered.')
    async def leaderboard(self, ctx, *, stat):
        #initializes the sheet
        empire_result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="General Stats!A1:Q150").execute()
        empire_values = empire_result.get('values')
        leaderboard = [[]]
        #uses two variables because the x keeps counting even after it reaches it, which may be able to be a return statement but this is how I chose to do it
        x = 0
        y = None
        embed = discord.Embed(title=f'Top 5 Empires for {stat.title()}', color = 0x000080)
        for field in empire_values[0]:
            x += 1
            if field.lower() == stat.lower():
                y = x - 1
                
        #if the stat is not found, sends error message
        if y == None:
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Stat", value='You must provide a correct stat.')
            await ctx.send(embed=embed)
            return
        
        #initializes the list 
        empires = []

        #cleans up the values within the list so it is always an integer
        for empire in empire_values[1:]:
            empirenotclean = empire[y].replace('#N/A', '0')
            empirekindaclean = empirenotclean.replace('%', '')
            empiremostlyclean = empirekindaclean.replace('$', '')
            empireclean = empiremostlyclean.replace(',', '')
            empireclean = int(empireclean)
            empires.append([empire[1], empireclean])
        empires = empires[1:]
        #sorts the list
        empires.sort(reverse=True,key = lambda row: (row[1],row[0]))
        n=0
        #sends the leaderboard
        for owner_pair in empires:
            n+=1
            embed.add_field(name = f'{n}: {owner_pair[0]}', value = f'{owner_pair[1]}', inline=False)
            if n == 5:
                break
        await ctx.send(embed=embed)

    #error handling for the leaderboard command
    @leaderboard.error
    async def leaderboard_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Argument", value='You must provide a stat. Make sure it is correct as well.')
            await ctx.send(embed=embed)

    #sends info for any territory on the spreadsheet
    @commands.command(aliases=['ti'], description='Gets the information for a specifc territory.')
    async def territoryinfo(self, ctx, *, territory):
        #initializes the spreadsheet
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Territories!A1:Q1400").execute()
        values = result.get('values')
        #loop to find the specific row, and gets the list of stats for that row
        found = False
        if not found:
            for owner_pair in values[1:]:
                for field in owner_pair:
                    if field.lower() == territory.lower():
                        embed = discord.Embed(title='Territory:', color=0x000080)
                        embed.add_field(name=f'{owner_pair[6]}', value=f'owns {owner_pair[1]}.')
                        embed.add_field(name='Stats:', value=f'GDP: {owner_pair[2]}\n Population: {owner_pair[3]}\n Area: {owner_pair[4]} sq mi\n Coast: {owner_pair[5]}\n GDP per Capita: {owner_pair[7]}\n Population Density: {owner_pair[9]} people per sq mi\n Iron: {owner_pair[10]}\n Aluminum: {owner_pair[11]}\n Silver: {owner_pair[12]}\n Gold: {owner_pair[13]}\n Oil: {owner_pair[14]}\n Forts: {owner_pair[16]}\n Ports: {owner_pair[15]}', inline = False)
                        found = True
                        await ctx.send(embed=embed)
                    else:
                        pass
        #if territory is not found, return an error
        else:
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Territory", value='Makes sure your territory actually exists, and check your spelling.')
            await ctx.send(embed=embed)
        
    #error handling for territory info
    @territoryinfo.error
    async def ti_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Argument", value='You must provide a territory. Make sure it is correct as well.')
            await ctx.send(embed=embed)

    #sends the user info about an empire in the game
    @commands.command(aliases=['ei', 'nationinfo', 'ni', 'countryinfo', 'ci'], description='Gets the stats of any empire entered.')
    async def empireinfo(self, ctx, *, empire:str):
        #initializes the spreadsheet
        empire_result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="General Stats!A1:Q150").execute()
        empire_values = empire_result.get('values')
        #loop to find the empire
        found = False
        if not found:
            for owner_pair in empire_values[1:]:
                for field in owner_pair:
                    if field.lower() == empire.lower():
                        embed = discord.Embed(title=f'{empire.capitalize()}:', color=0x000080)
                        embed.add_field(name='Stats:', value=f'Number of Territories: {owner_pair[16]} territories\n GDP: {owner_pair[5]}\n Population: {owner_pair[2]}\n Area: {owner_pair[3]} sq mi\n Coast: {(owner_pair[7])} coastal territories\n GDP per Capita: {owner_pair[6]}\n Population Density: {owner_pair[4]} people per sq mi\n Iron: {owner_pair[9]} deposits\n Aluminum: {owner_pair[10]} deposits\n Silver: {owner_pair[11]} deposits\n Gold: {owner_pair[12]} deposits\n Oil: {owner_pair[13]} deposits\n Forts: {owner_pair[14]} forts\n Ports: {owner_pair[15]} ports', inline = False)
                        found = True
                        await ctx.send(embed=embed)
                    else:
                        pass
        #returns an error if empire is not found
        if found == False:
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Territory", value='Makes sure your territory actually exists, and check your spelling.')
            await ctx.send(embed=embed)

    @commands.command(alias=['chartc'], description='Sends a graph of currency and oil for said empire.')
    async def graphc(self, ctx, *, empire):
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Invoice!A1:D3000").execute()
        values = result.get('values')
        lresult = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Logging!A1:B3000").execute()
        lvalues = lresult.get('values')
        lresult2 = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Logging!D1:E3000").execute()
        lvalues2 = lresult2.get('values')
        empire_graph_list = []
        x1 = [0]
        x2 = [0]
        counter = 0
        counter2 = 0
        y_money = [0]
        y_oil = [0]
        worked = False
        for row in lvalues:
            if row[0] == empire:
                counter += 1
                empire_graph_list.append(row)
                x1.append(counter)
                y_oil.append(float(row[1]))
                worked = True
        for row in lvalues2:
            if row[0] == empire:
                counter2 += 1
                x2.append(counter2)
                y_money.append(float(row[1]))
                worked = True
        if worked == False:
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Empire", value='Makes sure your empire actually exists, or check if you have not made any transactions yet.')
            await ctx.send(embed=embed)
        plt.plot(x2, y_money)
        plt.plot(x1, y_oil)
        plt.title(f'{empire}\'s Invoice')
        plt.xlabel("Commands used involving currency")
        plt.ylabel("Amount")
        plt.legend(["Map Game Coins", "Oil Barrels"])
        plt.savefig('empire_graph.png')
        await ctx.send(file = discord.File("empire_graph.png"))

    @commands.command(aliases=["chartt"])
    async def grapht(self, ctx):
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Logging!G1:H3000").execute()
        values = result.get('values')
        empire_result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="General Stats!A1:Q150").execute()
        empire_values = empire_result.get('values')

        empire_names = []

        for row in empire_values[1:]:
            empire_names.append(row[1])

        key = []
        for empire in empire_names:
            x = [0]
            y = [0]
            counter = 0
            worked = False
            
            for row in values:
                if row[0] == empire:
                    counter += 1
                    x.append(counter)
                    y.append(float(row[1]))
                    worked = True
                    
            if worked == True:
                key.append(empire)
                plt.plot(x, y)

        plt.title('Territories')
        plt.xlabel('Commands')
        plt.ylabel('Amount')
        plt.legend(key)
        plt.savefig('territory_graph.png')
        await ctx.send(file = discord.File("territory_graph.png"))

    @empireinfo.error
    async def ei_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Argument", value='You must provide an empire. Make sure it is correct as well.')
            await ctx.send(embed=embed)
    
    #sends a dm to a user that has been declared war on
    @commands.command(aliases=['dw', 'war', 'declare'], description='Declares war on another player.')
    async def declarewar(self, ctx, user:discord.Member):
        embed = discord.Embed(title='War Declaration Sent.', description=f'I hope you\'re ready {ctx.author.name}...', color=0x000080)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870689026053664808/fighticon2.png')
        await ctx.send(embed=embed)
        
        embed = discord.Embed(title=f'{ctx.author} Has Declared War!', description='That can\'t be good...', color=0x000080)
        embed.add_field(name="Warning: Do not dm this bot.", value="It will not end well.")
        await user.send(embed=embed)
        print(ctx.author.name + ' has declared war on ' + user.display_name)

    #manually updates an owner of a territory
    @commands.command(aliases=['uo'], description='Updates an owner of a territory manually.')
    async def updateowner(self, ctx, *, territory):
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Territories!A1:Q1400").execute()
        values = result.get('values')
        found = False
        questions = ["Who is the new owner?"]

        answers = []

        def check (m):
            return m.author == ctx.author and m.channel == ctx.channel

        for i in questions:
            await ctx.send(i)

            try:
                msg = await self.bot.wait_for('message', check=check)
            except asyncio.TimeoutError:
                await ctx.send("You did not answer in time.", delete_after=10)
                return
            else:
                answers.append(msg.content)

        


        if not found:
            for owner_stats in values:
                for field in owner_stats:
                    if field == territory:
                        maptest.update_cell(int(owner_stats[0]),7, f'{answers[0]}')
                        embed = discord.Embed(title='Territory Updated.', color=0x000080)
                        embed.add_field(name=f'{owner_stats[6]}', value=f'has lost {owner_stats[1]} to {answers[0]}.')
                        found = True
                        await ctx.send(embed=embed)
                        empire_result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                        range="General Stats!A1:Q150").execute()
                        empire_values = empire_result.get('values')
                        for row in empire_values:
                            if row[1] == answers[0]:
                                check = int(row[16])
                        log_inputs = [[answers[0], check]]
                        MapGame.log(self, 'G1:H1000', log_inputs)
                    else:
                        pass
        else:
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Territory", value='Makes sure your territory actually exists, and check your spelling.')
            await ctx.send(embed=embed)

    #a function to check for NPCs
    def npc_check(self, territory):
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Territories!A1:Q1400").execute()
        values = result.get('values')
        for owner_pair in values[1:]:
            for field in owner_pair:
                if field.lower() == territory.lower():
                    NPC_CHECK = owner_pair
                    return NPC_CHECK

    def pick_unit(self, aia, ada, aaa, aid, add, aad, player):
        picked = False
        while picked == False:
            unit = random.randint(1,3)
            if player == 'attacker':
                if not aia > 0  and ada > 0 and aaa > 0:
                    picked == True
                    return "done"
                if unit == 1 and aia > 0:
                    picked = True
                    return "infantry"
                if unit == 2 and ada > 0:
                    picked = True
                    return "destroyer"
                if unit == 3 and aaa > 0:
                    picked = True
                    return "airforce"
            if player == 'defender':
                if not aia > 0  and ada > 0 and aaa > 0:
                    picked == True
                    return "done"
                if unit == 1 and aid > 0:
                    picked = True
                    return "infantry"
                if unit == 2 and add > 0:
                    picked = True
                    return "destroyer"
                if unit == 3 and aad > 0:
                    picked = True
                    return "airforce"


    #attacks a territory, and runs the battle odds, and if the attackers win against an NPC, it claims it automatically.
    @commands.command(aliases=['att'], description='Attacks a territory with specifc units of a single type.')
    @commands.cooldown(25, 86400,commands.BucketType.user)
    async def attack(self, ctx, amount_infantry_attacker:int, amount_destroyer_attacker:int, amount_airforce_attacker:int, amount_infantry_defender:int, amount_destroyer_defender:int, amount_airforce_defender:int, *, territory):
        #initializes spreadsheet for later
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Territories!A1:Q1400").execute()
        values = result.get('values')
        #for if the attacker wins
        questions = ["Who is the new owner?"]
        answers = []
        #setting up boolean variables
        found = False
        foundfirst = False
        global retreat_flag 
        retreat_flag = False
        #this is for later calculations of casualties
        amt_infantry_attacker = amount_infantry_attacker
        amt_infantry_defender = amount_infantry_defender
        amt_destroyer_attacker = amount_destroyer_attacker
        amt_destroyer_defender = amount_destroyer_defender
        amt_airforce_attacker = amount_airforce_attacker
        amt_airforce_defender = amount_airforce_defender
        defense_bonus = 1

        #this function checks if the territory is owned by NPCs
        NPC_CHECK = MapGame.npc_check(self, territory)

        #if the territory is not held by an NPC and has at least one fort, apply the defense bonus
        if NPC_CHECK[6] != 'NPC':
            if not foundfirst:
                for owner_stats in values:
                    for field in owner_stats:
                        if field == territory:
                            if int(owner_stats[16]) > 0 or int(owner_stats[15]) > 0:
                                defense_bonus = 1.5

        attacker_t_u = amt_infantry_attacker+amt_destroyer_attacker+amt_airforce_attacker
        defender_t_u = amt_infantry_defender+amt_destroyer_defender+amt_airforce_defender

        #main battle loop
        while attacker_t_u > 0 and defender_t_u > 0:
            #rolls for both attacker and defender
            attacker_infantry_roll_mod = amt_infantry_attacker*2
            attacker_destroyer_roll_mod = amt_destroyer_attacker*3
            attacker_airforce_roll_mod = amt_airforce_attacker*5
            defender_infantry_roll_mod = amt_infantry_defender*2
            defender_destroyer_roll_mod = amt_destroyer_defender*3
            defender_airforce_roll_mod = amt_airforce_defender*5
            attacker_roll = random.randint(0, attacker_airforce_roll_mod+attacker_destroyer_roll_mod+attacker_infantry_roll_mod)
            defender_roll = random.randint(0, round(defender_airforce_roll_mod+defender_destroyer_roll_mod+defender_infantry_roll_mod)*defense_bonus)
            print(attacker_roll)
            print(defender_roll)
            defense_bonus_shown = (defense_bonus - 1)*100
            #if the attacker retreats this handles the casualties and ending of the loop
            if retreat_flag == True:
                winner = 'Defenders'
                loser = 'Attackers'
                #casualties calculator
                losses_attacker_i = amount_infantry_attacker - amt_infantry_attacker
                losses_defender_i = amount_infantry_defender - amt_infantry_defender
                losses_winner_i = losses_defender_i
                losses_loser_i = losses_attacker_i
                losses_attacker_d = amount_destroyer_attacker - amt_destroyer_attacker
                losses_defender_d = amount_destroyer_defender - amt_destroyer_defender
                losses_winner_d = losses_defender_d
                losses_loser_d = losses_attacker_d
                losses_attacker_a = amount_airforce_attacker - amt_airforce_attacker
                losses_defender_a = amount_airforce_defender - amt_airforce_defender
                losses_winner_a = losses_defender_a
                losses_loser_a = losses_attacker_a
                inputs = [winner, loser, territory, losses_winner_i, losses_loser_i, losses_winner_d, losses_loser_d, losses_winner_a, losses_loser_a]
                battles = [inputs, ['','','','','']]
                #writes to battle log
                request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                    range="Battle Record!A1", valueInputOption="USER_ENTERED", body={"values":battles}).execute()
                embed = discord.Embed(title="You have fled the battle.", color=0x000080)
                await ctx.send(embed=embed)
                break

            #handles attackers winning
            if attacker_roll > defender_roll:

                unit_lost = MapGame.pick_unit(self, amt_infantry_attacker, amt_destroyer_attacker, amt_airforce_attacker, amt_infantry_defender, amt_destroyer_defender, amt_airforce_defender, 'defender')
                if unit_lost == "infantry":
                    amt_infantry_defender -= 1
                if unit_lost == "destroyer":
                    amt_destroyer_defender -= 1
                if unit_lost == "airforce":
                    amt_airforce_defender -= 1
                if unit_lost == "done":
                    return
                
                attacker_t_u = amt_infantry_attacker+amt_destroyer_attacker+amt_airforce_attacker
                defender_t_u = amt_infantry_defender+amt_destroyer_defender+amt_airforce_defender

                embed = discord.Embed(title=f'Battle of {territory}:', color=0x000080)
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870689026053664808/fighticon2.png')
                embed.add_field(name=f'{ctx.author.name} has won the battle.', value='They have killed one more unit from the defense.')
                embed.add_field(name='The rolls were:', value=f'Attackers had: {attacker_roll}\n Defenders had: {defender_roll}')
                embed.add_field(name='Infantry Remaining:', value=f"Attackers: {amt_infantry_attacker}\n Defenders: {amt_infantry_defender}", inline=False)
                embed.add_field(name='Destroyers Remaining:', value=f"Attackers: {amt_destroyer_attacker}\n Defenders: {amt_destroyer_defender}")
                embed.add_field(name='Airforce Remaining:', value=f"Attackers: {amt_airforce_attacker}\n Defenders: {amt_airforce_defender}")
                embed.set_footer(text=f'{defense_bonus_shown}% bonus to the defense')
                await ctx.send(embed=embed)
                await asyncio.sleep(3)
                
            #handles defenders winning
            elif defender_roll >= attacker_roll:
                
                unit_lost = MapGame.pick_unit(self, amt_infantry_attacker, amt_destroyer_attacker, amt_airforce_attacker, amt_infantry_defender, amt_destroyer_defender, amt_airforce_defender, 'attacker')
                if unit_lost == "infantry":
                    amt_infantry_attacker -= 1
                if unit_lost == "destroyer":
                    amt_destroyer_attacker -= 1
                if unit_lost == "airforce":
                    amt_airforce_attacker -= 1
                if unit_lost == "done":
                    return

                attacker_t_u = amt_infantry_attacker+amt_destroyer_attacker+amt_airforce_attacker
                defender_t_u = amt_infantry_defender+amt_destroyer_defender+amt_airforce_defender
                
                embed = discord.Embed(title=f'Battle of {territory}:', color=0x000080)
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870689026053664808/fighticon2.png')
                embed.add_field(name=f"You have lost a unit {ctx.author.name}.", value='Perhaps reconsider this land\'s value.')
                embed.add_field(name='The rolls were:', value=f'Attackers had: {attacker_roll}\n Defenders had: {defender_roll}', inline=False)   
                embed.add_field(name='Infantry Remaining:', value=f"Attackers: {amt_infantry_attacker}\n Defenders: {amt_infantry_defender}")
                embed.add_field(name='Destroyers Remaining:', value=f"Attackers: {amt_destroyer_attacker}\n Defenders: {amt_destroyer_defender}")
                embed.add_field(name='Airforce Remaining:', value=f"Attackers: {amt_airforce_attacker}\n Defenders: {amt_airforce_defender}")
                embed.set_footer(text=f'{defense_bonus_shown}% bonus to the defense')
                await ctx.send(embed=embed)
                await asyncio.sleep(3)
            
            #this handles errors with the amount of units
            else:
                embed=discord.Embed(title='Error', color=0xFF0000)
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
                embed.add_field(name="Invalid Value", value=f'You must use numbers for the amount of units on both sides.')
                await ctx.send(embed=embed)
                break
        
        #casualty calculator for normal battles
        losses_attacker_i = amount_infantry_attacker - amt_infantry_attacker
        losses_defender_i = amount_infantry_defender - amt_infantry_defender
        
        losses_attacker_d = amount_destroyer_attacker - amt_destroyer_attacker
        losses_defender_d = amount_destroyer_defender - amt_destroyer_defender
        losses_attacker_a = amount_airforce_attacker - amt_airforce_attacker
        losses_defender_a = amount_airforce_defender - amt_airforce_defender
        winner = ''
        loser = ''
        
        #handles a defender loss of the whole battle
        if amt_infantry_defender == 0 and amt_destroyer_defender == 0 and amt_airforce_defender == 0:
            winner = 'Attackers'
            loser = 'Defenders'
            losses_loser_d = losses_defender_d
            losses_winner_d = losses_attacker_d
            losses_loser_a = losses_defender_a
            losses_winner_a = losses_attacker_a
            losses_loser_i = losses_defender_i
            losses_winner_i = losses_attacker_i
            inputs = [winner, loser, territory, losses_winner_i, losses_loser_i, losses_winner_d, losses_loser_d, losses_winner_a, losses_loser_a]
            battles = [inputs]

            request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                range="Battle Record!A1", valueInputOption="USER_ENTERED", body={"values":battles}).execute()

            embed = discord.Embed(title='Attackers have won!', description='They now get occupy the territory!', color=0x000080)
            await ctx.send(embed=embed)

            #checks if territory is NPC
            NPC_CHECK = MapGame.npc_check(self, territory)
            
            #if territory is owned by NPC, automatically update it with the User inputted empire.
            if NPC_CHECK[6] == 'NPC':

                def check (m):
                    return m.author == ctx.author and m.channel == ctx.channel

                for i in questions:
                    await ctx.send(i)

                try:
                    msg = await self.bot.wait_for('message', check=check)
                except asyncio.TimeoutError:
                    await ctx.send("You did not answer in time.", delete_after=10)
                    return
                else:
                    answers.append(msg.content)

                
                
                #sends confirmation that the territory was indeed updated
                if not found:
                    for owner_stats in values:
                        for field in owner_stats:
                            if field == territory:
                                maptest.update_cell(int(owner_stats[0]),7, f'{answers[0]}')
                                embed = discord.Embed(title='Territory Updated.', color=0x000080)
                                embed.add_field(name=f'{owner_stats[6]}', value=f'has lost {owner_stats[1]} to {answers[0]}.')
                                found = True
                                await ctx.send(embed=embed)
                                empire_result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                            range="General Stats!A1:I150").execute()
                                empire_values = empire_result.get('values')
                                for row in empire_values:
                                    if row[1] == answers[0]:
                                        check = int(row[16])
                                log_inputs = [[answers[0], check]]
                                MapGame.log(self, 'G1:H1000', log_inputs)
                            else:
                                pass
                
                #this sends an error if the territory is not in the game
                else:
                    embed=discord.Embed(title='Error', color=0xFF0000)
                    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
                    embed.add_field(name="Invalid Territory", value='Makes sure your territory actually exists, and check your spelling.')
                    await ctx.send(embed=embed)
        
        #this handles defenders winning the entire battle
        if amt_infantry_attacker == 0 and amt_destroyer_attacker == 0 and amt_airforce_attacker == 0:
            winner = 'Defenders'
            loser = 'Attackers'
            losses_winner_d = losses_defender_d
            losses_loser_d = losses_attacker_d
            losses_winner_a = losses_defender_a
            losses_loser_a = losses_attacker_a
            losses_winner_i = losses_defender_i
            losses_loser_i = losses_attacker_i
            inputs = [winner, loser, territory, losses_winner_i, losses_loser_i, losses_winner_d, losses_loser_d, losses_winner_a, losses_loser_a]
            battles = [inputs]

            request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                range="Battle Record!A1", valueInputOption="USER_ENTERED", body={"values":battles}).execute()

            embed = discord.Embed(title='Defenders have won!', description='They have held onto their land!', color=0x000080)
            await ctx.send(embed=embed)

    #error handler for misc errors in the attack command
    @attack.error
    async def attackerror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Arguments", value='You must provide all required fields. Make sure they are correct as well.')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Argument", value='All arguments must be integers except the territory.')
            await ctx.send(embed=embed)

    #starts a retreat for the attacker
    @commands.command(description='Retreats from a battle in progress. You still take any casualties that have happened.')
    async def retreat(self, ctx):
        global retreat_flag
        retreat_flag = True
        await ctx.send("Retreat initialized.")

    
    #sends a leaderboard for any inputted military stat
    @commands.command(description='Shows the top five empires for a military related stat.')
    async def militarytop(self, ctx, *, stat:str):

        #this makes it so putting in the s doesn't give an error
        if stat.lower() == 'destroyers':
            stat = 'destroyer'
        #initalizing spreadsheet
        military_result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Military Stats!A1:I50").execute()
        military_values = military_result.get('values')
        military_scores = [['','']]
        embed = discord.Embed(title='Top 5 Military Scores:', description='This weights different units based off of their power.', color=0x000080)
       
        #this starts the list counter
        x = 0
        y = None
        embed = discord.Embed(title=f'Top 5 Empires for {stat.title()}', color = 0x000080)
        for field in military_values[0]:
            x += 1
            if field.lower() == stat.lower():
                y = x - 1

        #sends error if stat doesn't exist
        if y == None:
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Stat", value='You must provide a correct stat.')
            await ctx.send(embed=embed)
            return

        #cleans up values and appends it to the list
        for owner_pair in military_values[1:]:
            stat_chosen = owner_pair[y].replace('#N/A', '0')
            owner_military = [owner_pair[0],int(stat_chosen)]
            military_scores.append(owner_military)
        military_scores = military_scores[1:]
        #sorts the list
        military_scores.sort(reverse=True,key = lambda row: (row[1],row[0]))
        x=0
        #creates the embed
        for owner_pair in military_scores:
            x+=1
            embed.add_field(name = f'{x}: {owner_pair[0]}', value = f'{owner_pair[1]}', inline=False)
            if x == 5:
                break
        await ctx.send(embed=embed)

    #sends info about the different resources
    @commands.command(aliases=['resourcehelp'], description='Shows what the resource entered does.')
    async def resourceinfo(self, ctx, *, resource:str = 'None'):
        #sends general list if no argument is passed
        if resource == 'None':
            embed = discord.Embed(title='Resource List:', description='GDP, GDP per Capita, Population, Population Density, Area, Gold, Silver, Iron, Aluminum and Oil', color = 0x000080)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/873704201740517416/gold_icon.png')
            await ctx.send(embed=embed)
        elif resource.upper() == 'GDP':
            embed = discord.Embed(title='GDP Help:', description='Affects the production of all units within the game.', color = 0x000080)
            await ctx.send(embed=embed)
        elif resource.lower() == 'gdp per capita':
            embed = discord.Embed(title='GDP per Capita Help:', description='Affects production of Destroyers, Transports and Airforce.', color = 0x000080)
            await ctx.send(embed=embed)
        elif resource.lower() == 'population' or resource.lower() == 'pop':
            embed = discord.Embed(title='Population Help:', description='Affects production of all units within the game.', color = 0x000080)
            await ctx.send(embed=embed)
        elif resource.lower() == 'population density' or resource.lower() == 'pop density':
            embed = discord.Embed(title='Population Density Help:', description='Affects production of Infrantry and Airforce.', color = 0x000080)
            await ctx.send(embed=embed)
        elif resource.lower() == 'area':
            embed = discord.Embed(title='Area Help:', description='Affects production of Airforce.', color = 0x000080)
            await ctx.send(embed=embed)
        elif resource.lower() == 'gold':
            embed = discord.Embed(title='Gold Help:', description='Grants three currency per day.', color = 0x000080)
            await ctx.send(embed=embed)
        elif resource.lower() == 'silver':
            embed = discord.Embed(title='Silver Help:', description='Grants one currency per day.', color = 0x000080)
            await ctx.send(embed=embed)
        elif resource.lower() == 'iron':
            embed = discord.Embed(title='Iron Help:', description='Boosts infantry ouput.', color = 0x000080)
            await ctx.send(embed=embed)
        elif resource.lower() == 'aluminum':
            embed = discord.Embed(title='Aluminum Help:', description='Boosts airforce output.', color = 0x000080)
            await ctx.send(embed=embed)
        elif resource.lower() == 'oil':
            embed = discord.Embed(title='Oil Help:', description='Boosts Destroyer production and allows you to travel at double speed for a single flight at a cost of 1 oil per 200 miles (rounded up).', color = 0x000080)
            await ctx.send(embed=embed)
        #if stat isn't found, sends error
        else:
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Argument", value='You must pick a valid resource.')
            await ctx.send(embed=embed)

    #handles misc errors for resourceinfo
    @resourceinfo.error
    async def resourceinfoerror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Arguments", value='You must provide all required fields. Make sure they are correct as well.')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Argument", value='You must pick a valid resource.')
            await ctx.send(embed=embed)

    #sends help for attacking related actions in the Map Game
    @commands.command(aliases=['atthelp'])
    async def attackhelp(self, ctx):
        embed = discord.Embed(title='Attack Help', color = 0x000080)
        embed.add_field(name="Rolls:", value="Rolls are the random numbers that are generated whenever you attack or defend. It is calculated based off of a units strength and the amount of the unit. In a fight, whoever rolls higher will kill a unit from the other nation.", inline=False)
        embed.add_field(name='NPC vs PvP combat:', value="When attacking NPCs, you gain the territory after 2 hours of occupation. During this time you cannot attack through that territory. In PvP combat however, you occupy the territory instantly, but gain no value out of it until a peace deal is reached or the opponent is completely annexed. You may still move through the territory however.", inline=False)
        embed.add_field(name='Valid Attacking Locations:', value="When attacking a territory, you must attack with troops on adjancent territories, or from one of 2 things:\n    Paradropping with a plane within 300 miles of a territory.\n    Navally invading a port with armies and transport ships from a connected port.", inline=False)
        embed.add_field(name="Retreating:", value='As the attacker, you may retreat from a battle after any number of casualties, but you will still take however many casualties you took.', inline=False)
        embed.add_field(name="Unit Strength Table:", value='Infrantry: 2\nDestroyers: 3\nAirforce: 5\nTransports: 0 (they only transport up to 5 armies)', inline=False)
        embed.add_field(name="Attack Cap:", value='You may only attack up to 25 NPCs per day. This allows you to attack whenever you are able to, but also limits any one person hardlining for the victory.', inline=False)
        await ctx.send(embed=embed)

    #sends help for starting out in the Map Game
    @commands.command(aliases=['startinghelp', 'starthelp'])
    async def claimshelp(self, ctx):
        embed = discord.Embed(title='Claims Help', color = 0x000080)
        embed.add_field(name="Valid Claiming Locations:", value='There are a few limitations on what you can claim upon the start of your empire. For one, you cannot claim territories that are already owned by another empire. Additionally, you must group your territories in groups of five, ten and five, or fifteen.', inline=False)
        embed.add_field(name='Starting Military:', value="Upon creating your empire, you are able to deploy a certain amount of each unit type (see below table). In addition to the below table, you are able to deploy whatever production of military your nation has to start the game with.", inline=False)
        embed.add_field(name='Starting Military Table:', value='Infrantry: 20\nDestroyers: 2\nAirforce: 1\nTransports: 3', inline=False)
        await ctx.send(embed=embed)

    #sends help for military actions not covered in attacking
    @commands.command(aliases=['armyhelp', 'milhelp'])
    async def militaryhelp(self, ctx):
        embed = discord.Embed(title='Military Help', description = 'If you are looking for military scores and how to attack, do "%attackhelp".', color = 0x000080)
        embed.add_field(name="Military Production:", value='Military is produced per day from your empires stats in every resource. All resources are spread throughout the map where they would be in real life, making some locations more strategic than others. Additionally, if your capital gets captured, or you move it, you must wait a day before getting more military units. For more information on how every resource affects each of the unit types, see "%resourceinfo".', inline=False)
        embed.add_field(name="Border Skirmishes:", value="You are able to do a border skirmish with another player that you border every 24 hours over one territory. If the opposition loses the territory, they cannot take it back for 24 hours through a border skirmish unless they declare formal war. This is different from a formal war however because there is no grace period before the attack, and after it is over you instantly get to occupy the land and gain the stats from it. Border Skirmishes encourage players to protect their borders against other players. However, you cannot do border skirmishes over water or air.", inline=False)
        embed.add_field(name="Defensive Terrain and Forts:", value="Territories with high elevation have a +25% modifier to the defenses military score, rounded up. Forts give a larger bonus, of +50%, but you cannot stack this more than once (as in if there is more than a single fort its still a +50% modifier). Forts also give a bonus to infrantry production.", inline=False)
        embed.add_field(name="Shop Rapid Deployments:", value="You earn money based off of your empires silver and gold production. Using that money, you may buy extra divisions to place on the map. You may also purchase forts to put on the map.", inline=False)
        embed.add_field(name="Garrisons:", value="You must garrison every single territory in your empire with at least one division (as long as its not a transport). The exceptions to this are if you don't have enough divisions, or you have a DMZ (see later). In the first scenario that would disable you from attacking any NPCs or players, but in the second it would not.", inline=False)
        embed.add_field(name="Travel:", value="Infrantry units all move instantly through any contigious territories that you own. Naval units do the same, but only through continous ports that you have access to (make sure to look at the naval transport routes before sending your naval units somewhere to avoid cheating.). Otherwise naval units take time to reach their destination just like air units. Air units take time to reach their destination however, taking one hour to travel 720 miles.", inline=False)
        embed.add_field(name="Demilitarized Zones (DMZ):", value="These zones can be set in treaties, and can only be along a border with another player. In these zones you may not deploy any military there or garrison it. You also may not attack through it or do border conflicts to or from it. These can only be removed through another treaty, declaring war, or having war declared on you. In any case, it takes 12 hours to remilitarize a zone.")
        await ctx.send(embed=embed)

    #allows the user to travel to another location on the map.
    @commands.command(aliases=['move', 'fly', 'position'], description='Moves a naval or air unit to a different valid territory.')
    async def travel(self, ctx, distance:int, typetravel:str, *, empire:str):
        #initializes spreadsheet
        flight_result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Territories!A1:O1400").execute()
        flight_values = flight_result.get('values')
        #sets up travel types so the default is air travel if messed up
        traveltype = None
        if typetravel.lower() == 'airforce' or typetravel.lower() == 'air' or typetravel.lower() == 'plane' or typetravel.lower() == 'jet':
            traveltype = 1
            typetravel = "Air"

        if typetravel.lower() == 'naval' or typetravel.lower() == 'navy' or typetravel.lower() == 'water' or typetravel.lower() == 'ship' or typetravel.lower() == 'boat':
            traveltype = 3
            typetravel = "Naval"
        
        if traveltype == None:
            traveltype = 1

        #initializes questions
        questions = ["What is the territory of origin?", "What is the territory you are arriving in?"]
        answers = []
        for i in questions:
            await ctx.send(i)

            def check (m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                msg = await self.bot.wait_for('message', check=check)
            except asyncio.TimeoutError:
                await ctx.send("You did not answer in time.", delete_after=10)
                return
            else:
                answers.append(msg.content)
        #calculates time that it will take
        time = "An error occured."
        if traveltype == 3:
            time = round(distance/720*60*3)
            print(time)
        if traveltype == 1:
            time = round(distance/720*60)
            print(time)
        
        #updates spreadsheet
        inputs = [[empire, answers[0], answers[1], distance, time, typetravel]]

        request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                range="Travel Log!A1", valueInputOption="USER_ENTERED", body={"values":inputs}).execute()
        
        #sends embed
        embed = discord.Embed(title=f'{typetravel} Route Created', color=0x000080)
        embed.add_field(name=f'Distance:', value=f'{distance} miles')
        embed.add_field(name='Duration:', value=f'{time} minutes')
        embed.add_field(name="Type:", value=f"{typetravel}")
        embed.add_field(name="Start:", value=f"{answers[0]}", inline=False)
        embed.add_field(name="Finish:", value=f"{answers[1]}")
        await ctx.send(embed=embed)
    
    #handles misc travel errors
    @travel.error
    async def travelerror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Arguments", value='You must provide all required fields. Make sure they are correct as well.')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Argument", value='You must enter an integer for distance.')
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MapGame(bot))