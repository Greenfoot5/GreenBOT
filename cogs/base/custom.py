import discord
from discord.ext import commands
import pickle
import asyncio
import cogs.base.checks as chec

class Custom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.modules = ['misc','mindustry']

    #Initial Command
    @commands.group(name='setup')
    @commands.has_permissions(manage_guild=True)
    async def setup(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Please refer to the documentation for how to use this command.")

    #Change/view the prefix
    @setup.command(name='prefix')
    async def set_prefix(self,ctx,newPrefix=None):
        prefixData = {}
        prefixData = pickle.load(open('data/prefix.data', 'rb'))
        try:
            prefix = prefixData[f'{ctx.guild.id}']
        except KeyError:
            prefix = ['b!']
        if newPrefix == None:
            await ctx.send(f"Your current prefix is `{prefix[0]}`.")
            return
        prefixData[f'{ctx.guild.id}'] = [f'{newPrefix}']
        await ctx.send(f"Your new prefix is `{newPrefix}`")
        pickle.dump(prefixData, open('data/prefix.data', 'wb'))

    @setup.command(name='enable')
    async def enable_module(self,ctx,module=None):
        if module not in self.modules or module == None:
            await ctx.send("Please select a valid module to enable. Check the docs to see toggleable modules.")
            return
        serverData = {}
        #serverData = pickle.load(open('data/serverInfo.data', 'rb'))
        try:
            if serverData[f'{ctx.guild.id}'][module] == True:
                await ctx.send("You can't enable an enabled module.")
                return
        except KeyError:
            serverData[f'{ctx.guild.id}'] = {'misc':True,'mindustry':False}
        serverData[f'{ctx.guild.id}'][module] = True
        pickle.dump(serverData, open('data/serverInfo.data', 'wb'))
        await ctx.send("Module enabled.")

    @setup.command(name='disable')
    async def disable_module(self,ctx,module=None):
        if module not in self.modules or module == None:
            await ctx.send("Please select a valid module to enable. Check the docs to see toggleable modules.")
            return
        serverData = {}
        #serverData = pickle.load(open('data/serverInfo.data', 'rb'))
        try:
            if serverData[f'{ctx.guild.id}'][module] == False:
                await ctx.send("So, you want to... ok... disable a ... carry the one... add 7... nope. I don't get it.")
                return
        except KeyError:
            serverData[f'{ctx.guild.id}'] = {'misc':True,'mindustry':False}
        serverData[f'{ctx.guild.id}'][module] = False
        pickle.dump(serverData, open('data/serverInfo.data', 'wb'))
        await ctx.send("Module disabled.")
        

def setup(bot):
    bot.add_cog(Custom(bot))
