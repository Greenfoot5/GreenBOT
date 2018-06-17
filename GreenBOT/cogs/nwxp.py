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
lvls_xp = [500,1500,2500,5000,10000,25000,50000]
ranks = [0,444489213141057546,444487988827914253,446382522041892888,444489049751945216,444489418355638282,444490040543019018,444490176840859669]

#Format:
#id P/N/M XP time level rank#
class NWXPCog:
    def __init__(self, bot):
        self.bot = bot
            
    @commands.group(name='value',aliases=['v'])
    async def nwv(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("You haven't sent a Value subcommand. Chat to Greenfoot5 to find out how to use the command.")
            
    @nwv.command(name='worth')
    async def CCheck(self, ctx,  *, member: discord.Member=None):
        if member is None:
            member = ctx.author
        if ctx.guild == None:
            return
        XPList = []
        XPList = pickle.load(open('nwxp.data', 'rb'))
        added = False
        placement = 0
        for y in range(len(XPList)):
            if XPList[y][0] == (member.id):
                added = True
                placement = y
                break
        if added == True:
            embed = discord.Embed(title="Stats for",
                              description=member.name,
                              colour=discord.utils.find(lambda r: r.id == ranks[XPList[placement][3]], member.guild.roles).colour)
            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url_as(format='png'))
            embed.add_field(name='Position',
                            value=str(placement))
            embed.add_field(name='Rank',
                            value=discord.utils.find(lambda r: r.id == ranks[XPList[placement][3]], member.guild.roles).name)
            embed.add_field(name='Level',
                            value=XPList[placement][3])
            embed.add_field(name='XP',
                            value=int((XPList[placement][2])))
            embed.set_footer(text=ctx.guild.name,
                             icon_url=ctx.guild.icon_url_as(format='png'))

            await ctx.send(content='**Displaying user Worth**', embed=embed)
            
    @nwv.command(name='rank')
    @commands.is_owner()
    async def CRank(self, ctx, placement:int=None):
        if ctx.guild == None:
            return
        if placement == None:
            placement = 1
        CoinList = []
        CoinList = pickle.load(open('nwxp.data', 'rb'))
        added = False
        if (placement) >= len(CoinList) or placement < 1:
            await ctx.send("There isn't a person at that rank.")
            return
        
        member = self.bot.get_user(int(CoinList[placement][0]))
        embed = discord.Embed(title="Worth for",
                              description=member.display_name,
                              colour=RankColour(CoinList[placement][1]))
        embed.set_author(name=member.display_name,
                         icon_url=member.avatar_url_as(format='jpg'))

        embed.add_field(name='Rank',
                        value=(placement))
        embed.add_field(name='Worth',
                        value=(CoinList[placement][2])*1000000)
        if placement == 1:
            embed.add_field(name='Worth to next rank',
                            value="You are #1!")
        else:
            embed.add_field(name='Worth to next rank',
                            value=(((CoinList[placement-1][1])-(CoinList[placement][1]))+1)*1000000)
        embed.set_footer(text=ctx.guild.name,
                        icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='**Displaying rank Worth**', embed=embed)

    @nwv.command(name='top')
    async def VTop(self,ctx):
        if ctx.guild == None:
            return
        XPList=[]
        XPList = pickle.load(open('nwxp.data','rb'))
        placement = 1
        value1 = "•**name:** "+str(ctx.guild.get_member(XPList[1][0]))+"\n•**Level:** "+str(XPList[1][3])+"\n•**XP:** "+str(XPList[1][2])
        value2 = "•**name:** "+str(ctx.guild.get_member(XPList[2][0]))+"\n•**Level:** "+str(XPList[2][3])+"\n•**XP:** "+str(XPList[2][2])
        value3 = "•**name:** "+str(ctx.guild.get_member(XPList[3][0]))+"\n•**Level:** "+str(XPList[3][3])+"\n•**XP:** "+str(XPList[3][2])
        value4 = "•**name:** "+str(ctx.guild.get_member(XPList[4][0]))+"\n•**Level:** "+str(XPList[4][3])+"\n•**XP:** "+str(XPList[4][2])
        value5 = "•**name:** "+str(ctx.guild.get_member(XPList[5][0]))+"\n•**Level:** "+str(XPList[5][3])+"\n•**XP:** "+str(XPList[5][2])
        embed = discord.Embed(title="Top Members",
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
        embed.add_field(name='#5',
                        value=value5)
        embed.set_footer(text=ctx.guild.name,
                        icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='**Displaying top worth**', embed=embed)

    @nwv.command(name='reset')
    @commands.is_owner()
    async def vReset(self,ctx):
        XPList=[]
        XPList.append([0,100000000000, 0,0,0,0])
        for x in range(len(ctx.guild.members)):
            XPList.append([ctx.guild.members[x].id, 0, 0, 0, 0])
        def getKey(item):
            return item[1]
        XPList = sorted(XPList,reverse=True,key=getKey)
        pickle.dump(XPList, open('nwxp.data','wb'))
        print("Done")

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(NWXPCog(bot))
