import discord
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class AdditionalFeatures(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def send_tutorial_message(self, user: discord.Member, channel: discord.TextChannel):
        """Send tutorial message after successful verification"""
        guild_id = str(user.guild.id)
        
        # Get custom tutorial message or use default
        tutorial_config = self.bot.guild_configs.get(guild_id, {}).get('tutorial', {})
        custom_message = tutorial_config.get('message', '')
        custom_color = tutorial_config.get('color', '#00ff7f')
        
        if custom_message:
            # Use custom message with placeholders
            message_text = custom_message.replace('{mention}', user.mention)
            message_text = message_text.replace('{user}', user.display_name)
            message_text = message_text.replace('{server}', user.guild.name)
            
            # Convert hex color to int
            if isinstance(custom_color, str) and custom_color.startswith('#'):
                color_int = int(custom_color[1:], 16)
            else:
                color_int = 0x00ff7f
            
            embed = discord.Embed(
                title="🎓 Welcome Tutorial",
                description=message_text,
                color=color_int
            )
        else:
            embed = discord.Embed(
                title="🎓 Tutorial Verifikasi",
                description=f"@everyone 🎉 **Silahkan ubah nickname Roblox kamu dengan menambahkan OG dibelakangnya untuk mendapatkan role <@&1400519466860675072> lalu lakukan verifikasi dengan cara:**\n\n\`\`\`!verify <username roblox kamu>\`\`\`\n\n⚠️ **Ingat ya, gunakan USERNAME bukan Nickname!**\n\n📝 **Contoh:**\n\`\`\`!verify lazir1st\`\`\`\n\n🤖 **Bot akan melakukan verifikasi secara otomatis**\n\n⚡ *Buat yang merasa role OG membernya dicopot, harap verifikasi ulang!!!!*",
                color=0x00ff7f
            )
            
            embed.add_field(
                name="📋 Baca Rules Server",
                value="Pastikan untuk membaca semua aturan server agar tidak terjadi masalah.",
                inline=False
            )
            
            embed.add_field(
                name="🎭 Dapatkan Role Lainnya", 
                value="Cek channel roles untuk mendapatkan akses ke area server yang berbeda.",
                inline=False
            )
            
            embed.add_field(
                name="❓ Butuh Bantuan?",
                value="Gunakan `!help` untuk melihat semua command dan fitur yang tersedia.",
                inline=False
            )
            
            embed.add_field(
                name="🔄 Update Harian",
                value="Status verifikasi kamu akan dicek otomatis setiap hari untuk perubahan.",
                inline=False
            )
            
            embed.set_footer(text="🎮 Selamat bermain di server!")
        
        await channel.send(embed=embed)

    @commands.command(name='settutorial')
    @commands.has_permissions(manage_guild=True)
    async def set_tutorial(self, ctx, channel: discord.TextChannel = None, *, args: str = ''):
        """Configure auto tutorial messages after verification
        Usage: !settutorial [#channel] [enabled=true/false] [color=#hex] [message="custom message"]
        """
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.bot.guild_configs:
            self.bot.guild_configs[guild_id] = {}
        
        if 'tutorial' not in self.bot.guild_configs[guild_id]:
            self.bot.guild_configs[guild_id]['tutorial'] = {}
        
        tutorial_config = self.bot.guild_configs[guild_id]['tutorial']
        
        # Parse arguments
        if args:
            options = self.parse_options(args)
            
            if 'enabled' in options:
                enabled = options['enabled'].lower() in ['true', '1', 'yes', 'on']
                tutorial_config['enabled'] = enabled
            
            if 'color' in options:
                color = options['color']
                if color.startswith('#') and len(color) == 7:
                    tutorial_config['color'] = color
            
            if 'message' in options:
                tutorial_config['message'] = options['message']
        
        if channel:
            tutorial_config['channel_id'] = channel.id
        
        # Show current configuration
        embed = discord.Embed(
            title="✅ Tutorial Configuration",
            color=0x00ff00
        )
        
        enabled = tutorial_config.get('enabled', True)
        channel_id = tutorial_config.get('channel_id')
        custom_message = tutorial_config.get('message', '')
        custom_color = tutorial_config.get('color', '#00ff7f')
        
        embed.add_field(name="Status", value="✅ Enabled" if enabled else "❌ Disabled", inline=True)
        
        if channel_id:
            ch = ctx.guild.get_channel(channel_id)
            embed.add_field(name="Channel", value=f"#{ch.name}" if ch else "Channel not found", inline=True)
        else:
            embed.add_field(name="Channel", value="Not set", inline=True)
        
        embed.add_field(name="Color", value=custom_color, inline=True)
        
        if custom_message:
            embed.add_field(name="Custom Message", value=custom_message[:100] + "..." if len(custom_message) > 100 else custom_message, inline=False)
        else:
            embed.add_field(name="Message", value="Using default tutorial message", inline=False)
        
        embed.add_field(name="Available Placeholders", value="`{mention}` `{user}` `{server}`", inline=False)
        
        self.bot.save_json("guild_configs.json", self.bot.guild_configs)
        
        await ctx.send(embed=embed)
    
    def parse_options(self, args_string):
        """Parse command options like color=#hex message="text" """
        import re
        options = {}
        
        # Match quoted values: key="value with spaces"
        quoted_pattern = r'(\w+)=(?:"([^"]*)")'
        quoted_matches = re.findall(quoted_pattern, args_string)
        for key, value in quoted_matches:
            options[key] = value
        
        # Remove quoted parts from string
        args_string = re.sub(quoted_pattern, '', args_string)
        
        # Match unquoted values: key=value
        unquoted_pattern = r'(\w+)=(\S+)'
        unquoted_matches = re.findall(unquoted_pattern, args_string)
        for key, value in unquoted_matches:
            options[key] = value
        
        return options
    
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
        
        self.bot.save_json("guild_configs.json", self.bot.guild_configs)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AdditionalFeatures(bot))
