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
#User Name Points Participations
class CPCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="cp")
    async def CP(self, ctx):
        if ctx.invoked_subcommand is None:
            if ctx.channel.id != 433349202433802250:
                await ctx.message.delete()
                await ctx.send(content="Wrong channel. Please use #bot_spammin.",delete_after=5)
                return
            await ctx.send("You haven't sent a Clan Points subcommand. Use `&help cp` to find out how to use the command.")

    @CP.command(name='stats')
    async def TCheck(self, ctx,  *, member: discord.Member=None):
        if ctx.channel.id != 433349202433802250:
            await ctx.message.delete()
            await ctx.send(content="Wrong channel. Please use #bot_spammin.",delete_after=5)
            return
        if member is None:
            member = ctx.author
        if ctx.guild == None:
            return
        CPList = []
        CPList = pickle.load(open('CP.data', 'rb'))
        added = False
        for y in range(len(CPList)):
            if CPList[y][0] == (member.id):
                added = True
                placement = y
                break
        if added == True:
            embed = discord.Embed(title="Stats for",
                              description=member.name,
                              colour=RankColour(placement))
            embed.set_author(name=member.display_name,
                             icon_url=member.avatar_url_as(format='png'))
                             #icon_url=self.bot.user.avatar_url_as(format='png'))
                                 #icon_url='https://cdn.discordapp.com/avatars/421718079265964032/7805693d09954641ab8bbb51f3582f07.png')
            #embed.set_thumbnail(url=ctx.author.avatar_url_as(format='png'))
            embed.add_field(name='Rank',
                            value=(placement)+1)
            embed.add_field(name='Points',
                            value=(CPList[placement][2]))
            embed.set_footer(text=ctx.guild.name,
                             icon_url=ctx.guild.icon_url_as(format='png'))

            await ctx.send(content='**Displaying user CPs**', embed=embed)
            print(CPList)
            print('')
            
    @CP.command(name='rank')
    async def TRank(self, ctx, placement:int=None):
        if ctx.channel.id != 433349202433802250:
            await ctx.message.delete()
            await ctx.send(content="Wrong channel. Please use #bot_spammin.",delete_after=5)
            return
        if ctx.guild == None:
            return
        if placement == None:
            placement = 1
        CPList = []
        CPList = pickle.load(open('CP.data', 'rb'))
        added = False
        if (placement) >= len(CPList) or placement < 1:
            await ctx.send("There isn't a person at that rank.")
            return
        
        member = self.bot.get_user(int(CPList[placement][0]))
        embed = discord.Embed(title="Clan Points for",
                              description=member.display_name,
                              colour=RankColour(placement))
        embed.set_author(name=member.display_name,
                         icon_url=member.avatar_url_as(format='jpg'))

        embed.add_field(name='Rank',
                        value=(placement))
        embed.add_field(name='Points',
                        value=(CPList[placement][2]))
        if placement == 1:
            embed.add_field(name='CPs to next rank',
                            value="You are #1!")
        else:
            embed.add_field(name='CPs to next rank',
                            value=((CPList[placement-1][2])-(CPList[placement][2]))+1)
        embed.set_footer(text=ctx.guild.name,
                        icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='**Displaying rank CPs**', embed=embed)
        print(CPList)
        print('')
        
    @CP.command(name='top')
    async def CPTop(self,ctx):
        #if ctx.channel.id != 433349202433802250:
        #    await ctx.message.delete()
        #    await ctx.send(content="Wrong channel. Please use #bot_spammin.",delete_after=5)
        #    return
        if ctx.guild == None:
            return
        XPList=[]
        XPList = pickle.load(open('CP.data','rb'))
        placement = 1
        value1 = "•**Name:** "+str(ctx.guild.get_member(XPList[1][0]))+"\n•**CPs:** "+str(XPList[1][2])
        value2 = "•**Name:** "+str(ctx.guild.get_member(XPList[2][0]))+"\n•**CPs:** "+str(XPList[2][2])
        value3 = "•**Name:** "+str(ctx.guild.get_member(XPList[3][0]))+"\n•**CPs:** "+str(XPList[3][2])
        value4 = "•**Name:** "+str(ctx.guild.get_member(XPList[4][0]))+"\n•**CPs:** "+str(XPList[4][2])
        value5 = "•**Name:** "+str(ctx.guild.get_member(XPList[5][0]))+"\n•**CPs:** "+str(XPList[5][2])
        embed = discord.Embed(title="Season 1 results!",
                              description="Ranks 1-5",
                              colour=0xFFd700)
        embed.set_author(icon_url=self.bot.user.avatar_url_as(format='png'),
                         name=self.bot.user.name)
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

        await ctx.send(content='**Displaying top CP**', embed=embed)
  

        
# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(CPCog(bot))
    random.seed()
