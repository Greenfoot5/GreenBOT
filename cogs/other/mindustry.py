import discord
from discord.ext import commands
import pickle
import asyncio
import time
import cogs.base.checks as chec
from typing import Union
import socket # Used to send UDP packets
import random
import colorsys
import time

'''
Init
'''

# Functions needed to decode the message
def PopString(stack):
    print("-=-")
    length = 1+int.from_bytes(stack[:1],byteorder='big')
    print(length)
    string = stack[1:length].decode("utf-8")
    print(string)
    print("-=-")
    return stack[length:], string

def PopInt(stack):
    #we are using 4 bytes for an int
    integer = int.from_bytes(stack[:4],byteorder='big')
    return stack[4:],integer

def ParseResponse(response):
    response, info = PopString(response) #msg would be server
    print(response)
    response, mapName  = PopString(response)
    response, players  = PopInt(response)
    response, wave     = PopInt(response)
    response, version  = PopInt(response)
    response =  {'info': info,
                'mapName': mapName,
                'players': players,
                'wave': wave,
                'version': version}
    return response

def ping(host:str, port:int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(4) #request timedout
    ms = 'Ping failed.'
    try:
        sent = sock.sendto(b'\xFE\x01',(host, port)) #send [-2,1] (bytes)
        start = time.time()
        data, server = sock.recvfrom(1024)
        ms = '%.d ms' %((time.time()-start)*1000)        
    finally:
        response = {'ping':ms}        
        sock.close()
        if (ms!='Ping failed.'):
            response.update(ParseResponse(data))
        return response

class MindustryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.servers = ['milinadustry.ddns.net',
                        'milinadustry.ddns.net:6568',
                        'mindustry.kr',
                        'mindustry.kr:7000',
                        'mindustry.kr:7001',
                        'games.prwh.de']

    @commands.group(name="mindustry",aliases=["Mindustry","M","m"])
    @chec.is_module_enabled('mindustry')
    async def Mindustry(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Please specify a subcommand.")

    @Mindustry.command(name="ping")
    async def MPing(self,ctx,server:str=None, port:str='6567'):
        if server is None:
            await ctx.send("Please specify a server.")
            return
        try:
            if ':' in server:
                ip, port = server.split(':')
            else:
                ip = server
            response = ping(ip, int(port))
            randomColour = [int(x*255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1)]
            randomColour = discord.Colour.from_rgb(*randomColour)
            embed = discord.Embed(title=server,
                                  colour=randomColour)
            embed.set_author(name=self.bot.user.display_name,
                             icon_url=self.bot.user.avatar_url_as(format='png'))
            for key in response:
                embed.add_field(name=key,
                                value=response[key])

            embed.set_footer(text=ctx.guild.name,
                             icon_url=ctx.guild.icon_url_as(format='png'))
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    @Mindustry.command(name='servers')
    async def MServers(self,ctx):
        randomColour = [int(x*255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1)]
        randomColour = discord.Colour.from_rgb(*randomColour)
        embed = discord.Embed(title="Verified Servers:",
                              colour=randomColour)
        embed.set_author(name=self.bot.user.display_name,
                         icon_url=self.bot.user.avatar_url_as(format='png'))
        embed.add_field(name="_*IP*_",
                        value="*Map* || || *Players* || || *Wave*")
        for server in self.servers:
            try:
                if ':' in server:
                    ip, port = server.split(':')
                else:
                    ip, port = server, '6567'
                response = ping(ip, int(port))
                if len(response) != 1:
                    embed.add_field(name=server,
                                    value=f"{response['mapName']} || || {response['players']} || || {response['wave']}")
                else:
                    embed.add_field(name=server,
                                    value="**`OFFLINE`**")

            except Exception as e:
                print(e)
        embed.set_footer(text=ctx.guild.name,
                        icon_url=ctx.guild.icon_url_as(format='png'))
        await ctx.send(embed=embed)

    @Mindustry.command(name='verify')
    @chec.i_ss('UnOMSL')
    async def MVerify(self,ctx,ip=None,port:int='6567'):
        if ip == None:
            await ctx.send("I need something to verify...")
            return
        servers = pickle.load(open("data/verify.data", "rb"))
        try:
            print(servers[f'{ip}:{port}'])
            await ctx.send(f"{ctx.author.mention}, you have already submitted `{ip}:{port}` for verification. Please be patient. We will get to it eventually.")
            return
        except KeyError:
            servers[f'{ip}:{port}'] = {'id':len(servers),'host':ctx.author.id,'port':port,'timeOfRequest':time.time(),'pings':0}
            pickle.dump(servers,open("data/verify.data","wb"))
        channel = self.bot.get_channel(550409054258987028)
        embed = discord.Embed(title="New certification request:",
                              colour=0x00FFEE)
        embed.set_author(name=self.bot.user.display_name,
                        icon_url=self.bot.user.avatar_url_as(format='png'))
        embed.add_field(name='IP',
                        value=f'`{ip}:{port}`')
        embed.add_field(name='Requester',
                        value=f"`{ctx.author.name}#{ctx.author.discriminator}`")
        embed.set_footer(text=ctx.guild.name,
                        icon_url=ctx.guild.icon_url_as(format='png'))
        await channel.send(embed=embed)
        channel = self.bot.get_channel(471002326824386591)
        embed.set_field_at(index=1,name="Requester",
                           value=f"{ctx.author.mention}")
        await channel.send(embed=embed)
            
    @Mindustry.command(name='clear_queue')
    @commands.has_any_role("Moderator")
    @chec.i_ss('UnOMSL')
    async def MQC(self,ctx):
        servers = {}
        pickle.dump(servers,open("data/verify.data","wb"))

def setup(bot):
    bot.add_cog(MindustryCog(bot))
