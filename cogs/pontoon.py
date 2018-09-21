import discord
from discord.ext import commands
import asyncio
import pickle
import random

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
                elif module == "pontoon":
                    if guilds[a][4][0] == True:
                        return True
    return commands.check(pred)

'''
del my_list[1] # Removes index 1 from the list
print my_list # [1,4,6,7]
my_list.remove(4) # Removes the integer 4 from the list, not the index 4
print my_list # [1,6,7]
my_list.pop(2) # Removes index 2 from the list
'''

class PontoonCog:
    def __init__(self, bot):
        self.bot = bot
        #A standard card deck. It's used for getting. Not setting.
        self.Deck = [["A♠",1],["2♠",2],["3♠",3],["4♠",4],["5♠",5],["6♠",6],["7♠",7],["8♠",8],["9♠",9],["10♠",10],["J♠",10],["Q♠",10],["K♠",10],
                     ["A♥",1],["2♥",2],["3♥",3],["4♥",4],["5♥",5],["6♥",6],["7♥",7],["8♥",8],["9♥",9],["10♥",10],["J♥",10],["Q♥",10],["K♥",10],
                     ["A♣",1],["2♣",2],["3♣",3],["4♣",4],["5♣",5],["6♣",6],["7♣",7],["8♣",8],["9♣",9],["10♣",10],["J♣",10],["Q♣",10],["K♣",10],
                     ["A♦",1],["2♦",2],["3♦",3],["4♦",4],["5♦",5],["6♦",6],["7♦",7],["8♦",8],["9♦",9],["10♦",10],["J♦",10],["Q♦",10],["K♦",10]]
        #Contains a list of all the users currently hosting a game.
        self.hosts = []
        #Contains a list of all the users currently playing a game. Includes hosts.
        self.players = []
        #All the data related to the tables. I mean, ALL the data.
        '''
        self.tables[TableID][Hand/data][Card/id]
        ([[False,Turn,[deck],Type],[ctx.author.id,ptot],[Ps.id,ibet,tbet,ptot]],[True,50,1,[Deck][Host.id,ptot,[Card1Face,Card1Value],[Card2Face,Card2Value]],[Player2.id,ibet,tbet,ptot,[Card1Face,Card1Value],[Card2Face,Card2Value],[Card3Face,Card3Value]]])
        '''
        self.tables = []

    #Base command
    @commands.group(name="pt")
    @is_module_enabled('pontoon')
    async def pt(self, ctx):
        #Channel check
        if ctx.channel.id != 425370985626075137:
            await ctx.message.delete()
            await ctx.send(content="Wrong channel. Please use `#pontoon`.",delete_after=5)
            return
        #Subcommand check
        if ctx.invoked_subcommand is None:
            await ctx.send("You haven't sent a pontoon subcommand. To start a game send `!pt host`. To join one send `!pt join <member>`. You need to mention the host of the game to join.")

    #Explains how to play the game
    @pt.command(name="howto")
    async def pthowto(self,ctx):
        embed = discord.Embed(title="How to play Pontoon",
                              description="An outline of the rules of Pontoon",
                              colour=0x231F26)
        embed.set_author(name=self.bot.name,
                         icon_url=self.bot.avatar_url_as(format='png'))
        embed.add_field(name='Game-Setup',
                        value="•The host sets up a game by typing `!pt host <setup>`. The setup depends on which type of game they wish to play. Make sure you know which you are joining!\n•All player can then join by typing `!pt join <hosts name>`. This will then add them to the game.\n•Players can be kicked from a game at any time if the host types `!pt kick <player>`. The host can do this as much as they wish and the player can re-join but if there are any problems, please contact a mod.\n\uFEFF")
        embed.add_field(name='Starting the game',
                        value='•The host can type `!pt start` when they have at least two players in their game. They cannot have more than 10 (including the host).\n•Each player shall then recieve one card and betting begins.\uFEFF')
        embed.add_field(name='Placing initial bets',
                        value="•Starting with the player who first joined (the dealer doesn't bet) they may place a bet by typing `!pt bet <amount>` the minimum and maximum values for this bet are pre-determined by the setup type.\n•Once a player has bet the turn moves on.\n•The dealer doesn't bet.\n\uFEFF")
        embed.add_field(name='Play begins',
                        value="•Once all players have bet then the first player recieved another card. They may then ask the dealer for another card or stick on their current amount.\n•`!pt twist` will twist the player another card. They cannot then pay for another card. This card is shown to everyone.\n•`!pt buy <amount>` will buy another card. He can bet up to twice his initial bet but cannot bet less. This card isn't shown to everyone. The player may twist on their next turn.\n•`!pt stick` Stay on their current amount. Play then moves to the next player.\n•If it is permitted a player can use `!pt split` to split their cards. They then have two hands and play them one by one. They must then place the same initial bet on their second hand. This can only happen when a player has two cards of the same. The player can do this as many times as they want.\n•Should a player go over 21 at any time they lose immediatly and their bet are paid to the host. Play with then move on to the next game.\n\uFEFF")
        embed.add_field(name="Host's turn",
                        value="•Once all player have had their turn, it becomes the host's! The host must then try to beat all the other player's hands.\n•Their play is the same apart from the fact that their play is seen by everyone.\n•They cannot split hands.\n•They cannot buy cards as they cannot bet.\n\uFEFF")
        embed.add_field(name="Game over",
                        value="•Once the dealer has stuck all players hands are revelaled and bets payed towith winner be that the host or the player.\n•If a player runs out of Teics they are ejected out of the game. A player's Teics can go negaive.\n•If the host doesn't have enough Teics the game ends. The amount is determined by their setup type. If neccessary the host can go into neagtive Teics.\n•The game can then be re-played if enough player are still playing.\n\uFEFF")
        embed.add_field(name="Scoring",
                        value="•All number cards have their face value.\n•Picture cards/lettered cards are worth 10.\n•Ace is worth 1 or 11.\n•Pontoon is where a player has 10 and an Ace in their first two cards.\n•If the host and he player have the same amount, the host wins.\n•If a player have 5 cards they have a `Five Card Trick` is paid twice the player's bet. If the dealer achieves this they are given double the player's stake.\n•If a player manages to get `3*7` then they beat all vales except a true pontoon.\n\uFEFF")
        embed.set_footer(text=ctx.guild.name,
                         icon_url=ctx.guild.icon_url_as(format='png'))
        await ctx.author.send(content='', embed=embed)
        
    '''
    Pre-Game setup
    '''

    #Allows a user to setup a game
    @pt.command(name="host")
    async def pthost(self, ctx, setupType:int = 0):
        #Channel check
        if ctx.channel.id != 425370985626075137:
            return
        #Host Check
        if ctx.author.id in self.hosts:
            await ctx.send("You are already hosting a game.")
            return
        #Check if it is a setup
        if setupType < 1 or setupType > 6:
            await ctx.send("Please specify a game setup. Use `!pt setup` for a list of all the types.")
            return
        #Coming soon
        if setupType in (5,6):
            await ctx.send("These setups are coming soon. Please be patient.")
            return
        #Check if user has enough Teics to host
        TeicList = pickle.load(open('Teic.data', 'rb'))
        for y in range(len(TeicList)):
            if TeicList[y][0] == (ctx.author.id):
                #1-5 bet
                if setupType == 1:
                    if TeicList[y][1] < 50:
                        await ctx.send("You don't have enough Teics. You require at least 50 Teics before hosting.")
                        return
                #10-50 bet
                elif setupType in (2,5):
                    if TeicList[y][1] < 500:
                        await ctx.send("You don't have enough Teics. You require at least 500 Teics before hosting.")
                        return
                #100-500 bet
                elif setupType in (3,6):
                    if TeicList[y][1] < 5000:
                        await ctx.send("You don't have enough Teics. You require at least 5000 Teics before hosting.")
                        return
                #1000-5000
                elif setupType == 4:
                    if TeicList[y][1] < 50000:
                        await ctx.send("You haven't got 50000 Teics. Gosh! What a surprise!")
        #Adds the data to the lists
        self.hosts.append(ctx.author.id)
        self.players.append(ctx.author.id)
        self.tables.append([[False,0,[],setupType],[ctx.author.id,0]])
        #Tell the user that their game is ready
        await ctx.send("{}, your game is ready. When enough people have joined you can run `!pt start`.".format(ctx.author.mention))

    #Lists all the setup types for the host can use or will be able to use.
    @pt.command(name="setup")
    async def ptsetup(self, ctx):
        if ctx.channel.id != 425370985626075137:
            return
        embed = discord.Embed(title="Setup Types",
                              description="A list of all the different setups avaliable.",
                              colour=0xFFEED9)
        embed.set_author(name=self.bot.name,
                         icon_url=self.bot.avatar_url_as(format='png'))
        #List of all the currect setup types and their settings
        embed.add_field(name='__Setup 1:__',
                        value="**A begger's game**\n•Min bet = 1\n•Max bet = 5\n•No Splitting hands.\n•3*7 isn't Pontoon.")
        embed.add_field(name='__Setup 2:__',
                        value="**Originally average**\n•Min bet = 10\n•Max bet = 50\n•No Splitting hands.\n•3*7 isn't Pontoon.")
        embed.add_field(name='__Setup 3:__',
                        value="**A rich man's game**\n•Min bet = 100\n•Max bet = 500\n•No Splitting hands.\n•3*7 isn't Pontoon.")
        embed.add_field(name='__Setup 4:__',
                        value="**Too many Teics...**\n•Min bet = 100\n•Max bet = 500\n•No Splitting hands.\n•3*7 isn't Pontoon.")
        #Lists planned setups that are either being worked on or I haven't got round to doing.
        embed.add_field(name='\uFEFF',
                        value='__**Coming Soon:**__')
        embed.add_field(name='__Setup 5:__',
                        value="**An average game but with a little bit extra**\n•Min bet = 10\n•Max bet = 50\n•No Splitting hands.\n•3*7 is Pontoon.")
        embed.add_field(name='__Setup 6:__',
                        value="**A rich man wants pontoon**\n•Min bet = 100\n•Max bet = 500\n•No Splitting hands.\n•3*7 is Pontoon.")
        embed.set_footer(text=ctx.guild.name,
                         icon_url=ctx.guild.icon_url_as(format='png'))
        await ctx.send(content='', embed=embed)

    #Allows a user to join a game
    @pt.command(name="join")
    async def ptjoin(self,ctx,*,member: discord.Member=None):
        #Channel check
        if ctx.channel.id != 425370985626075137:
            return
        #Check if that person is hosting a game
        if member is None:
            await ctx.send("{}, you haven't specified a host's game. To host one yourslf type `!pt host`.".format(ctx.author.mention))
            return
        #Check if the user is hosting a game already
        if ctx.author.id in self.hosts:
            await ctx.send("{}, you are already hosting a game!".format(ctx.author.mention))
            return
        #Checks if the user is already in a game.
        if ctx.author.id in self.players:
            await ctx.send("{}, you are already in a game!".format(ctx.author.mention))
            return
        #Checks if the person is hosting a game
        if member.id not in self.hosts:
            await ctx.send("{}, that person isn't hosting a game!".format(ctx.author.mention))
            return
        #Finds the correct table
        for a in range(len(self.tables)):
            if self.tables[a][1][0] == member.id:
                #Check if the game has started
                if self.tables[a][0][0] == True:
                    await ctx.send("That game has already started!")
                    return
                #Check if the game has the maximum amount if players
                if len(self.tables[a]) >= 10:
                    await ctx.send("That game has too many players. Please join another or host your own with `!pt host <setup>`")
                    return
                #Checks if the player has enough Teics to play
                TeicList = pickle.load(open('Teic.data', 'rb'))
                for y in range(len(TeicList)):
                    if TeicList[y][0] == (ctx.author.id):
                        #1-5 bet
                        if self.tables[a][0][3] == 1:
                            if TeicList[y][1] < 5:
                                await ctx.send("You don't have enough Teics. You require at least 5 Teics before joining.".format(ctx.author.mention))
                                return
                        #10-50 bet
                        elif self.tables[a][0][3] in (2,5):
                            if TeicList[y][1] < 50:
                                await ctx.send("You don't have enough Teics. You require at least 50 Teics before joining.".format(ctx.author.mention))
                                return
                        #100-500 bet
                        elif self.tables[a][0][3] in (3,6):
                            if TeicList[y][1] < 500:
                                await ctx.send("You don't have enough Teics. You require at least 500 Teics before joining.".format(ctx.author.mention))
                                return
                        #1000-5000 bet
                        if self.tables[a][0][3] == 4:
                            if TeicList[y][1] < 5000:
                                await ctx.send("You don't have enough Teics. You require at least 5000 Teics before joining.".format(ctx.author.mention))
                                return
                #Adds the user's data to the tables
                self.tables[a].append([ctx.author.id,0,0,0])
                self.players.append(ctx.author.id)
                #Informs the host and user that players have joined their game.
                await ctx.send("{} has joined {}'s game.".format(ctx.author.mention,member.mention))
                #Tells the host ifthey have the maximum amount of player so that they can start the game A.S.A.P.
                if len(self.tables[a]) == 10:
                    await ctx.send(f"{member.mention} your game has hit maximum capacity.")
                    return

    #Kicks a player from a game. Original idea came from the fact that a user could wait infinatly for their turn if another user doesn't respond.
    #TODO - Actually kick them
    #TODO - check turn.
    @pt.command(name="kick")
    @commands.has_any_role('beta')
    async def ptkick(self,ctx,*,member:discord.Member=None):
        #Channel check
        if ctx.channel.id != 425370985626075137:
            return
        #Checks if the command invoker is a host
        if ctx.author.id not in self.hosts:
            await ctx.send("{}, you aren't hosting a game!".format(ctx.author.mention))
            return
        #Checks that the host selected someone
        if member is None:
            await ctx.send("{}, you haven't selected anyone to kick from you game.".format(ctx.author.mention))
            return
        #Checks if that person is playing
        if member.id not in self.players:
            await ctx.send("{}, that person isn't in a game!".format(ctx.author.mention))
            return
        added = False
        #Finds the correct table
        for a in range(len(self.tables)):
            #Checks if the invoker is hosting that table
            if self.tables[a][1][0] == ctx.author.id:
                #Finds the correct user in a table
                for b in range(len(self.tables[a])):
                    if self.tables[a][b][0] == (member.id):
                        added = True
                        #Informs the player that was kicked and the host that they were kicked
                        await ctx.send("{} has been kicked from {}'s game. Their bet(s) have been returned".format(ctx.author.mention,(discord.utils.find(lambda m: m.id == self.tables[y][1][0], ctx.guild.members)).mention))
                        #Returns the kicked user's bets
                        TeicList = pickle.load(open('Teic.data', 'rb'))
                        for y in range(len(TeicList)):
                            if self.tables[a][b][0] == TeicList[y][0]:
                                TeicList[y][1] += self.tables[a][b][2]
                        #Sorts the Teic List
                        def getKey(item):
                            return item[1]
                        TeicList = sorted(TeicList,reverse=True,key=getKey)
                        pickle.dump(TeicList, open('Teic.data','wb'))
                        #Removes the player from the table and player list
                        del self.tables[a][b]
                        for c in range(len(self.players)):
                            if self.players[c] == (ctx.author.id):
                                del self.players[c]
                                break
                #Checks if the host still has enough player to play and that they are playing. If they aren't then it still alows player to join the game.
                if len(self.tables[a]) < 3 and self.tables[a][0][0] == True:
                    host = (discord.utils.find(lambda m: m.id == self.tables[a][1][0], ctx.guild.members))
                    await ctx.send("{}, you don't have enough players to continue. Your game has been stopped.".format(host.mention))
                    self.players.remove(self.tables[a][1][0])
                    del self.tables[a]
                #Sends an error message if the player isn't in their game.
                if added == False:
                    await ctx.send(f"{ctx.author.mention}, that player isn't in your game!")

    '''
    The actual game
    '''

    #Begins the game and starts the dealing
    @pt.command(name="start")
    async def ptstart(self,ctx):
        #Channel check
        if ctx.channel.id != 425370985626075137:
            return
        #Check if the user is hosting a game
        if ctx.author.id not in self.hosts:
            await ctx.send("{}, you aren't hosting a game and therefore cannot start one. To host a game type `!pt host <setup type>`".format(ctx.author.mention))
            return
        #Finds the correct table
        for a in range(len(self.tables)):
            if self.tables[a][1][0] == (ctx.author.id):
                #Checks if the table has already started
                if self.tables[a][0][0] == True:
                    await ctx.send("The game is already running.")
                    return
                #Checks if the user is alone on their table
                if len(self.tables[a]) < 3:
                    await ctx.send("{}, you can't play on your own!".format(ctx.author.mention))
                    return
                else:
                    #Sets variable on the table to begin the game.
                    self.tables[a][0][0] = True
                    self.tables[a][0][2] = self.Deck
                    self.tables[a][0][1] = 0
                    #Deals each player a card
                    for b in range(2,len(self.tables[a])):
                        #Chooses a random card
                        cardNum = random.randint(0,len(self.tables[a][0][2])-1)
                        #Adds the card to the user's hand
                        self.tables[a][b].append(self.tables[a][0][2][cardNum])
                        #Adds the value to their total
                        self.tables[a][b][3] += self.tables[a][0][2][cardNum][1]
                        #Tells them their first card
                        await (discord.utils.find(lambda m: m.id == self.tables[a][b][0], ctx.guild.members)).send("Your first card is: {}".format(self.tables[a][b][len(self.tables[a][b])-1][0]))
                        #Removes the card from the deck
                        del self.tables[a][0][2][cardNum]
                    #Gives the dealer their first card
                    cardNum = random.randint(0,len(self.tables[a][0][2]))
                    self.tables[a][1].append(self.tables[a][0][2][cardNum])
                    self.tables[a][1][1] += self.tables[a][0][2][cardNum][1]
                    await (discord.utils.find(lambda m: m.id == self.tables[a][1][0], ctx.guild.members)).send("Your first card is: {}".format(self.tables[a][1][len(self.tables[a][1])-1][0]))
                    del self.tables[a][0][2][cardNum]
                    #Sets the first player's turn to bet
                    self.tables[a][0][1] = -2
                    #Displays whose turn it is to bet
                    embed = discord.Embed(title="Betting begins with:",
                                          description=(discord.utils.find(lambda m: m.id == self.tables[a][1][0], ctx.guild.members)).display_name + "'s game",
                                          colour=(discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]*(-1)][0], ctx.guild.members)).colour)
                    embed.set_author(name=(discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]*(-1)][0], ctx.guild.members)).display_name,
                                     icon_url=(discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]*(-1)][0], ctx.guild.members)).avatar_url_as(format='jpg'))
                    embed.add_field(name='Current round:',
                            value='Initial bet')
                    embed.set_footer(text=ctx.guild.name,
                                     icon_url=ctx.guild.icon_url_as(format='png'))

                    await ctx.send(content='', embed=embed)
                    #Tells the user how to and how much and how little they can bet
                    if self.tables[a][0][3] == 1:
                        await (discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]*(-1)][0], ctx.guild.members)).send("You can bet a minimum of 1 and a maximum of 5. Use `!pt bet <amount>` in #the-casino to bet some Teics")
                    elif self.tables[a][0][3] in (2,5):
                        await (discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]*(-1)][0], ctx.guild.members)).send("You can bet a minimum of 10 and a maximum of 50. Use `!pt bet <amount>` in #the-casino to bet some Teics")
                    elif self.tables[a][0][3] in (3,6):
                        await (discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]*(-1)][0], ctx.guild.members)).send("You can bet a minimum of 100 and a maximum of 500. Use `!pt bet <amount>` in #the-casino to bet some Teics")
                    elif self.tables[a][0][3] == 4:
                        await (discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]*(-1)][0], ctx.guild.members)).send("You can bet a minimum of 1000 and a maximum of 5000. Use `!pt bet <amount>` in #the-casino to bet some Teics")

    @pt.command(name="bet")
    async def ptbet(self,ctx,bet:int=0):
        if ctx.channel.id != 425370985626075137:
            return
        if ctx.author.id not in self.players:
            await ctx.send("You aren't in a game.")
            return
        if bet < 1:
            await ctx.send("You can't be nothing!")
            return
        for a in range(len(self.tables)):
            if (self.tables[a][(self.tables[a][0][1])*(-1)][0]) == ctx.author.id:
                if self.tables[a][0][0] == False:
                    await ctx.send("The game hasn't started.")
                    return
                if self.tables[a][0][1] > 0:
                    await ctx.send("The game isn't in the betting phase yet.")
                    return
                for b in range(2,len(self.tables[a])):
                    if self.tables[a][b][0] == ctx.author.id:
                        if (b*-1) != self.tables[a][0][1]:
                            await ctx.send(f"{ctx.author.mention}, it's not your turn yet!")
                            return
                if self.tables[a][0][3] == 1:
                    if bet > 5:
                        await ctx.send("That bet exceeds the maxmimum. Please bet an amount lower than 5.")
                        return
                elif self.tables[a][0][3] in (2,5):
                    if bet > 50:
                        await ctx.send("That bet exceeds the maximum. Please bet an amount lower than 50.")
                        return
                    elif bet < 10:
                        await ctx.send("That bet is below the minimum. Please bet an amount higher than 10.")
                        return
                elif self.tables[a][0][3] in (3,6):
                    if bet > 500:
                        await ctx.send("That bet exceeds the maximum. Please bet an amount lower than 500.")
                        return
                    elif bet < 100:
                        await ctx.send("That bet is below the minimum. Please bet an amount higher than 100.")
                        return
                elif self.tables[a][0][3] == 4:
                    if bet > 5000:
                        await ctx.send("That bet exceeds the maximum. Please bet an amount lower than 5000.")
                        return
                    elif bet < 1000:
                        await ctx.send("That bet is below the minimum. Please bet an amount higher than 1000.")
                        return
                TeicList = pickle.load(open('Teic.data', 'rb'))
                for y in range(len(TeicList)):
                    if TeicList[y][0] == (ctx.author.id):
                        TeicList[y][1] -= bet
                        await ctx.send(f"{ctx.author.mention}'s new balance: **{TeicList[y][1]}** Teics")
                def getKey(item):
                    return item[1]
                TeicList = sorted(TeicList,reverse=True,key=getKey)
                pickle.dump(TeicList, open('Teic.data','wb'))
                self.tables[a][(self.tables[a][0][1]*(-1))][1] = bet
                self.tables[a][(self.tables[a][0][1]*(-1))][2] = bet
                await ctx.send("{} bet {} Teics".format(ctx.author.mention,bet))
                self.tables[a][0][1] -= 1
                if self.tables[a][0][1] < (len(self.tables[a])-1)*(-1):
                    for b in range(2,len(self.tables[a])):
                        cardNum = random.randint(0,len(self.tables[a][0][2]))
                        self.tables[a][b].append(self.tables[a][0][2][cardNum])
                        self.tables[a][b][3] += self.tables[a][0][2][cardNum][1]
                        await (discord.utils.find(lambda m: m.id == self.tables[a][b][0], ctx.guild.members)).send("Your second card is: {}".format(self.tables[a][b][len(self.tables[a][b])-1][0]))
                        del self.tables[a][0][2][cardNum]
                    cardNum = random.randint(0,len(self.tables[a][0][2])-1)
                    self.tables[a][1].append(self.tables[a][0][2][cardNum])
                    self.tables[a][1][1] += self.tables[a][0][2][cardNum][1]
                    await (discord.utils.find(lambda m: m.id == self.tables[a][1][0], ctx.guild.members)).send("Your second card is: {}".format(self.tables[a][1][len(self.tables[a][1])-1][0]))
                    del self.tables[a][0][2][cardNum]
                    self.tables[a][0][1] = 2
                    embed = discord.Embed(title="Play begins with:",
                                          description=(discord.utils.find(lambda m: m.id == self.tables[a][1][0], ctx.guild.members)).display_name + "'s game",
                                          colour=(discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]][0], ctx.guild.members)).colour)
                    embed.set_author(name=(discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]][0], ctx.guild.members)).display_name,
                                     icon_url=(discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]][0], ctx.guild.members)).avatar_url_as(format='jpg'))
                    embed.add_field(name='Current round:',
                            value="1st player")
                    embed.set_footer(text=ctx.guild.name,
                                     icon_url=ctx.guild.icon_url_as(format='png'))
                    await (discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]][0], ctx.guild.members)).send("You can now get more cards by doing `!pt twist`\nYou can also use `!pt stick` to stay on your current amount.\nFor information on how these commands work use `!help pontoon`.")
                else:
                    embed = discord.Embed(title="Next bet is with:",
                                          description=(discord.utils.find(lambda m: m.id == self.tables[a][1][0], ctx.guild.members)).display_name + "'s game",
                                          colour=(discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]*(-1)][0], ctx.guild.members)).colour)
                    embed.set_author(name=(discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]*(-1)][0], ctx.guild.members)).display_name,
                                     icon_url=(discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]*(-1)][0], ctx.guild.members)).avatar_url_as(format='jpg'))
                    embed.add_field(name='Current round:',
                            value='Initial bet')
                    embed.set_footer(text=ctx.guild.name,
                                     icon_url=ctx.guild.icon_url_as(format='png'))
                    if self.tables[a][0][3] == 1:
                        await (discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]*(-1)][0], ctx.guild.members)).send("You can bet a minimum of 1 and a maximum of 5. Use `!pt bet <amount>` in #the-casino to bet some Teics")
                    if self.tables[a][0][3] in (2,5):
                        await (discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]*(-1)][0], ctx.guild.members)).send("You can bet a minimum of 10 and a maximum of 50. Use `!pt bet <amount>` in #the-casino to bet some Teics")
                    if self.tables[a][0][3] in (3,6):
                        await (discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]*(-1)][0], ctx.guild.members)).send("You can bet a minimum of 100 and a maximum of 500. Use `!pt bet <amount>` in #the-casino to bet some Teics")
                    if self.tables[a][0][3] == 4:
                        await (discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]*(-1)][0], ctx.guild.members)).send("You can bet a minimum of 1000 and a maximum of 5000. Use `!pt bet <amount>` in #the-casino to bet some Teics")
                await ctx.send(content='', embed=embed)

    @pt.command("twist")
    async def pttwist(self,ctx):
        if ctx.channel.id != 425370985626075137:
            return
        if ctx.author.id not in self.players:
            await ctx.send("You aren't in a game.")
            return
        for a in range(len(self.tables)):
            if (self.tables[a][(self.tables[a][0][1])][0]) == ctx.author.id:
                if self.tables[a][0][0] == False:
                    await ctx.send("The game hasn't started.")
                    return
                if self.tables[a][0][1] < 0:
                    await ctx.send("The game isn't in the play phase yet.")
                    return
                for b in range(2,len(self.tables[a])):
                    if self.tables[a][b][0] == ctx.author.id:
                        if b != self.tables[a][0][1]:
                            await ctx.send(f"{ctx.author.mention}, it's not your turn yet!")
                            return
                if self.tables[a][0][1] != 1:
                    cardNum = random.randint(0,len(self.tables[a][0][2]))
                    self.tables[a][self.tables[a][0][1]].append(self.tables[a][0][2][cardNum])
                    self.tables[a][self.tables[a][0][1]][3] += self.tables[a][0][2][cardNum][1]
                    embed = discord.Embed(title="Player twisted a card:",
                                            description=(discord.utils.find(lambda m: m.id == self.tables[a][1][0], ctx.guild.members)).display_name + "'s game",
                                            colour=(discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]][0], ctx.guild.members)).colour)
                    embed.set_author(name=(discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]][0], ctx.guild.members)).display_name,
                                        icon_url=(discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]][0], ctx.guild.members)).avatar_url_as(format='jpg'))
                    embed.add_field(name='Recieved',
                                    value=self.tables[a][0][2][cardNum][0])
                    embed.add_field(name='Cards in hand',
                                    value=len(self.tables[a][self.tables[a][0][1]])-4)
                    embed.set_footer(text=ctx.guild.name,
                                        icon_url=ctx.guild.icon_url_as(format='png'))
                    await ctx.send(content='', embed=embed)
                    await ctx.author.send("You recieved {}".format(self.tables[a][self.tables[a][0][1]][len(self.tables[a][self.tables[a][0][1]])-1][0]))
                    del self.tables[a][0][2][cardNum]
                    if self.tables[a][self.tables[a][0][1]][3] > 21:
                        await ctx.send("{} went bust!".format(ctx.author.mention))
                        TeicList = pickle.load(open('Teic.data', 'rb'))
                        for y in range(len(TeicList)):
                            if TeicList[y][0] == self.tables[a][1][0]:
                                TeicList[y][1] += bet
                                await ctx.send(f"{(discord.utils.find(lambda m: m.id == self.tables[a][1][0], ctx.guild.members)).mention}'s new balance: **{TeicList[y][1]}** Teics")
                        def getKey(item):
                            return item[1]
                        TeicList = sorted(TeicList,reverse=True,key=getKey)
                        pickle.dump(TeicList, open('Teic.data','wb'))
                        self.tables[a][self.tables[a][0][1]][1] == 0
                        self.tables[a][0][1] += 1
                        if self.tables[a][1][0] >= len(self.tables[a]):
                            self.tables[a][0][1] = 1
                        embed = discord.Embed(title="It's this player's turn!",
                                              description=(discord.utils.find(lambda m: m.id == self.tables[a][1][0], ctx.guild.members)).display_name + "'s game",
                                              colour=(discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]][0], ctx.guild.members)).colour)
                        embed.set_author(name=(discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]][0], ctx.guild.members)).display_name,
                                         icon_url=(discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]][0], ctx.guild.members)).avatar_url_as(format='jpg'))
                        if self.tables[a][1][0] == 1:
                            embed.add_field(name='Current round:',
                                            value="Host's turn")
                        else:
                            embed.add_field(name='Current round:',
                                    value="Player {}'s turn".format((discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]][0], ctx.guild.members))))
                        embed.set_footer(text=ctx.guild.name,
                                         icon_url=ctx.guild.icon_url_as(format='png'))
                        await (discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]][0], ctx.guild.members)).send("You can now get more cards by doing `!pt twist`\nYou can also use `!pt stick` to stay on your current amount.\nFor information on how these commands work use `!help pontoon`.")
                        await ctx.send(content='',embed=embed)
                elif self.tables[a][0][1] == 1:
                    cardNum = random.randint(0,len(self.tables[a][0][2]))
                    self.tables[a][1].append(self.tables[a][0][2][cardNum])
                    self.tables[a][1][1] += self.tables[a][0][2][cardNum][1]
                    embed = discord.Embed(title="Host twisted a card:",
                                            description=(discord.utils.find(lambda m: m.id == self.tables[a][1][0], ctx.guild.members)).display_name + "'s game",
                                            colour=(discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]][0], ctx.guild.members)).colour)
                    embed.set_author(name=(discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]][0], ctx.guild.members)).display_name,
                                        icon_url=(discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]][0], ctx.guild.members)).avatar_url_as(format='jpg'))
                    embed.add_field(name='Recieved',
                                    value=self.tables[a][0][2][cardNum][0])
                    embed.add_field(name='Cards in hand',
                                    value=len(self.tables[a][self.tables[a][0][a]])-2)
                    embed.set_footer(text=ctx.guild.name,
                                        icon_url=ctx.guild.icon_url_as(format='png'))
                    await ctx.send(content='', embed=embed)
                    del self.tables[a][0][2][cardNum]
                    await ctx.author.send("You recieved {}".format(self.tables[a][1][len(self.tables[a][1])-1][0]))
                    if self.tables[a][self.tables[a][0][1]][1] > 21:
                        await ctx.send("{} went bust!".format(ctx.author.mention))
                        self.tables[a][self.tables[a][0][a]][1] = 0
                        embed = discord.Embed(title='Final hands!',
                                              colour=0x006622)
                        hHand = ''
                        for d in range(2,len(self.tables[a][1])):
                            hHand = hHand + self.tables[a][1][d][0] + ', '
                        for d in range(2,len(self.tables[a][1])):
                            if self.tables[a][1][d][1] == 1:
                                self.tables[a][1][1] += 10
                                if self.tables[a][1][1] > 21:
                                    self.tables[a][1][1] -= 10
                        special = ''
                        if len(self.tables[a][1])-2 == 2 and self.tables[a][1][1] == 21:
                            special = '\n__**Pontoon!**__'
                        elif len(self.tables[a][1])-2 == 5:
                            special = '\n__**Five Card Trick!**__'
                        embed.add_field(name=f"{ctx.author}'s hand:",
                                        value=f"Total = {self.tables[a][1][1]}\nHand = {hHand}{special}")
                        if len(self.tables[a][1])-2 == 2 and self.tables[a][1][1] == 21:
                            self.tables[a][1][1] == 23
                        elif len(self.tables[a][1])-2 == 5:
                            self.tables[a][1][1] == 22
                        for c in range(2,len(self.tables[a])):
                            hand = ''
                            for d in range(4,len(self.tables[a][c])):
                                hand = hand + self.tables[a][c][d][0] + ', '
                            for d in range(2,len(self.tables[a][1])):
                                if self.tables[a][c][d][1] == 1:
                                    self.tables[a][c][1] += 10
                                    if self.tables[a][c][1] > 21:
                                        self.tables[a][c][1] -= 10
                            special = ''
                            if len(self.tables[a][c])-2 == 2 and self.tables[a][c][1] == 21:
                                special = '\n__**Pontoon!**__'
                            elif len(self.tables[a][c])-2 == 5:
                                special = '\n__**Five Card Trick!**__'
                            if len(self.tables[a][1])-2 == 2 and self.tables[a][1][1] == 21:
                                self.tables[a][1][1] == 23
                            elif len(self.tables[a][1])-2 == 5:
                                self.tables[a][1][1] == 22
                            if hand > hHand:
                                hasWon = 'Won!'
                                TeicList = pickle.load(open('Teic.data', 'rb'))
                                for y in range(len(TeicList)):
                                    if TeicList[y][0] == self.tables[a][1][0]:
                                        TeicList[y][1] -= self.tables[a][c][2]
                                        await ctx.send(f"{(discord.utils.find(lambda m: m.id == self.tables[a][1][0], ctx.guild.members)).mention}'s new balance: **{TeicList[y][1]}** Teics")
                                    if TeicList[y][0] == self.tables[a][c][0]:
                                        TeicList[y][1] += 2*self.tables[a][c][2]
                                        await ctx.send(f"{(discord.utils.find(lambda m: m.id == self.tables[a][c][0], ctx.guild.members)).mention}'s new balance: **{TeicList[y][1]}** Teics")
                                def getKey(item):
                                    return item[1]
                                TeicList = sorted(TeicList,reverse=True,key=getKey)
                                pickle.dump(TeicList, open('Teic.data','wb'))
                            else:
                                hasWon = 'Lost...'
                                TeicList = pickle.load(open('Teic.data', 'rb'))
                                for y in range(len(TeicList)):
                                    if TeicList[y][0] == self.tables[a][1][0]:
                                        TeicList[y][1] += bet
                                        await ctx.send(f"{(discord.utils.find(lambda m: m.id == self.tables[a][1][0], ctx.guild.members)).mention}'s new balance: **{TeicList[y][1]}** Teics")
                                def getKey(item):
                                    return item[1]
                                TeicList = sorted(TeicList,reverse=True,key=getKey)
                                pickle.dump(TeicList, open('Teic.data','wb'))
                            if hand > 21:
                                hand = 21
                            embed.add_field(name="{}'s hand".format(discord.utils.find(lambda m: m.id == self.tables[a][c][0], ctx.guild.members)),
                                value=f"\n__{hasWon}__\nTotal = {self.tables[a][c][3]}\nhand = {hand}\nTotal bet = {self.tables[a][c][2]}{special}")
                        embed.set_author(name=f"{ctx.author.display_name}'s game",
                                             icon_url=ctx.author.avatar_url_as(format='png'))
                        embed.set_footer(text=ctx.guild.name,
                                             icon_url=ctx.guild.icon_url_as(format='png'))
                        await ctx.send(content='',embed=embed)
                        for c in range(2,len(self.tables[a])):
                            self.tables[a][c] = [self.tables[a][c][0],0,0,0]
                        self.tables[a][1] = [self.tables[a][1][0],0]
                        self.tables[a][0][0] = False

    #TODO - add host secton
    @pt.command("buy")
    @commands.has_any_role('beta')
    async def ptbuy(self,ctx,amount:int=0):
        if ctx.channel.id != 425370985626075137:
            return
        if amount < 0:
            await ctx.send("You can't bet nothing!")
            return
        if ctx.author.id not in self.players:
            await ctx.send("You aren't in a game.")
            return
        for a in range(len(self.tables)):
            if (self.tables[a][(self.tables[a][0][1])][0]) == ctx.author.id:
                if self.tables[a][0][0] == False:
                    await ctx.send("The game hasn't started.")
                    return
                if self.tables[a][0][1] < 0:
                    await ctx.send("The game isn't in the play phase yet.")
                    return
                for b in range(2,len(self.tables[a])):
                    if self.tables[a][b][0] == ctx.author.id:
                        if b != self.tables[a][0][1]:
                            await ctx.send(f"{ctx.author.mention}, it's not your turn yet!")
                            return
                TeicList = pickle.load(open('Teic.data', 'rb'))
                for y in range(len(TeicList)):
                    if TeicList[y][0] == (ctx.author.id):
                        if TeicList[y][1] < amount:
                            await ctx.send("You can't afford that!")
                            return
                if self.tables[a][0][1] != 1:
                    #TODO - take money, 21 check
                    cardNum = random.randint(0,len(self.tables[a][0][2]))
                    self.tables[a][self.tables[a][0][1]].append(self.tables[a][0][2][cardNum])
                    embed = discord.Embed(title="Player bought a card:",
                                            description=(discord.utils.find(lambda m: m.id == self.tables[a][1][0], ctx.guild.members)).display_name + "'s game",
                                            colour=(discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]][0], ctx.guild.members)).colour)
                    embed.set_author(name=(discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]][0], ctx.guild.members)).display_name,
                                        icon_url=(discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]][0], ctx.guild.members)).avatar_url_as(format='jpg'))
                    embed.add_field(name='Recieved',
                                    value='??')
                    embed.add_field(name='Cards in hand',
                                    value=len(self.tables[a][self.tables[a][0][1]])-4)
                    embed.set_footer(text=ctx.guild.name,
                                        icon_url=ctx.guild.icon_url_as(format='png'))
                    await ctx.send(content='', embed=embed)
                    del self.tables[a][0][2][cardNum]
                    await ctx.author.send("You recieved {}".format(self.tables[a][1][len(self.tables[a][1])-1][0]))

    @pt.command("stick")
    async def ptstick(self,ctx):
        if ctx.channel.id != 425370985626075137:
            return
        if ctx.author.id not in self.players:
            await ctx.send("You aren't in a game.")
            return
        for a in range(len(self.tables)):
            if (self.tables[a][(self.tables[a][0][1])][0]) == ctx.author.id:
                if self.tables[a][0][0] == False:
                    await ctx.send("The game hasn't started.")
                    return
                if self.tables[a][0][1] < 0:
                    await ctx.send("The game isn't in the play phase yet.")
                    return
                for b in range(len(self.tables[a])):
                    if self.tables[a][b][0] == ctx.author.id:
                        if b != self.tables[a][0][1]:
                            await ctx.send(f"{ctx.author.mention}, it's not your turn yet!")
                            return
                        if self.tables[a][0][1] == 1:
                            embed = discord.Embed(title='Final hands!',
                                                  colour=0x006622)
                            hHand = ''
                            for d in range(2,len(self.tables[a][b])):
                                hHand = hHand + self.tables[a][b][d][0] + ', '
                            for d in range(2,len(self.tables[a][b])):
                                if self.tables[a][b][d][1] == 1:
                                    self.tables[a][b][1] += 10
                                    if self.tables[a][b][1] > 21:
                                        self.tables[a][b][1] -= 10
                            special = ''
                            if (len(self.tables[a][b])-2 == 2 and self.tables[a][b][1] == 21):
                                special = '\n__**Pontoon!**__'
                            elif len(self.tables[a][b])-2 == 5:
                                special = '\n__**Five Card Trick!**__'
                            embed.add_field(name=f"{ctx.author}'s hand:",
                                            value=f"Total = {self.tables[a][b][1]}\nHand = {hHand}{special}")
                            if len(self.tables[a][b])-2 == 2 and self.tables[a][b][1] == 21:
                                self.tables[a][b][1] == 23
                            elif len(self.tables[a][b])-2 == 5:
                                self.tables[a][b][1] == 22
                            for c in range(2,len(self.tables[a])):
                                hand = ''
                                for d in range(4,len(self.tables[a][c])):
                                    hand = hand + self.tables[a][c][d][0] + ', '
                                for d in range(4,len(self.tables[a][c])):
                                    if self.tables[a][c][d][1] == 1:
                                        self.tables[a][c][1] += 10
                                        if self.tables[a][c][1] > 21:
                                            self.tables[a][c][1] -= 10
                                special = ''
                                if len(self.tables[a][c])-2 == 2 and self.tables[a][c][1] == 21:
                                    special = '\n__**Pontoon!**__'
                                elif len(self.tables[a][c])-2 == 5:
                                    special = '\n__**Five Card Trick!**__'
                                if len(self.tables[a][c])-2 == 2 and self.tables[a][c][1] == 21:
                                    self.tables[a][c][1] == 23
                                elif len(self.tables[a][c])-2 == 5:
                                    self.tables[a][c][1] == 22
                                if hand > hHand:
                                    hasWon = 'Won!'
                                    TeicList = pickle.load(open('Teic.data', 'rb'))
                                    for y in range(len(TeicList)):
                                        if TeicList[y][0] == self.tables[a][1][0]:
                                            TeicList[y][1] -= self.tables[a][c][2]
                                            await ctx.send(f"{(discord.utils.find(lambda m: m.id == self.tables[a][1][0], ctx.guild.members)).mention}'s new balance: **{TeicList[y][1]}** Teics")
                                        if TeicList[y][0] == self.tables[a][c][0]:
                                            TeicList[y][1] += 2*self.tables[a][c][2]
                                            await ctx.send(f"{(discord.utils.find(lambda m: m.id == self.tables[a][c][0], ctx.guild.members)).mention}'s new balance: **{TeicList[y][1]}** Teics")
                                    def getKey(item):
                                        return item[1]
                                    TeicList = sorted(TeicList,reverse=True,key=getKey)
                                    pickle.dump(TeicList, open('Teic.data','wb'))
                                else:
                                    hasWon = 'Lost...'
                                    TeicList = pickle.load(open('Teic.data', 'rb'))
                                    for y in range(len(TeicList)):
                                        if TeicList[y][0] == self.tables[a][1][0]:
                                            TeicList[y][1] += bet
                                            await ctx.send(f"{(discord.utils.find(lambda m: m.id == self.tables[a][1][0], ctx.guild.members)).mention}'s new balance: **{TeicList[y][1]}** Teics")
                                    def getKey(item):
                                        return item[1]
                                    TeicList = sorted(TeicList,reverse=True,key=getKey)
                                    pickle.dump(TeicList, open('Teic.data','wb'))
                                if self.tables[a][c][1] > 21:
                                    self.tables[a][c][1] = 21
                                embed.add_field(name="{}'s hand".format(discord.utils.find(lambda m: m.id == self.tables[a][c][0], ctx.guild.members)),
                                    value=f"\n__{hasWon}__\nTotal = {self.tables[a][c][3]}\nHand = {hand}\nTotal bet = {self.tables[a][c][2]}{special}")
                            embed.set_author(name=f"{ctx.author.display_name}'s game",
                                                 icon_url=ctx.author.avatar_url_as(format='png'))
                            embed.set_footer(text=ctx.guild.name,
                                                 icon_url=ctx.guild.icon_url_as(format='png'))
                            await ctx.send(content='',embed=embed)
                            for c in range(2,len(self.tables[a])):
                                self.tables[a][c] = [self.tables[a][c][0],0,0,0]
                            self.tables[a][1] = [self.tables[a][1][0],0]
                            self.tables[a][0][0] = False
                        else:
                            await ctx.send(f"{ctx.author.mention} stuck.")
                            self.tables[a][self.tables[a][0][1]][1] == 0
                            self.tables[a][0][1] += 1
                            if self.tables[a][1][0] >= len(self.tables[a]):
                                self.tables[a][0][1] = 1
                            embed = discord.Embed(title="It's this player's turn!",
                                                  description=(discord.utils.find(lambda m: m.id == self.tables[a][1][0], ctx.guild.members)).display_name + "'s game",
                                                  colour=(discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]][0], ctx.guild.members)).colour)
                            embed.set_author(name=(discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]][0], ctx.guild.members)).display_name,
                                             icon_url=(discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]][0], ctx.guild.members)).avatar_url_as(format='jpg'))
                            if self.tables[a][1][0] == 1:
                                embed.add_field(name='Current round:',
                                                value="Host's turn")
                            else:
                                embed.add_field(name='Current round:',
                                        value="Player {}'s turn".format((discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]][0], ctx.guild.members))))
                            embed.set_footer(text=ctx.guild.name,
                                             icon_url=ctx.guild.icon_url_as(format='png'))
                            await (discord.utils.find(lambda m: m.id == self.tables[a][self.tables[a][0][1]][0], ctx.guild.members)).send("You can now get more cards by doing `!pt twist`\nYou can also use `!pt stick` to stay on your current amount.\nFor information on how these commands work use `!help pontoon`.")
                            await ctx.send(content='',embed=embed)

    #TODO - well, what do you think?
    @pt.command("split")
    async def ptsplit(self,ctx):
        if ctx.channel.id != 425370985626075137:
            return
        if ctx.author.id not in self.players:
            await ctx.send("You aren't in a game.")
            return
        for a in range(len(self.tables)):
            if (self.tables[a][(self.tables[a][0][1])][0]) == ctx.author.id:
                if self.tables[a][0][0] == False:
                    await ctx.send("The game hasn't started.")
                    return
                if self.tables[a][0][1] < 0:
                    await ctx.send("The game isn't in the play phase yet.")
                    return
                for b in range(2,len(self.tables[a])):
                    if self.tables[a][b][0] == ctx.author.id:
                        if b != self.tables[a][0][1]:
                            await ctx.send(f"{ctx.author.mention}, it's not your turn yet!")
                            return
        await ctx.send("No valid setup types support this command.")
                
    '''
    Stopping or leaving a game
    '''
                                                                   
    @pt.command(name="stop")
    async def ptstop(self,ctx):
        if ctx.channel.id != 425370985626075137:
            return
        if ctx.author.id not in self.hosts:
            await ctx.send("{}, you aren't hosting a game and therefore cannot stop one. To leave one type `!pt leave`".format(ctx.author.mention))
            return
        for a in range(len(self.tables)):
            if self.tables[a][1][0] == (ctx.author.id):
                await ctx.send("{}, all bets will be returned and the game ended.".format(ctx.author.mention))
                del self.hosts[a]
                TeicList = pickle.load(open('Teic.data', 'rb'))
                for b in range(2,len(self.tables[a])):
                    for y in range(len(TeicList)):
                        if self.tables[a][b][0] == TeicList[y][0]:
                            TeicList[y][1] += self.tables[a][b][2]
                for b in range(1,len(self.tables[a])):
                    self.players.remove(self.tables[a][b][0])
                def getKey(item):
                    return item[1]
                TeicList = sorted(TeicList,reverse=True,key=getKey)
                pickle.dump(TeicList, open('Teic.data','wb'))
                del self.tables[a]

    @pt.command(name="leave")
    async def ptleave(self,ctx):
        if ctx.channel.id != 425370985626075137:
            return
        if ctx.author.id not in self.players:
            await ctx.send("{}, you aren't playing a game!".format(ctx.author.mention))
            return
        if ctx.author.id in self.hosts:
            await ctx.send("{}, you are hosting a game! Use `!pt stop` to stop hosting.".format(ctx.author.mention))
            return
        for a in range(len(self.tables)):
            for b in range(len(self.tables[a])):
                if self.tables[a][b][0] == (ctx.author.id):
                    if self.tables[a][0][0] == True:
                        await ctx.send("Game is currently running. Cannot leave.")
                        return
                    await ctx.send("{} has left {}'s game. Their bet(s) have been returned".format(ctx.author.mention,(discord.utils.find(lambda m: m.id == self.tables[y][1][0], ctx.guild.members)).mention))
                    TeicList = pickle.load(open('Teic.data', 'rb'))
                    for y in range(len(TeicList)):
                        if self.tables[a][b][0] == TeicList[y][0]:
                            TeicList[y][1] += self.tables[a][b][2]
                    def getKey(item):
                        return item[1]
                    TeicList = sorted(TeicList,reverse=True,key=getKey)
                    pickle.dump(TeicList, open('Teic.data','wb'))
                    del self.tables[a][b]
                    for c in range(len(self.players)):
                        if self.players[c] == (ctx.author.id):
                            del self.players[c]
                            break
            if len(self.tables[a]) < 3 and self.tables[a][0][0] == True:
                host = (discord.utils.find(lambda m: m.id == self.tables[a][1][0], ctx.guild.members))
                await ctx.send("{}, you don't have enough players to continue. Your game has been stopped.".format(host.mention))
                self.players.remove(self.tables[a][1][0])
                del self.tables[a]
                
# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(PontoonCog(bot))
    random.seed()

##pontoon = <#425370985626075137>
##the-casino = <#421712364774227978>
##slots = <#425371010024341525>
##trivia = <#425370923684593674>
