from discord.ext import commands
import asyncio
import discord
import pickle


class ModCog:

    def __init__(self, bot):
        self.bot = bot

    '''
    All commands here are xp based moderation commands.
    '''
    @commands.command('xpclear')
    @commands.is_owner()
    async def XPClear(self, ctx):
        #XPList = pickle.load(open('XP.data', 'rb'))
        XPList = [[0,1000000000,0,0]]
        pickle.dump(XPList, open('Coin.data','wb'))
        await ctx.send('Cleared XP')
        print(XPList)

    @commands.command('xpadd')
    @commands.is_owner()
    async def XPAdd(self,ctx,addedXP:int,member: discord.Member=None):
        if ctx.guild == None:
            return
        if member is None:
            member = ctx.author
        XPList = []
        XPList = pickle.load(open('XP.data', 'rb'))
        added = False
        for y in range(len(XPList)):
            if XPList[y][0] == (member.id):
                added = True
                placement = y
                break
        #Debug
        #import ipdb; ipdb.set_trace()
        if added == False:
            Lvl = LevelSet(addedXP)
            XPList.append([member.id,addedXP,Lvl,0])
            pickle.dump(XPList, open('XP.data','wb'))
        if added == True:
            XPList[placement][1] +=  addedXP
            XPList[placement][2] = LevelSet(XPList[placement][1])
            while XPList[placement][1] > XPList[placement-1][1]:
                prev = XPList[placement-1]
                XPList[placement-1] = XPList[placement]
                XPList[placement-1] = prev
                placement-=1
            pickle.dump(XPList, open('XP.data','wb'))
            print(member.name,XPList[placement][1])

    @commands.command('xptake')
    @commands.is_owner()
    async def XPTake(self,ctx,addedXP:int,member: discord.Member=None):
        if ctx.guild == None:
            return
        if member is None:
            member = ctx.author
        XPList = []
        XPList = pickle.load(open('XP.data', 'rb'))
        added = False
        for y in range(len(XPList)):
            if XPList[y][0] == (member.id):
                added = True
                placement = y
                break
        #Debug
        #import ipdb; ipdb.set_trace()
        if added == False:
            await ctx.send('This person has no xp to take.')
        if added == True:
            if XPList[placement][1] < addedXP:
                await ctx.send("This person doesn't have enough XP")
                return
            XPList[placement][1] -=  addedXP
            XPList[placement][2] = LevelSet(XPList[placement][1])
            while XPList[placement][1] < XPList[placement+1][1]:
                prev = XPList[placement-1]
                XPList[placement+1] = XPList[placement]
                XPList[placement+1] = prev
                placement+=1
            pickle.dump(XPList, open('XP.data','wb'))
            print(member.name,XPList[placement][1])

    @commands.command(name='xpranking')
    @commands.is_owner()
    async def XPRankIng(self,ctx,placement:int=None):
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
        while XPList[placement][1] > XPList[placement-1][1]:
                prev = XPList[placement-1]
                XPList[placement-1] = XPList[placement]
                XPList[placement] = prev
                placement-=1
        pickle.dump(XPList, open('XP.data','wb'))
        print(XPList)
    '''
    All commands listed here are base moderation commands
    '''
    @commands.command(name='art')
    @commands.is_owner()
    async def AddRoleTimed(self,ctx,role:str,member: discord.Member,time:int=None):
        roles = discord.utils.get(ctx.author.guild.roles, name=str(role))
        await member.add_roles(roles)
        print(roles,"was added.")
        print(member.roles)
        await ctx.send("Added Role.")
        if time != None:
            await asyncio.sleep(time*60)
            await member.remove_roles(roles)

    @commands.command(name='rrt')
    @commands.is_owner()
    async def RemRoleTimed(self,ctx,role:str,member: discord.Member,time:int=None):
        roles = discord.utils.get(member.guild.roles, name=str(role))
        await member.remove_roles(roles)
        print(roles,"was removed.")
        print(member.roles)
        await ctx.send("Removed Role.")
        if time != None:
            await asyncio.sleep(time*60)
            await member.add_roles(roles)
    '''
    All commands listed here are raffle moderation commands.
    '''
    @commands.command(name='raff', hidden=True)
    @commands.is_owner()
    async def raff(self,ctx, first: str):
        first.lower()
        raffleList = []
        raffleList = pickle.load(open('raffle.list', 'rb'))
        print(raffleList)
        print(range(len(raffleList)))
        if first == 'draw':
            winner = random.randint(0,(len(raffleList)-1))
            winnerName  = raffleList[winner]
            del raffleList[winner]
            await ctx.send(f'{winnerName.mention} has won!')
            pickle.dump(raffleList, open('raffle.list','wb'))
        if first == 'clear':
            raffleList = []
            pickle.dump(raffleList, open('raffle.list','wb'))
            await ctx.send('Cleared raffle')

def setup(bot):
    bot.add_cog(ModCog(bot))
