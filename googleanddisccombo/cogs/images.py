import discord
from discord.ext import commands
import random
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from io import BytesIO

#this is the images cog, it deals with things to do with Images and most of the stuff in here is purely joking around
praises = ["He is such a cutie isn't he? 😊", "He is def my supreme leader! 🥰", "Now this is what u call a hottie. 🥵"]

leader_images = ["https://cdn.discordapp.com/attachments/800039486339678250/870413731392286741/kimmy.png",
                'https://cdn.discordapp.com/attachments/800039486339678250/870413737213984808/KIMMYWITHHATTY.jpg',
                'https://cdn.discordapp.com/attachments/800039486339678250/870414524795224104/unknown.png']


class Images(commands.Cog, description='Commands that have to do with images, gifs, or tweaking a users profile picture.'):

    """These commands have something to do with an image or gif."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['supreme', 'sl', 'leader', 'kimmy'])
    async def supremeleader(self, ctx):
        """shows you a picture of the glorious leader"""
        embed = discord.Embed(title="Kim Jong-Un", description=random.choice(praises), color=0x000080)
        embed.set_image(url=random.choice(leader_images))
        await ctx.send(embed = embed)

    @commands.command()
    async def deceitler(self, ctx):
        embed = discord.Embed(title='The photoshop the world needed...')
        embed.set_image(url='https://cdn.discordapp.com/attachments/874298438131531840/882443554679566436/AdolfDeceitler.jpg')
        await ctx.send(embed=embed)

    #this guy is an inside joke between me and the creator of the map game
    @commands.command()
    async def schlafly(self, ctx):
        """sends deceit to whoever uses it"""
        await ctx.send('https://tenor.com/view/schlafly-schlafly-laugh-laugh-laughing-schlafly-gif-21159913')

    @commands.command(aliases=['burg', 'trigburg', 'burgtriggered', 'burgtrig'])
    async def triggeredburg(self, ctx):
        """sends a triggered burg gif"""
        await ctx.send(file=discord.File('burgtrig.gif'))

    @commands.command()
    async def deceit(self, ctx, user:discord.Member):
        if not user:
            user = ctx.author
        #opens file
        schlafly = Image.open("deceit.png")
        #prepares to draw onto that image
        draw = ImageDraw.Draw(schlafly)
        #derives the font from a ttf file
        font = ImageFont.truetype("COMIC.ttf", 36)
        #sets the text
        text = "DECEIT"
        #gets the users profile picture and sets it to a 64x64 image
        asset = user.avatar_url_as(size = 64)
        data = BytesIO(await asset.read())
        #opens the profile picture
        pfp = Image.open(data)

        #it resizes to fit the window better
        pfp = pfp.resize((69,69))

        #this pastes the pfp at the selected coordinates
        schlafly.paste(pfp, (93,0))
        #this draws the text in the set font
        draw.text((0,175),text,(75,0,0), font=font)

        #these save the image and then sends it to discord.
        schlafly.save("profile.png")
        await ctx.send(file=discord.File("profile.png"))

    @commands.command()
    async def ship(self, ctx, user1:discord.Member, user2:discord.Member):
        ship = Image.open("presidentship.png")
        draw = ImageDraw.Draw(ship)
        font = ImageFont.truetype("COMIC.ttf", 20)
        text1 = str(user1.name)
        text2 = str(user2.name)
        asset1 = user1.avatar_url_as(size=64)
        asset2 = user2.avatar_url_as(size=64)
        data1 = BytesIO(await asset1.read())
        data2 = BytesIO(await asset2.read())
        pfp1 = Image.open(data1)
        pfp2 = Image.open(data2)

        ship.paste(pfp1, (35, 96))
        ship.paste(pfp2, (128, 96))
        draw.text((28, 184), text1, (255, 255, 0), font=font)
        draw.text((110, 184), text2, (255, 255, 0), font=font)

        ship.save("thegoodship.png")

        ship_score = random.randint(0, 1000)
        if ship_score < 5:
            ship_statement = "You go worse than dinosaurs and comets and then some. Just say goodbye to that matchup."
        elif 5 <= ship_score < 25:
            ship_statement = "You go together like Kimmy and South Korea. Not well, as South Korea clearly doesn't exist. Its just The People's Democratic Republic of Korea. They just like to be rebellious..."
        elif 25 <= ship_score < 50:
            ship_statement = "Schlafly would be a better match than this for both of you."
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
        else:
            ship_statement = "Y'all are **so** good, Schlafly wouldn't call it deceit."
        await ctx.send(file=discord.File("thegoodship.png"))
        await ctx.send(f'{user1.name} :hearts: {user2.name}\n Ship Score: {ship_score}\n {ship_statement}')

    @ship.error
    async def shiperror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Arguments", value='You must provide all required fields.')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Argument", value='All arguments must be mentions of users.')
            await ctx.send(embed=embed)

    @commands.command()
    async def urmom(self, ctx, user:discord.Member):
        if not user:
            user = ctx.author

        mom = Image.open("urmom.png")

        asset = user.avatar_url_as(size = 512)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((469,469))

        mom.paste(pfp, (119,0))

        mom.save("mom.png")

        await ctx.send(file=discord.File("mom.png"))

    @commands.command(aliases=["vs"])
    async def versus(self, ctx, user1:discord.Member, user2:discord.Member):
        vs_start = Image.open("VERSUS.png")

        asset1 = user1.avatar_url_as(size = 256)
        data1 = BytesIO(await asset1.read())
        pfp1 = Image.open(data1)

        vs_start.paste(pfp1, (4, 45))

        asset2 = user2.avatar_url_as(size = 256)
        data2 = BytesIO(await asset2.read())
        pfp2 = Image.open(data2)

        vs_start.paste(pfp2, (460, 45))

        vs_start.save("vs.png")

        await ctx.send(file=discord.File("vs.png"))

    @versus.error
    async def vserror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Arguments", value='You must provide all required fields.')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Argument", value='All arguments must be mentions of users.')
            await ctx.send(embed=embed)

    @commands.command()
    async def surveysays(self, ctx, *, text:str):
        harvey = Image.open("STEVEHARVEY.jpg")
        draw = ImageDraw.Draw(harvey)
        font = ImageFont.truetype("Gelasio-Regular.ttf", 96)
        
        draw.text((1000,10),text,(0,0,0), font=font)

        harvey.save("surveysays.jpg")

        await ctx.send(file=discord.File("surveysays.jpg"))
    @surveysays.error
    async def surveyerror(self,ctx,error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Arguments", value='You must provide all required fields.')
            await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(Images(bot))