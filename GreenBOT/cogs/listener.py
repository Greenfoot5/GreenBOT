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

lvls_xp = [0,500,1500,2500,5000,10000,25000,50000]
ranks = [0,444489213141057546,444487988827914253,446382522041892888,444489049751945216,444489418355638282,444490040543019018,444490176840859669]

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
        if ctx.guild.id == 454312815436496896:
            message = ctx.content.lower()
            if "cookie" in message or '\U0001F36A' in message or "cookies" in message:
                await ctx.add_reaction('\U0001F36A')
        if ctx.guild.id == 441635774232788993:
            #id XP XPNow lvl time
            if ctx.author.bot == True:
                return
            XPList = []
            XPList = pickle.load(open('nwxp.data', 'rb'))
            added = False
            addedXP = random.randint(5,15)
            for y in range(len(XPList)):
                if XPList[y][0] == (ctx.author.id):
                    if (time.time()) < (XPList[y][4]):
                        return
                    added = True
                    placement = y
                    break
            if added == True:
                XPList[placement][1] += addedXP
                XPList[placement][2] += addedXP
                XPList[placement][4] = time.time() + 60
                if XPList[placement][2] > lvls_xp[XPList[placement][3]]:
                    XPList[placement][2] -= lvls_xp[XPList[placement][3]]
                    XPList[placement][3] += 1
                    await ctx.channel.send(f'{ctx.author.mention} has ranked up! The are now at rank `{discord.utils.find(lambda r: r.id == ranks[XPList[placement][3]], ctx.guild.roles)}`')
                    await ctx.author.add_roles(discord.utils.find(lambda r: r.id == ranks[XPList[placement][3]], ctx.guild.roles))
                    if XPList[placement][3] != 1:
                        await ctx.author.remove_roles(discord.utils.find(lambda r: r.id == ranks[XPList[placment][3]-1], ctx.guild.roles))
            def getKey(item):
                return item[1]
            XPList = sorted(XPList,reverse=True,key=getKey)
            pickle.dump(XPList, open('nwxp.data','wb'))

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
