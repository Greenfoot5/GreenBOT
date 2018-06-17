import discord
from discord.ext import commands
import random
import sys, traceback
import pickle

"""These examples make use of Python 3.6.2 and the rewrite version on the lib.

For examples on cogs for the async version:
https://gist.github.com/leovoel/46cd89ed6a8f41fd09c5

Rewrite Documentation:
http://discordpy.readthedocs.io/en/rewrite/api.html

Rewrite Commands Documentation:
http://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html

Familiarising yourself with the documentation will greatly help you in creating your bot and using cogs.
"""
'''
=-=-=
Greenfoot5’s Cody Cavern

436600674017476608
=-=-=
'''

def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Can use spaces. Keep simple though.
    prefixes = ['&&']

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow this prefix to be used in DMs
        return ['&&']

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Think of it like a dot path import
initial_extensions = ['cogs.help',
                      'cogs.misc',
                      'cogs.trivia',
                      'cogs.listener',
                      'cogs.members',
                      'cogs.setup',
                      'cogs.owner',
                      'cogs.coin',
                      'cogs.nwxp',
                      'cogs.mindustry']

bot = commands.Bot(command_prefix=get_prefix, description="A bot for Greenfoot5's Cody Cavern", self_bot=False)
bot.remove_command('help')

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()


@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: v1.3.1\n')

    #pickle.dump([['a',5,2,5]], open('XP.data','wb'))
    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    await bot.change_presence(activity=discord.Activity(name="&&pings | v1.3.1",
                                                        type=0))
    print(f'Successfully logged in and booted...!\n')

bot.run('token', bot=True, reconnect=True)
