from discord.ext import commands
import pickle
import discord

class OwnerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Allows us to load a file as a cod manually.
    # Can use to load test cogs.
    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def cug_load(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    # Allows us to unload a command manually.
    # Can be used to unload a cog if there's an error of we've finished testing something.
    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def cug_unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    # Reloads a file. So, it unloads it and then loads it again.
    # Good if we've made changes and we don't want to restart the bot.
    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def cug_reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    # Displays an example embed and a link to an embed cretor website.
    # Good reference for when creating an embed.
    @commands.command(name='embeds')
    @commands.is_owner()
    async def example_embed(self, ctx):
        """A simple command which showcases the use of embeds.

        Have a play around and visit the Visualizer."""

        embed = discord.Embed(title='Example Embed',
                              description='Showcasing the use of Embeds...\nSee the visualizer for more info.',
                              colour=0x98FB98)
        embed.set_author(name='MysterialPy',
                         url='https://gist.github.com/MysterialPy/public',
                         icon_url='http://i.imgur.com/ko5A30P.png')
        embed.set_image(url='https://cdn.discordapp.com/attachments/84319995256905728/252292324967710721/embed.png')

        embed.add_field(name='Embed Visualizer', value='[Click Here!](https://leovoel.github.io/embed-visualizer/)')
        embed.add_field(name='Command Invoker', value=ctx.author.mention)
        embed.set_footer(text='Made in Python with discord.py@rewrite', icon_url='http://i.imgur.com/5BFecvA.png')

        await ctx.send(content='**A simple Embed for discord.py@rewrite in cogs.**', embed=embed)

    # Adds a spacer to the console. Good reference marker
    @commands.command('spacer')
    @commands.is_owner()
    async def Test(self,ctx):
        print("--------------------------------------------------")

    # Lists the amount of users the bot can see.
    @commands.command('users')
    @commands.is_owner()
    async def Users(self,ctx):
        await ctx.send(len(self.bot.users))

    # Lists the current members of the guild.
    @commands.command('members')
    @commands.is_owner()
    async def Members(self,ctx):
        await ctx.send(len(guild.members))

    # Used for transferring a file from the server to the client.
    @commands.command('file')
    @commands.is_owner()
    async def SendFile(self,ctx,fileName:str):
        file = discord.File(fp=f'media/temp/{fileName}')
        await ctx.send(content='File sent.',file=file)

def setup(bot):
    bot.add_cog(OwnerCog(bot))
