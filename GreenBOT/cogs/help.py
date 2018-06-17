import discord
from discord.ext import commands
import pickle
import random
import asyncio

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


class HelpCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='info')
    async def info(self, ctx):
        embed = discord.Embed(title='Bot info',
                              description="What do you want this to say?",
                              colour=0x008800)
        embed.set_author(name=self.bot.user.name,
                         icon_url=self.bot.user.avatar_url_as(format='png'))
        embed.add_field(name='Hello!',
                        value='I am a bot created by Greenfoot5. Recent updates can be see with the `&&updates` command')
        embed.add_field(name='Prefix',
                        value='My current prefix is `&&`')
        embed.add_field(name='It broke what do I do?',
                        value='Post in on the support server and wait for it to be notied. Until then, please be patient. If possible warn others of the problem.')
        embed.add_field(name='Can I support the bot in any way?',
                        value="Other than joining the support server and offering input not at the moment.")
        embed.add_field(name='Credits',
                        value=f"This bot was created by Greenfoot5#2535.")
        embed.set_footer(text=ctx.guild.name,
                         icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='**Displaying info**', embed=embed)

    @commands.command(name='updates')
    async def updates(self, ctx):
        embed = discord.Embed(title='Updates',
                              description=f"My most recent updates!!",
                              colour=0x6B4BD1)
        embed.set_author(name=self.bot.user.name,
                         icon_url=self.bot.user.avatar_url_as(format='png'))
        embed.add_field(name='v1.3.1',
                        value='Removed blurple commands. Added `&&deal` commands to the misc section.')
        embed.add_field(name='v1.3.0',
                        value='Discord turns three! Celebrate with project Blurple!')
        embed.add_field(name='v1.2.1',
                        value="Added `&&servers` which shows how many servers the bot is currently connected to.")
        embed.add_field(name='v1.2.0',
                        value="Added the bot to server lists and modified the prefix to `&&`. `&&enable` and `&&disable` now work. Also added a global trivia leaderboard!")
        embed.add_field(name='v1.1.2',
                        value="Prepaed the bot to become universal.\nAdded `&&invite` to invite the bot to your server.\nAdded the setup section. Currently has no functionality")
        embed.add_field(name='v1.1.1',
                        value='Fixed some bugs in the embeds and added `&&support` which shows the link to the support server.')
        embed.add_field(name='v1.1.0',
                        value="Trivia and Miscellaneous commands were added.")
        embed.add_field(name='v1.0.0',
                        value="I was born with a __very__ basic set of commands. This one and two others... Not a very exciting beginning.")
        embed.set_footer(text=ctx.guild.name,
                         icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='**Displaying updates**', embed=embed)

    @commands.command(name='support')
    async def support(self, ctx):
        embed = discord.Embed(title='Support',
                              description=f"What the support server is and the link",
                              colour=0xFFAA00)
        embed.set_author(name=self.bot.user.name,
                         icon_url=self.bot.user.avatar_url_as(format='png'))
        embed.add_field(name='Support server',
                        value="You join the support server [here.](https://discord.gg/MVzHqdm)")
        embed.add_field(name='Why join?',
                        value="In the server you get firsthand (and often early) information about what will happen to the bot!\nYou will also get to see discussions on what will be added to the bot and even have input on it!")
        embed.add_field(name='What happens if I see a bug?',
                        value="Take a screenshot, join the server and post it in #bugs!")
        embed.set_footer(text=ctx.guild.name,
                         icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='**Link = https://discord.gg/MVzHqdm**', embed=embed)

    @commands.command(name='invite')
    async def invite(self, ctx):
        await ctx.send("https://discordapp.com/api/oauth2/authorize?client_id=436947191395909642&permissions=2146958583&scope=bot")
        
    @commands.group(name='help',aliases=['h','Help','H'])
    async def helps(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title='Help',
                              description=f"Type `&&help <category>` for more info on a category.\n[] Are optional.\n<> Are required.\n() Are aliases",
                              colour=0x469BFF)
            embed.set_author(name=self.bot.user.name,
                              icon_url=self.bot.user.avatar_url_as(format='png'))

            embed.add_field(name='Aliases',
                            value='`Help`,`help`,`H`,`h')
            embed.add_field(name="Website",
                            value="[https://scrapbox.io/GreenBOT](https://scrapbox.io/GreenBOT)")
            embed.add_field(name='Base',
                            value='All basic commands for the bot.')
            guilds = []
            guilds = pickle.load(open("guilds.data", "rb"))
            for a in range(len(guilds)):
                if guilds[a][0] == ctx.guild.id:
                    if guilds[a][3][0] == True:
                        embed.add_field(name='Members',
                                        value="Some commands to learn about the server and it's members.")
                    if guilds[a][2][0] == True:
                        embed.add_field(name='Trivia',
                                        value='Do you have the knowledge to answer the questions correctly?')
                    if guilds[a][1][0] == True:
                        embed.add_field(name='Miscellaneous',
                                        value="A.K.A. Misc. Commands that don't have a category.")
            embed.add_field(name='Setup',
                            value="All commands necessary to setup the bot correctly. (Requires manage server permission)")
            embed.set_footer(text=ctx.guild.name,
                             icon_url=ctx.guild.icon_url_as(format='png'))

            await ctx.send(content='**Displaying help**', embed=embed)
    '''
    @helps.command(name='blurple')
    async def hplurple(self,ctx):
        embed = discord.Embed(title='Blurple commands commands',
                              description="Type `&&help <category>` for more info on a category.\n[] Are optional.\n<> Are required.\n() Are aliases",
                              colour=0x7289DA)
        embed.set_author(name=self.bot.user.name,
                        icon_url=self.bot.user.avatar_url_as(format='png'))
        embed.add_field(name='&&blurple <image>',
                        value='Displays the amount of blurple in an image')
        embed.add_field(name='&&blurplefy <image> (&&blurplefier)',
                        value="Blurfplifies an image! Note this isn't perfect.")
        embed.add_field(name='&&blueplefygif',
                        value="Blurplifies a gif! Note this isn't perfect.")
        embed.add_field(name='&&bpinvite',
                        value="Send a link to the project blurple discord server.")
        embed.set_footer(text=ctx.guild.name,
                         icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='**Happy birthday discord!**', embed=embed)

    @commands.command(name='pbinvite')
    async def pbinvite(self,ctx):
        await ctx.send("**Invite:** https://discord.gg/qEmKyCf")
    '''
    
    @helps.command(name='base',aliases=['Base','basic','Baisc','B','b'])
    async def base(self,ctx):
        embed = discord.Embed(title='Base commands',
                              description="Type `&&help <category>` for more info on a category.\n[] Are optional.\n<> Are required.\n() Are aliases",
                              colour=0xFFAA00)
        embed.set_author(name=self.bot.user.name,
                        icon_url=self.bot.user.avatar_url_as(format='png'))

        embed.add_field(name='Aliases',
                        value='`Base`,`base`,`Basic`,`basic`,`B`,`b`')
        embed.add_field(name='&&help',
                        value='Displays help and lists commands on the bot.')
        embed.add_field(name='&&info',
                        value='Displays information about the bot.')
        embed.add_field(name='&&support',
                        value='Displays the link to the support server.')
        embed.add_field(name='&&updates',
                        value='Displays the most recent updates for the bot.')
        embed.add_field(name='&&servers',
                        value='Replies with how many servers the bot is connected to.')
        embed.add_field(name='&&invite',
                        value="Send a link so you can invite the bot to your server!")
        embed.set_footer(text=ctx.guild.name,
                         icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='**Displaying base category help**', embed=embed)

    @helps.command(name='members',aliases=['Members','member','Member','M','m'])
    @is_module_enabled('members')
    async def Hmembers(self,ctx):
        embed = discord.Embed(title='Base commands',
                              description="Type `&&help <category>` for more info on a category.\n[] Are optional.\n<> Are required.\n() Are aliases",
                              colour=0xFFAA00)
        embed.set_author(name=self.bot.user.name,
                        icon_url=self.bot.user.avatar_url_as(format='png'))

        embed.add_field(name='Aliases',
                        value='`Member`,`member`,`Members`,`members`,`M`,`m`')
        embed.add_field(name='&&joined',
                        value='Shows when a member joined the server.')
        embed.add_field(name='&&perms [member]',
                        value='Displays all the permissions for a member. If ne member is selected it will choose the sender.')
        embed.add_field(name='&&avatar [member]',
                        value='Displays the avatar for a user. If no user is selected it will choose the sender.')
        embed.add_field(name='&&icon',
                        value='Shows the icon for the server.')
        embed.set_footer(text=ctx.guild.name,
                         icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='**Displaying members category help**', embed=embed)

    @helps.command(name='trivia',aliases=['Trivia','tr','Tr'])
    @is_module_enabled('trivia')
    async def Htrivia(self,ctx):
        embed = discord.Embed(title='Trivia Commands',
                              description="Type `&&help <category>` for more info on a category.\n[] Are optional.\n<> Are required.\n() Are aliases",
                              colour=0x000055)
        embed.set_author(name=self.bot.user.name,
                        icon_url=self.bot.user.avatar_url_as(format='png'))

        embed.add_field(name='Aliases',
                        value='`Trivia`,`trivia`,`Tr`,`tr`')
        embed.add_field(name='Base info',
                        value='Each answer for a person must be their full name unless stated otherwise.\nDates are formatted `DD/MM/YYYY`.\nThe USA will always be called the US unless from someone.\n20 seconds timout per question. If 7 are left unanswered in a row then the trivia will stop.\nOne point per correct answer if you are first.\nQuestions are constantly being added. If you have a question you want to see added PM Greenfoot5!')
        embed.add_field(name='&&tr',
                        value="Base command for trivia. Does nothing on it's own.")
        embed.add_field(name='&&tr start',
                        value='Starts a game of trivia. Anyone can pariticpate.')
        embed.add_field(name='&&tr length',
                        value="Shows how many questions are currently in the system.")
        embed.add_field(name='&&tr stats [member]',
                        value="Shows the stats for a member of the server. If no member is selected it will select the sender.")
        embed.add_field(name='&&tr rank [integer]',
                        value="Shows the stats for a user at the specified rank. They may not be in your server. If no number is selected it will select 1.")
        embed.add_field(name='&&tr top',
                        value="Displays the top trivia players")
        embed.set_footer(text=ctx.guild.name,
                         icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='**Displaying trivia category help**', embed=embed)

    
    @helps.command(name='Misc',aliases=['misc','miscellaneous','Miscellaneous'])
    @is_module_enabled('misc')
    async def Hmisc(self,cxt):
        embed = discord.Embed(title='Miscellaneous commands.',
                              description="Type `&&help <category>` for more info on a category.\n[] Are optional.\n<> Are required.\n() Are aliases",
                              colour=0x0099FF)
        embed.set_author(name=self.bot.user.name,
                        icon_url=self.bot.user.avatar_url_as(format='png'))

        embed.add_field(name='Aliases',
                        value='`Misc`,`misc`,`Miscellaneous`,`miscellaneous`')
        embed.add_field(name='&&random int <minimum> <maximum>',
                        value='Displays a random integer between the two values.\nIt is inclusive\nThe two numbers must be in the correct order.')
        embed.add_field(name='&&random random',
                        value='Selects a random non-integer between 0 and 1')
        embed.add_field(name='&&add <first number> <second number>',
                        value='Adds the two numbers together and displays the answer.')
        embed.add_field(name='&&deal public',
                        value='Deals you a card for everyone to see.')
        embed.add_field(name='&&deal private',
                        value='Deals you a card via DM')
        embed.add_field(name='&&deal to [member]',
                        value='Deals a card to a member. If nobody is selected it chooses you. It will send it via DM and publically.')
        embed.add_field(name='&&deal pto [member]',
                        value='Privatly sends a card to the specified user via DM. If nobody is specified it will select you.')
        embed.set_footer(text=cxt.guild.name,
                         icon_url=cxt.guild.icon_url_as(format='png'))

        await cxt.send(content='&**Displaying Misc category help**', embed=embed)

    @helps.command(name='Setup',aliases=['setup'])
    async def HSetup(self, ctx):
        perms = '\n'.join(perm for perm, value in ctx.author.guild_permissions if value)
        if "manage_guild" in perms:
            embed = discord.Embed(title='Miscellaneous commands.',
                                  description="Type `&&help <category>` for more info on a category.\n[] Are optional.\n<> Are required.\n() Are aliases",
                                  colour=0x0099FF)
            embed.set_author(name=self.bot.user.name,
                            icon_url=self.bot.user.avatar_url_as(format='png'))

            embed.add_field(name='Aliases',
                            value='`Setup`,`setup`')
            embed.add_field(name='Note',
                            value="This is a WIP section so not all these commands will work.")
            embed.add_field(name='&&setup',
                            value="Main setup command")
            embed.add_field(name="&&setup reset",
                            value="Resets or sets up your server ready for use. (Requires administrator permissions)")
            embed.add_field(name='&&first',
                            value="If this is your first time using this bot or a discord bot this will run you through how to use the bot.")
            embed.add_field(name='&&setup enable <module>',
                            value="Enables a module. You can find a list of avaliable modules [here.](https://scrapbox.io/GreenBOT/Avaliable_modules)")
            embed.add_field(name='&&setup disable <module>',
                            value="Disables a module. You can find a list of avaliable modules [here.](https://scrapbox.io/GreenBOT/Avaliable_modules)")
            embed.set_footer(text=ctx.guild.name,
                             icon_url=ctx.guild.icon_url_as(format='png'))

            await ctx.send(content='**Displaying Setup category help**', embed=embed)
        else:
            await ctx.send("You need the manage server permission to run this command.")

    @helps.command(name='owner',aliases=['Owner','OWNER'])
    @commands.is_owner()
    async def owner_only(self,ctx):
        embed = discord.Embed(title='Bot Owner Commands',
                              description="Type `&&help <category>` for more info on a category.\n[] Are optional.\n<> Are required.\n() Are aliases",
                              colour=0xFFAA00)
        embed.set_author(name=self.bot.name,
                        icon_url=self.bot.avatar_url_as(format='png'))

        embed.add_field(name='Aliases',
                        value='`OWNER`,`Owner`,`owner`')
        embed.add_field(name='&&[re/un]load <filepath>',
                        value="[Re/Un]Loads a cog.\nRemember to use the filepath so that instead of a `/` it's a `.`.\n.py is uncessary.")
        embed.add_field(name='&&embeds',
                        value='Displays an example embed.\nAlso has a formatting image.')
        embed.add_field(name='&&setup fix',
                        value="Fixes/updates setup. Need to change code each time use command though.")
        embed.set_footer(text=ctx.guild.name,
                        icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='**Displaying owner only commands**', embed=embed, delete_after=10)
        await ctx.message.delete()

