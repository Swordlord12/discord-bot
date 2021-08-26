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

SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']

creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

client = gspread.authorize(creds)

maptest = client.open("Map Game VI Database").worksheet("Territories")

# The ID spreadsheet.
SAMPLE_SPREADSHEET_ID = '1EodY2Cs1t1UfarRwF80pIcLLGsD2OfdiyIImRD02g8g'

service = build('sheets', 'v4', credentials=creds)

sheet = service.spreadsheets()

income_result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="General Stats!A1:N1000").execute()
income_values = income_result.get('values')

os.chdir("C:\\Users\\Jude\\googleanddisccombo")


mainshop = [{"name":"Fort Construction Materials", "price": 25, "description":"allows you to place a fort anywhere on the map."},
            {"name":"5 Infrantry", "price": 50, "description":"Allows you to deploy 5 additional infrantry."},
            {"name":"5 Destroyers", "price":75, "description":"Allows you to deploy 5 additional destroyers."},
            {"name":"5 Planes", "price":125, "description":"Allows you to deploy 5 additional airforce."}
            ]

winningConditions = [ 
    [0,1,2],
    [3,4,5],
    [6,7,8],
    [0,3,6],
    [1,4,7],
    [2,5,8],
    [0,4,8],
    [2,4,6]
]

player1 = ''
player2 = ''
turn = ""
gameOver = True

board = []

def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]]  == mark and board[condition[2]] == mark:
            gameOver = True

