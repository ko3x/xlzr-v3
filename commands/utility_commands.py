import discord
from discord.ext import commands

class UtilityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='level')
    async def check_level(self, ctx, member: discord.Member = None):
        """Check user level and XP"""
        if not member:
            member = ctx.author
        
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)
        
        user_data = self.bot.user_levels.get(guild_id, {}).get(user_id, {'xp': 0, 'level': 1})
        
        embed = discord.Embed(
            title="📊 Level Information",
            color=0x7289da
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="User", value=member.mention, inline=True)
        embed.add_field(name="Level", value=str(user_data['level']), inline=True)
        embed.add_field(name="XP", value=f"{user_data['xp']}/{user_data['level'] * 100}", inline=True)
        
        # Calculate progress bar
        progress = user_data['xp'] / (user_data['level'] * 100)
        bar_length = 20
        filled_length = int(bar_length * progress)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        embed.add_field(name="Progress", value=f"`{bar}` {progress:.1%}", inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='help')
    async def help_command(self, ctx, command_name=None):
        """Show help information"""
        if command_name:
            # Show specific command help
            command = self.bot.get_command(command_name)
            if not command:
                await ctx.send(f"❌ Command `{command_name}` not found!")
                return
            
            embed = discord.Embed(
                title=f"Help: {command.name}",
                description=command.help or "No description available",
                color=0x7289da
            )
            embed.add_field(name="Usage", value=f"`!{command.name} {command.signature}`", inline=False)
            await ctx.send(embed=embed)
            return
        
        # Show general help
        embed = discord.Embed(
            title="🤖 XLZR Bot Help",
            description="A powerful Discord bot with configurable features",
            color=0x7289da
        )
        
        # Configuration Commands
        config_commands = [
            "`!setwelcome` - Configure welcome messages with placeholders",
            "`!setgoodbye` - Configure goodbye messages with placeholders", 
            "`!setleveling` - Configure auto-leveling system",
            "`!setwarnings` - Configure warning system",
            "`!settutorial` - Configure auto tutorial after verification",
            "`!setcommandonly` - Set channels to only allow bot commands"
        ]
        embed.add_field(name="⚙️ Configuration", value="\n".join(config_commands), inline=False)
        
        # Detailed tutorial configuration examples
        tutorial_examples = [
            "**Tutorial Configuration:**",
            "`!settutorial #channel enabled=true` - Enable tutorial in channel",
            "`!settutorial message=\"Welcome {mention}!\"` - Set custom message",
            "`!settutorial color=#ff0000` - Set embed color",
            "**Placeholders:** `{mention}`, `{user}`, `{server}`"
        ]
        embed.add_field(name="📚 Tutorial Setup", value="\n".join(tutorial_examples), inline=False)
        
        # Command-only channel examples
        command_filter_examples = [
            "**Command-Only Channels:**",
            "`!setcommandonly #self-verify true` - Enable command filter",
            "`!setcommandonly #channel false` - Disable command filter",
            "Only messages starting with `!` will be allowed"
        ]
        embed.add_field(name="🚫 Channel Filters", value="\n".join(command_filter_examples), inline=False)
        
        # Moderation Commands
        mod_commands = [
            "`!warn <user> [reason]` - Warn a user",
            "`!warnings <user>` - View user warnings"
        ]
        embed.add_field(name="🛡️ Moderation", value="\n".join(mod_commands), inline=False)
        
        # Utility Commands
        utility_commands = [
            "`!level [user]` - Check level/XP",
            "`!help [command]` - Show help information"
        ]
        embed.add_field(name="📊 Utility", value="\n".join(utility_commands), inline=False)
        
        # Verification & Special Features
        verification_commands = [
            "`!verify <username>` - Verify Roblox account",
            "`!setkeyword <keyword> <role>` - Set verification keyword",
            "`!getpicture [@user]` - Get user's profile picture"
        ]
        embed.add_field(name="🔐 Verification & Features", value="\n".join(verification_commands), inline=False)
        
        embed.set_footer(text="Use !help <command> for detailed information about a specific command")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UtilityCommands(bot))
