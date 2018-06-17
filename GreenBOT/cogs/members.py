import discord
from discord.ext import commands
import pickle

'''
Initialisation
'''

def is_module_enabled(module):
    """A :func`.check` that checks if the module is enabled on the server"""
    async def pred(ctx):
        guilds = []
        guilds = pickle.load(open("guilds.data", "rb"))
        for a in range(len(guilds)):
            if guilds[a][0] == ctx.guild.id:
                if module == "misc":
                    if guilds[a][1][0] == True:
                        return True
                elif module == "trivia":
                    if guilds[a][2][0] == True:
                        return True
                elif module == "members":
                    if guilds[a][3][0] == True:
                        return True
    return commands.check(pred)


class MembersCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @is_module_enabled('members')
    async def joined(self, ctx, *, member: discord.Member):
        """Says when a member joined."""
        await ctx.send(f'{member.display_name} joined on {member.joined_at}')
        
    #needs to display all user's roles and exclude @everyone.
    '''
    @commands.command(name='top_role', aliases=['toprole'])
    @commands.guild_only()
    async def show_toprole(self, ctx, *, member: discord.Member=None):
        """Simple command which shows the members Top Role."""

        if member is None:
            member = ctx.author

        await ctx.send(f'The top role for {member.display_name} is', mRoles)
    '''

    @commands.command(name='perms', aliases=['perms_for', 'permissions'])
    @commands.guild_only()
    @is_module_enabled('members')
    async def check_permissions(self, ctx, *, member: discord.Member=None):
        """A simple command which checks a members Guild Permissions.
        If member is not provided, the author will be checked."""

        if not member:
            member = ctx.author

        # Here we check if the value of each permission is True.
        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)

        # And to make it look nice, we wrap it in an Embed.
        embed = discord.Embed(title='Permissions for:', description=ctx.guild.name, colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))

        # \uFEFF is a Zero-Width Space, which basically allows us to have an empty field name.
        embed.add_field(name='\uFEFF', value=perms)

        await ctx.send(content=None, embed=embed)
        # Thanks to Gio for the Command.

    @commands.command(name='avatar', hidden=True)
    @is_module_enabled('members')
    async def show_avatar(self, ctx, member: discord.Member=None):
        if member == None:
            member = ctx.author
        icon = {member.avatar_url_as(format='png')}
        await ctx.send(icon)

    @commands.command(name='icon', hidden=True)
    @commands.guild_only()
    @is_module_enabled('members')
    async def show_icon(self, ctx):
        icon = {ctx.guild.icon_url_as(format='png')}
        await ctx.send(icon)

    @commands.command(name='servers')
    async def guilds(self,ctx):
        await ctx.send(len(self.bot.guilds))
        print(self.bot.guilds)

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(MembersCog(bot))
