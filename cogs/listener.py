import discord
from discord.ext import commands
import pickle
import random
import time


"""A simple cog example with simple commands. Showcased here are some check decorators, and the use of events in cogs.

For a list of inbuilt checks:
http://dischttp://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#checksordpy.readthedocs.io/en/rewrite/ext/commands/api.html#checks

You could also create your own custom checks. Check out:
https://github.com/Rapptz/discord.py/blob/master/discord/ext/commands/core.py#L689

For a list of events:
http://discordpy.readthedocs.io/en/rewrite/api.html#event-reference
http://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#event-reference
"""

class Listener:
    """SimpleCog"""

    def __init__(self, bot):
        self.bot = bot

    #async def on_member_ban(self, guild, user):
        """Event Listener which is called when a user is banned from the guild.
        For this example I will keep things simple and just print some info.
        Notice how because we are in a cog class we do not need to use @bot.event

        For more information:
        http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_member_ban

        Check above for a list of events.
        """

        #print(f'{user.name}-{user.id} was banned from {guild.name}-{guild.id}')

    async def on_message(self, ctx):
        if ctx.guild == None:
            return
        if ctx.channel.id == 436600674017476610:
            memberRole = (discord.utils.find(lambda r: r.id == 436602828593561610, ctx.guild.roles))
            await ctx.author.add_roles(memberRole)
        if ctx.guild.id == 454312815436496896 or 472863145992650792:
            message = ctx.content.lower()
            if "cookie" in message or '\U0001F36A' in message or "cookies" in message:
                await ctx.add_reaction('\U0001F36A')
        if ctx.guild.id == 462842304638484481:
            #id XP XPNow lvl time
            if ctx.author.bot == True:
                return
            XPList = []
            XPList = pickle.load(open('g5xp.data', 'rb'))
            added = False
            addedXP = random.randint(400000,500000)
            if ctx.channel.id in [484445582937686016, 481019924748304385, 463450775264296992]:
                return
            for y in range(len(XPList)):
                if XPList[y]['id'] == (ctx.author.id):
                    if (time.time()) < (XPList[y]['timeOfNextXpEarn']):
                        return
                    added = True
                    placement = y
                    break
            if added == True:
                XPList[placement]['xp'] += addedXP
                XPList[placement]['timeOfNextXpEarn'] = time.time() + 60
            elif added == False:
                XPList.append({'id':ctx.author.id,'xp':addedXP, 'timeOfNextXpEarn':time.time()+60})
            def getKey(item):
                return item['xp']
            XPList = sorted(XPList,reverse=True,key=getKey)
            pickle.dump(XPList, open('g5xp.data','wb'))
            if added == False:
                return

            if ctx.author.id == 458611812737482762:
                return

            #Add roles
            if XPList[placement]['xp'] >= 15000000 and XPList[placement]['xp'] < 30000000 and discord.utils.find(lambda r: r.id == 484747494975340554, ctx.guild.roles) not in ctx.author.roles:
                await ctx.author.add_roles(discord.utils.find(lambda r: r.id == 484747494975340554, ctx.guild.roles))
                await ctx.channel.send(f"Congratualtions {ctx.author.mention}! The marines want you so bad you've earnt a 15 Million bounty! You now have the title of `Bandit`!")

            elif XPList[placement]['xp'] >= 30000000 and XPList[placement]['xp'] < 50000000 and discord.utils.find(lambda r: r.id == 484716087888445460, ctx.guild.roles) not in ctx.author.roles:
                await ctx.author.add_roles(discord.utils.find(lambda r: r.id == 484716087888445460, ctx.guild.roles))
                await ctx.channel.send(f"Congratualtions {ctx.author.mention}! The marines want you so bad you've earnt a 30 Million bounty! You now have the title of `Bounty Hunter`!")
                await ctx.author.remove_roles(discord.utils.find(lambda r: r.id == 484747494975340554, ctx.guild.roles))

            elif XPList[placement]['xp'] >= 50000000 and XPList[placement]['xp'] < 100000000 and discord.utils.find(lambda r: r.id == 484715672417468438, ctx.guild.roles) not in ctx.author.roles:
                await ctx.author.add_roles(discord.utils.find(lambda r: r.id == 484715672417468438, ctx.guild.roles))
                await ctx.channel.send(f"Congratualtions {ctx.author.mention}! The marines want you so bad you've earnt a 50 Million bounty! You now have the title of `Rookie`!")
                await ctx.author.remove_roles(discord.utils.find(lambda r: r.id == 484716087888445460, ctx.guild.roles))

            elif XPList[placement]['xp'] >= 100000000 and XPList[placement]['xp'] < 200000000 and discord.utils.find(lambda r: r.id == 484716087271882753, ctx.guild.roles) not in ctx.author.roles:
                await ctx.author.add_roles(discord.utils.find(lambda r: r.id == 484716087271882753, ctx.guild.roles))
                await ctx.channel.send(f"Congratualtions {ctx.author.mention}! The marines want you so bad you've earnt a 100 Million bounty! You now have the title of `Grand Line Rookie`!")
                await ctx.author.remove_roles(discord.utils.find(lambda r: r.id == 484715672417468438, ctx.guild.roles))

            elif XPList[placement]['xp'] >= 200000000 and XPList[placement]['xp'] < 300000000 and discord.utils.find(lambda r: r.id == 484717400743215104, ctx.guild.roles) not in ctx.author.roles:
                await ctx.author.add_roles(discord.utils.find(lambda r: r.id == 484717400743215104, ctx.guild.roles))
                await ctx.channel.send(f"Congratualtions {ctx.author.mention}! The marines want you so bad you've earnt a 200 Million bounty! You now have the title of `Supernova`!")
                await ctx.author.remove_roles(discord.utils.find(lambda r: r.id == 484716087271882753, ctx.guild.roles))

            elif XPList[placement]['xp'] >= 300000000 and XPList[placement]['xp'] < 500000000 and discord.utils.find(lambda r: r.id == 484716090090323968, ctx.guild.roles) not in ctx.author.roles:
                await ctx.author.add_roles(discord.utils.find(lambda r: r.id == 484716090090323968, ctx.guild.roles))
                await ctx.channel.send(f"Congratualtions {ctx.author.mention}! The marines want you so bad you've earnt a 300 Million bounty! You now have the title of `Headliner`!")
                await ctx.author.remove_roles(discord.utils.find(lambda r: r.id == 484717400743215104, ctx.guild.roles))

            elif XPList[placement]['xp'] >= 500000000 and XPList[placement]['xp'] < 750000000 and discord.utils.find(lambda r: r.id == 484715505173790720, ctx.guild.roles) not in ctx.author.roles:
                await ctx.author.add_roles(discord.utils.find(lambda r: r.id == 484715505173790720, ctx.guild.roles))
                await ctx.channel.send(f"Congratualtions {ctx.author.mention}! The marines want you so bad you've earnt a 500 Million bounty! You now have the title of `Warlord`!")
                await ctx.author.remove_roles(discord.utils.find(lambda r: r.id == 484716090090323968, ctx.guild.roles))

            elif XPList[placement]['xp'] >= 750000000 and XPList[placement]['xp'] < 1000000000 and discord.utils.find(lambda r: r.id == 484715772434841609, ctx.guild.roles) not in ctx.author.roles:
                await ctx.author.add_roles(discord.utils.find(lambda r: r.id == 484715772434841609, ctx.guild.roles))
                await ctx.channel.send(f"Congratualtions {ctx.author.mention}! The marines want you so bad you've earnt a 750 Million bounty! You now have the title of `Calamity`!")
                await ctx.author.remove_roles(discord.utils.find(lambda r: r.id == 484715505173790720, ctx.guild.roles))
                
            elif XPList[placement]['xp'] >= 1000000000 and XPList[placement]['xp'] < 2000000000 and discord.utils.find(lambda r: r.id == 484716086562914334, ctx.guild.roles) not in ctx.author.roles:
                await ctx.author.add_roles(discord.utils.find(lambda r: r.id == 484716086562914334, ctx.guild.roles))
                await ctx.channel.send(f"Congratualtions {ctx.author.mention}! The marines want you so bad you've earnt a 1 Billion bounty! You now have the title of `Yonkou's Right Hand`!")
                await ctx.author.remove_roles(discord.utils.find(lambda r: r.id == 484715772434841609, ctx.guild.roles))
                
            elif XPList[placement]['xp'] >= 2000000000 and XPList[placement]['xp'] < 4000000000 and discord.utils.find(lambda r: r.id == 484715771809890315, ctx.guild.roles) not in ctx.author.roles:
                await ctx.author.add_roles(discord.utils.find(lambda r: r.id == 484715771809890315, ctx.guild.roles))
                await ctx.channel.send(f"Congratualtions {ctx.author.mention}! The marines want you so bad you've earnt a 2 Billion bounty! You now have the title of `Rocks Legends`!")
                await ctx.author.remove_roles(discord.utils.find(lambda r: r.id == 484716086562914334, ctx.guild.roles))
                
            elif XPList[placement]['xp'] >= 4000000000 and XPList[placement]['xp'] < 5000000000 and discord.utils.find(lambda r: r.id == 484715769146376192, ctx.guild.roles) not in ctx.author.roles:
                await ctx.author.add_roles(discord.utils.find(lambda r: r.id == 484715769146376192, ctx.guild.roles))
                await ctx.channel.send(f"Congratualtions {ctx.author.mention}! The marines want you so bad you've earnt a 4 Billion bounty! You now have the title of `Gold Lion`!")
                await ctx.author.remove_roles(discord.utils.find(lambda r: r.id == 484715771809890315, ctx.guild.roles))
                
            elif XPList[placement]['xp'] >= 5000000000 and XPList[placement]['xp'] < 7500000000 and discord.utils.find(lambda r: r.id == 484715766617473024, ctx.guild.roles) not in ctx.author.roles:
                await ctx.author.add_roles(discord.utils.find(lambda r: r.id == 484715766617473024, ctx.guild.roles))
                await ctx.channel.send(f"Congratualtions {ctx.author.mention}! The marines want you so bad you've earnt a 5 Billion bounty! You now have the title of `Dark King`!")
                await ctx.author.remove_roles(discord.utils.find(lambda r: r.id == 484715769146376192, ctx.guild.roles))
                
            elif XPList[placement]['xp'] >= 7500000000 and XPList[placement]['xp'] < 1000000000 and discord.utils.find(lambda r: r.id == 484715763240927233, ctx.guild.roles) not in ctx.author.roles:
                await ctx.author.add_roles(discord.utils.find(lambda r: r.id == 484715763240927233, ctx.guild.roles))
                await ctx.channel.send(f"Congratualtions {ctx.author.mention}! The marines want you so bad you've earnt a 7.5 Billion bounty! You now have the title of `World's Strongest Man`!")
                await ctx.author.remove_roles(discord.utils.find(lambda r: r.id == 484715766617473024, ctx.guild.roles))
                
            elif XPList[placement]['xp'] >= 10000000000 and discord.utils.find(lambda r: r.id == 484715770694074368, ctx.guild.roles) not in ctx.author.roles:
                await ctx.author.add_roles(discord.utils.find(lambda r: r.id == 484715770694074368, ctx.guild.roles))
                await ctx.channel.send(f"Congratualtions {ctx.author.mention}! The marines want you so bad you've earnt a 10 Billion bounty! You now have the epic title of __`☠️Most Wanted☠ 10 Billion Bounty`__!")
                await ctx.author.remove_roles(discord.utils.find(lambda r: r.id == 484715763240927233, ctx.guild.roles))

            elif XPList[placement]['xp'] >= 13000000000 and discord.utils.find(lambda r: r.id == 474563999477006336, ctx.guild.roles) not in ctx.author.roles:
                await ctx.author.add_roles(discord.utils.find(lambda r: r.id == 474563999477006336, ctx.guild.roles))
                await ctx.channel.send(f"Congratualtions {ctx.author.mention}! The marines want you so bad you've earnt a 13 Billion bounty! You now have the legendary title of __**`Pirate King Buggy`**__!")
                await ctx.author.remove_roles(discord.utils.find(lambda r: r.id == 484715770694074368, ctx.guild.roles))
                
    async def on_message_delete(self, ctx):
        if ctx.channel.id == 436600674017476610:
            memberRole = (discord.utils.find(lambda r: r.id == 436602828593561610, ctx.guild.roles))
            await ctx.author.remove_roles(memberRole)
            await ctx.delete()

    async def on_member_join(self,member):
        if member.guild.id == 441635774232788993:
            memberRole = (discord.utils.find(lambda r: r.id == 442410209747664898, member.guild.roles))
            await member.add_roles(memberRole)
            rankRole = (discord.utils.find(lambda r: r.id == 444487826126536717, member.guild.roles))
            await member.add_roles(rankRole)
            locationRole = (discord.utils.find(lambda r: r.id == 444616783052275722, member.guild.roles))
            await member.add_roles(locationRole)
            hobbiesRole = (discord.utils.find(lambda r: r.id == 445310755584081920, member.guild.roles))
            await member.add_roles(hobbiesRole)
            gamesRole = (discord.utils.find(lambda r: r.id == 441994780742909953, member.guild.roles))
            await member.add_roles(gamesRole)
            genderRole = (discord.utils.find(lambda r: r.id == 4453096882346960128, member.guild.roles))
            await member.add_roles(genderRole)
            XPList = []
            XPList = pickle.load(open('nwxp.data', 'rb'))
            for y in range(len(XPList)):
                if XPList[y][0] == (member.id):
                    return
            XPList.append([member.id, 0, 0, 0, 0])
            def getKey(item):
                return item[1]
            XPList = sorted(XPList,reverse=True,key=getKey)
            pickle.dump(XPList, open('nwxp.data','wb'))
        if member.guild.id == 405926267050000384:
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
                CPList.append([member.id,member.name,0])
            def getKey(item):
                return item[1]
            CPList = sorted(CPList,reverse=True,key=getKey)
            pickle.dump(CPList, open('CP.data','wb'))
            print(f"New player\n{CPList}")

    async def on_guild_join(self, guild):
        #Added to setup
        guilds = []
        guilds = pickle.load(open("guilds.data", "rb"))
        guilds.append([guild.id, [False], [False], [False], [False, []]])
        print("Server Added")
        pickle.dump(guilds, open("guilds.data", "wb"))

    async def on_guild_remove(self, guild):
        #Remove from setup
        guilds = []
        guilds = pickle.load(open("guilds.data", "rb"))
        for a in range(len(guilds)):
            if guilds[a][0] == guild.id:
                guilds.pop(a)
        #index out of range
        print("Server Removed")
        pickle.dump(guilds, open("guilds.data", "wb"))

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(Listener(bot))
