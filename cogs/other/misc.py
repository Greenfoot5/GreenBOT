import discord
from discord.ext import commands
import pickle
import random
import asyncio
import time
import cogs.base.checks as chec

'''
Initialisation
'''

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Deck = [["A♠",1,'cards/deck/AS.png'],["2♠",2,'cards/deck/2S.png'],["3♠",3,'cards/deck/3S.png'],["4♠",4,'cards/deck/4S.png'],["5♠",5,'cards/deck/5S.png'],["6♠",6,'cards/deck/6S.png'],["7♠",7,'cards/deck/7S.png'],["8♠",8,'cards/deck/8S.png'],["9♠",9,'cards/deck/9S.png'],["10♠",10,'cards/deck/10S.png'],["J♠",10,'cards/deck/JS.png'],["Q♠",10,'cards/deck/QS.png'],["K♠",10,'cards/deck/KS.png'],
                     ["A♥",1,'cards/deck/AH.png'],["2♥",2,'cards/deck/2H.png'],["3♥",3,'cards/deck/3H.png'],["4♥",4,'cards/deck/4H.png'],["5♥",5,'cards/deck/5H.png'],["6♥",6,'cards/deck/6H.png'],["7♥",7,'cards/deck/7H.png'],["8♥",8,'cards/deck/8H.png'],["9♥",9,'cards/deck/9H.png'],["10♥",10,'cards/deck/10H.png'],["J♥",10,'cards/deck/JH.png'],["Q♥",10,'cards/deck/QH.png'],["K♥",10,'cards/deck/KH.png'],
                     ["A♣",1,'cards/deck/AC.png'],["2♣",2,'cards/deck/2C.png'],["3♣",3,'cards/deck/3C.png'],["4♣",4,'cards/deck/4C.png'],["5♣",5,'cards/deck/5C.png'],["6♣",6,'cards/deck/6C.png'],["7♣",7,'cards/deck/7C.png'],["8♣",8,'cards/deck/8C.png'],["9♣",9,'cards/deck/9C.png'],["10♣",10,'cards/deck/10C.png'],["J♣",10,'cards/deck/JC.png'],["Q♣",10,'cards/deck/QC.png'],["K♣",10,'cards/deck/KC.png'],
                     ["A♦",1,'cards/deck/AD.png'],["2♦",2,'cards/deck/2D.png'],["3♦",3,'cards/deck/3D.png'],["4♦",4,'cards/deck/4D.png'],["5♦",5,'cards/deck/5D.png'],["6♦",6,'cards/deck/6D.png'],["7♦",7,'cards/deck/7D.png'],["8♦",8,'cards/deck/8D.png'],["9♦",9,'cards/deck/9D.png'],["10♦",10,'cards/deck/10D.png'],["J♦",10,'cards/deck/JD.png'],["Q♦",10,'cards/deck/QD.png'],["K♦",10,'cards/deck/KD.png']]
    
    @commands.command(name='g')
    @commands.is_owner()
    async def guild(self,ctx):
        guild = []
        guild.append(ctx.guild.name)
        guild.append(ctx.guild.members)
        guild.append(ctx.guild.role_hierarchy)
        guild.append(ctx.guild.id)
        print('=-=-=')
        for x in range(len(guild)):
            print(guild[x])
            print('')
        print('=-=-=')

    @commands.group(name='deal', aliases=['D','d'])
    @chec.is_module_enabled('misc')
    async def deal(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Would you like to deal `private`, `public` or `to <member>`?')

    @deal.command(name='private',aliases=['pr'], pass_context=True)
    async def dPrivate(self,ctx):
        cardNum = random.randint(0,len(self.Deck)-1)
        file = discord.File(fp=self.Deck[cardNum][2],filename='card.png')
        await ctx.author.send(content=f'You recieved {self.Deck[cardNum][0]}',file=file)

    @deal.command(name='public',aliases=['pu'])
    async def dPublic(self,ctx):
        cardNum = random.randint(0,len(self.Deck)-1)
        file = discord.File(fp=self.Deck[cardNum][2],filename='card.png')
        await ctx.send(content=f'{ctx.author.mention} recieved {self.Deck[cardNum][0]}',file=file)

    @deal.command(name='to')
    async def dTo(self, ctx,  *, member: discord.Member=None):
        if member is None:
            member = ctx.author
        cardNum = random.randint(0,len(self.Deck)-1)
        file = discord.File(fp=self.Deck[cardNum][2],filename='card.png')
        await ctx.send(content=f'{member.mention} recieved {self.Deck[cardNum][0]} from {ctx.author.mention}',file=file)
        await member.send(content=f'You recieved {self.Deck[cardNum][0]} from {ctx.author.name}',file=file)

    @deal.command(name='pto')
    async def dPTo(self, ctx,  *, member: discord.Member=None):
        if member is None:
            member = ctx.author
        cardNum = random.randint(0,len(self.Deck)-1)
        file = discord.File(fp=self.Deck[cardNum][2],filename='card.png')
        await member.send(content=f'You recieved {self.Deck[cardNum][0]} from {ctx.author.name}',file=file)

    @commands.command(name='colour', aliases=['color'])
    @commands.has_permissions(manage_roles=True)
    async def roleColour(self,ctx,role:discord.Role=None,colour:discord.Color=None):
        if role is None:
            await ctx.send("Please input a role.")
            return
        if colour is None:
            await ctx.send("Please input a colour.")
            return
        try:
            await role.edit(color=colour,reason=f'{ctx.author.name}#{ctx.author.discriminator} wanted to change it.')
        except discord.errors.Forbidden:
            await ctx.send("I can't do that.")
            return
        await ctx.send("Changed role colour.")

    @commands.command(name='cookies')
    async def showCookies(self,ctx):
        cookies = pickle.load(open('data/cookies.data', 'rb'))
        embed = discord.Embed(title='Cookies',
                          description=f"",
                          colour=0x00DD99)
        embed.set_author(name=self.bot.user.name,
                          icon_url=self.bot.user.avatar_url_as(format='png'))

        embed.add_field(name=f'{cookies["accepted"] + cookies["denied"]} :cookie:',
                        value=f"{cookies['accepted']} <:Check:530810250786242560>\n{cookies['denied']} <:Cross:524597009575968768>")
        embed.set_footer(text=ctx.guild.name,
                         icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='', embed=embed)

    @commands.command(name='sinvite')
    @commands.has_permissions(create_instant_invite=True)
    async def createAnInvite(self,ctx,limit:int=0):
        theInvite = await ctx.channel.create_invite(max_uses=limit,reason=f"Requested by: {ctx.author.name}#{ctx.author.discriminator}")
        await ctx.send(theInvite)
    
    
# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(Misc(bot))
    random.seed()
