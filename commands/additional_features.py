import discord
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class AdditionalFeatures(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def send_tutorial_message(self, user: discord.Member, channel: discord.TextChannel):
        """Send tutorial message after successful verification"""
        embed = discord.Embed(
            title="🎓 Welcome Tutorial",
            description=f"Hello {user.mention}! Your verification was successful. Here's what you need to know:",
            color=0x00ff7f
        )
        
        embed.add_field(
            name="📋 Read the Rules",
            value="Make sure to read all server rules to avoid any issues.",
            inline=False
        )
        
        embed.add_field(
            name="🎭 Get Roles",
            value="Check out the roles channel to get access to different areas of the server.",
            inline=False
        )
        
        embed.add_field(
            name="❓ Need Help?",
            value="Use `!help` to see all available commands and features.",
            inline=False
        )
        
        embed.add_field(
            name="🔄 Daily Updates",
            value="Your verification status will be automatically checked daily for any changes.",
            inline=False
        )
        
        embed.set_footer(text="Enjoy your time in the server!")
        
        try:
            await channel.send(embed=embed)
            logger.info(f"Sent tutorial message for {user.name}")
        except discord.Forbidden:
            logger.warning(f"Cannot send tutorial message in {channel.name}")
    
    @commands.command(name='settutorial')
    @commands.has_permissions(manage_guild=True)
    async def set_tutorial(self, ctx, channel: discord.TextChannel = None, enabled: bool = True):
        """Configure auto tutorial messages after verification"""
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.bot.guild_configs:
            self.bot.guild_configs[guild_id] = {}
        
        if 'tutorial' not in self.bot.guild_configs[guild_id]:
            self.bot.guild_configs[guild_id]['tutorial'] = {}
        
        tutorial_config = self.bot.guild_configs[guild_id]['tutorial']
        tutorial_config['enabled'] = enabled
        
        if channel:
            tutorial_config['channel_id'] = channel.id
        
        embed = discord.Embed(
            title="✅ Tutorial Configuration Updated",
            color=0x00ff00
        )
        
        if enabled:
            channel_name = channel.name if channel else tutorial_config.get('channel_id', 'Not set')
            embed.add_field(name="Status", value="✅ Enabled", inline=True)
            embed.add_field(name="Channel", value=f"#{channel_name}" if channel else "Not set", inline=True)
            embed.add_field(name="Info", value="Tutorial messages will be sent automatically after successful verification", inline=False)
        else:
            embed.add_field(name="Status", value="❌ Disabled", inline=True)
            embed.add_field(name="Info", value="Tutorial messages are disabled", inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='setcommandonly')
    @commands.has_permissions(manage_guild=True)
    async def set_command_only(self, ctx, channel: discord.TextChannel = None, enabled: bool = True):
        """Configure command-only channel filter"""
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.bot.guild_configs:
            self.bot.guild_configs[guild_id] = {}
        
        if 'command_only' not in self.bot.guild_configs[guild_id]:
            self.bot.guild_configs[guild_id]['command_only'] = {}
        
        command_config = self.bot.guild_configs[guild_id]['command_only']
        
        if channel:
            if enabled:
                if 'channels' not in command_config:
                    command_config['channels'] = []
                if channel.id not in command_config['channels']:
                    command_config['channels'].append(channel.id)
            else:
                if 'channels' in command_config and channel.id in command_config['channels']:
                    command_config['channels'].remove(channel.id)
        
        embed = discord.Embed(
            title="✅ Command-Only Filter Updated",
            color=0x00ff00
        )
        
        if channel:
            status = "✅ Enabled" if enabled else "❌ Disabled"
            embed.add_field(name="Channel", value=f"#{channel.name}", inline=True)
            embed.add_field(name="Status", value=status, inline=True)
            
            if enabled:
                embed.add_field(name="Info", value="Only bot commands (starting with !) will be allowed in this channel. All other messages will be deleted.", inline=False)
            else:
                embed.add_field(name="Info", value="Command-only filter disabled for this channel", inline=False)
        else:
            channels = command_config.get('channels', [])
            if channels:
                channel_list = []
                for ch_id in channels:
                    ch = ctx.guild.get_channel(ch_id)
                    if ch:
                        channel_list.append(f"#{ch.name}")
                embed.add_field(name="Active Channels", value="\n".join(channel_list) if channel_list else "None", inline=False)
            else:
                embed.add_field(name="Status", value="No command-only channels configured", inline=False)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AdditionalFeatures(bot))
