import discord
from discord.ext import commands
import asyncio
import random
import pickle
import sys
import math
import time

#NAMES
#I just can't catch a break today, that last one was terrible.
#Epic Hurricane April Showers bring May Flowers Hoopla Tournament
#Freeze Change Up ThrowDown Tournament
#Southern Santa's Little Helper Rise Ball Tournament
#Make 'Em Believe Crossroads Armed Forces Day World Series Tournment
#Ouch that really hurt.
#Guess who's back, back again\nClan games back, tell a friend\nGuess who's back guess who's back?\nGuess who's back guess who's back?\nGuess who's back guess who's back?\nGuess who's back?
class EmbedCog:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group('t')
    async def t(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @t.command('start')
    @commands.has_any_role('BotMod')
    async def tstart(self, ctx, tType:int):
        greenfoot = (discord.utils.find(lambda m: m.id == 270190067354435584, ctx.guild.members))
        test = (discord.utils.find(lambda c: c.id == 432974224609771531, ctx.guild.channels))
        ctx.message.delete()
        if tType == 1:
            embed = discord.Embed(title='Clan Games!',
                                  description="This is a clan games for members of the clan.",
                                  colour=0x008800)
            embed.set_author(name='Tourney Master',
                              icon_url=self.bot.user.avatar_url_as(format='png'))
            embed.add_field(name='__**Offical name**__',
                            value="__Southern Santa's Little Helper Rise Ball Tournament__")
            embed.add_field(name='Rules:',
                            value="•All players wishing to enter must submit a screenshot of their lifetime gold to Tourney Offical via DM within 24 hours of me sending this message.\n•Be honest with the times of your screenshots.\n•Players under ms 500 cannot enter.\n•No using cheats or exploits gain an advantage over other players.\n•If you leave the clan at any time you will be disquallified as you are no longer a clan member.\n•You **must** have fun.\n•Failure to follow these rules will result in you being kicked from the current tourney and maybe a ban from future ones.")
            embed.add_field(name='How does it work?',
                            value="•Players are given 24 hours to enter the tournament.\n•Players must then increase their career gold by as much as possible.\n•All players will then submit their scores withing 7 days (168 hours) from the time they entered.\n•All player will then be pitted against each other to see who multipled their career gold by the most.\n•Players will submit updates of their lifetime gold. If it is submitted outside the time frame it will not be counted.\ne.g. if i have 1,000 lifetime gold at the start and by the end of the tournament I have 1M I will have a score of 1000.")
            embed.add_field(name='How do I play?',
                            value="To join you must first DM Clan Games Offical a screenshot of your carrer gold. This can be found in your ahievements or your stats.\nFrom the time you post that images you have exactally 7 days (168 hours) to improve your career gold.\nAlong the way feel free to give updated (in the form of screenshots) of your career gold.\nAfter your time runs out your score will be determined from the first screenshot and the last.\nIf any screenshots are sent after your time has ended it will not count.\nShould you wish to retire from the tournament at any time you may do so via DM to Clan Games Official.")
            embed.add_field(name='What can I win?',
                            value='•Get to add a custom emoji on the server.\n•Get a special `King of the Hill` role!\n•Gain Clan Points!\n**Remember, there are also participant prizes for everyone to win!**')
            embed.add_field(name='Got any questions?',
                            value=f'Direct them towards {greenfoot.display_name} with a simple ping or DM!')
            embed.set_footer(text='Família Relik',
                            icon_url=ctx.guild.icon_url_as(format='png'))
        if tType == 3:
            embed = discord.Embed(title='Clan Games!',
                                  description="This is a clan games for members of the discord.",
                                  colour=0x008800)
            embed.set_author(name='Tourney Master',
                              icon_url=self.bot.user.avatar_url_as(format='png'))
            embed.add_field(name='__**Offical name**__',
                            value="__Guess who's back, back again\nClan games back, tell a friend\nGuess who's back, guess who's back?\nGuess who's back, guess who's back?\nGuess who's back, guess who's back?\nGuess who's back?__")
            embed.add_field(name='Rules:',
                            value="•All players wishing to enter must submit a screenshot of their lifetime gold to Tourney Offical via DM within 24 hours of me sending this message.\n•Be honest with the times of your screenshots.\n•Players under ms 1000 cannot enter.\n•No using cheats or exploits gain an advantage over other players.\n•You **must** have fun.\n•Failure to follow these rules will result in you being kicked from the current clan games and maybe a ban from future ones.")
            embed.add_field(name='How does it work?',
                            value="•Players are given 24 hours to enter the clan games.\n•Players must then increase their career gold by as much as possible.\n•All players will then submit their scores withing 7 days (168 hours) from the time they entered.\n•All player will then be pitted against each other to see who multipled their career gold by the most.\n•Players can submit updates of their lifetime gold. If it is submitted outside the time frame it will not be counted. If an update is not given by the end of the Clan Games they will DNF.\ne.g. if i have 1,000 lifetime gold at the start and by the end of the clan games I have 1M I will have a score of 1000.")
            embed.add_field(name='How do I play?',
                            value="To join you must first DM Clan Games Offical a screenshot of your carrer gold. This can be found under your career stats.\nFrom the time you post that images you have exactally 7 days (168 hours) to improve your career gold.\nAlong the way feel free to give updates (in the form of screenshots) of your career gold.\nAfter your time runs out your score will be determined from the first screenshot and the last.\nIf any screenshots are sent after your time has ended it will not count.\nShould you wish to retire from the tournament at any time you may do so via DM to Clan Games Official.")
            embed.add_field(name='What can I win?',
                            value='•Get to add a custom emoji on the server.\n•Get a special `King of the Hill` role!\n•Gain Clan Points!')
            embed.add_field(name='Got any questions?',
                            value=f'Direct them towards {greenfoot.display_name} with a simple ping or DM!')
            embed.set_footer(text='Família Relik',
                            icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='', embed=embed)

        #691200 = 8 days
        #await asyncio.sleep(691200)
    @t.command('end')
    @commands.has_any_role('BotMod')
    async def tend(self,ctx):
        greenfoot = (discord.utils.find(lambda m: m.id == 270190067354435584, ctx.guild.members))
        test = (discord.utils.find(lambda c: c.id == 432974224609771531, ctx.guild.channels))
        ctx.message.delete()
        embed = discord.Embed(title='Clan Games over!',
                              description="The tournament is now over and all scores are now final. As they are totted up please wait for the winner to be announced.",
                              colour=0xCC0000)
        embed.set_author(name='Tourney Master',
                          icon_url=self.bot.user.avatar_url_as(format='png'))
        embed.set_footer(text='Família Relik',
                        icon_url=ctx.guild.icon_url_as(format='png'))
 
        await ctx.send(content='', embed=embed)

    @t.command('w')
    @commands.has_any_role('BotMod')
    async def twinner(self, ctx, winner: discord.Member):
        eve = (discord.utils.find(lambda m: m.id == 379503236660592641, ctx.guild.members))
        test = (discord.utils.find(lambda c: c.id == 432974224609771531, ctx.guild.channels))
        embed = discord.Embed(title='And the winner is...',
                              description="Drumroll please...",
                              colour=0xCC9900)
        embed.set_author(name='Tourney Master',
                          icon_url=self.bot.user.avatar_url_as(format='png'))

        embed.add_field(name=f'{winner.display_name}',
                        value=f'Yay! Please speak to {eve.display_name} to setup your emoji! Your role will be given shortly.\nThe rankings shall be revealed soon...')
        embed.set_footer(text='Família Relik',
                        icon_url=ctx.guild.icon_url_as(format='png'))
 
        await ctx.send(content='', embed=embed)
        ctx.message.delete()

    @t.command('r')
    @commands.has_any_role('BotMod')
    async def tranks(self,ctx):
        #Name, score, points won.
        ranks = [[356196306319966208,105,250],[379503236660592641,89,130],[187300230998261761,60,130],[157307521198063616,38,100],[270190067354435584,22,100],[403153703202455562,0,100],[316856059807399936,0,100],[253147353530368000,0,100]]
        embed = discord.Embed(title='Clan Games ranking:',
                              description="The rankings for the latest clan games",
                              colour=0x130D31)
        for x in range(len(ranks)):
            embed.add_field(name=f"#{x+1}",
                            value=f"Name: {(discord.utils.find(lambda m: m.id == ranks[x][0], ctx.guild.members)).name}\nScore: {str(ranks[x][1])}\nClan Points earned: {str(ranks[x][2])}")
        embed.set_author(name=self.bot.user.name,
                         icon_url=self.bot.user.avatar_url_as(format='png'))
        embed.set_footer(text=ctx.guild.name,
                         icon_url=ctx.guild.icon_url_as(format='png'))
        await ctx.send(content='And the ranking follows:', embed=embed)

    @t.command('stop')
    @commands.has_any_role('BotMod')
    async def tstop(self,ctx):
        embed = discord.Embed(title='Clan join registry closed!',
                              description="As 24 hours have passed since the start of the tournament started so you can no longer join this tournament.",
                              colour=0xFF8800)
        embed.set_author(name='Tourney Master',
                          icon_url=self.bot.user.avatar_url_as(format='png'))
        embed.set_footer(text='Família Relik',
                        icon_url=ctx.guild.icon_url_as(format='png'))
 
        await ctx.send(content='', embed=embed)

    @t.command('timer')
    @commands.has_any_role('BotMod')
    async def ttimer(self,ctx,timeMin:int=0):
        if time == 0:
            await ctx.send("Timer cannot begin on zero.")
            return
        timeRemainingMin = timeMin
        while timeRemainingMin > 0:
            timeRemaining = str(int(timeRemainingMin/1440)) + ':' + str(int((timeRemainingMin%1440)/60)) + ':' + str((timeRemainingMin%1440)%60)
            await self.bot.change_presence(game=discord.Game(name=f"{timeRemaining} Remaining"))
            print(timeRemaining)
            await asyncio.sleep(60)
            timeRemainingMin -= 1
            if timeRemainingMin == 1440:
                embed = discord.Embed(title='Clan Games Reminder!',
                                      description="24 hours remaning till the end of the clan games!",
                                      colour=0xFF8800)
                embed.set_author(name='Tourney Master',
                                  icon_url=self.bot.user.avatar_url_as(format='png'))
                embed.set_footer(text='Família Relik',
                                icon_url=ctx.guild.icon_url_as(format='png'))
         
                await ctx.send(content='', embed=embed)
        eve = (discord.utils.find(lambda m: m.id == 379503236660592641, ctx.guild.members))
        test = (discord.utils.find(lambda c: c.id == 432974224609771531, ctx.guild.channels))
        embed = discord.Embed(title='And the winner is...',
                              description="Drumroll please...",
                              colour=0xCC9900)
        embed.set_author(name='Tourney Master',
                          icon_url=self.bot.user.avatar_url_as(format='png'))

        embed.add_field(name=f'{winner.display_name}',
                        value=f'Yay! Please speak to {eve.display_name} to setup your emoji! Your role will be given shortly.\nThe rankings shall be revealed soon...')
        embed.set_footer(text='Família Relik',
                        icon_url=ctx.guild.icon_url_as(format='png'))
 
        await ctx.send(content='', embed=embed)

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(EmbedCog(bot))
