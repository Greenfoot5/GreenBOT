import discord
from discord.ext import commands
import random
import sys, traceback
import pickle

def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow this prefix to be used in DMs
        return ['&&']

    #Get the prefix data
    pList = {}
    pList = pickle.load(open('data/prefix.data', 'rb'))

    #Finds the prefix in the data.
    try:
        prefix = pList[f'{message.guild.id}']
    #If there's no prefix for the server, set it to default.
    except KeyError:
        prefix = ['&&']

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefix)(bot, message)


# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Think of it like a dot path import
initial_extensions = ['cogs.base.help',
                      'cogs.base.custom',
                      'cogs.base.error_handler',
                      'cogs.base.listener',
                      'cogs.base.owner',
                      'cogs.other.credits',
                      'cogs.other.misc',
                      'cogs.other.mindustry',
                      'cogs.ss.botmod',
                      'cogs.ss.CP',
                      'cogs.ss.gear5',
                      'cogs.ss.scrim',
                      'cogs.ss.BL']

bot = commands.Bot(command_prefix=get_prefix, description="A Greenfoot5 bot.", self_bot=False)
bot.remove_command('help')

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            print(f"Successfully loaded extension - {extension}")
        except Exception as e:
            print(f"Failed to load extension {extension}.", file=sys.stderr)
            traceback.print_exc()


@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: 2.1.1\n')

    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    await bot.change_presence(activity=discord.Activity(name="GreenBOT 2.1.1",type=0))

    print(f'Successfully logged in and booted!\n')

print("Connecting to discordapp...")

tooken = pickle.load(open('tooken.data','rb'))
bot.run(tooken, bot=True, reconnect=True)
