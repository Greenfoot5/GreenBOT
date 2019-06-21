import discord
from discord.ext import commands
import pickle
import random
import asyncio

'''
Initialisation
'''

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='info')
    async def info(self, ctx):
        embed = discord.Embed(title='Bot info',
                              description="What do you want this to say?",
                              colour=0x008800)
        embed.set_author(name=self.bot.user.name,
                         icon_url=self.bot.user.avatar_url_as(format='png'))
        embed.add_field(name='Hello!',
                        value='I am a bot created by Greenfoot5. Recent updates can be see with the `&&updates` command')
        embed.add_field(name='Prefix',
                        value='My current prefix is `&&`')
        embed.add_field(name='It broke what do I do?',
                        value='Post in on the support server and wait for it to be notied. Until then, please be patient. If possible warn others of the problem.')
        embed.add_field(name='Can I support the bot in any way?',
                        value="Other than joining the support server and offering input not at the moment.")
        embed.add_field(name='Credits',
                        value=f"This bot was created by Greenfoot5#2535.")
        embed.set_footer(text=ctx.guild.name,
                         icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='**Displaying info**', embed=embed)

    @commands.command(name='updates', aliases=['changelog','history'])
    async def updates(self, ctx):
        embed = discord.Embed(title='Updates',
                              description=f"My most recent updates!!",
                              colour=0x6B4BD1)
        embed.set_author(name=self.bot.user.name,
                         icon_url=self.bot.user.avatar_url_as(format='png'))
        embed.add_field(name='You can find the complete changelog here:',
                        value='https://scrapbox.io/GreenBOT/Changelog')
        embed.set_footer(text=ctx.guild.name,
                         icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='**Displaying updates**', embed=embed)

    @commands.command(name='support')
    async def support(self, ctx):
        embed = discord.Embed(title='Support',
                              description=f"What the support server is and the link",
                              colour=0xFFAA00)
        embed.set_author(name=self.bot.user.name,
                         icon_url=self.bot.user.avatar_url_as(format='png'))
        embed.add_field(name='Support server',
                        value="You join the support server [here.](https://discord.gg/MVzHqdm)")
        embed.add_field(name='Why join?',
                        value="In the server you get firsthand (and often early) information about what will happen to the bot!\nYou will also get to see discussions on what will be added to the bot and even have input on it!")
        embed.add_field(name='What happens if I see a bug?',
                        value="Take a screenshot, join the server and post it in #bugs!")
        embed.set_footer(text=ctx.guild.name,
                         icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='**Link = https://discord.gg/MVzHqdm**', embed=embed)

    @commands.command(name='invite')
    async def invite(self, ctx):
        await ctx.send("https://discordapp.com/api/oauth2/authorize?client_id=436947191395909642&permissions=2146958583&scope=bot")
        
    @commands.group(name='help',aliases=['h','Help','H'])
    async def helps(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title='Help',
                                  description=f"Please note that the website is still a WIP.",
                                  colour=0x469BFF)
            embed.set_author(name=self.bot.user.name,
                              icon_url=self.bot.user.avatar_url_as(format='png'))

            embed.add_field(name='Click the link!',
                            value="https://scrapbox.io/GreenBOT/")
            embed.set_footer(text=ctx.guild.name,
                             icon_url=ctx.guild.icon_url_as(format='png'))

            await ctx.send(content='**Displaying help.**', embed=embed)

    @commands.command(name='vote')
    async def vote(self,ctx):
        embed = discord.Embed(title='Vote for the bot',
                              description=f"Click on the link to be taken to the voting page!",
                              colour=0x469BFF)
        embed.set_author(name=self.bot.user.name,
                          icon_url=self.bot.user.avatar_url_as(format='png'))

        embed.add_field(name='Discord Bot List',
                        value="https://discordbots.org/bot/436947191395909642/vote")
        embed.set_footer(text=ctx.guild.name,
                         icon_url=ctx.guild.icon_url_as(format='png'))

        await ctx.send(content='**Displaying vote link**', embed=embed)

    @helps.command(name='blurple')
    async def halp_command(self, ctx, command=''):
        def default_embed():
            embed = discord.Embed(title='help', description='Lists commands or provides advanced help for a command.\n`help <command>`')
            embed.color=int(0x7289da)
            embed.add_field(name='lightfy', value='Manipulate the image color over a curve of dark blurple, blurple, and white.')
            embed.add_field(name='darkfy', value='Manipulate the image color over a curve of not quite black, dark blurple, and blurple.')
            embed.set_footer(text="Blurplefier | " + str(ctx.author), icon_url='https://images-ext-1.discordapp.net/external/2qAD1AHfsqGs7h3CydMrskwnNjHBITIg9atQy9PEIhs/%3Fv%3D1/https/cdn.discordapp.com/emojis/412788702897766401.png')
            return embed

        def help_embed():
            embed = discord.Embed(title='Command: help', description='Lists commands or provides help for a command.')
            embed.color = int(0x7289da)
            embed.add_field(name='Usage:', value='`help <command>`')
            embed.set_footer(text="Blurplefier | " + str(ctx.author), icon_url='https://images-ext-1.discordapp.net/external/2qAD1AHfsqGs7h3CydMrskwnNjHBITIg9atQy9PEIhs/%3Fv%3D1/https/cdn.discordapp.com/emojis/412788702897766401.png')
            return embed

        def lightfy_embed():
            embed = discord.Embed(title='Command: lightfy', description='Manipulate the image color over a curve of dark blurple, blurple, and white.')
            embed.color = int(0x7289da)
            embed.add_field(name='Usage:', value='`lightfy [method] [variations=[None]]... [who]`')
            embed.set_footer(text="Blurplefier | " + str(ctx.author), icon_url='https://images-ext-1.discordapp.net/external/2qAD1AHfsqGs7h3CydMrskwnNjHBITIg9atQy9PEIhs/%3Fv%3D1/https/cdn.discordapp.com/emojis/412788702897766401.png')
            return embed

        def darkfy_embed():
            embed = discord.Embed(title='Command: darkfy', description='Manipulate the image color over a curve of not quite black, dark blurple, and blurple.')
            embed.color = int(0x7289da)
            embed.add_field(name='Usage:', value='`darkfy [method] [variations=[None]]... [who]`')
            embed.set_footer(text="Blurplefier | " + str(ctx.author), icon_url='https://images-ext-1.discordapp.net/external/2qAD1AHfsqGs7h3CydMrskwnNjHBITIg9atQy9PEIhs/%3Fv%3D1/https/cdn.discordapp.com/emojis/412788702897766401.png')
            return embed

        def error_embed():
            embed = discord.Embed(title='Command not found', description='Please re-check your help query.')
            embed.color = int(0x7289da)
            embed.set_footer(text="Blurplefier | " + str(ctx.author), icon_url='https://images-ext-1.discordapp.net/external/2qAD1AHfsqGs7h3CydMrskwnNjHBITIg9atQy9PEIhs/%3Fv%3D1/https/cdn.discordapp.com/emojis/412788702897766401.png')
            return embed

        HELP_MESSAGES = {
            '' : default_embed(),
            'help' : help_embed(),
            'lightfy' : lightfy_embed(),
            'darkfy' : darkfy_embed(),
            'error' : error_embed()
        }

        try:
            message = HELP_MESSAGES[command]
        except KeyError:
            message = HELP_MESSAGES['error']

        await ctx.send(embed=message)

    @commands.command(name="servers")
    async def servers(self,ctx):
        await ctx.send(f"I'm in {len(self.bot.guilds)} servers!")
        print("\n---\n")
        print(self.bot.guilds)
        print("\n---\n")
        

def setup(bot):
    bot.add_cog(HelpCog(bot))
