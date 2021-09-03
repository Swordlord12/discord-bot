#imports
from cogs.mapgame import MapGame
from itertools import count
import discord
from discord.client import Client
from discord.ext import commands
import json
import os
import random
import asyncio
from googleapiclient.discovery import build
from google.oauth2 import service_account
from pprint import pprint
import gspread
from datetime import datetime
import pytz

#holds API keys for the google service accounts
SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']

creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

client = gspread.authorize(creds)

maptest = client.open("Map Game VI Database").worksheet("Territories")

#Starts the spreadsheet up
SAMPLE_SPREADSHEET_ID = '1EodY2Cs1t1UfarRwF80pIcLLGsD2OfdiyIImRD02g8g'

service = build('sheets', 'v4', credentials=creds)

sheet = service.spreadsheets()



os.chdir("C:\\Users\\Jude\\googleanddisccombo")

#initializes shop
mainshop = [{"name":"Fort/Port", "price": 25, "description":"allows you to place a fort anywhere on the map."},
            {"name":"Infantry", "price": 50, "description":"Allows you to deploy 5 additional infrantry."},
            {"name":"Destroyers", "price":75, "description":"Allows you to deploy 5 additional destroyers."},
            {"name":"Planes", "price":125, "description":"Allows you to deploy 5 additional airforce."}
            ]