'''
    @helps.command(name='beta',aliases=['BETA','Beta'])
    @commands.has_any_role('beta')
    async def beta(self,ctx):
        if ctx.channel.id != 421712364774227978:
            await ctx.message.delete()
            await ctx.send(content="Wrong channel. Please use `#the-casino`.",delete_after=5)
            return
        embed = discord.Embed(title='Beta Access Commands',
                              description="A bot for The Democratic People's Republic of VorTeic.\nType `!help <category>` for more info on a category.\n[] Are optional.\n<> Are required.\n() Are aliases",
                              colour=0x0099FF)
        embed.set_author(name='The Dealer',
                        icon_url='https://cdn.discordapp.com/avatars/421718079265964032/7805693d09954641ab8bbb51f3582f07.png')

        embed.add_field(name='Aliases',
                        value='`BETA`,`Beta`,`beta`')
        embed.add_field(name='Current access to commands',
                        value='`beta`')
        embed.add_field(name='!pt',
                        value="Base Pontoon command. Refer to `!pt help` for more information.")
        embed.set_footer(text='DPRoVT',
                         icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='&&Displaying Beta commands&&', embed=embed, delete_after=10)
        await ctx.message.delete()

    @helps.command(name='slots',aliases=['Slots','slot','Slot','S','s'])
    async def slots(self,ctx):
        if ctx.channel.id != 425371010024341525:
            await ctx.message.delete()
            await ctx.send(content="Wrong channel. Please use `#slots`.",delete_after=5)
            return
        embed = discord.Embed(title='Slots commands',
                              description="A bot for The Democratic People's Republic of VorTeic.\nType `!help <category>` for more info on a category.\n[] Are optional.\n<> Are required.\n() Are aliases",
                              colour=0xFFAA00)
        embed.set_author(name='The Dealer',
                              icon_url='https://cdn.discordapp.com/avatars/421718079265964032/7805693d09954641ab8bbb51f3582f07.png')

        embed.add_field(name='Aliases',
                        value='`Slots`,`slots`,`Slot`,`slot`,`S`,`s`')
        embed.add_field(name='!s',
                        value='Base command.')
        embed.add_field(name='!s list',
                        value='Lists all the avlaiable slots.')
        embed.add_field(name='!s <Slot> <Bet>',
                        value='Plays one of the slots. Bet is the amout you wish to bet. Slot is the slot you wish to play on. They can be found in `!s list`. All slots can be written as such for 25:75...\n25:75\n25/75\nTwentyfiveSeventyfive\ntwentyfiveseventyfive\ntfsf')
        embed.set_footer(text='DPRoVT',
                         icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='&&Displaying members category help&&', embed=embed)

    @helps.command(name='pontoon',aliases=['Pontoon','Pt','pt'])
    async def pontoon(self,ctx):
        if ctx.channel.id != 425370985626075137:
            await ctx.message.delete()
            await ctx.send(content="Wrong channel. Please use `#pontoon`.",delete_after=5)
            return
        embed = discord.Embed(title='Pontoon Commands',
                              description="A bot for The Democratic People's Republic of VorTeic.\nType `!help <category>` for more info on a category.\n[] Are optional.\n<> Are required.\n() Are aliases",
                              colour=0xFFAA00)
        embed.set_author(name='The Dealer',
                        icon_url='https://cdn.discordapp.com/avatars/421718079265964032/7805693d09954641ab8bbb51f3582f07.png')

        embed.add_field(name='Aliases',
                        value='`Pontoon`,`pontoon`,`Pt`,`pt`')
        embed.add_field(name='Current access to commands',
                        value='`beta`')
        embed.add_field(name='!pt',
                        value="Base Pontoon command.")
        embed.add_field(name='!pt howto',
                        value='Explains how to play the game via DM.')
        embed.add_field(name='!pt host <setup>',
                        value='Sets you up to host a game of pontoon.')
        embed.add_field(name='!pt setup',
                        value='Lists all the current setup types for hosting a game.')
        embed.add_field(name='!pt join <host>',
                        value="Joins a host's game. You must mention the host or the bot won't know which game to add you to! You cannot take part in more than one game at a time.")
        embed.add_field(name='!pt start',
                        value='Begins the current game. Will not work if there is only one person in the game. Host only command.')
        embed.add_field(name='!pt bet <amount>',
                        value='When it is your turn to bet, you will be asked to run this command. You may only bet when it is your turn in the game.')
        embed.add_field(name='!pt twist',
                        value='When it is your turn, you can run this command to be twisted a card.')
        embed.add_field(name='!pt buy <amount>',
                        value='&&beta only!&&\nWhen it is your turn, you can run this command to buy a card.')
        embed.add_field(name='!pt stick',
                        value='When it is your turn, you can run this command to stick with your current cards.')
        embed.add_field(name='!pt kick <member>',
                        value='&&beta only&&\nKicks a member from your game. Their bets will be returned. Host only command')
        embed.add_field(name='!pt stop',
                        value='Stops the game you are currently hosting. Host only command.')
        embed.add_field(name='!pt leave',
                        value='Leaved the table you are part of. You cannot leave a game if you are hosting it.')
        embed.set_footer(text='DPRoVT',
                         icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='&&Displaying Pontoon commands&&', embed=embed)

    @helps.command(name='mod',aliases=['Mod','MOD'])
    @commands.has_any_role('Bot Mod')
    async def modshelp(self,ctx):
        embed = discord.Embed(title='Bot Owner Commands',
                              description='A basic discord bot for i G o d l i k e.\nType `!help <category>` for more info on a category.\n[] Are optional.\n<> Are required.\n() Are aliases',
                              colour=0x6600AA)
        embed.set_author(name='uGodlike',
                        icon_url='https://cdn.discordapp.com/avatars/404658318431485953/2b96cd8e226e84de327b0c7dc4ec499c.png?size=1024')

        embed.add_field(name='Aliases',
                        value='`MOD`,`Mod`,`mod`')
        embed.add_field(name='!raff draw',
                        value='Draws a winner from the current raffle and then deletes the user from the raffle.')
        embed.add_field(name='!raff clear',
                        value='Deletes all members currently entered into the raffle.')
        embed.add_field(name='!xpclear',
                        value='Deletes __all__ xp information.\nForever! No recovery/backup of this data!')
        embed.add_field(name='!xpadd <xp to add> [user]',
                        value='Adds XP to the user.\nUse a !xptake to take XP away.\nIf user is None then the person who sent the command is selected.')
        embed.add_field(name='!xpranking [user]',
                        value='Checks to see if the user has more xp than any of the users above them.\nThey will then be moved accordingly.')
        embed.add_field(name='!art <role name> <user> [time in mins]',
                        value='Adds a role for an amount of time.\nrole name is just the name of the role. It does not need to be tagged.\nuser is the user. They do need to be tagged.\nIf time is unspecified then it will permenantly add the role.')
        embed.add_field(name='!rrt <role name> <user> [time in mins]',
                        value='Removes a role for an amount of time.\nrole name is just the name of the role. It does not need to be tagged. If the role is two works you need to surround it in "".\nuser is the user. They do need to be tagged.\nIf time is unspecified then it will permenantly remove the role.')
        embed.set_footer(text='i G o d l i k e',
                         icon_url='https://cdn.discordapp.com/icons/404654967350362112/78d3c8c87474924f6326401b57e9bc32.jpg?size=1024')

        await ctx.send(content='&&Displaying owner only commands&&', embed=embed, delete_after=10)
        await ctx.message.delete()

    @helps.command(name='Leaderboard',aliases=['lb','leaderboard','LB'])
    async def leaderboards(self, ctx):
        embed = discord.Embed(title='Leaderboard commands.',
                              description='A basic discord bot for i G o d l i k e.\nType `!help <category>` for more info on a category.\n[] Are optional.\n<> Are required.\n() Are aliases',
                              colour=0xFFEE22)
        embed.set_author(name='uGodlike',
                              icon_url='https://cdn.discordapp.com/avatars/404658318431485953/2b96cd8e226e84de327b0c7dc4ec499c.png?size=1024')

        embed.add_field(name='Aliases',
                        value='`Leaderboard`,`leaderboard`,`LB`,`lb`')
        embed.add_field(name='!lb',
                        value='Coming soon...')
        embed.set_footer(text='i G o d l i k e',
                        icon_url='https://cdn.discordapp.com/icons/404654967350362112/78d3c8c87474924f6326401b57e9bc32.jpg?size=1024')

        await ctx.send(content='&&Displaying leaderboard category help&&', embed=embed)

    @helps.command(name='Raffle',aliases=['rf','raffle','RF'])
    async def Raffles(self, ctx):
        embed = discord.Embed(title='Raffle commands.',
                              description='A basic discord bot for i G o d l i k e.\nType `!help <category>` for more info on a category.\n[] Are optional.\n<> Are required.\n() Are aliases',
                              colour=0xCC0011)
        embed.set_author(name='uGodlike',
                              icon_url='https://cdn.discordapp.com/avatars/404658318431485953/2b96cd8e226e84de327b0c7dc4ec499c.png?size=1024')

        embed.add_field(name='Aliases',
                        value='`Raffle`,`raffle`,`RF`,`rf`')
        embed.add_field(name='&&Disclaimer!&&',
                        value="There may not neccessarily be a raffle going on currently.\nIf this is the case all raffle commands won't work.")
        embed.add_field(name='!raffle info',
                        value='Displays information about the current raffle and the prize(s).')
        embed.add_field(name='!raffle join',
                        value='Adds you to the current raffle.\nYou can only be entered once per raffle.')
        embed.add_field(name='!raffle leave',
                        value='Removes you from the current raffle.\nYou may rejoin by typing `!raffle join`.')
        embed.set_footer(text='i G o d l i k e',
                        icon_url='https://cdn.discordapp.com/icons/404654967350362112/78d3c8c87474924f6326401b57e9bc32.jpg?size=1024')

        await ctx.send(content='&&Displaying raffle category help&&', embed=embed)

    @helps.command(name='XP',aliases=['xp','experience','Experience'])
    async def xphelp(self, ctx):
        embed = discord.Embed(title='XP commands.',
                              description='A basic discord bot for i G o d l i k e.\nType `!help <category>` for more info on a category.\n[] Are optional.\n<> Are required.\n() Are aliases',
                              colour=0x66CCDD)
        embed.set_author(name='uGodlike',
                              icon_url='https://cdn.discordapp.com/avatars/404658318431485953/2b96cd8e226e84de327b0c7dc4ec499c.png?size=1024')

        embed.add_field(name='Aliases',
                        value='`XP`,`xp`,`Experience`,`experience`')
        embed.add_field(name='!xp [member]',
                        value='Displays the xp for that user.\nIf no user is mentioned then your xp will be displayed.')
        embed.add_field(name='!xprank [integer]',
                        value='Displays the user at that rank.\nIf no user is selected it just show the top user.')
        embed.set_footer(text='i G o d l i k e',
                        icon_url='https://cdn.discordapp.com/icons/404654967350362112/78d3c8c87474924f6326401b57e9bc32.jpg?size=1024')

        await ctx.send(content='&&Displaying leaderboard category help&&', embed=embed)
'''

def setup(bot):
    bot.add_cog(HelpCog(bot))
