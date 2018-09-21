import discord
from discord.ext import commands
import pickle
import random
import asyncio
import time

'''
Initialisation
'''

def is_module_enabled(module):
    """A :func`.check` that checks if the module is enabled on the server"""
    async def pred(ctx):
        guilds = []
        guilds = pickle.load(open("guilds.data", "rb"))
        for a in range(len(guilds)):
            if guilds[a][0] == ctx.guild.id:
                if module == "misc":
                    if guilds[a][1][0] == True:
                        return True
                elif module == "trivia":
                    if guilds[a][2][0] == True:
                        return True
                elif module == "members":
                    if guilds[a][3][0] == True:
                        return True
    return commands.check(pred)

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

class Misc:
    def __init__(self, bot):
        self.bot = bot
        self.Deck = [["A♠",1,'cards/deck/AS.png'],["2♠",2,'cards/deck/2S.png'],["3♠",3,'cards/deck/3S.png'],["4♠",4,'cards/deck/4S.png'],["5♠",5,'cards/deck/5S.png'],["6♠",6,'cards/deck/6S.png'],["7♠",7,'cards/deck/7S.png'],["8♠",8,'cards/deck/8S.png'],["9♠",9,'cards/deck/9S.png'],["10♠",10,'cards/deck/10S.png'],["J♠",10,'cards/deck/JS.png'],["Q♠",10,'cards/deck/QS.png'],["K♠",10,'cards/deck/KS.png'],
                     ["A♥",1,'cards/deck/AH.png'],["2♥",2,'cards/deck/2H.png'],["3♥",3,'cards/deck/3H.png'],["4♥",4,'cards/deck/4H.png'],["5♥",5,'cards/deck/5H.png'],["6♥",6,'cards/deck/6H.png'],["7♥",7,'cards/deck/7H.png'],["8♥",8,'cards/deck/8H.png'],["9♥",9,'cards/deck/9H.png'],["10♥",10,'cards/deck/10H.png'],["J♥",10,'cards/deck/JH.png'],["Q♥",10,'cards/deck/QH.png'],["K♥",10,'cards/deck/KH.png'],
                     ["A♣",1,'cards/deck/AC.png'],["2♣",2,'cards/deck/2C.png'],["3♣",3,'cards/deck/3C.png'],["4♣",4,'cards/deck/4C.png'],["5♣",5,'cards/deck/5C.png'],["6♣",6,'cards/deck/6C.png'],["7♣",7,'cards/deck/7C.png'],["8♣",8,'cards/deck/8C.png'],["9♣",9,'cards/deck/9C.png'],["10♣",10,'cards/deck/10C.png'],["J♣",10,'cards/deck/JC.png'],["Q♣",10,'cards/deck/QC.png'],["K♣",10,'cards/deck/KC.png'],
                     ["A♦",1,'cards/deck/AD.png'],["2♦",2,'cards/deck/2D.png'],["3♦",3,'cards/deck/3D.png'],["4♦",4,'cards/deck/4D.png'],["5♦",5,'cards/deck/5D.png'],["6♦",6,'cards/deck/6D.png'],["7♦",7,'cards/deck/7D.png'],["8♦",8,'cards/deck/8D.png'],["9♦",9,'cards/deck/9D.png'],["10♦",10,'cards/deck/10D.png'],["J♦",10,'cards/deck/JD.png'],["Q♦",10,'cards/deck/QD.png'],["K♦",10,'cards/deck/KD.png']]
        self.digits = ['0','1','2','3','4','5','6','7','8','9']


    '''
    ['Família Relik',
        [<Role id=405927064659558401 name='Overlord'>,
        <Role id=413164339298566144 name='Grand Master'>,
        <Role id=413161956237901825 name='Master'>,
        <Role id=409005003336974346 name='Captain'>,
        <Role id=409017620696924173 name='Knight'>,
        <Role id=409018170272382976 name='Recruit'>,
        <Role id=410297043756777472 name='Mee6'>,
        <Role id=429330592472236043 name='*NomaD*'>,
        <Role id=405926267050000384 name='@everyone'>],
    405926267050000384]

    ['Noob Status',
        [<Role id=313911665769054209 name='Admin'>,
        <Role id=313912036075634689 name='Member'>,
        <Role id=429857694573395969 name='Tap Titans 2'>,
        <Role id=429857856788103178 name='RuneScape'>,
        <Role id=429858070907322368 name='The Inner Circle'>,
        <Role id=429862376972484628 name='GTA Online'>,
        <Role id=430044218325467139 name='Destiny 2'>,
        <Role id=201794488287363072 name='@everyone'>],
    201794488287363072]
    '''
    
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
        
    @commands.group(name ='random')
    @is_module_enabled('misc')
    async def rand(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid arguments')

    @rand.command(name='int')
    async def integer(self, ctx, mini: int, maxi: int):
        if ctx.channel.id != 421712364774227978:
            return
        ans = random.randint(mini,maxi)
        await ctx.send(ans)

    @rand.command(name='random')
    async def floating(self, ctx):
        if ctx.channel.id != 421712364774227978:
            return
        ans = random.random()
        await ctx.send(ans)

    @commands.command(name='add', aliases=['plus'])
    @is_module_enabled('misc')
    async def do_addition(self, ctx, first: int, second: int):
        """A simple command which does addition on two integer values."""
        if ctx.channel.id != 421712364774227978:
            await ctx.message.delete()
            await ctx.send(content="Wrong channel. Please use `#the_casino`.",delete_after=5)
            return
        total = first + second
        await ctx.send(f'The sum of **{first}** and **{second}**  is  **{total}**')
        await ctx.message.delete()

    @commands.group(name='deal', aliases=['Deal','D','d'])
    @is_module_enabled('misc')
    async def deal(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Would you like to deal `private`, `public` or `to <member>`?')

    @deal.command(name='private',aliases=['pr'])
    @is_module_enabled('misc')
    async def dPrivate(self,ctx):
        cardNum = random.randint(0,len(self.Deck)-1)
        #file = discord.File(fp='/home/pi/Pictures/Art/Pixel Art/Exported/Birthdays/Claire.png')
        file = discord.File(fp=self.Deck[cardNum][2],filename='card.png')
        await ctx.author.send(content=f'You recieved {self.Deck[cardNum][0]}',file=file)

    @deal.command(name='public',aliases=['pu'])
    @is_module_enabled('misc')
    async def dPublic(self,ctx):
        cardNum = random.randint(0,len(self.Deck)-1)
        file = discord.File(fp=self.Deck[cardNum][2],filename='card.png')
        await ctx.send(content=f'{ctx.author.mention} recieved {self.Deck[cardNum][0]}',file=file)

    @deal.command(name='to')
    @is_module_enabled('misc')
    async def dTo(self, ctx,  *, member: discord.Member=None):
        if member is None:
            member = ctx.author
        cardNum = random.randint(0,len(self.Deck)-1)
        file = discord.File(fp=self.Deck[cardNum][2],filename='card.png')
        await ctx.send(content=f'{member.mention} recieved {self.Deck[cardNum][0]} from {ctx.author.mention}',file=file)
        await member.send(content=f'You recieved {self.Deck[cardNum][0]} from {ctx.author.name}',file=file)

    @deal.command(name='pto')
    @is_module_enabled('misc')
    async def dPTo(self, ctx,  *, member: discord.Member=None):
        if member is None:
            member = ctx.author
        cardNum = random.randint(0,len(self.Deck)-1)
        file = discord.File(fp=self.Deck[cardNum][2],filename='card.png')
        await member.send(content=f'You recieved {self.Deck[cardNum][0]} from {ctx.author.name}',file=file)

    @commands.command(name='colour')
    @commands.has_any_role('bot perms')
    async def roleColour(self,ctx,role:discord.Role=None,colour:discord.Color=None):
        if role is None:
            await ctx.send("Please input a role.")
            return
        if colour is None:
            await ctx.send("Please input a colour.")
            return
        print(colour)
        await role.edit(color=colour,reason=f'{ctx.author.name}#{ctx.author.discriminator} wanted to change it.')
        await ctx.send("Changed role colour.")
        
'''
    @commands.command(name='?')
    async def unknown(self,ctx):
        option = random.randint(1,741)
        if option <= 10:
            await ctx.send("???")
        elif option <= 20:
            await ctx.send("...")
        elif option <= 30:
            await ctx.send("Oops")
        elif option <= 40:
            await ctx.send(".\n.\n.")
        elif option <= 50:
            await ctx.send("Um...")
        elif option <= 60:
            await ctx.send("Lel")
        elif option <= 70:
            await ctx.send("Yes!")
        elif option <= 80:
            await ctx.send("¯\_(ツ)_/¯")
        elif option <= 90:
            await ctx.send("`¯\_(ツ)_/¯`")
        elif option <= 100:
            await ctx.send("Am I really a bot?..")
        elif option <= 110:
            await ctx.send("..Or do you just think I am?")
        elif option <= 120:
            await ctx.send("Ha!")
        elif option <= 130:
            await ctx.send("No!")
        elif option <= 140:
            await ctx.send("Not again...")
        elif option <= 150:
            await ctx.send("`...`")
        elif option <= 160:
            await ctx.send("```\n.\n.\n.\n```")
        elif option <= 170:
            await ctx.send("```\n...\n```")
        elif option <= 180:
            await ctx.send("S.O.S")
        elif option <= 190:
            await ctx.send("I wonder if pontoon has been finished yet?")
        elif option <= 200:
            await ctx.send("Did poker ever become a thing?")
        elif option <= 210:
            await ctx.send("Reading football team are trash.")
        elif option <= 220:
            await ctx.send("hmm...")
        elif option <= 230:
            await ctx.send("Opinions are like assholes: Some people use it to crap all over everything they see.")
        elif option <= 240:
            await ctx.author.send("Happy DMs!")
        elif option <= 250:
            await ctx.send("The struggle is real.")
        elif option <= 260:
            await ctx.send("If my friends were as boring as yours I would also spend the whole evening looking at my phone instead of talking to them.")
        elif option <= 270:
            await ctx.send("I give 0 fucks about your opinion.")
        elif option <= 280:
            await ctx.send("Woking 5 days a week to have 2 'free' days, what a Golden Age, hmm?")
        elif option <= 290:
            await ctx.send("Of course it's what's inside that matters...")
        elif option <= 300:
            await ctx.send('`null`')
        elif option <= 310:
            await ctx.send("Remember that embarrassing thing you did a long time ago? Well, everyone else remembers.")
        elif option <= 320:
            await ctx.send("Maybe the reason they didn't answer your message was because they didn't see it, stop being paranoid.")
        elif option <= 330:
            await ctx.send("Being intelligent, but lazy, is such an easy excuse.")
        elif option <= 340:
            await ctx.send("Have you heard the news? No one loves you.")
        elif option <= 350:
            await ctx.send("Having a college degree doesn't make you a better person.")
        elif option <= 360:
            await ctx.send("You could... you know... stop being lazy and all.")
        elif option <= 370:
            await ctx.send("Such a lovely day for you to ruin it with your face.")
        elif option <= 380:
            await ctx.send("`Am I the only one here who...` No, you are not, you self-righteous shithead.")
        elif option <= 390:
            await ctx.send("Maybe the reason they didn't asnwer your message was because they were busy doing something else.")
        elif option <= 400:
            await ctx.send("Bad-mood is not an excuse to be a dick.")
        elif option <= 410:
            await ctx.send("Wanna know who asked about you?, Yes, no one!")
        elif option <= 420:
            TeicList = []
            TeicList = pickle.load(open('Teic.data', 'rb'))
            added = False
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    added = True
                    placement = y
                    break
            if added == True:
                TeicList[placement][1] -=  20
            def getKey(item):
                return item[1]
            TeicList = sorted(TeicList,reverse=True,key=getKey)
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    placement = y
            embed = discord.Embed(title="-20 Teics...",
                                  description=TeicList[placement][1],
                                  colour=0x990000)
            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url_as(format='jpg'))
            embed.set_footer(text='DPRoVT',
                             icon_url=ctx.guild.icon_url_as(format='png'))

            await ctx.send(content='Oops...', embed=embed)
            pickle.dump(TeicList, open('Teic.data','wb'))
            J = pickle.load((open('Jackpot.num','rb')))
            pickle.dump(J+20,open('Jackpot.num','wb'))
            print("Jackpot =",pickle.load(open('Jackpot.num','rb')))
        elif option <= 430:
            TeicList = []
            TeicList = pickle.load(open('Teic.data', 'rb'))
            added = False
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    added = True
                    placement = y
                    break
            if added == True:
                TeicList[placement][1] +=  20
            def getKey(item):
                return item[1]
            TeicList = sorted(TeicList,reverse=True,key=getKey)
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    placement = y
            embed = discord.Embed(title="+20 Teics!",
                                  description=TeicList[placement][1],
                                  colour=0x33AA00)
            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url_as(format='jpg'))
            embed.set_footer(text='DPRoVT',
                             icon_url=ctx.guild.icon_url_as(format='png'))

            await ctx.send(content='Oooh! Look at you!', embed=embed)
            pickle.dump(TeicList, open('Teic.data','wb'))
            J = pickle.load((open('Jackpot.num','rb')))
            pickle.dump(J-20,open('Jackpot.num','wb'))
            print("Jackpot =",pickle.load(open('Jackpot.num','rb')))
        elif option <= 440:
            TeicList = []
            TeicList = pickle.load(open('Teic.data', 'rb'))
            added = False
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    added = True
                    placement = y
                    break
            if added == True:
                TeicList[placement][1] +=  100
                #Debug
                #import ipdb; ipdb.set_trace()
            def getKey(item):
                return item[1]
            TeicList = sorted(TeicList,reverse=True,key=getKey)
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    placement = y
            embed = discord.Embed(title="+100 Teics!",
                                  description=TeicList[placement][1],
                                  colour=0x33AA00)
            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url_as(format='jpg'))
            embed.set_footer(text='DPRoVT',
                             icon_url=ctx.guild.icon_url_as(format='png'))

            await ctx.send(content='Oooh! Look at you!', embed=embed)
            pickle.dump(TeicList, open('Teic.data','wb'))
            J = pickle.load((open('Jackpot.num','rb')))
            pickle.dump(J-100,open('Jackpot.num','wb'))
            print("Jackpot =",pickle.load(open('Jackpot.num','rb')))
        elif option <= 450:
            TeicList = []
            TeicList = pickle.load(open('Teic.data', 'rb'))
            added = False
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    added = True
                    placement = y
                    break
            if added == True:
                TeicList[placement][1] -=  100
                #Debug
                #import ipdb; ipdb.set_trace()
            def getKey(item):
                return item[1]
            TeicList = sorted(TeicList,reverse=True,key=getKey)
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    placement = y
            embed = discord.Embed(title="-100 Teics...",
                                  description=TeicList[placement][1],
                                  colour=0x990000)
            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url_as(format='jpg'))
            embed.set_footer(text='DPRoVT',
                             icon_url=ctx.guild.icon_url_as(format='png'))

            await ctx.send(content='Oooh! Look at you!', embed=embed)
            pickle.dump(TeicList, open('Teic.data','wb'))
            J = pickle.load((open('Jackpot.num','rb')))
            pickle.dump(J+100,open('Jackpot.num','wb'))
            print("Jackpot =",pickle.load(open('Jackpot.num','rb')))
        elif option <= 460:
            TeicList = []
            TeicList = pickle.load(open('Teic.data', 'rb'))
            added = False
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    added = True
                    placement = y
                    break
            if added == True:
                bal = TeicList[placement][1]
                TeicList[placement][1] = 0
                #Debug
                #import ipdb; ipdb.set_trace()
            def getKey(item):
                return item[1]
            TeicList = sorted(TeicList,reverse=True,key=getKey)
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    placement = y
            embed = discord.Embed(title="You now have 0 Teics...",
                                  description="0",
                                  colour=0x990000)
            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url_as(format='jpg'))
            embed.set_footer(text='DPRoVT',
                             icon_url=ctx.guild.icon_url_as(format='png'))

            await ctx.send(content='Oooh! Look at you!', embed=embed)
            pickle.dump(TeicList, open('Teic.data','wb'))
            J = pickle.load((open('Jackpot.num','rb')))
            pickle.dump(J+bal,open('Jackpot.num','wb'))
            print("Jackpot =",pickle.load(open('Jackpot.num','rb')))
        elif option <= 470:
            TeicList = []
            TeicList = pickle.load(open('Teic.data', 'rb'))
            added = False
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    added = True
                    placement = y
                    break
            if added == True:
                bal = TeicList[placement][1]
                TeicList[placement][1] +=  bal
            def getKey(item):
                return item[1]
            TeicList = sorted(TeicList,reverse=True,key=getKey)
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    placement = y
            embed = discord.Embed(title="Doubled Teics!",
                                  description=TeicList[placement][1],
                                  colour=0x33AA00)
            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url_as(format='jpg'))
            embed.set_footer(text='DPRoVT',
                             icon_url=ctx.guild.icon_url_as(format='png'))

            await ctx.send(content='Oooh! Look at you!', embed=embed)
            pickle.dump(TeicList, open('Teic.data','wb'))
            J = pickle.load((open('Jackpot.num','rb')))
            pickle.dump(J-bal,open('Jackpot.num','wb'))
            print("Jackpot =",pickle.load(open('Jackpot.num','rb')))
        elif option <= 480:
            TeicList = []
            TeicList = pickle.load(open('Teic.data', 'rb'))
            added = False
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    added = True
                    placement = y
                    break
            if added == True:
                bal = int(TeicList[placement][1])
                bal = int(bal/2)
                TeicList[placement][1] +=  bal
                #Debug
                #import ipdb; ipdb.set_trace()
            def getKey(item):
                return item[1]
            TeicList = sorted(TeicList,reverse=True,key=getKey)
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    placement = y
            embed = discord.Embed(title="Balance + 50%!",
                                  description=TeicList[placement][1],
                                  colour=0x33AA00)
            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url_as(format='jpg'))
            embed.set_footer(text='DPRoVT',
                             icon_url=ctx.guild.icon_url_as(format='png'))

            await ctx.send(content='Oooh! Look at you!', embed=embed)
            pickle.dump(TeicList, open('Teic.data','wb'))
            J = pickle.load((open('Jackpot.num','rb')))
            pickle.dump(J-bal,open('Jackpot.num','wb'))
            print("Jackpot =",pickle.load(open('Jackpot.num','rb')))
        elif option <= 490:
            TeicList = []
            TeicList = pickle.load(open('Teic.data', 'rb'))
            added = False
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    added = True
                    placement = y
                    break
            if added == True:
                bal = int(TeicList[placement][1])
                bal = int(bal/2)
                TeicList[placement][1] -=  bal
            def getKey(item):
                return item[1]
            TeicList = sorted(TeicList,reverse=True,key=getKey)
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    placement = y
            embed = discord.Embed(title="Balance - 50%...",
                                  description=TeicList[placement][1],
                                  colour=0x990000)
            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url_as(format='jpg'))
            embed.set_footer(text='DPRoVT',
                             icon_url=ctx.guild.icon_url_as(format='png'))

            await ctx.send(content='Oooh! Look at you!', embed=embed)
            pickle.dump(TeicList, open('Teic.data','wb'))
            J = pickle.load((open('Jackpot.num','rb')))
            pickle.dump(J+bal,open('Jackpot.num','wb'))
            print("Jackpot =",pickle.load(open('Jackpot.num','rb')))
        elif option <= 500:
            TeicList = []
            TeicList = pickle.load(open('Teic.data', 'rb'))
            addeda = False
            amount = random.randint(0,200)
            placementm = random.randint(1,len(TeicList)-2)
            while TeicList[placementm][0] == ctx.author.id:
                placementm = random.randint(1,len(TeicList)-2)
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    addeda = True
                    placementa = y
                    break
            if addeda == True:
                TeicList[placementa][1] -=  amount
            TeicList[placementm][1] +=  amount
            memberID = TeicList[placementm][0]
            def getKey(item):
                return item[1]
            TeicList = sorted(TeicList,reverse=True,key=getKey)
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    placementa = y
                if TeicList[y][0] == memberID:
                    placementm = y
            embed = discord.Embed(title="Your New Balance:",
                                  description=TeicList[placementa][1],
                                  colour=RankColour(placementa))
            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url_as(format='jpg'))
            embed.set_footer(text='DPRoVT',
                             icon_url=ctx.guild.icon_url_as(format='png'))

            await ctx.send(content='You payed out some Teics...', embed=embed)

            embed = discord.Embed(title="Their New Balance:",
                                  description=TeicList[placementm][1],
                                  colour=RankColour(placementm))
            embed.set_author(name=(discord.utils.find(lambda m: m.id == TeicList[placementm][0], ctx.guild.members)).display_name,
                             icon_url=(discord.utils.find(lambda m: m.id == TeicList[placementm][0], ctx.guild.members)).avatar_url_as(format='jpg'))
            embed.set_footer(text='DPRoVT',
                             icon_url=ctx.guild.icon_url_as(format='png'))

            await ctx.send(content=str(amount) + " Teics.", embed=embed)
            pickle.dump(TeicList, open('Teic.data','wb'))
            print(TeicList)
        elif option <= 510:
            TeicList = []
            TeicList = pickle.load(open('Teic.data', 'rb'))
            addeda = False
            amount = random.randint(0,200)
            placementm = random.randint(1,len(TeicList)-2)
            while TeicList[placementm][0] == ctx.author.id:
                placementm = random.randint(1,len(TeicList)-2)
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    addeda = True
                    placementa = y
                    break
            if addeda == True:
                TeicList[placementa][1] +=  amount
            TeicList[placementm][1] -=  amount
            memberID = TeicList[placementm][0]
            def getKey(item):
                return item[1]
            TeicList = sorted(TeicList,reverse=True,key=getKey)
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    placementa = y
                if TeicList[y][0] == memberID:
                    placementm = y
            embed = discord.Embed(title="Your New Balance:",
                                  description=TeicList[placementa][1],
                                  colour=RankColour(placementa))
            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url_as(format='jpg'))
            embed.set_footer(text='DPRoVT',
                             icon_url=ctx.guild.icon_url_as(format='png'))

            await ctx.send(content='You stole some Teics...', embed=embed)

            embed = discord.Embed(title="Their New Balance:",
                                  description=TeicList[placementm][1],
                                  colour=RankColour(placementm))
            embed.set_author(name=(discord.utils.find(lambda m: m.id == TeicList[placementm][0], ctx.guild.members)).display_name,
                             icon_url=(discord.utils.find(lambda m: m.id == TeicList[placementm][0], ctx.guild.members)).avatar_url_as(format='jpg'))
            embed.set_footer(text='DPRoVT',
                             icon_url=ctx.guild.icon_url_as(format='png'))

            await ctx.send(content=str(amount) + " Teics.", embed=embed)
            pickle.dump(TeicList, open('Teic.data','wb'))
            print(TeicList)
        elif option <= 520:
            roles = discord.utils.get(ctx.author.guild.roles, name=str('beta'))
            await ctx.author.add_roles(roles)
            await ctx.send(f"{ctx.author.mention}, you are now a Beta Tester for The Dealer!")
        elif option <= 530:
            await ctx.send("Gotta catch 'em all!")
        elif option <= 540:
            await ctx.send("I have infinite Teics!")
        elif option <= 550:
            await ctx.send("Will you rise or fall?")
        elif option <= 560:
            await ctx.send("Every day I'm shuffulin'...")
        elif option <= 570:
            await ctx.send("1, 10, 11, 100, 101, once I caught a fish alive...")
        elif option <= 580:
            await ctx.send("...110, 111, 1000, 1001, 1010, then I let it go again.")
        elif option <= 590:
            await ctx.send("Will you data? 'Cause she's not my type...")
        elif option <= 600:
            TeicList = []
            TeicList = pickle.load(open('Teic.data', 'rb'))
            added = False
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    added = True
                    placement = y
                    break
            if added == True:
                embed = discord.Embed(title="010100110111010001100001011101000111001100100000011001100110111101110010",
                                     description=''.join(format(ord(x), 'b') for x in ctx.author.name),
                                     colour=RankColour(random.randint(1,500)))
                embed.set_author(name="01010100011010000110010100100000010001000110010101100001011000110010101110010",
                                 icon_url=self.bot.user.avatar_url_as(format='png'))
                embed.set_thumbnail(url=ctx.author.avatar_url_as(format='png'))
                embed.add_field(name='01010010011000010110111001101011',
                                value=''.join(format(ord(x), 'b') for x in str(placement)))
                embed.add_field(name='01000010011000010110110001100001011011100110001101100101',
                                value=''.join(format(ord(x), 'b') for x in str(TeicList[placement][1])))
                embed.add_field(name='0101011011010010110111001110011',
                                value=''.join(format(ord(x), 'b') for x in str(TeicList[placement][3])))
                embed.add_field(name='0100110001101111011100110110010101110011',
                                value=''.join(format(ord(x), 'b') for x in str(TeicList[placement][4])))
                embed.add_field(name='010000110110111101110010011100100110010101100011011101000010000001010100011100100110100101110110011010010110000100100000011000010110111001110011011101110110010101110010011110011',
                                value=''.join(format(ord(x), 'b') for x in str(TeicList[placement][5])))
             
                if (time.time()) > (TeicList[placement][2]):
                    TeicList[placement][2] = 0
                
                embed.add_field(name='010100110110010101100011011011110110111001100100011100110010000001110100011010010110110001101100001000000110111001100101011110000111010000100000011000110110110001100001011010010110110100111010',
                                value=''.join(format(ord(x), 'b') for x in str(int(TeicList[placement][2]))))
                embed.set_footer(text='010001000101000001010011011110101011001010100',
                                 icon_url=ctx.guild.icon_url_as(format='png'))
  
                await ctx.send(content='0100111101101000001000000100011001010110000101110010001011100010111000101110', embed=embed)
        elif option <= 610:
            for x in range(1,random.randint(1,100),1):
                await ctx.send(f"Messages sent: {x}")
        elif option <= 620:
            await ctx.send("Boolean others is mean. Don't do it.")
        elif option <= 630:
            await ctx.send("Is a parameter longer or shorter than a kilometer?")
        elif option <= 640:
            await ctx.send("Look after your bots and they will look after you.")
        elif option <= 650:
            await ctx.send("1010 green bottles sitting on a wall...")
        elif option <= 660:
            await ctx.send("Why was 110 scared of 111? Because 111, 1000, 1001...")
        elif option <= 670:
            await ctx.send("Why was 6 scared of 7? Because 7,8,9...")
        elif option <= 680:
            await ctx.send("There are 10 types of people in the world. Those who understand binary and those who don't.")
        elif option <= 690:
            await ctx.send("My friends row about image size. I hope there's are reolution...")
        elif option <= 700:
            await ctx.send("Anna Log talks constantly, while Digit Al just speaks in bits...")
        elif option <= 710:
            await ctx.send("You can buy apples with four cores?")
        elif option <= 720:
            await ctx.send("When I am stressed I eat ice cream, cake, chocolate and sweets. Why? Stressed spelt backwards is desserts!")
        elif option <= 740:
            TeicList = []
            TeicList = pickle.load(open('Teic.data', 'rb'))
            added = False
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    added = True
                    placement = y
                    break
            if added == True:
                TeicList[placement][1] -=  500
            def getKey(item):
                return item[1]
            TeicList = sorted(TeicList,reverse=True,key=getKey)
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    placement = y
            embed = discord.Embed(title="-500 Teics...",
                                  description=TeicList[placement][1],
                                  colour=0x990000)
            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url_as(format='jpg'))
            embed.set_footer(text='DPRoVT',
                             icon_url=ctx.guild.icon_url_as(format='png'))

            await ctx.send(content='Oops...', embed=embed)
            pickle.dump(TeicList, open('Teic.data','wb'))
            J = pickle.load((open('Jackpot.num','rb')))
            pickle.dump(J+500,open('Jackpot.num','wb'))
            print("Jackpot =",pickle.load(open('Jackpot.num','rb')))
        elif option <= 750:
            TeicList = []
            TeicList = pickle.load(open('Teic.data', 'rb'))
            added = False
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    added = True
                    placement = y
                    break
            if added == True:
                TeicList[placement][1] +=  500
            def getKey(item):
                return item[1]
            TeicList = sorted(TeicList,reverse=True,key=getKey)
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    placement = y
            embed = discord.Embed(title="+500 Teics!",
                                  description=TeicList[placement][1],
                                  colour=0x33AA00)
            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url_as(format='jpg'))
            embed.set_footer(text='DPRoVT',
                             icon_url=ctx.guild.icon_url_as(format='png'))

            await ctx.send(content='Oooh! Look at you!', embed=embed)
            pickle.dump(TeicList, open('Teic.data','wb'))
            J = pickle.load((open('Jackpot.num','rb')))
            pickle.dump(J-500,open('Jackpot.num','wb'))
            print("Jackpot =",pickle.load(open('Jackpot.num','rb')))
        else:
            TeicList = []
            TeicList = pickle.load(open('Teic.data', 'rb'))
            J = pickle.load((open('Jackpot.num','rb')))
            added = False
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    added = True
                    placement = y
                    break
            if added == True:
                TeicList[placement][1] +=  J
            def getKey(item):
                return item[1]
            TeicList = sorted(TeicList,reverse=True,key=getKey)
            for y in range(len(TeicList)):
                if TeicList[y][0] == (ctx.author.id):
                    placement = y
            embed = discord.Embed(title="You won the Jackpot!!!",
                                  description=TeicList[placement][1],
                                  colour=0x33AA00)
            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url_as(format='jpg'))
            embed.set_footer(text='DPRoVT',
                             icon_url=ctx.guild.icon_url_as(format='png'))

            await ctx.send(content='Wow.', embed=embed)
            pickle.dump(TeicList, open('Teic.data','wb'))
            pickle.dump(0,open('Jackpot.num','wb'))
            print("Jackpot has been won by ",ctx.author.display_name)
'''
    
# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(Misc(bot))
    random.seed()