class Economy(commands.Cog, description='Handles the commands that deal with currency and oil for the Map Game.'):

    """the fake schmoney"""

    def __init__(self, bot):
        self.bot=bot

    #stores function for creating a users account in the json file
    async def open_account(self, user):
        
        users = await self.get_bank_data()

        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["wallet"] = 0
            users[str(user.id)]["bank"] = 0
            users[str(user.id)]["bag"] = []

        
        with open("mainbank.json", "w") as f:
            json.dump(users,f)
        return True
    
    #stores the ability to get the data from the json file
    async def get_bank_data(self):
        with open("mainbank.json", "r") as f:
            users = json.load(f)

        return users

    #gets balance of said player
    @commands.command(aliases=['bal'])
    async def balance(self, ctx, member:discord.Member = None):
        if member == None:
            member = ctx.author

        await self.open_account(member)

        users = await self.get_bank_data()

        user = member
        
        wallet_amount = users[str(user.id)]["wallet"]
        bank_amount = users[str(user.id)]["bank"]
        
        em = discord.Embed(title = f'{member.name}\'s Balance', color = 0x000080)
        em.add_field(name = "Wallet", value = f'<:mapgamecoin:874347046587486248>{wallet_amount}.')
        #em.add_field(name = "Bank", value = f'<:mapgamecoin:874347046587486248>{bank_amount}.', inline=False)
        await ctx.send(embed = em)

    #grants users income based off of the deposits they have
    @commands.command(aliases=["daily", "money", "revenue"])
    #@commands.cooldown(1, 86400,commands.BucketType.user)
    async def income(self, ctx, *, empire:str):
        """awards you with your empires income for the day."""
        await self.open_account(ctx.author)

        income_result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="General Stats!A1:N1000").execute()
        income_values = income_result.get('values')

        

        users = await self.get_bank_data()
        user = ctx.author
        earnings = 0
        oil_earned = 0
        found = False
        if not found:
            for owner_row in income_values[1:]:
                if owner_row[1].lower() == empire.lower():
                    embed = discord.Embed(title=f"{empire.title()}'s Daily Income", color=0x000080)
                    earnings = int(owner_row[12]) + int(owner_row[11])*3
                    oil_earned = int(owner_row[13])
                    embed.add_field(name='Amount:', value=f'<:mapgamecoin:874347046587486248>{earnings}')
                    embed.add_field(name="Gold Deposits:", value=f"{owner_row[12]}", inline=False)
                    embed.add_field(name="Silver Deposits:", value=f"{owner_row[11]}", inline=False)
                    embed.add_field(name="Oil Earned:", value=f'{oil_earned} barrels')
                    await ctx.send(embed=embed)
                    found = True
                else:
                    pass
        
        
        if found == False:
            embed = discord.Embed(title="Error", color = 0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Empire", value='You must enter a valid empire name.')
            await ctx.send(embed=embed)
            return
        
        
        

        #starts the process of getting a timestamp
        eastern = pytz.timezone('US/Eastern')
        utc = pytz.utc
        time = datetime.now(tz=eastern)
        string_time = time.strftime("%m/%d/%Y %H:%M:%S")
        inputs = [[empire, earnings, oil_earned, string_time]]
        #writes to spreadsheet
        request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                range="Invoice!A1", valueInputOption="USER_ENTERED", body={"values":inputs}).execute()
        #gets logging spreadsheet
        log_result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Military Stats!A1:N1000").execute()
        log_values = log_result.get('values')

        #goes through loop to get both values
        total_oil = 'error'
        total_cur = 'error'
        for row in log_values[1:]:
            if row[0].lower() == empire.lower():
                print('worked')
                total_oil = row[1]
                total_cur = row[2]
            else: 
                pass
        #logs total Oil on sheet for graphing
        ol_input = [[empire, total_oil]]
        oil_log = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Logging!A1:B1000", valueInputOption="USER_ENTERED", body={"values":ol_input}).execute()

        currency = [[empire, total_cur]]
        currency_log = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Logging!D1:E1000", valueInputOption="USER_ENTERED", body={"values":currency}).execute()

        users[str(user.id)]["wallet"] += earnings

        with open("mainbank.json", "w") as f:
            json.dump(users,f)
    
    #holds function for updating a users bank to a different value
    async def update_bank(self, user, change = 0, mode = "wallet"):
        users = await self.get_bank_data()

        users[str(user.id)][mode] += change

        with open("mainbank.json", "w") as f:
            json.dump(users,f)

        bal = [users[str(user.id)]['wallet'],users[str(user.id)]['bank']]
        return bal

    #brings user to the shop
    @commands.command(aliases=['store'])
    async def shop(self, ctx):
        em =discord.Embed(title='Shop', color=0x000080)

        for item in mainshop:
            name = item['name']
            price = item['price']
            description = item['description']
            em.add_field(name=name, value=f'<:mapgamecoin:874347046587486248>{price} - {description}')

        await ctx.send(embed = em)

    #allows user to purchase items from the shop
    @commands.command(aliases=['purchase'])
    async def buy(self, ctx, amount:int, item, *, empire):
        await self.open_account(ctx.author)
        log_result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Military Stats!A1:N1000").execute()
        log_values = log_result.get('values')

        res = await self.buy_this(ctx.author,item,amount)

        if not res[0]:
            if res[1]==1:
                await ctx.send("That object does not exist.")
            if res[1]==2:
                await ctx.send(f'You are too broke to purchase {amount} of {item}(s)')

        else:
            await ctx.send(f'You just bought {amount} {item}')
            inputs = [[empire, item, amount]]
            request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                            range="Purchases!A1", valueInputOption="USER_ENTERED", body={"values":inputs}).execute()
            for items in mainshop:
                name = items['name'].lower()
                if name == item:
                    name_ = name
                    price = items['price']
                    break
            cost = price*amount
            invoice_input = [[empire,"-" + str(cost)]]
            request2 = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                            range="Invoice!D1:E1000", valueInputOption="USER_ENTERED", body={"values":inputs}).execute()
            total_cur = 'error'
            for row in log_values[1:]:
                if row[0].lower() == empire.lower():
                    print('worked')
                    total_cur = row[2]
                else: 
                    pass
            currency = [[empire, total_cur]]
            currency_log = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="Logging!D1:E1000", valueInputOption="USER_ENTERED", body={"values":currency}).execute()

    #error handling for buy command
    @buy.error
    async def buyerror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Argument", value='You must provide an item, amount and empire. Make sure they are correct as well.')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Argument", value='The amount must be an integer.')
            await ctx.send(embed=embed)

    #this function handles the account when a user buys something
    async def buy_this(self,user,item_name,amount:int):
        item_name = item_name.lower()
        name_ = None
        
        #this looks for the item and assigns it a price
        for item in mainshop:
            name = item['name'].lower()
            if name == item_name:
                name_ = name
                price = item['price']
                break
        
        #this sends back an error code if the item is not found
        if name_ == None:
            return [False,1]

        cost = price*amount

        users = await self.get_bank_data()

        bal = await self.update_bank(user)

        #this sends back a different error code if the user cannot afford the items
        if bal[0]<cost:
            return [False,2]

        try:
            index = 0
            t = None

            #this adds the object into the players inventory
            for thing in users[str(user.id)]["bag"]:
                n = thing["item"]
                if n == item_name:
                    old_amt = thing["amount"]
                    new_amt = old_amt + amount
                    users[str(user.id)]["bag"][index]["amount"] = new_amt
                    t = 1
                    break
                index+=1
            if t == None:
                obj = {"item":item_name, "amount":amount}
                users[str(user.id)]["bag"].append(obj)
        except:
            obj = {"item":item_name, 'amount':amount}
            users[str(user.id)]["bag"] = [obj]

        with open("mainbank.json", "w") as f:
            json.dump(users,f)

        await self.update_bank(user,cost*-1,"wallet")

        #sends back a success code if it works successfully
        return [True,"Worked"]

    #sends the user what is in their inventory
    @commands.command(aliases=['inv','bag', 'storage'], description='Shows what you have purchased.')
    async def inventory(self, ctx):
        await self.open_account(ctx.author)
        user = ctx.author
        users = await self.get_bank_data()

        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []


        em = discord.Embed(title = "Bag", color=0x000080)
        for item in bag:
            name = item["item"]
            amount = item["amount"]

            em.add_field(name=name.title(), value=amount)
        await ctx.send(embed = em)

    @commands.command(aliases=['u'])
    async def useitem(self,ctx, amount:int, item, *, empire):
        await self.open_account(ctx.author)

        res = await self.use_this(ctx.author,item,amount)

        #handles error codes
        if not res[0]:
            if res[1]==1:
                await ctx.send('You don\'t own that object.')
                return
            if res[1]==2:
                await ctx.send(f"You don't have {amount} {item}.")
                return
            if res[1]==3:
                await ctx.send(f"You don't have {item} anywhere.")
                return

        else:
            await ctx.send(f'You have used {amount} {item} from your inventory.')
            inputs = [[empire, item, -amount]]
            request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                            range="Purchases!A1", valueInputOption="USER_ENTERED", body={"values":inputs}).execute()

    #error handling for useitem command
    @useitem.error
    async def useitemerror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Argument", value='You must provide an empire, item and amount. Make sure they are correct as well.')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Argument", value='The amount must be an integer.')
            await ctx.send(embed=embed)

    #this function handles using items in a users inventory
    async def use_this(self,user,item_name,amount):
        item_name = item_name.lower()
        name_ = None

        #checks to see if the item is in the shop
        for item in mainshop:
            name = item["name"].lower()
            if name == item_name:
                name_ = name
                price = 0 #item["price"], this is equal to zero because you are not refunding the value
                break
        
        #returns error code of one if item is not in shop
        if name_ == None:
            return [False,1]

        cost = price*amount

        users = await self.get_bank_data()

        bal = await self.update_bank(user)


        try:
            index = 0
            t = None

            #removes the object from the users bag
            for thing in users[str(user.id)]["bag"]:
                n = thing["item"]
                if n == item_name:
                    old_amt = thing["amount"]
                    new_amt = old_amt - amount
                    if new_amt < 0:
                        return [False,2]
                    users[str(user.id)]["bag"][index]["amount"] = new_amt
                    t =1
                    break
                index+=1

            if t == None:
                return [False, 3]

        except:
            return [False, 3]

        with open("mainbank.json", "w") as f:
            json.dump(users,f)

        await self.update_bank(user,cost,"wallet")
        #sends success code upon working correctly
        return [True, "Worked"]
    
    #more code that can be brung back later as needed
    #@commands.command(aliases=['cf',"doubleornothing","don"])
    #async def coinflip(self, ctx, amount = None):
     #   await self.open_account(ctx.author)

      #  if amount == None:
       #     await ctx.send("Please enter an amount to gamble.")
        #    return

        #bal = await self.update_bank(ctx.author)
        #if amount == 'all':
         #   result = random.randint(1,2)
          #  embed = discord.Embed(title='Double or Nothing!', color = 0x000080)
           # if result == 1:
            #    await self.update_bank(ctx.author, bal[0])
             #   embed.add_field(name='Win!', value="Doubled!")

            #elif result == 2:
             #   await self.update_bank(ctx.author,-1*bal[0])
              #  embed.add_field(name='Loss..', value="Nothing...")

            #await ctx.send(embed=embed)
            #return

      #  amount = int(amount)
     #   if amount>bal[0]:
     #       await ctx.send("You cannot gamble an amount larger than you own.")
      #      return
     #   if amount<0:
    #        await ctx.send("It must be a positive number.")
       #     return

      #  result = random.randint(1,2)
     #   embed = discord.Embed(title='Double or Nothing!',color = 0x000080)
      #  if result == 1:
      #      await self.update_bank(ctx.author, amount)
      #      embed.add_field(name='Win!', value="Doubled!")

      #  elif result == 2:
       #     await self.update_bank(ctx.author,-1*amount)
      #      embed.add_field(name='Loss..', value="Nothing...")

       # await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Economy(bot))
