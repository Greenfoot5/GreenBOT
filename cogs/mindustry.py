import discord
from discord.ext import commands
import asyncio
import socket #used to send UDP packets
import random
import colorsys
import time
import pickle

#functions needed to decode the message
def popString(stack):
    length =  1+int.from_bytes(stack[:1],byteorder='big')
    string = stack[1:length].decode("utf-8")
    return stack[length:], string

def popInt(stack):
    integer = int.from_bytes(stack[:4],byteorder='big')
    return stack[4:],integer

def parseResponse(response):
    response, info = popString(response) #msg would be server
    response, mapName  = popString(response)
    response, players  = popInt(response)
    response, wave     = popInt(response)
    response, version  = popInt(response)
    response =  {'info': info,
                'mapName': mapName,
                'players': players,
                'wave': wave,
                'version': version}
    return response

def ping(host:str, port:int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(4) #request timedout
    ms = 'ping failed'
    try:
        sent = sock.sendto(b'\xFE\x01',(host, port)) #send [-2,1] (bytes)
        start = time.time()
        data, server = sock.recvfrom(1024) #because the owners make the infomsg too long
        ms = '%.d ms' %((time.time()-start)*1000)        
    except Exception as e:
        print(str(e))
    finally:
        response = {'ping':ms}        
        sock.close()
        if (ms!='ping failed'):
            response.update(parseResponse(data))
        return response


class MindustryCog:
    def __init__(self, bot):
        self.bot = bot
        self.servers = ["mindustry.kr","mindustry.indielm.com"]

    @commands.group(name='mindustry',aliases=["m"])
    async def mindustry(self, ctx):
        #Subcommand check
        if ctx.invoked_subcommand is None:
            await ctx.send("You haven't sent a mindustry subcommand. To learn how to use this command say `&&help mindustry`.")

    #LengthOfHostName HostName, LengthOfMapName MapName, PlayerAmount, Wave, Version
    @mindustry.command(name='ping')
    async def Mping(self,ctx,server:str=None, port:str='6567'):
        print(server)
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
            print(server, response)
        except Exception as e:
            print(e)
        
    @mindustry.command(name='servers')
    async def MServers(self,ctx):
        randomColour = [int(x*255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1)]
        randomColour = discord.Colour.from_rgb(*randomColour)
        embed = discord.Embed(title="Servers:",
                              colour=randomColour)
        embed.set_author(name=self.bot.user.display_name,
                         icon_url=self.bot.user.avatar_url_as(format='png'))
        embed.add_field(name="_*IP*_",
                        value="*Map*, *Players*, *Wave*")
        for server in self.servers:
            try:
                if ':' in server:
                    ip, port = server.split(':')
                else:
                    ip, port = server, '6567'
                response = ping(ip, int(port))
                if len(response) != 1:
                    embed.add_field(name=server,
                                    value=f"{response['mapName']},{response['players']},{response['wave']}")
                else:
                    embed.add_field(name=server,
                                    value="**OFFLINE**")

            except Exception as e:
                print(e)
        embed.set_footer(text=ctx.guild.name,
                        icon_url=ctx.guild.icon_url_as(format='png'))
        await ctx.send(embed=embed)

    @mindustry.command(name='certify',aliases=['verify'])
    async def MCertify(self,ctx,ip=None):
        await ctx.send('not updated yet might cause a crash')
        if ip == None:
            await ctx.send("Please input an ip.")
            return
        else:
            servers = pickle.load(open("verify.data", "rb"))
            try:
                print(servers[f'{ip}'])
                await ctx.send(f"{ctx.author.mention}, you have already submitted `{ip}` for verification. Please be patient. We will get to it eventually.")
                return
            except KeyError:
                servers[f'{ip}'] = {'id':len(servers),'host':ctx.author.id,'timeOfRequest':time.time(),'pings':0}
            channel = self.bot.get_channel(469612268439601152)
            embed = discord.Embed(title="New certification request:",
                                  colour=0x00FFEE)
            embed.set_author(name=self.bot.user.display_name,
                            icon_url=self.bot.user.avatar_url_as(format='png'))
            embed.add_field(name='IP',
                            value=ip)
            embed.add_field(name='Requester',
                            value=f"{ctx.author.name}#{ctx.author.discriminator}")
            embed.set_footer(text=ctx.guild.name,
                            icon_url=ctx.guild.icon_url_as(format='png'))
            await channel.send(embed=embed)
            channel = self.bot.get_channel(471002326824386591)
            embed.set_field_at(index=1,name="Requester",
                               value=f"{ctx.author.mention}")
            await channel.send(embed=embed)
            pickle.dump(servers, open('verify.data','wb'))
            serverList = pickle.load(open("verify.list","rb"))
            serverList.append(f'{ip}')
            pickle.dump(serverList,open('verify.list','wb'))
            await ctx.send(f"I have submitted `{ip}` for verification.")
            for i in range(1,500):
                try:
                    async with websockets.connect(f'ws://{ip}:6568') as websocket:
                        await websocket.send('ping')
                        reply = await websocket.recv()
                        dreply = base64.b64decode(reply)
                        servers[f'{ip}']['pings'] += 1
                except OSError:
                    adsh = 0
                time.sleep(172.8)
            if server[f'{ip}']['pings'] < 475:
                channel = self.bot.get_channel(469612268439601152)
                embed = discord.Embed(title="IP Denied:",
                                      colour=0x990000)
                embed.set_author(name=self.bot.user.display_name,
                                icon_url=self.bot.user.avatar_url_as(format='png'))
                embed.add_field(name='IP',
                                value=ip)
                embed.add_field(name='Requester',
                                value=self.bot.get_user(servers[f"{ip}"]["host"]).name+'#'+self.bot.get_user(servers[f"{ip}"]["host"]).discriminator)
                embed.add_field(name='Denier',
                                value=f"{self.bot.user.mention}")
                embed.add_field(name='Reason',
                                value="Server failed to have 95% uptime.")
                embed.set_footer(text=ctx.guild.name,
                                icon_url=ctx.guild.icon_url_as(format='png'))
                await channel.send(embed=embed)
                channel = self.bot.get_channel(471002326824386591)
                embed.set_field_at(index=1,name="Host",
                                   value=self.bot.get_user(ctx.author.id).mention)
                await channel.send(embed=embed)
                servers.pop(ip)
                pickle.dump(servers, open('verify.data','wb'))
                serverList = pickle.load(open("verify.list","rb"))
                serverList.remove(ip)
                pickle.dump(serverList,open('verify.list','wb'))
            else:
                channel = self.bot.get_channel(469612268439601152)
                await channel.send(f"IP `{ip}` has at least 95% uptime.")
                    

    @mindustry.command(name='allow',aliases=['approve'])
    @commands.has_any_role('Verification Helper')
    async def MAllow(self,ctx,ip=None):
        if ip == None:
            await ctx.send("Please input an ip.")
            return
        else:
            servers = pickle.load(open("verify.data", "rb"))
            try:
                print(servers[f'{ip}'])
            except KeyError:
                await ctx.send(f"The ip `{ip}` hasn't been submitted for verification.")
                return
            if (servers[f'{ip}']['timeOfRequest']+(60*60*24)) > time.time():
                await ctx.send(f"Please wait at least 24 hours so that uptime can be measured.")
                return
            channel = self.bot.get_channel(469612268439601152)
            embed = discord.Embed(title="IP Verified:",
                                  colour=0x008800)
            #Difficulty, Catching, obtaining high *, Arena, community
            embed.set_author(name=self.bot.user.display_name,
                            icon_url=self.bot.user.avatar_url_as(format='png'))
            embed.add_field(name='IP',
                            value=ip)
            embed.add_field(name='Host',
                            value=self.bot.get_user(servers[f"{ip}"]["host"]).name+'#'+self.bot.get_user(servers[f"{ip}"]["host"]).discriminator)
            embed.add_field(name='Verifier',
                            value=f"{self.bot.get_user(ctx.author.id).mention}")
            embed.set_footer(text=ctx.guild.name,
                            icon_url=ctx.guild.icon_url_as(format='png'))
            await channel.send(embed=embed)
            channel = self.bot.get_channel(471002326824386591)
            embed.set_field_at(index=1,name="Host",
                               value=self.bot.get_user(servers[f"{ip}"]["host"]).mention)
            await channel.send(embed=embed)
            servers.pop(ip)
            pickle.dump(servers, open('verify.data','wb'))
            serverList = pickle.load(open("verify.list","rb"))
            serverList.remove(ip)
            pickle.dump(serverList,open('verify.list','wb'))
            

    @mindustry.command(name='queue')
    async def MVNext(self,ctx,position=0):
        serverList = pickle.load(open("verify.list", "rb"))
        try: 
            await ctx.send(serverList[position-1])
        except IndexError:
            print(serverList)
            await ctx.send("There isn't an ip at that position")

    @mindustry.command(name='deny')
    @commands.has_any_role('Verification Helper')
    async def MDeny(self,ctx,ip=None,*,reason=None):
        if ip is None:
            await ctx.send("Please input an ip.")
            return
        elif reason is None:
            await ctx.send("Please input a reason.")
            return
        else:
            servers = pickle.load(open("verify.data", "rb"))
            try:
                print(servers[f'{ip}'])
            except KeyError:
                await ctx.send(f"The ip `{ip}` hasn't been submitted for verification.")
                return
            channel = self.bot.get_channel(469612268439601152)
            embed = discord.Embed(title="IP Denied:",
                                  colour=0x990000)
            embed.set_author(name=self.bot.user.display_name,
                            icon_url=self.bot.user.avatar_url_as(format='png'))
            embed.add_field(name='IP',
                            value=ip)
            embed.add_field(name='Requester',
                            value=self.bot.get_user(servers[f"{ip}"]["host"]).name+'#'+self.bot.get_user(servers[f"{ip}"]["host"]).discriminator)
            embed.add_field(name='Denier',
                            value=f"{self.bot.get_user(ctx.author.id).mention}")
            embed.add_field(name='Reason',
                            value=reason)
            embed.set_footer(text=ctx.guild.name,
                            icon_url=ctx.guild.icon_url_as(format='png'))
            await channel.send(embed=embed)
            channel = self.bot.get_channel(471002326824386591)
            embed.set_field_at(index=1,name="Requester",
                               value=self.bot.get_user(servers[f"{ip}"]["host"]).mention)
            await channel.send(embed=embed)
            servers.pop(ip)
            pickle.dump(servers, open('verify.data','wb'))
            serverList = pickle.load(open("verify.list","rb"))
            serverList.remove(ip)
            pickle.dump(serverList,open('verify.list','wb'))

    @mindustry.command(name='position')
    async def MVProgress(self,ctx,ip):
        servers = pickle.load(open("verify.list", "rb"))
        for index in range(len(servers)):
            if servers[index] == ip:
                await ctx.send(f"Your ip is at position {index+1}.")
                return
        await ctx.send("I couldn't find that ip in the verification queue.")

    @mindustry.command(name='v_reset')
    @commands.has_any_role('Verification Helper')
    async def MVReset(self,ctx):
        #{'ip':{'id':0,'host':hostID,'timeOfRequest':time.time,'pings':500}}
        servers = {}
        serverList = []
        pickle.dump(servers, open('verify.data','wb'))
        pickle.dump(serverList, open('verify.list','wb'))

    @mindustry.command(name='vote')
    async def MVote(self,ctx,ip=None,score=None):
        if ip is None:
            await ctx.send("Please input an ip.")
            return
        if score is None:
            await ctx.send("Please input a score.")
            return
        try:
            if int(score) < 0 or int(score) > 10:
                await ctx.send("Please input a valid score.")
                return
        except ValueError:
            await ctx.send("Please input a valid score.")
            return
        servers = pickle.load(open("verified.data", "rb"))
        try:
            currServ = servers[f'{ip}']
        except KeyError:
            await ctx.send(f"The ip `{ip}` hasn't been verified.")
            return
        for item in range(len(servers[f'{ip}']['votes'])):
            if servers[f'{ip}']['votes'][item][1] == ctx.author.id:
                servers[f'{ip}']['votes'][item][0] = score
                if len(servers[f'{ip}']['votes']) > 4:
                    servers[f'{ip}']['score'] = 0
                    for item in servers[f'{ip}']['votes']:
                        servers[f'{ip}']['score'] += item[0]
                    servers[f'{ip}']['score'] = servers[f'{ip}']['score'] / len(servers[f'{ip}']['votes'])
                pickle.dump(servers, open('verified.data','wb'))
                await ctx.send("Vote changed")
                return
        servers[f'{ip}']['votes'].append([int(score),ctx.author.id])
        if len(servers[f'{ip}']['votes']) > 4:
            servers[f'{ip}']['score'] = 0
            for item in servers[f'{ip}']['votes']:
                servers[f'{ip}']['score'] += item[0]
            servers[f'{ip}']['score'] = servers[f'{ip}']['score'] / len(servers[f'{ip}']['votes'])
        pickle.dump(servers, open('verified.data','wb'))
        await ctx.send("Vote submitted")

    @mindustry.command(name='info')
    async def MServerInfo(self,ctx,ip=None):
        if ip is None:
            await ctx.send("Please input an ip.")
            return
        servers = pickle.load(open("verified.data", "rb"))
        try:
            currServ = servers[f'{ip}']
        except KeyError:
            await ctx.send(f"The ip `{ip}` hasn't been verified.")
            return
        embed = discord.Embed(title=f"{ip}'s info:")
        embed.set_author(name=self.bot.get_user(servers[f'{ip}']['host']).display_name,
                        icon_url=self.bot.get_user(servers[f'{ip}']['host']).avatar_url_as(format='png'))
        if servers[f'{ip}']['score'] == -1:
            embed.add_field(name='Score',
                            value='Needs 5 votes to score')
        else:
            embed.add_field(name='Score',
                            value=servers[f'{ip}']['score'])
            embed.set_footer(text=ctx.guild.name,
                        icon_url=ctx.guild.icon_url_as(format='png'))
        await ctx.send(embed=embed)

    @mindustry.command(name='add')
    @commands.has_any_role('Verification Helper')
    async def MServerAdd(self,ctx,ip=None,host:discord.Member=None):
        if ip is None or host is None:
            await ctx.send("Please input __all__ required data.")
        server=pickle.load(open('verified.data','rb'))
        server[f'{ip}'] = {'host':host.id,'votes':[],'score':-1}
        pickle.dump(server, open('verified.data','wb'))
        await ctx.send("Server added.")

    @mindustry.command(name='remove')
    @commands.has_any_role('Verification Helper')
    async def MServerRemove(self,ctx,ip=None):
        if ip is None:
            await ctx.send("Please input an ip.")
            return
        servers = pickle.load(open("verified.data", "rb"))
        try:
            currServ = servers[f'{ip}']
        except KeyError:
            await ctx.send(f"The ip `{ip}` hasn't been verified.")
            return
        servers.pop(f'{ip}')
        pickle.dump(servers, open('verified.data','wb'))
        await ctx.send("Server removed.")

    @mindustry.command(name='clear')
    @commands.has_any_role('Verification Helper')
    async def MVServerClear(self,ctx):
        servers = {}
        pickle.dump(servers, open('verified.data','wb'))

    @mindustry.command(name='edit')
    @commands.has_any_role('Verification Helper', 'Verified Host')
    async def MServerEdit(self,ctx):
        await ctx.send("There isn't any data to edit.")
        
# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(MindustryCog(bot))
