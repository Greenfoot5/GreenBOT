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

def LevelSet(xp):
    lvl=0
    while xp >= lvls_xp[lvl]:
        lvl += 1
    return lvl

def XPRem(xp):
    lvl=0
    while xp >= lvls_xp[lvl]:
        lvl += 1
    xp -= lvls_xp[lvl]
    return -xp

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
#User Coins (time.time())OfNextCoinClaim Wins Loses
class SetupCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="setup")
    #@commands.has_permissions(manage_guild=True)
    async def setup(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("You haven't sent a setup subcommand.")

    @setup.command(name="reset")
    #@commands.has_permissions(administrator=True)
    async def SetupReset(self,ctx):
        guilds = []
        guilds = pickle.load(open("guilds.data", "rb"))
        for a in range(len(guilds)):
            if guilds[a][0] == ctx.guild.id:
                guilds[a] = [ctx.guild.id, [False], [False], [False], [False, []]]
                pickle.dump(guilds, open("guilds.data", "wb"))
                print("Server Reset")
                await ctx.send("Server Setup Reset")
                return
        guilds.append([guild.id, [False], [False], [False], [False, []]])
        print("Server Added")
        pickle.dump(guilds, open("guilds.data", "wb"))

    @commands.command("first")
    async def FirstTime(self,ctx):
        await ctx.send("https://scrapbox.io/GreenBOT/First_Time%3F_Check_Here!\nImprovements <:soon:233642257817927680>.")

    @setup.command(name="enable")
    async def SetupEnable(self,ctx,module:str=None):
        module = module.lower()
        guilds = []
        guilds = pickle.load(open("guilds.data", "rb"))
        for a in range(len(guilds)):
            if guilds[a][0] == ctx.guild.id:
                if module == "misc":
                    guilds[a][1] = [True]
                elif module == "trivia":
                    guilds[a][2] = [True]
                elif module == "members":
                    guilds[a][3] = [True]
                elif module == None:
                    await ctx.send("Please select a module. The avaliable modules are `misc`,`trivia`,`members`.")
                    return
                else:
                    await ctx.send("That isn't an avaliable module. The avaliable modules are `misc`, `trivia`, `members`.")
                    return
                await ctx.send(f"Enabled module `{module}`")
                pickle.dump(guilds, open("guilds.data", "wb"))
                return
        await ctx.send("You have not run `&&setup reset` yet.")

    @setup.command(name="disable")
    async def SetupDisable(self,ctx,module:str=None):
        module = module.lower()
        guilds = []
        guilds = pickle.load(open("guilds.data", "rb"))
        for a in range(len(guilds)):
            if guilds[a][0] == ctx.guild.id:
                if module == "misc":
                    guilds[a][1] = [False]
                elif module == "trivia":
                    guilds[a][2] = [False]
                elif module == "members":
                    guilds[a][3] = [False]
                elif module == None:
                    await ctx.send("Please select a module. The avaliable modules are `misc`,`trivia`,`members`.")
                    return
                else:
                    await ctx.send("That isn't an avaliable module. The avaliable modules are `misc`, `trivia`, `members`.")
                    return
                await ctx.send(f"Disabled module `{module}`.")
                pickle.dump(guilds, open("guilds.data", "wb"))
                return
        await ctx.send("You have not run `&&setup reset` yet.")

    @setup.command('fix')
    @commands.is_owner()
    async def SetupFix(self, ctx):
        #Debug
        #import ipdb; ipdb.set_trace()
        guilds = []
        guilds = pickle.load(open("guilds.data", "rb"))
        guildsList = self.bot.guilds
        for y in range(len(guilds)):
            for x in range(0,len(guildsList)):
                if guildsList[x].id == guilds[y][0]:
                    guildsList.pop(x)
                    break
        for z in range(len(guildsList)):
            guilds.append([guildsList[z].id, [False], [False], [False], [False, []]])
        print(len(guilds))
        pickle.dump(guilds, open("guilds.data", "wb"))

        
# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(SetupCog(bot))
    random.seed()
