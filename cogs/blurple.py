import discord # discord.py rewrite
# pip install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice]
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import asyncio
from PIL import Image, ImageEnhance, ImageSequence
import PIL
#pip install Pillow
from io import BytesIO
import io
import datetime
import aiohttp
import copy
import sys
import time
from resizeimage import resizeimage
#pip install python-resize-image
import math


class BlurpleifyCog:
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def blurple(self, ctx, arg1 = None):
        picture = None

        await ctx.send(f"{ctx.message.author.mention}, starting blurple image analysis (Please note that this may take a while)")


        start = time.time()
        if arg1 != None:
            if "<@!" in arg1:
                arg1 = arg1[:-1]
                arg1 = arg1[3:]
            if "<@" in arg1:
                arg1 = arg1[:-1]
                arg1 = arg1[2:]
            if arg1.isdigit() == True:
                try:
                    user = await self.bot.get_user_info(int(arg1))
                    picture = user.avatar_url
                except Exception:
                    pass
            else:
                picture = arg1
        else:
            link = ctx.message.attachments
            if len(link) != 0:
                for image in link:
                    picture = image.url

        if picture == None:
            picture = ctx.author.avatar_url

        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(picture) as r:
                    response = await r.read()
        except ValueError:
            await ctx.send(f"{ctx.author.display_name}, please link a valid image URL")
            return

        colourbuffer = 20

        try:
            im = Image.open(BytesIO(response))
        except Exception:
            await ctx.send(f"{ctx.author.display_name}, please link a valid image URL")
            return

        im = im.convert('RGBA')
        imsize = list(im.size)
        impixels = imsize[0]*imsize[1]
        #1250x1250 = 1562500
        maxpixelcount = 1562500

        end = time.time()
        #await ctx.send(f'{ctx.message.author.display_name}, image fetched, analysing image (This process can sometimes take a while depending on the size of the image) ({end - start:.2f}s)')
        start = time.time()
        if impixels > maxpixelcount:
            downsizefraction = math.sqrt(maxpixelcount/impixels)
            im = resizeimage.resize_width(im, (imsize[0]*downsizefraction))
            imsize = list(im.size)
            impixels = imsize[0]*imsize[1]
            end = time.time()
            await ctx.send(f'{ctx.message.author.display_name}, image resized smaller for easier processing ({end-start:.2f}s)')
            start = time.time()

        def imager(im):
            global noofblurplepixels
            noofblurplepixels = 0
            global noofwhitepixels
            noofwhitepixels = 0
            global noofdarkblurplepixels
            noofdarkblurplepixels = 0
            global nooftotalpixels
            nooftotalpixels = 0
            global noofpixels
            noofpixels = 0

            blurple = (114, 137, 218)
            darkblurple = (78, 93, 148)
            white = (255, 255, 255)
            
            img = im.load()

            for x in range(imsize[0]):
                i = 1
                for y in range(imsize[1]):
                    pixel = img[x,y]
                    check = 1
                    checkblurple = 1
                    checkwhite = 1
                    checkdarkblurple = 1
                    for i in range(3):
                        if not(blurple[i]+colourbuffer > pixel[i] > blurple[i]-colourbuffer):
                            checkblurple = 0
                        if not(darkblurple[i]+colourbuffer > pixel[i] > darkblurple[i]-colourbuffer):
                            checkdarkblurple = 0
                        if not(white[i]+colourbuffer > pixel[i] > white[i]-colourbuffer):
                            checkwhite = 0
                        if checkblurple == 0 and checkdarkblurple == 0 and checkwhite == 0:
                            check = 0
                    if check == 0:
                        img[x,y] = (0, 0, 0, 255)
                    if check == 1:
                        nooftotalpixels += 1
                    if checkblurple == 1:
                        noofblurplepixels += 1
                    if checkdarkblurple == 1:
                        noofdarkblurplepixels += 1
                    if checkwhite == 1:
                        noofwhitepixels += 1
                    noofpixels += 1

            image_file_object = io.BytesIO()
            im.save(image_file_object, format='png')
            image_file_object.seek(0)
            return image_file_object

        with aiohttp.ClientSession() as session:
            start = time.time()
            image = await self.bot.loop.run_in_executor(None, imager, im)
            end = time.time()
            #await ctx.send(f"{ctx.author.display_name}, image data extracted ({end - start:.2f}s)")
            image = discord.File(fp=image, filename='image.png')

            blurplenesspercentage = round(((nooftotalpixels/noofpixels)*100), 2)
            percentblurple = round(((noofblurplepixels/noofpixels)*100), 2)
            percentdblurple = round(((noofdarkblurplepixels/noofpixels)*100), 2)
            percentwhite = round(((noofwhitepixels/noofpixels)*100), 2)

            blurpleuserrole = discord.utils.get(ctx.message.guild.roles, id=436300514561622016)
            embed = discord.Embed(Title = "", colour = 0x7289DA)
            embed.add_field(name="Total amount of Blurple", value=f"{blurplenesspercentage}%", inline=False)
            embed.add_field(name="Blurple (rgb(114, 137, 218))", value=f"{percentblurple}%", inline=True)
            embed.add_field(name="White (rgb(255, 255, 255))", value=f"{percentwhite}\%", inline=True)
            embed.add_field(name="Dark Blurple (rgb(78, 93, 148))", value=f"{percentdblurple}\%", inline=True)
            embed.add_field(name="Guide", value="Blurple, White, Dark Blurple = Blurple, White, and Dark Blurple (respectively) \nBlack = Not Blurple, White, or Dark Blurple", inline=False)
            embed.set_footer(text=f"Please note: Discord slightly reduces quality of the images, therefore the percentages may be slightly inaccurate. | Content requested by {ctx.author}")
            embed.set_image(url="attachment://image.png")
            embed.set_thumbnail(url=picture)
            await ctx.send(embed=embed, file=image)

            if blurplenesspercentage > 75 and picture == ctx.author.avatar_url and blurpleuserrole not in ctx.author.roles and percentblurple > 5:
                await ctx.send(f"{ctx.message.author.display_name}, as your profile pic has enough blurple (over 75% in total and over 5% blurple), you have recieved the role **{blurpleuserrole.name}**!")
                await ctx.author.add_roles(blurpleuserrole)
            elif picture == ctx.author.avatar_url and blurpleuserrole not in ctx.author.roles:
                await ctx.send(f"{ctx.message.author.display_name}, your profile pic does not have enough blurple (over 75% in total and over 5% blurple), therefore you are not eligible for the role '{blurpleuserrole.name}'. However, this colour detecting algorithm is automated, so if you believe your pfp is blurple enough, please DM a Staff member and they will manually give you the role if it is blurple enough. (Not sure how to make a blurple logo? Head over to <#412755378732793868> or <#436026199664361472>!)")

    @commands.command(aliases=['blurplfy', 'blurplefier'])
    async def blurplefy(self, ctx, arg1 = None):
        picture = None

        await ctx.send(f"{ctx.message.author.mention}, starting blurple image analysis (Please note that this may take a while)")


        start = time.time()
        if arg1 != None:
            if "<@!" in arg1:
                arg1 = arg1[:-1]
                arg1 = arg1[3:]
            if "<@" in arg1:
                arg1 = arg1[:-1]
                arg1 = arg1[2:]
            if arg1.isdigit() == True:
                try:
                    user = await self.bot.get_user_info(int(arg1))
                    picture = user.avatar_url
                except Exception:
                    pass
            else:
                picture = arg1
        else:
            link = ctx.message.attachments
            if len(link) != 0:
                for image in link:
                    picture = image.url

        if picture == None:
            picture = ctx.author.avatar_url

        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(picture) as r:
                    response = await r.read()
        except ValueError:
            await ctx.send(f"{ctx.author.display_name}, please link a valid image URL")
            return

        colourbuffer = 20

        try:
            im = Image.open(BytesIO(response))
        except Exception:
            await ctx.send(f"{ctx.author.display_name}, please link a valid image URL")
            return

        imsize = list(im.size)
        impixels = imsize[0]*imsize[1]
        #1250x1250 = 1562500
        maxpixelcount = 1562500

        try:
            i = im.info["version"]
            isgif = True
            gifloop = int(im.info["loop"])
        except Exception:
            isgif = False


        

        end = time.time()
        #await ctx.send(f'{ctx.message.author.display_name}, image fetched, analysing image (This process can sometimes take a while depending on the size of the image) ({end - start:.2f}s)')
        start = time.time()
        if impixels > maxpixelcount:
            downsizefraction = math.sqrt(maxpixelcount/impixels)
            im = resizeimage.resize_width(im, (imsize[0]*downsizefraction))
            imsize = list(im.size)
            impixels = imsize[0]*imsize[1]
            end = time.time()
            #await ctx.send(f'{ctx.message.author.display_name}, image resized smaller for easier processing ({end-start:.2f}s)')
            start = time.time()

        def imager(im):
            im = im.convert(mode='L')
            im = ImageEnhance.Contrast(im).enhance(1000)
            im = im.convert(mode='RGB')

            img = im.load()

            for x in range(imsize[0]-1):
                i = 1
                for y in range(imsize[1]-1):
                    pixel = img[x,y]

                    if pixel != (255, 255, 255):
                        img[x,y] = (114, 137, 218)

            image_file_object = io.BytesIO()
            im.save(image_file_object, format='png')
            image_file_object.seek(0)
            return image_file_object

        def gifimager(im, gifloop):
            frames = [frame.copy() for frame in ImageSequence.Iterator(im)]
            newgif = []

            for frame in frames:

                frame = frame.convert(mode='L')
                frame = ImageEnhance.Contrast(frame).enhance(1000)
                frame = frame.convert(mode='RGB')

                img = frame.load()

                for x in range(imsize[0]):
                    i = 1
                    for y in range(imsize[1]):
                        pixel = img[x,y]

                        if pixel != (255, 255, 255):
                            img[x,y] = (114, 137, 218)

                newgif.append(frame)

            image_file_object = io.BytesIO()

            gif = newgif[0]
            gif.save(image_file_object, format='gif', save_all=True, append_images=newgif[1:], loop=0)

            image_file_object.seek(0)
            return image_file_object


        with aiohttp.ClientSession() as session:
            start = time.time()
            if isgif == False:
                image = await self.bot.loop.run_in_executor(None, imager, im)
            else:
                image = await self.bot.loop.run_in_executor(None, gifimager, im, gifloop)
            end = time.time()
            #await ctx.send(f"{ctx.author.display_name}, image data extracted ({end - start:.2f}s)")
            if isgif == False:
                image = discord.File(fp=image, filename='image.png')
            else:
                image = discord.File(fp=image, filename='image.gif')

            try:
                embed = discord.Embed(Title = "", colour = 0x7289DA)
                embed.set_author(name="Blurplefier - makes your image blurple!")
                if isgif == False:
                    embed.set_image(url="attachment://image.png")
                    embed.set_footer(text=f"Please note - This blurplefier is automated and therefore may not always give you the best result. | Content requested by {ctx.author}")
                else:
                    embed.set_image(url="attachment://image.gif")
                    embed.set_footer(text=f"Please note - This blurplefier is automated and therefore may not always give you the best result. Disclaimer: This image is a gif, and the quality does not always turn out great. HOWEVER, the gif is quite often not as grainy as it appears in the preview | Content requested by {ctx.author}")
                embed.set_thumbnail(url=picture)
                await ctx.send(embed=embed, file=image)
            except Exception:
                await ctx.send(f"{ctx.author.display_name}, whoops! It looks like this gif is too big to upload. If you want, you can give it another go, except with a smaller version of the image. Sorry about that!")

    @commands.command(aliases=['blurplfygif', 'blurplefiergif'])
    async def blurplefygif(self, ctx, arg1 = None):
        picture = None

        await ctx.send(f"{ctx.message.author.mention}, starting blurple image analysis (Please note that this may take a while)")


        start = time.time()
        if arg1 != None:
            if "<@!" in arg1:
                arg1 = arg1[:-1]
                arg1 = arg1[3:]
            if "<@" in arg1:
                arg1 = arg1[:-1]
                arg1 = arg1[2:]
            if arg1.isdigit() == True:
                try:
                    user = await self.bot.get_user_info(int(arg1))
                    picture = user.avatar_url
                except Exception:
                    await ctx.send("Please send a valid user mention/ID")
            else:
                picture = arg1
        else:
            link = ctx.message.attachments
            if len(link) != 0:
                for image in link:
                    picture = image.url

        if picture == None:
            picture = ctx.author.avatar_url

        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(picture) as r:
                    response = await r.read()
        except ValueError:
            await ctx.send(f"{ctx.author.display_name}, please link a valid image URL")
            return

        colourbuffer = 20

        try:
            im = Image.open(BytesIO(response))
        except Exception:
            await ctx.send(f"{ctx.author.display_name}, please link a valid image URL")
            return

        if im.format != 'GIF':
            return

        imsize = list(im.size)
        impixels = imsize[0]*imsize[1]

        maxpixelcount = 1562500

        end = time.time()
        await ctx.send(f'{ctx.message.author.display_name}, image fetched, analysing image (This process can sometimes take a while depending on the size of the image) ({end - start:.2f}s)')
        start = time.time()
        if impixels > maxpixelcount:
            downsizefraction = math.sqrt(maxpixelcount/impixels)
            im = resizeimage.resize_width(im, (imsize[0]*downsizefraction))
            imsize = list(im.size)
            impixels = imsize[0]*imsize[1]
            end = time.time()
            await ctx.send(f'{ctx.message.author.display_name}, image resized smaller for easier processing ({end-start:.2f}s)')
            start = time.time()

        def imager(im):
            frames = [frame.copy() for frame in ImageSequence.Iterator(im)]
            newgif = []

            for frame in frames:

                frame = frame.convert(mode='L')
                frame = ImageEnhance.Contrast(frame).enhance(1000)
                frame = frame.convert(mode='RGB')

                img = frame.load()

                for x in range(imsize[0]):
                    i = 1
                    for y in range(imsize[1]):
                        pixel = img[x,y]

                        if pixel != (255, 255, 255):
                            img[x,y] = (114, 137, 218)

                newgif.append(frame)

            image_file_object = io.BytesIO()

            gif = newgif[0]
            gif.save(image_file_object, format='gif', save_all=True, append_images=newgif[1:], loop=0)

            image_file_object.seek(0)
            return image_file_object

        with aiohttp.ClientSession() as session:
            start = time.time()
            image = await self.bot.loop.run_in_executor(None, imager, im)
            end = time.time()
            await ctx.send(f"{ctx.author.display_name}, image data extracted ({end - start:.2f}s)")
            image = discord.File(fp=image, filename='image.gif')


            embed = discord.Embed(Title = "", colour = 0x7289DA)
            embed.set_author(name="Blurplefier - makes your image blurple!")
            embed.set_footer(text=f"Please note - This blurplefier is automated and therefore may not always give you the best result. This also currently does not work with gifs. | Content requested by {ctx.author}")
            embed.set_image(url="attachment://image.gif")
            embed.set_thumbnail(url=picture)
        await ctx.send(embed=embed, file=image)

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(BlurpleifyCog(bot))
