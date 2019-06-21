import discord
from discord.ext import commands
import pickle
import asyncio

'''
Init
'''

defaults = {'misc':True,'mindustry':False}
class ModuleDisabled(commands.CheckFailure):
    pass

class ModuleNotEnabled(commands.CheckFailure):
    pass

class NotInServer(commands.CheckFailure):
    pass

def is_not_owner():
    async def predicate(ctx):
        return ctx.author.id != 270190067354435584
    return commands.check(predicate)

def is_module_enabled(module:str):
    async def predicate(ctx):
        serverData = {}
        serverData = pickle.load(open('data/serverInfo.data', 'rb'))
        try:
            moduleStatus = serverData[f'{ctx.guild.id}'][f'{module}']
            if moduleStatus == True:
                return True
            else:
                raise ModuleDisabled("That command is disabled in the server.")
        except KeyError:
            if defaults[module] == False:
                raise ModuleNotEnabled("That command hasn't been enabled in this server.")
            else:
                return True
    return commands.check(predicate)

def i_ss(server:str):
    async def predicate(ctx):
        if server == 'FR' and ctx.guild.id == 405926267050000384:
            return True
        elif server == 'FR':
            raise NotInServer("You can't do that here.")
        elif server == 'G5' and ctx.guild.id == 462842304638484481:
            return True
        elif server == 'G5':
            raise NotInServer("You can't do that here.")
        elif server == 'PPTF' and ctx.guild.id == 541702393549684780:
            return True
        elif server == 'PPTF':
            raise NotInServer("You can't do that here.")
        elif server == 'UnOMSL' and ctx.guild.id == 454312815436496896:
            return True
        elif server == 'UnOMSL':
            raise NotInServer("You can't do that here.")
        else:
            print("Invalid server")
    return commands.check(predicate)


