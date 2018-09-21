import discord
from discord.ext import commands
import asyncio
import websockets
import base64
import random
import colorsys
import time
import pickle

class MindustryCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='Mindustry',aliases=["M"])
    async def Mindustry(self, ctx):
        #Subcommand check
        if ctx.invoked_subcommand is None:
            await ctx.send("You haven't sent a Mindustry subcommand. To learn how to use this command say `&&help Mindustry`.")

    @Mindustry.group(name='mods',aliases=['mod','Mod','Mods'])
    async def Mods(self,ctx):
        if ctx.invoked_subcommand is None:
            mods=pickle.load(open('MMLMods.data','rb'))
            text="```\nCurrent Mods:\n"
            for i in range(0,len(mods)):
                text = text+mods[i]['name']+"\n"
            text = text+"```"
            await ctx.send(text)

    @Mods.command(name='info',aliases=['i','I','Info'])
    async def ModInfo(self,ctx,modName:str=None):
        if modName == None:
            await ctx.send("Please enter a mod name.")
            return
        mods=pickle.load(open('MMLMods.data','rb'))
        for i in range(0,len(mods)):
            if mods[i]['name'] == modName:
                embed = discord.Embed(title=f"{modName} v{mods[i]['version']}",description=f"{mods[i]['description']}",colour=ctx.author.colour)
                embed.set_author(name=self.bot.get_user(mods[i]['author']).display_name,
                                icon_url=self.bot.get_user(mods[i]['author']).avatar_url_as(format='png'))
                if mods[i]['iconURL'] != None:
                    embed.set_thumbnail(url=mods[i]['iconURL'])
                embed.add_field(name='Download:',
                                value=mods[i]['link'])
                embed.set_footer(text=ctx.guild.name,
                                icon_url=ctx.guild.icon_url_as(format='png'))
                await ctx.send(embed=embed)
                return
        await ctx.send("No mod exists with that name.")

    @Mods.command(name='add',aliases=['a','A','Add'])
    @commands.has_any_role('Mod developer')
    async def ModAdd(self,ctx,name:str=None):
        if name is None:
            await ctx.send("Please give your mod a name!")
            return
        mods=pickle.load(open('MMLMods.data','rb'))
        for i in range(0,len(mods)):
            if mods[i]['name'] == name:
                await ctx.send("That mod already exists!")
                return
        mods.append({'name':f'{name}','score':0,'votes':{},'author':ctx.author.id,'description':'None','link':'None','version':'0.0.0','iconURL':None,'colour':0x000000})
        pickle.dump(mods, open('MMLMods.data','wb'))
        await ctx.send(f"Mod {name} by {ctx.author.mention} has been added.")

    @Mods.command(name='remove',aliases=['r','R','Remove'])
    @commands.has_any_role('Mod developer')
    async def ModRemove(self,ctx,name:str=None):
        if name is None:
            await ctx.send("Please input a mod to delete!")
            return
        mods=pickle.load(open('MMLMods.data','rb'))
        for i in range(0,len(mods)):
            if mods[i]['name'] == name and (mods[i]['author'] == ctx.author.id or discord.utils.find(lambda r: r.id == 467462004039483393, ctx.guild.roles) in ctx.author.roles):
                mods.pop(i)
                pickle.dump(mods, open('MMLMods.data','wb'))
                await ctx.send("Mod {name} by {ctx.author.mention} has been removed.")
                return
        await ctx.send("That mod didn't exist or you don't own it!")

    @Mods.command(name='edit',aliases=['e','E','Edit'])
    async def ModEdit(self,ctx,name:str=None,dataType:str=None,*,data:str=None):
        if name is None or dataType is None or data is None:
            await ctx.send("Please make sure to input __all__ parameters.")
            return
        mods=pickle.load(open('MMLMods.data','rb'))
        for i in range(0,len(mods)):
            if mods[i]['name'] == name and mods[i]['author'] == ctx.author.id:
                try:
                    mods[i][f'{dataType}'] = data
                    await ctx.send(f"`{dataType}` has been set to `{data}`")
                    pickle.dump(mods, open('MMLMods.data','wb'))
                    return
                except KeyError:
                    await ctx.send("That isn't a valid data type. Speak to @Greenfoot5#2535 to learn the data types.")
                    return
        await ctx.send("You aren't the author of a mod with that name!")

    @Mindustry.group(name='tps',aliases=['tp','TP','TPs','TPS'])
    async def TexturePacks(self,ctx):
        if ctx.invoked_subcommand is None:
            tps=pickle.load(open('MMLPacks.data','rb'))
            text="```\nCurrent Texture Packs:\n"
            for i in range(0,len(tps)):
                text = text+tps[i]['name']+"\n"
            text = text+"```"
            await ctx.send(text)

    @TexturePacks.command(name='info',aliases=['i','I','Info'])
    async def TPInfo(self,ctx,tpName:str=None):
        if tpName == None:
            await ctx.send("Please enter a texture pack name.")
            return
        packs=pickle.load(open('MMLPacks.data','rb'))
        for i in range(0,len(packs)):
            if packs[i]['name'] == tpName:
                embed = discord.Embed(title=f"{tpName} v{packs[i]['version']}",description=f"{packs[i]['description']}",colour=ctx.author.colour)
                embed.set_author(name=self.bot.get_user(packs[i]['author']).display_name,
                                icon_url=self.bot.get_user(packs[i]['author']).avatar_url_as(format='png'))
                if packs[i]['iconURL'] != None:
                    embed.set_thumbnail(url=packs[i]['iconURL'])
                embed.add_field(name='Download:',
                                value=packs[i]['link'])
                embed.set_footer(text=ctx.guild.name,
                                icon_url=ctx.guild.icon_url_as(format='png'))
                await ctx.send(embed=embed)
                return
        await ctx.send("No mod exists with that name.")

    @TexturePacks.command(name='add',aliases=['a','A','Add'])
    @commands.has_any_role('Spriter')
    async def TPAdd(self,ctx,name:str=None):
        if name is None:
            await ctx.send("Please give your texture pack a name!")
            return
        packs=pickle.load(open('MMLPacks.data','rb'))
        for i in range(0,len(packs)):
            if packs[i]['name'] == name:
                await ctx.send("That pack already exists!")
                return
        packs.append({'name':f'{name}','Soore':0,'bupVotes':{},'author':ctx.author.id,'description':'None','link':'None','version':'0.0.0','iconURL':None,'colour':0x000000})
        pickle.dump(packs, open('MMLPacks.data','wb'))
        await ctx.send(f"Pack {name} by {ctx.author.mention} has been added.")

    @TexturePacks.command(name='remove',aliases=['r','R','Remove'])
    @commands.has_any_role('Spriter')
    async def TPRemove(self,ctx,name:str=None):
        if name is None:
            await ctx.send("Please input a pack to delete!")
            return
        packs=pickle.load(open('MMLPacks.data','rb'))
        for i in range(0,len(packs)):
            if packs[i]['name'] == name and (packs[i]['author'] == ctx.author.id or discord.utils.find(lambda r: r.id == 467462004039483393, ctx.guild.roles) in ctx.author.roles):
                packs.pop(i)
                pickle.dump(packs, open('MMLPacks.data','wb'))
                await ctx.send(f"Texture pack {name} by {ctx.author.mention} has been removed.")
                return
        await ctx.send("Either that pack doesn't exist or you aren't the author!")

    @TexturePacks.command(name='edit',aliases=['e','E','Edit'])
    async def TPEdit(self,ctx,name:str=None,dataType:str=None,*,data:str=None):
        if name is None or dataType is None or data is None:
            await ctx.send("Please make sure to input __all__ parameters.")
            return
        packs=pickle.load(open('MMLPacks.data','rb'))
        for i in range(0,len(packs)):
            if packs[i]['name'] == name and packs[i]['author'] == ctx.author.id:
                try:
                    packs[i][f'{dataType}'] = data
                    await ctx.send(f"`{dataType}` has been set to `{data}`")
                    pickle.dump(packs, open('MMLPacks.data','wb'))
                    return
                except KeyError:
                    await ctx.send("That isn't a valid data type. Speak to @Greenfoot5#2535 to learn the data types.")
                    return
        await ctx.send("You aren't the author of a pack with that name!")

    @commands.command(name='reset_mind_mml_data')
    @commands.is_owner()
    async def ResetMindustryMMLData(self,ctx):
        mods = []
        pickle.dump(mods, open('MMLMods.data','wb'))
        packs = []
        pickle.dump(packs, open('MMLPacks.data','wb'))

    @TexturePacks.command(name='print')
    @commands.is_owner()
    async def DisplayTPData(self,ctx):
        packs=pickle.load(open('MMLPacks.data','rb'))
        print(packs)

    @Mods.command(name='print')
    @commands.is_owner()
    async def DisplayModData(self,ctx):
        mods=pickle.load(open('MMLMods.data','rb'))
        print(mods)
        
# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(MindustryCog(bot))
