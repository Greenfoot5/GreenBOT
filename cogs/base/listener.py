import discord
from discord.ext import commands
import pickle
import random
import time
import datetime


"""A simple cog example with simple commands. Showcased here are some check decorators, and the use of events in cogs.

For a list of inbuilt checks:
http://dischttp://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#checksordpy.readthedocs.io/en/rewrite/ext/commands/api.html#checks

You could also create your own custom checks. Check out:
https://github.com/Rapptz/discord.py/blob/master/discord/ext/commands/core.py#L689

For a list of events:
http://discordpy.readthedocs.io/en/rewrite/api.html#event-reference
http://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#event-reference
"""

class Listener(commands.Cog):
    """SimpleCog"""

    def __init__(self, bot):
        self.bot = bot
        #{serverID:{messageID:{stars:int,users:[],embed:int}}}
        self.messages = {}

    #async def on_member_ban(self, guild, user):
        """Event Listener which is called when a user is banned from the guild.
        For this example I will keep things simple and just print some info.
        Notice how because we are in a cog class we do not need to use @bot.event

        For more information:
        http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_member_ban

        Check above for a list of events.
        """

        #print(f'{user.name}-{user.id} was banned from {guild.name}-{guild.id}')

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.channel.id == 436600674017476610:
            memberRole = (discord.utils.find(lambda r: r.id == 436602828593561610, ctx.guild.roles))
            await ctx.author.add_roles(memberRole)
        message = ctx.content.lower()
        if ("cookie" in message or '\U0001F36A' in message or "cookies" in message) and ctx.author != self.bot.user:
            cookies = pickle.load(open('data/cookies.data', 'rb'))
            try:
                await ctx.add_reaction('\U0001F36A')
                cookies['accepted'] += 1
            except discord.errors.Forbidden:
                cookies['denied'] += 1
            pickle.dump(cookies, open('data/cookies.data','wb'))
        if ctx.guild == None:
            return
        if ctx.guild.id == 462842304638484481:
            #id XP XPNow lvl time
            if ctx.author.bot == True:
                return
            XPList = []
            XPList = pickle.load(open('data/g5xp.data', 'rb'))
            added = False
            addedXP = random.randint(200000,300000)
            if ctx.channel.id in [484445582937686016, 481019924748304385, 463450775264296992, 499700569972146196]:
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
            pickle.dump(XPList, open('data/g5xp.data','wb'))

    @commands.Cog.listener()
    async def on_message_delete(self, ctx):
        if ctx.channel.id == 436600674017476610:
            memberRole = (discord.utils.find(lambda r: r.id == 436602828593561610, ctx.guild.roles))
            await ctx.author.remove_roles(memberRole)
            await ctx.delete()

    @commands.Cog.listener()
    async def on_reaction_add(self,reaction,user):
        if str(reaction) == "⭐":
            if reaction.message.guild.id == 565170864128000000:
                sentMessage = False
                try:
                    messageStarred = self.messages[str(reaction.message.guild.id)]
                    try:
                        if user.id not in self.messages[str(reaction.message.guild.id)][str(reaction.message.id)]['users']:
                            self.messages[str(reaction.message.guild.id)][str(reaction.message.id)]['stars'] += 1
                            self.messages[str(reaction.message.guild.id)][str(reaction.message.id)]['users'].append(user.id)
                        sentMessage = True
                    except KeyError:
                        print('Message')
                        self.messages[str(reaction.message.guild.id)][str(reaction.message.id)] = {'stars':1,'users':[user.id]}
                except KeyError:
                    print('Server')
                    self.messages[str(reaction.message.guild.id)] = {f'{reaction.message.id}':{'stars':1,'users':[user.id]}}

                starChannel = reaction.message.guild.get_channel(565280526047379472)

                if sentMessage == False:
                    embed = discord.Embed(description=f"⭐ {self.messages[str(reaction.message.guild.id)][str(reaction.message.id)]['stars']}",
                                          timestamp=datetime.datetime.utcfromtimestamp(time.time() + 3600),
                                          colour=0xf6b035)
                    
                    embed.set_author(name=reaction.message.author.display_name,
                                     icon_url=reaction.message.author.avatar_url_as(format='png'))

                    embed.set_footer(text=reaction.message.guild.name,
                                     icon_url=reaction.message.guild.icon_url_as(format='png'))

                    embed.add_field(name="Content",
                                    value=reaction.message.content)
                    embed.add_field(name="Jump!",
                                    value=reaction.message.jump_url)

                    starredEmbed = await starChannel.send(embed=embed)
                    self.messages[str(reaction.message.guild.id)][str(reaction.message.id)]["embed"] = starredEmbed.id
                else:
                    sentMessage = await starChannel.fetch_message(self.messages[str(reaction.message.guild.id)][str(reaction.message.id)]["embed"])
                    print(sentMessage.embeds[0].timestamp)

                    embed = sentMessage.embeds[0]
                    embed.description = f"⭐ {self.messages[str(reaction.message.guild.id)][str(reaction.message.id)]['stars']}"

                    await sentMessage.edit(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_remove(self,reaction,user):
        if str(reaction) == "⭐":
            try:
                if user.id in self.messages[str(reaction.message.guild.id)][str(reaction.message.id)]['users']:
                    self.messages[str(reaction.message.guild.id)][str(reaction.message.id)]['stars'] -= 1
                    self.messages[str(reaction.message.guild.id)][str(reaction.message.id)]['users'].remove(user.id)
                    if self.messages[str(reaction.message.guild.id)][str(reaction.message.id)]['stars'] == 0:
                        print("coming soon")
            except KeyError:
                return
                

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(Listener(bot))
