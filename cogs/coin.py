import discord
from discord.ext import commands
import asyncio
import random
import pickle
import sys
import math
import time

#Levels
#Formula = prev. + (prev. * 1.1)
lvls_xp = [(5*(i**3)+50*i+100) for i in range(500)]

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
        elif rank > 100 and rank <= 250:
            return 0x9999FF
        else:
            return 0xFFFFFF

#Format:
#User Coins (time.time())OfNextCoinClaim Wins Loses
        
#Debug
#import ipdb; ipdb.set_trace()
        
class CoinCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="c")
    async def Coin(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("You haven't sent a Coin subcommand. Use `&&help Coin` to find out how to use the command.")

    @Coin.command(name="claim")
    @commands.is_owner()
    async def CClaim(self, ctx):
        if ctx.guild == None:
            return
        if ctx.author.bot == True:
            return
        CoinList = []
        CoinList = pickle.load(open('Coin.data', 'rb'))
        added = False
        DailyCoin = 0
        for y in range(len(CoinList)):
            if CoinList[y][0] == (ctx.author.id):
                if (time.time()) < (CoinList[y][2]):
                    text = "You must wait", 86400 - (time.time()%86400), "seconds before running that command."
                    embed = discord.Embed(title="Balance:",
                                          description=CoinList[y][1],
                                          colour=RankColour(y))
                    embed.set_author(name=ctx.author.display_name,
                                     icon_url=ctx.author.avatar_url_as(format='jpg'))
                    embed.add_field(name='Seconds till next claim',
                            value=int(86400 - (time.time()%86400)))
                    embed.set_footer(text=ctx.guild.name,
                                     icon_url=ctx.guild.icon_url_as(format='png'))

                    await ctx.send(content='', embed=embed)
                    return
                added = True
                placement = y
                break
        if added == False:
            plcamement = len(CoinList)
            CoinList.append([ctx.author.id,DailyCoin,time.time() + (86400 - (time.time()%86400)),0,0])
        if added == True:
            CoinList[placement][1] +=  DailyCoin
            CoinList[placement][2] = time.time() + (86400 - (time.time()%86400))
        def getKey(item):
            return item[1]
        CoinList = sorted(CoinList,reverse=True,key=getKey)
        for y in range(len(CoinList)):
            if CoinList[y][0] == (ctx.author.id):
                placement = y
        embed = discord.Embed(title="New Balance:",
                              description=CoinList[placement][1],
                              colour=RankColour(placement))
        embed.set_author(name=ctx.author.display_name,
                         icon_url=ctx.author.avatar_url_as(format='jpg'))
        embed.set_footer(text=ctx.guild.name,
                         icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='', embed=embed)
        pickle.dump(CoinList, open('Coin.data','wb'))
        text = "You now have",CoinList[placement][1],"Coins"

    @Coin.command(name='stats')
    @commands.has_any_role('Test Subject')
    async def CCheck(self, ctx,  *, member: discord.Member=None):
        if member is None:
            member = ctx.author
        if ctx.guild == None:
            return
        CoinList = []
        CoinList = pickle.load(open('Coin.data', 'rb'))
        added = False
        for y in range(len(CoinList)):
            if CoinList[y][0] == (member.id):
                added = True
                placement = y
                break
        if added == True:
            embed = discord.Embed(title="Stats for",
                              description=member.name,
                              colour=RankColour(placement))
            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url_as(format='png'))
            embed.add_field(name='Rank',
                            value=str(placement))
            embed.add_field(name='Balance',
                            value=(CoinList[placement][1]))
            TLB = []
            TLB = pickle.load(open('triviaLB.data', 'rb'))
            addedT = False
            for x in range(len(TLB)):
                if TLB[x][0] == (member.id):
                    addedT = True
                    embed.add_field(name='Correct Trivia Answers',
                                    value=(TLB[x][1]))
            if addedT == False:
                embed.add_field(name='Correct Trivia answers',
                                value='0')
            #embed.add_field(name='Seconds till next claim:',
            #                value=int(CoinList[placement][2]))
            if (time.time()) > (CoinList[placement][2]):
                CoinList[placement][2] = 0
            embed.set_footer(text=ctx.guild.name,
                             icon_url=ctx.guild.icon_url_as(format='png'))

            await ctx.send(content='**Displaying user Coins**', embed=embed)
            
    @Coin.command(name='rank')
    @commands.has_any_role('Test Subject')
    async def CRank(self, ctx, placement:int=None):
        if ctx.guild == None:
            return
        if placement == None:
            placement = 1
        CoinList = []
        CoinList = pickle.load(open('Coin.data', 'rb'))
        added = False
        if (placement) >= len(CoinList) or placement < 1:
            await ctx.send("There isn't a person at that rank.")
            return
        
        member = self.bot.get_user(int(CoinList[placement][0]))
        embed = discord.Embed(title="Coins for",
                              description=member.display_name,
                              colour=RankColour(placement))
        embed.set_author(name=member.display_name,
                         icon_url=member.avatar_url_as(format='jpg'))

        embed.add_field(name='Rank',
                        value=(placement))
        embed.add_field(name='Balance',
                        value=(CoinList[placement][1]))
        if placement == 1:
            embed.add_field(name='Coins to next rank',
                            value="You are #1!")
        else:
            embed.add_field(name='Coins to next rank',
                            value=((CoinList[placement-1][1])-(CoinList[placement][1]))+1)
        embed.set_footer(text=ctx.guild.name,
                        icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='**Displaying rank Coins**', embed=embed)

    @Coin.command(name="pay")
    @commands.is_owner()
    async def CPay(self, ctx, amount:int=0, member: discord.Member=None):
        if ctx.guild == None:
            return
        if ctx.author.bot == True:
            return
        if amount < 1:
            await ctx.send("You need to send some Coins!")
            return
        if member == None:
            await ctx.send("You haven't specified who to send the Coins to.")
            return
        if member == ctx.author:
            await ctx.send("Why would you want to pay yourself? I cannot compute.")
        CoinList = []
        CoinList = pickle.load(open('Coin.data', 'rb'))
        addeda = False
        for y in range(len(CoinList)):
            if CoinList[y][0] == (ctx.author.id):
                addeda = True
                placementa = y
                break
        if addeda == False:
            await ctx.send("You haven't earnt any Coins, yet.")
            return
        if CoinList[placementa][1] < amount:
            await ctx.send("You don't have enough Coins.")
            return
        if addeda == True:
            CoinList[placementa][1] -=  amount
        for x in range(len(CoinList)):
            if CoinList[x][0] == (member.id):
                addedm = True
                placementm = x
                break
        if addedm == False:
            placementm = len(CoinList)
            CoinList.append([member.id,amount,0,0,0,0])
        if addedm == True:
            CoinList[placementm][1] +=  amount
        def getKey(item):
            return item[1]
        CoinList = sorted(CoinList,reverse=True,key=getKey)
        for y in range(len(CoinList)):
            if CoinList[y][0] == (ctx.author.id):
                placementa = y
            if CoinList[y][0] == member.id:
                placementm = y
        embed = discord.Embed(title="Your New Balance:",
                              description=CoinList[placementa][1],
                              colour=RankColour(placementa))
        embed.set_author(name=ctx.author.display_name,
                         icon_url=ctx.author.avatar_url_as(format='jpg'))
        embed.set_footer(text=ctx.guild.name,
                         icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='', embed=embed)

        embed = discord.Embed(title="Their New Balance:",
                              description=CoinList[placementm][1],
                              colour=RankColour(placementm))
        embed.set_author(name=member.display_name,
                         icon_url=member.avatar_url_as(format='jpg'))
        embed.set_footer(text=ctx.guild.name,
                         icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='', embed=embed)
        pickle.dump(CoinList, open('Coin.data','wb'))

    @Coin.command(name='top')
    @commands.is_owner()
    async def CTop(self,ctx):
        if ctx.guild == None:
            return
        XPList=[]
        XPList = pickle.load(open('Coin.data','rb'))
        placement = 1
        value1 = "•**name:** "+str(ctx.guild.get_member(XPList[1][0]))+"\n•**XP:** "+str(XPList[1][1])
        value2 = "•**name:** "+str(ctx.guild.get_member(XPList[2][0]))+"\n•**XP:** "+str(XPList[2][1])
        value3 = "•**name:** "+str(ctx.guild.get_member(XPList[3][0]))+"\n•**XP:** "+str(XPList[3][1])
        value4 = "•**name:** "+str(ctx.guild.get_member(XPList[0][0]))+"\n•**XP:** "+str(XPList[0][1])
        #value5 = "•**name:** "+str(ctx.guild.get_member(XPList[5][0]))+"\n•**XP:** "+str(XPList[5][1])+"\n•**Level:** "+str(LevelSet(XPList[5][1]))
        embed = discord.Embed(title="Top Coins",
                              description="Ranks 1-5",
                              colour=0x663311)
        embed.set_author(name=self.bot.user.name,
                         icon_url=self.bot.user.avatar_url_as(format='png'))
        embed.add_field(name='#1',
                        value=value1)
        embed.add_field(name='#2',
                        value=value2)
        embed.add_field(name='#3',
                        value=value3)
        embed.add_field(name='#4',
                        value=value4)
        #embed.add_field(name='#5',
        #                value=value5)
        embed.set_footer(text=ctx.guild.name,
                        icon_url='https://cdn.discordapp.com/icons/404654967350362112/78d3c8c87474924f6326401b57e9bc32.jpg?size=1024')

        await ctx.send(content='**Displaying top Coins**', embed=embed)

    @commands.command(name='attach')
    @commands.is_owner()
    async def attach(self,ctx):
        file = discord.File(fp='cards/7D.png',filename='7-of-Diamonds.png')
        await ctx.send(content='Test',file=file)
        
# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(CoinCog(bot))
    random.seed()