class Economy(commands.Cog, description='Handles the commands that deal with currency and oil for the Map Game.'):

    """the fake schmoney"""

    def __init__(self, bot):
        self.bot=bot

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
    
    async def get_bank_data(self):
        with open("mainbank.json", "r") as f:
            users = json.load(f)

        return users

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
        em.add_field(name = "Bank", value = f'<:mapgamecoin:874347046587486248>{bank_amount}.', inline=False)
        await ctx.send(embed = em)

    @commands.command(aliases=["daily", "money", "revenue"])
    #@commands.cooldown(1, 86400,commands.BucketType.user)
    async def income(self, ctx, *, empire):
        """awards you with your empires income for the day."""
        await self.open_account(ctx.author)

        users = await self.get_bank_data()
        user = ctx.author

        found = False
        if not found:
            for owner_row in income_values[1:]:
                if owner_row[1].lower() == empire.lower():
                    embed = discord.Embed(title=f"{empire}'s Daily Income", color=0x000080)
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

        #await ctx.send(f"You have recieved <:mapgamecoin:874347046587486248>{earnings} from your empires wealth today.")
        if found == False:
            embed = discord.Embed(title="Error", color = 0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Empire", value='You must enter a valid empire name.')
            await ctx.send(embed=embed)
            return
        eastern = pytz.timezone('US/Eastern')
        utc = pytz.utc
        time = datetime.now(tz=eastern)
        string_time = time.strftime("%m/%d/%Y %H:%M:%S")
        inputs = [[empire, earnings, oil_earned, string_time]]
        request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                range="Invoice!A1", valueInputOption="USER_ENTERED", body={"values":inputs}).execute()

        users[str(user.id)]["wallet"] += earnings

        with open("mainbank.json", "w") as f:
            json.dump(users,f)
        
    async def update_bank(self, user, change = 0, mode = "wallet"):
        users = await self.get_bank_data()

        users[str(user.id)][mode] += change

        with open("mainbank.json", "w") as f:
            json.dump(users,f)

        bal = [users[str(user.id)]['wallet'],users[str(user.id)]['bank']]
        return bal

    @commands.command(aliases=['wd'])
    async def withdraw(self, ctx, amount:int = 0):
        """takes money from bank to put into wallet"""
        await self.open_account(ctx.author)

        if amount == 0:
            await ctx.send("Please enter an amount to withdrawal.")
            return

        bal = await self.update_bank(ctx.author)

        amount = int(amount)
        if amount>bal[1]:
            await ctx.send("You cannot withdrawal an amount larger than you have stored.")
            return
        if amount<0:
            await ctx.send("It must be a positive number.")
            return
        
        await self.update_bank(ctx.author, amount)
        await self.update_bank(ctx.author,-1*amount, "bank")
        await ctx.send(f'You withdrew {amount} dollars.')
    
    @commands.command(aliases=['dp', 'dep'])
    async def deposit(self, ctx, amount:int = 0):
        """takes money from wallet to put into bank"""
        await self.open_account(ctx.author)

        if amount == 0:
            await ctx.send("Please enter an amount to deposit.")
            return

        bal = await self.update_bank(ctx.author)

        amount = int(amount)

        if amount>bal[0]:
            await ctx.send("You cannot deposit an amount larger than you own.")
            return
        if amount<0:
            await ctx.send("It must be a positive number.")
            return
        
        
        await self.update_bank(ctx.author,-1*amount)
        await self.update_bank(ctx.author,amount, "bank")
        await ctx.send(f'You deposited {amount} dollars.')

    @deposit.error
    async def depositerror(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Argument", value='Only numbers are accepted for depositing.')
            await ctx.send(embed=embed)

    @withdraw.error
    async def withdrawerror(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Argument", value='Only numbers are accepted for withdrawing.')
            await ctx.send(embed=embed)

    @commands.command(aliases=['gift'])
    async def send(self, ctx,member:discord.Member, amount:int = 0):
        """gives user money from ur wallet"""
        await self.open_account(ctx.author)
        await self.open_account(member)


        if amount == 0:
            await ctx.send("Please enter an amount to send.")
            return

        bal = await self.update_bank(ctx.author)

        if int(amount)>bal[0]:
            await ctx.send("You cannot send an amount larger than you own.")
            return
        if int(amount)<0:
            await ctx.send("It must be a positive number.")
            return
        
        await self.update_bank(ctx.author,-1*amount)
        await self.update_bank(member,amount)
        await ctx.send(f'You gave {amount} dollars to {member.mention}.')

    @send.error
    async def senderror(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Argument", value='You must provide a number. Make sure they are correct as well.')
            await ctx.send(embed=embed)

#    @commands.command(aliases=['slots', 'gamble'])
#    async def slotmachine(self, ctx, amount:int = 0):
#        await self.open_account(ctx.author)
#
 #       if amount == 0:
  #          await ctx.send("Please enter an amount to gamble.")
   #         return
#
 #       bal = await self.update_bank(ctx.author)
#
 #       amount = int(amount)
  #      if amount>bal[0]:
   #         await ctx.send("You cannot gamble an amount larger than you own.")
    #        return
     #   if amount<0:
      #      await ctx.send("It must be a positive number.")
       #     return

   #     final = []
    #    for i in range(3):
     #       a = random.choice(["🥰", "😫", "🤩", "😎"])
#
 #           final.append(a)
#
 #       embed = discord.Embed(title='Slots', color=0x000080)
#
 #       if final[0] == final[1] and final[0] == final[2] and final[2] == final[1]:
  #          await self.update_bank(ctx.author,10*amount)
   #         embed.add_field(name=str(final), value="Major Win!")
#
 #       elif final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
  #          await self.update_bank(ctx.author,round(1.25*amount))
   #         embed.add_field(name=str(final), value="Minor Win!")
    #    else:
     #       await self.update_bank(ctx.author,-1*amount)
      #      embed.add_field(name=str(final), value="Loss...")
       # await ctx.send(embed=embed)
#
 #   @commands.command(aliases=['rob'])
  #  @commands.cooldown(1,600,commands.BucketType.user)
   # async def steal(self, ctx, member:discord.Member):
    #    await self.open_account(ctx.author)
     #   await self.open_account(member)
#
 #       bal = await self.update_bank(member)
#
 #       chance = random.randint(0,1)
#
 #       if chance == 1:
  #          await ctx.send("You got nothing!")
   #         return
#
 #       if bal[0]<100:
  #          await ctx.send("Don't try it Anakin... they are much too poor...")
   #         return
#
 #       loot = random.randrange(0, bal[0])
  #      
   #     await self.update_bank(ctx.author, loot)
    #    await self.update_bank(member,-1*loot)
#
 #       await ctx.send(f'You stole {loot} dollars from {member.mention}.') """
    
    #@steal.error
    #async def stealerror(self, ctx, error):
     #   if isinstance(error, MissingRequiredArgument):
      #      embed=discord.Embed(title='Error', color=0xFF0000)
       #     embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
        #    embed.add_field(name="Missing Argument", value='You must provide all required fields.')
         #   await ctx.send(embed=embed)

    @commands.command(aliases=['store'])
    async def shop(self, ctx):
        em =discord.Embed(title='Shop', color=0x000080)

        for item in mainshop:
            name = item['name']
            price = item['price']
            description = item['description']
            em.add_field(name=name, value=f'<:mapgamecoin:874347046587486248>{price} - {description}')

        await ctx.send(embed = em)

    @commands.command(aliases=['purchase'])
    async def buy(self, ctx, amount:int=1, *, item):
        await self.open_account(ctx.author)

        res = await self.buy_this(ctx.author,item,amount)

        if not res[0]:
            if res[1]==1:
                await ctx.send("That object does not exist.")
            if res[1]==2:
                await ctx.send(f'You are too broke to purchase {amount} of {item}(s)')

        else:
            await ctx.send(f'You just bought {amount} {item}')

    async def buy_this(self,user,item_name,amount:int):
        item_name = item_name.lower()
        name_ = None
        for item in mainshop:
            name = item['name'].lower()
            if name == item_name:
                name_ = name
                price = item['price']
                break

        if name_ == None:
            return [False,1]

        cost = price*amount

        users = await self.get_bank_data()

        bal = await self.update_bank(user)

        if bal[0]<cost:
            return [False,2]

        try:
            index = 0
            t = None
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

        return [True,"Worked"]

    @commands.command(aliases=['inventory','inv', 'storage'], description='Shows what you have purchased.')
    async def bag(self, ctx):
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

    """@commands.command()
    async def sell(self,ctx,item,amount:int = 1):
        await self.open_account(ctx.author)

        res = await self.sell_this(ctx.author,item,amount)

        if not res[0]:
            if res[1]==1:
                await ctx.send('You don\'t own that object.')
                return
            if res[1]==2:
                await ctx.send(f"You don't have {amount} {item} lying around")
                return
            if res[1]==3:
                await ctx.send(f"You don't have {item} anywhere")
                return

        else:
            await ctx.send(f'You have sold {amount} {item} from your bag.')

    async def sell_this(self,user,item_name,amount):
        item_name = item_name.lower()
        name_ = None
        for item in mainshop:
            name = item["name"].lower()
            if name == item_name:
                name_ = name
                price = item["price"]
                break
        
        if name_ == None:
            return [False,1]

        cost = price*amount

        users = await self.get_bank_data()

        bal = await self.update_bank(user)


        try:
            index = 0
            t = None
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

        return [True, "Worked"]"""

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