import discord
from discord.ext import commands
import asyncio
import random
import pickle
import sys
import math
import time

def LevelSet(xp):
    lvl=0
    while xp >= lvls_xp[lvl]:
        lvl += 1
    return lvl

def XPRem(xp):
    lvl=0
    while xp >= lvls_xp[lvl]:
        lvl += 1
    xp -= lvls_xp[lvl]
    return -xp

#Colouring
def RankColour(rank):
        if rank == 1:
            return 0xFFFF11
        elif rank == 2:
            return 0xAAAAAA
        elif rank == 3:
            return 0x994400
        elif rank > 3 and rank <= 5:
            return 0x00FFFF
        elif rank > 5 and rank <= 10:
            return 0xFF3377
        elif rank > 10 and rank <= 25:
            return 0x00CC66
        elif rank > 25 and rank <= 50:
            return 0xCC4411
        elif rank > 50 and rank <= 100:
            return 0x990055
        else:
            return 0xFFFFFF

#Format:
#User TotalXP Level (time.time())OfNextXPEarn
class XPCog:
    def __init__(self, bot):
        self.bot = bot
        self.lvl_xp = [(5*(i**2)+50*i+100) for i in range(500)]
        for x in range(1,len(lvl_xp)):
	    lvl_xp[x] = lvl_xp[x] + lvl_xp[x-1]
    
    async def on_message(self, ctx):
        #Debug
        #import ipdb; ipdb.set_trace()
        if ctx.guild is None:
            return
        if ctx.channel.id == 404662949500813313 or ctx.channel.id == 404661808742400000:
            return
        if ctx.author.bot == True:
            return
        if ctx.guild.id != 436600674017476608:
            return
        XPList = []
        XPList = pickle.load(open('KillerXP.data', 'rb'))
        added = False
        addedXP = random.randint(25,50)
        #if ctx.channel.id == '404662949500813313' or ctx.channel.id == '404661808742400000':
        #    addedXP = 0
        if ctx.channel.id == 472863145992650792:
            addedXP = random.randint(10,25)
        for y in range(len(XPList)):
            if XPList[y][0] == (ctx.author.id):
                if (time.time()) < (XPList[y][3]):
                    return
                added = True
                placement = y
                break
        print(XPList)
        
        #Debug
        #import ipdb; ipdb.set_trace()
        if added == False:
            placement = len(XPList)
            XPList.append([ctx.author.id,addedXP,0,time.time() + 0])
            XPList[placement][2] = LevelSet(XPList[placement][1])
            while XPList[placement][1] > XPList[placement-1][1]:
                prev = XPList[placement-1]
                XPList[placement-1] = XPList[placement]
                XPList[placement] = prev
                placement-=1
        if added == True:
            XPList[placement][1] +=  addedXP
            XPList[placement][2] = LevelSet(XPList[placement][1])
            XPList[placement][3] = time.time() + 60
            #Debug
            #import ipdb; ipdb.set_trace()
            while XPList[placement][1] > XPList[placement-1][1]:
                prev = XPList[placement-1]
                XPList[placement-1] = XPList[placement]
                XPList[placement] = prev
                placement-=1
        pickle.dump(XPList, open('XP.data','wb'))
    
    @commands.command(name='xp')
    async def XPCheck(self, ctx,  *, member: discord.Member=None):
        if member is None:
            member = ctx.author
        if ctx.guild == None:
            return
        XPList = []
        XPList = pickle.load(open('XP.data', 'rb'))
        added = False
        for y in range(len(XPList)):
            if XPList[y][0] == (member.id):
                added = True
                placement = y
                break
        if added == False:
            await ctx.send("This person hasn't earnt any xp yet.")
        if added == True:
            embed = discord.Embed(title="XP for",
                              description=member.name,
                              colour=RankColour(placement))
            embed.set_author(name=member.display_name,
                         icon_url=member.avatar_url_as(format='jpg'))

            embed.add_field(name='Rank',
                            value=(placement))
            embed.add_field(name='Level',
                            value=(LevelSet(XPList[placement][1])))
            embed.add_field(name='Total XP',
                            value=(XPList[placement][1]))
            embed.add_field(name='XP to next level',
                            value=(XPRem(XPList[placement][1])))
            embed.set_footer(text='i G o d l i k e',
                             icon_url='https://cdn.discordapp.com/icons/404654967350362112/78d3c8c87474924f6326401b57e9bc32.jpg?size=1024')

            await ctx.send(content='**Displaying user XP**', embed=embed)

    @commands.command(name='xprank')
    @commands.is_owner()
    async def XPRank(self, ctx, placement:int=None):
        #Debug
        #import ipdb; ipdb.set_trace()
        if ctx.guild == None:
            return
        if placement == None:
            placement = 1
        XPList = []
        XPList = pickle.load(open('XP.data', 'rb'))
        added = False
        if (placement) >= len(XPList) or placement < 1:
            await ctx.send("There isn't a person at that rank.")
            return
        
        member = self.bot.get_user(int(XPList[placement][0]))
        embed = discord.Embed(title="XP for",
                              description=member.display_name,
                              colour=RankColour(placement))
        embed.set_author(name=member.display_name,
                         icon_url=member.avatar_url_as(format='jpg'))

        embed.add_field(name='Rank',
                        value=(placement))
        embed.add_field(name='Level',
                        value=(LevelSet(XPList[placement][1])))
        embed.add_field(name='Total XP',
                        value=(XPList[placement][1]))
        embed.add_field(name='XP to next level',
                        value=(XPRem(XPList[placement][1])))
        embed.set_footer(text='i G o d l i k e',
                        icon_url='https://cdn.discordapp.com/icons/404654967350362112/78d3c8c87474924f6326401b57e9bc32.jpg?size=1024')

        await ctx.send(content='**Displaying rank XP**', embed=embed)
        print(XPList)

    @commands.command(name='xptop')
    async def XPTop(self,ctx):
        if ctx.guild == None:
            return
        XPList=[]
        XPList = pickle.load(open('XP.data','rb'))
        placement = 1
        value1 = "•**name:** "+str(ctx.guild.get_member(XPList[1][0]))+"\n•**XP:** "+str(XPList[1][1])+"\n•**Level:** "+str(LevelSet(XPList[1][1]))
        value2 = "•**name:** "+str(ctx.guild.get_member(XPList[2][0]))+"\n•**XP:** "+str(XPList[2][1])+"\n•**Level:** "+str(LevelSet(XPList[2][1]))
        value3 = "•**name:** "+str(ctx.guild.get_member(XPList[3][0]))+"\n•**XP:** "+str(XPList[3][1])+"\n•**Level:** "+str(LevelSet(XPList[3][1]))
        value4 = "•**name:** "+str(ctx.guild.get_member(XPList[4][0]))+"\n•**XP:** "+str(XPList[4][1])+"\n•**Level:** "+str(LevelSet(XPList[4][1]))
        embed = discord.Embed(title="Top XP",
                              description="Ranks 1-4",
                              colour=0x663311)
        embed.set_author(name='uGodlike',
                         icon_url='https://cdn.discordapp.com/avatars/404658318431485953/2b96cd8e226e84de327b0c7dc4ec499c.png?size=1024')
        embed.add_field(name='#1',
                        value=value1)
        embed.add_field(name='#2',
                        value=value2)
        embed.add_field(name='#3',
                        value=value3)
        embed.add_field(name='#4',
                        value=value4)
        embed.set_footer(text='i G o d l i k e',
                        icon_url='https://cdn.discordapp.com/icons/404654967350362112/78d3c8c87474924f6326401b57e9bc32.jpg?size=1024')

        await ctx.send(content='**Displaying top XP**', embed=embed)

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(XPCog(bot))
