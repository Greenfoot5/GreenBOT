from discord.ext import commands
import pickle
import discord

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
        
class BotModCog:

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command('cp_reset')
    @commands.has_any_role('BotMod')
    async def CPClear(self, ctx):
        CPList = [[0, 'First', 100000000000000], [433308130756132875, 'Clan Games Master', -9999999999999999]]
        for a in range(len(ctx.guild.members)):
            if ctx.guild.members[a].bot != True and ctx.guild.members[a].id != 297331249700274176:
                CPList.append([ctx.guild.members[a].id,ctx.guild.members[a].name,0,0])
        def getKey(item):
            return item[2]
        CPList = sorted(CPList,reverse=True,key=getKey)
        pickle.dump(CPList, open('CP.data','wb'))
        await ctx.send('Reset CP.')
        print(CPList)

    @commands.command('cp_fix')
    @commands.has_any_role('BotMod')
    async def CPFix(self, ctx):
        CPList = []
        CPList = pickle.load(open('CP.data',rb))
        for a in range(1,len(CPList)-1):
            CPList[a][2] = CPList[a][2] * 2
        def getKey(item):
            return item[2]
        CPList = sorted(CPList,reverse=True,key=getKey)
        pickle.dump(CPList, open('CP.data','wb'))
        await ctx.send('Reset CP.')
        print(CPList)
        
    @commands.command('cp_add')
    @commands.has_any_role('BotMod')
    async def CPAdd(self,ctx,addedCP:int,member: discord.Member=None):
        if ctx.guild == None:
            return
        if member is None:
            member = ctx.author
        print(addedCP)
        CPList = []
        CPList = pickle.load(open('CP.data', 'rb'))
        added = False
        for y in range(len(CPList)):
            if CPList[y][0] == (member.id):
                added = True
                placement = y
                break
        #Debug
        #import ipdb; ipdb.set_trace()
        if added == False:
            placement = len(CPList)
            CPList.append([member.id,addedCP,0,0,0,0])
            pickle.dump(CPList, open('CP.data','wb'))
        if added == True:
            CPList[placement][2] +=  int(addedCP)
        def getKey(item):
            return item[2]
        CPList = sorted(CPList,reverse=True,key=getKey)
        for y in range(len(CPList)):
            if CPList[y][0] == (member.id):
                placement = y
        pickle.dump(CPList, open('CP.data','wb'))
        print(member.name,CPList[placement][2],addedCP)
        embed = discord.Embed(title="New Balance:",
                              description=CPList[placement][2],
                              colour=RankColour(placement))
        embed.set_author(name=member.display_name,
                         icon_url=member.avatar_url_as(format='jpg'))
        embed.set_footer(text='DPRoVT',
                         icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='', embed=embed)

    @commands.command('cp_take')
    @commands.has_any_role('BotMod')
    async def CPTake(self,ctx,addedCP:int,member: discord.Member=None):
        if ctx.guild == None:
            return
        if member is None:
            member = ctx.author
        CPList = []
        CPList = pickle.load(open('CP.data', 'rb'))
        added = False
        for y in range(len(CPList)):
            if CPList[y][0] == (member.id):
                added = True
                placement = y
                break
        #Debug
        #import ipdb; ipdb.set_trace()
        if added == False:
            await ctx.send('This person has no CPs to take.')
        if added == True:
            if CPList[placement][2] < addedCP:
                await ctx.send("This person doesn't have enough CPs")
                return
            CPList[placement][2] -=  int(addedCP)
            def getKey(item):
                return item[2]
            CPList = sorted(CPList,reverse=True,key=getKey)
            pickle.dump(CPList, open('CP.data','wb'))
            for y in range(len(CPList)):
                if CPList[y][0] == (member.id):
                    placement = y
            print(member.name,CPList[placement][2])
        embed = discord.Embed(title="New Balance:",
                              description=CPList[placement][2],
                              colour=RankColour(placement))
        embed.set_author(name=member.display_name,
                         icon_url=member.avatar_url_as(format='jpg'))
        embed.set_footer(text='DPRoVT',
                         icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='', embed=embed)
    '''
    @commands.command('j_reset')
    @commands.is_owner()
    async def JReset(self,ctx):
        J = 0
        pickle.dump(J, open('Jackpot.num','wb'))
        await ctx.send('Reset Jackpot.')
        print("Jackpot = ",pickle.load(open('Jackpot.num','rb')))
    '''

    @commands.command('cp_sort')
    @commands.has_any_role('BotMod')
    async def TSort(self,ctx):
        if ctx.guild == None:
            return
        CPList = []
        CPList = pickle.load(open('CP.data','rb'))
        def getKey(item):
            return item[1]
        CPList = sorted(CPList,reverse=True,key=getKey)
        pickle.dump(CPList, open('CP.data','wb'))
        print(CPList)
        await ctx.send('CPs Sorted.')

def setup(bot):
    bot.add_cog(BotModCog(bot))
