import discord
from discord.ext import commands
import asyncio
import random
import pickle
import sys
import math
import time
from PIL import Image, ImageFont, ImageDraw
from functools import partial
from io import BytesIO
from typing import Union
import aiohttp
from discord.ext.commands.cooldowns import BucketType

#Format:
#id XP time level rank#
class NWXPCog:
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)

    async def get_avatar(self, user: Union[discord.User, discord.Member]) -> bytes:
        #generally an avatar will be 1024x1024, but we shouldn't rely on this.
        avatar_url = user.avatar_url_as(format="png")

        async with self.session.get(avatar_url) as response:
            #this gives us our response object, and now we can read the bytes from it.
            avatar_bytes = await response.read()

        return avatar_bytes

    @staticmethod
    def processing(avatar_bytes: bytes, colour: tuple, ctx, placement:int, added:bool, member) -> BytesIO:

        #we must use BytesIO to load the image here as PIL expects a stream instead of just raw bytes.
        with Image.open(BytesIO(avatar_bytes)) as im:

            #this creates a new image the same size as the user's avatar, with the background colour being the user's colour.
            with Image.open('media/OnePieceWantedPosters.png') as background:

                #this ensures that the user's avatar lacks an alpha channel as we're going to be submitting our own here
                rgb_avatar = im.convert("RGB")

                #Resizes the avatar
                rgb_avatar = rgb_avatar.resize(size=(339,258))

                #this is the mask image we will be using to create the circle cutout effect on the avatar
                with Image.new("L", rgb_avatar.size, 0) as mask:

                    #ImageDraw lets us draw on the image. In this instance we will be using it to draw a white circle on the mask image.
                    mask_draw = ImageDraw.Draw(mask)

                    #draw the white circle from 0, 0 to the bottom right corner of the image.
                    mask_draw.rectangle([(0,0),500,300],fill=255)

                    #paste the alpha-less avatar on the background using the new circle mask we just created.
                    background.paste(rgb_avatar, (35,125), mask=mask)

                if ctx.guild.id != 462842304638484481:

                    #this is the mask image we will be using to create the text
                    with Image.new("L", rgb_avatar.size,0) as mask:

                        #ImageDraw lets us draw on the image. In this instance we will be using it to draw text on the image
                        fontDraw = ImageDraw.Draw(mask)

                        XPList = pickle.load(open('g5xp.data','rb'))

                        #we get the font.
                        nameFont = ImageFont.truetype(font='media/Vanib.ttf',size=35)
                            
                        #Make sure only 15 chars of the member's nickname is selected. If there aren't 15 chars then all are displayed without errors
                        if len(member.display_name) < 15:
                            maxLen = len(member.display_name)-1
                        else:
                            maxLen = 14

                        #we draw it on
                        fontDraw.multiline_text(xy=(0,0),text=f"{member.display_name[0:maxLen]}",fill=0x008800,font=nameFont,align="center",spacing=2)
                            
                        background.paste((56, 46, 46),(45,440),mask=mask)

                    with Image.new("L", rgb_avatar.size,0) as mask:

                        #ImageDraw lets us draw on the image. In this instance we will be using it to draw text on the image
                        fontDraw = ImageDraw.Draw(mask)

                        #we get the font.
                        numberFont = ImageFont.truetype(font='media/verdanab.ttf',size=32)

                        #we draw it on
                        fontDraw.multiline_text(xy=(0,0),text=f"{random.randint(0,9999999999999)}",fill=0x008800,font=numberFont,align="center",spacing=2)

                        background.paste((56, 46, 46),(70,500),mask=mask)

                else:

                    #this is the mask image we will be using to create the text
                    with Image.new("L", rgb_avatar.size,0) as mask:

                        #ImageDraw lets us draw on the image. In this instance we will be using it to draw text on the image
                        fontDraw = ImageDraw.Draw(mask)

                        #we get the font.
                        nameFont = ImageFont.truetype(font='media/Vanib.ttf',size=35)

                        XPList = pickle.load(open('g5xp.data','rb'))

                        if added == True and member == None:

                            member = ctx.guild.get_member(XPList[placement]['id'])

                        #Make sure only 15 chars of the member's nickname is selected. If there aren't 15 chars then all are displayed without errors
                        if len(member.display_name) < 15:
                            maxLen = len(member.display_name)
                        else:
                            maxLen = 15

                        #we draw it on
                        fontDraw.multiline_text(xy=(0,0),text=f"{member.display_name[0:maxLen]}",fill=0x008800,font=nameFont,align="center",spacing=2)

                        background.paste((56, 46, 46),(45,440),mask=mask)

                    with Image.new("L", rgb_avatar.size,0) as mask:

                        #ImageDraw lets us draw on the image. In this instance we will be using it to draw text on the image
                        fontDraw = ImageDraw.Draw(mask)

                        #we get the font.
                        numberFont = ImageFont.truetype(font='media/verdanab.ttf',size=32)

                        #we get the user's xp/bounty
                        XPList = pickle.load(open('g5xp.data','rb'))
                        if added == False:
                            fontDraw.multiline_text(xy=(0,0),text=f"{XPList[placement]['xp']}",fill=0x008800,font=nameFont,align="center",spacing=2)
                        else:
                            #we draw it on
                            fontDraw.multiline_text(xy=(0,0),text=f"{XPList[placement]['xp']}",fill=0x008800,font=numberFont,align="center",spacing=2)

                        background.paste((56, 46, 46),(70,500),mask=mask)

                #prepare the stream to save this image into
                final_buffer = BytesIO()

                #save into the stream, using png format.
                background.save(final_buffer, "png")

            #seek back to the start of the stream
            final_buffer.seek(0)

            return final_buffer

    @commands.command(name='wanted')
    async def Wanted(self,ctx,*,member:discord.Member = None):
        member = member or ctx.author
        async with ctx.typing():
            #this means that the bot will type while it is processing and uploading the image

            if isinstance(member, discord.Member):
                #get the user's colour, pretty self explanatory
                member_colour = member.colour.to_rgb()
            else:
                #if this is in a DM or something went seriously wrong
                member_colour = (0,0,0)

            #grab theuser's avatar as bytes
            avatar_bytes = await self.get_avatar(member)

            #create partial function so we don't have to stack the args in run_in_executor
            fn = partial(self.processing,avatar_bytes,member_colour,ctx,0,False,member)

            #this runs our processing in an executor, stopping it from blocking the thread loop as we already seeked back the buffer in the other thread.
            final_buffer = await self.bot.loop.run_in_executor(None,fn)

            #prepares the file
            file = discord.File(filename="wanted.png", fp=final_buffer)

            #send it
            await ctx.send(file=file)

            
    @commands.group(name='bounty',aliases=['reward','worth','value'])
    async def g5b(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("You haven't sent a bounty subcommand. Subcommands are: `check` and `rank`.")

    @g5b.command(name='check')
    async def CCheck(self, ctx, *, member:discord.Member = None):
        """Display the user's avatar on their colour"""

        #this means that if the user does not supply a member, it will default to the author of the message.
        member = member or ctx.author

        XPList = []
        XPList = pickle.load(open('g5xp.data', 'rb'))
        added = False
        addedXP = random.randint(30,35)
        placement = 0
        for y in range(len(XPList)):
            if XPList[y]['id'] == member.id:
                added = True
                placement = y
                break
        if added == True:
            
            async with ctx.typing():
                #this means that the bot will type while it is processing and uploading the image

                if isinstance(member, discord.Member):
                    #get the user's colour, pretty self explanatory
                    member_colour = member.colour.to_rgb()
                else:
                    #if this is in a DM or something went seriously wrong
                    member_colour = (0,0,0)

                #grab theuser's avatar as bytes
                avatar_bytes = await self.get_avatar(member)

                #create partial function so we don't have to stack the args in run_in_executor
                fn = partial(self.processing,avatar_bytes,member_colour,ctx,placement,True,member)

                #this runs our processing in an executor, stopping it from blocking the thread loop as we already seeked back the buffer in the other thread.
                final_buffer = await self.bot.loop.run_in_executor(None,fn)

                #prepares the file
                file = discord.File(filename="wanted.png", fp=final_buffer)

                #send it
                await ctx.send(content=f"Most wanted **#{placement}**",file=file)

        elif added == False:
            await ctx.send("That user don't currently have any XP yet.")
            
    @g5b.command(name='rank')
    @commands.cooldown(120,seconds,Buckettype.user)
    async def CRank(self, ctx, placement:int=None):
        if ctx.guild == None:
            return
        if placement == None:
            placement = 1
        XPList = []
        XPList = pickle.load(open('g5xp.data', 'rb'))
        added = False
        if (placement) >= len(XPList) or placement < 1:
            await ctx.send("There isn't a person at that rank.")
            return
        member = self.bot.get_user_info(XPList[placement]['id'])

        async with ctx.typing():
            #this means that the bot will type while it is processing and uploading the image

            if isinstance(member, discord.Member):
                #get the user's colour, pretty self explanatory
                member_colour = member.colour.to_rgb()
            else:
                #if this is in a DM or something went seriously wrong
                member_colour = (0,0,0)

            #grab theuser's avatar as bytes
            avatar_bytes = await self.get_avatar(member)

            #create partial function so we don't have to stack the args in run_in_executor
            fn = partial(self.processing,avatar_bytes,member_colour,ctx,placement,True,member)

            #this runs our processing in an executor, stopping it from blocking the thread loop as we already seeked back the buffer in the other thread.
            final_buffer = await self.bot.loop.run_in_executor(None,fn)

            #prepares the file
            file = discord.File(filename="wanted.png", fp=final_buffer)

            #send it
            await ctx.send(content=f"Most wanted **#{placement}**",file=file)

    @g5b.command(name='reset')
    @commands.is_owner()
    async def vReset(self,ctx):
        XPList=[]
        XPList.append({'id':0,'xp':10000000000000000, 'timeOfNextXpEarn':0})
        pickle.dump(XPList, open('g5xp.data','wb'))
        print("Done")

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(NWXPCog(bot))
