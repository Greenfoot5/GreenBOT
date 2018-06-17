import discord
from discord.ext import commands
import asyncio
import websockets
import base64

class MindustryCog:
    def __init__(self, bot):
        self.bot = bot

    #LengthOfHostName HostName, LengthOfMapName MapName, PlayerAmount, Wave, Version
    @commands.command(name='ping')
    async def Mping(self,ctx,server:str=None):
        if server is None:
            await ctx.send("Please specify a server.")
            return
        async with websockets.connect(f'ws://{server}:6568') as websocket:
            await websocket.send('ping')
            reply = await websocket.recv()
            dreply = base64.b64decode(reply)
            embed = discord.Embed(title=server,
                                  colour=0x33CCFF)
            embed.set_author(name=self.bot.user.display_name,
                            icon_url=self.bot.user.avatar_url_as(format='png'))

            embed.add_field(name='Host',
                            value=str(dreply[1:(dreply[0]+1)])[2:(dreply[0]+2)])
            embed.add_field(name='Map',
                            value=f'{str(dreply[(dreply[0]+2):(dreply[0]+2+dreply[dreply[0]+1])])[2:(dreply[0]+dreply[dreply[0]+1])]}')
            embed.add_field(name='Players',
                            value=dreply[dreply[0]+5+dreply[dreply[0]+1]])
            embed.set_footer(text=ctx.guild.name,
                            icon_url=ctx.guild.icon_url_as(format='png'))
            await ctx.send(embed=embed)
        
# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(MindustryCog(bot))
