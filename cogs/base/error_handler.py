import traceback
import sys
from discord.ext import commands
import discord
from discord.ext.commands.cooldowns import BucketType
import cogs.base.checks as chec

class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        # This prevents any commands with local handlers being handled here in on_command_error.
        #if hasattr(ctx.command, 'on_error'):
        #    return

        ignored = (commands.CommandNotFound, commands.UserInputError)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            print(error)
            return

        #Checks if it's disabled
        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'`{ctx.prefix}{ctx.command}` has been disabled.')

        #Private messages check
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f"`{ctx.prefix}{ctx.command}` can't be used in Private Messages.")
            except:
                pass

        #Cooldown check
        elif isinstance(error, commands.errors.CommandOnCooldown):
            seconds = error.retry_after
            seconds = round(seconds, 2)
            hours, remainder = divmod(int(seconds), 3600)
            minutes, seconds = divmod(remainder, 60)
            return await ctx.send(
                f'**`{ctx.prefix}{ctx.command}` is on Cooldown:**\n'
                f'{minutes}m and {seconds}s remaining',
                delete_after=15)

        #Checks if modules have  been enabled/disabled
        elif isinstance(error, chec.ModuleNotEnabled):
            try:
                return await ctx.message.add_reaction(emoji='disabled:550409453405601822')
            except Exception as e:
                print(e)
                pass

        #Checks if module is disabled
        elif isinstance(error, chec.ModuleDisabled):
            try:
                return await ctx.message.add_reaction(emoji='disabled:550409453405601822')
            except Exception as e:
                print(e)
                pass

        #Checks if server specific and in that server
        elif isinstance(error, chec.NotInServer):
            try:
                return await ctx.send("You can't do that here.")
            except:
                pass

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
                return await ctx.send('I could not find that member. Please try again.')

        elif isinstance(error, commands.CheckFailure):
            try:
                return await ctx.send(f"{ctx.author.mention}, you can't do that.")
            except:
                pass

        # All other Errors not returned come here... And we can just print the default TraceBack.
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)                

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
