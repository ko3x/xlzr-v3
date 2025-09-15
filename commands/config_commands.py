import discord
from discord.ext import commands
import re
import shlex

class ConfigCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def parse_options(self, args):
        """Parse command options from arguments with proper quote handling"""
        options = {}
        
        # Join all args to work with the full string
        args_string = ' '.join(args)
        
        # Pattern explanation:
        # (\w+)= - captures the key followed by equals
        # (?:"([^"]*)"|([^"\s]+(?:\s+(?![^=]*=)[^=\s]+)*)) - captures either:
        #   - quoted string: "anything inside quotes"
        #   - unquoted value: continues until next key=value or end
        pattern = r'(\w+)=(?:"([^"]*)"|([^"\s]+(?:\s+(?![^=]*=)[^=\s]+)*))'
        matches = re.findall(pattern, args_string)
        
        for match in matches:
            key = match[0]
            value = match[1] if match[1] else match[2]  # Use quoted value if available, otherwise unquoted
            
            if key in ['autokick', 'autoban']:
                try:
                    options[key] = int(value)
                except ValueError:
                    continue
            else:
                options[key] = value.strip()
        
        return options

    @commands.command(name='setwelcome')
    @commands.has_permissions(manage_guild=True)
    async def set_welcome(self, ctx, *args):
        """Configure welcome messages"""
        # Parse arguments to find channel and options
        channel = None
        options_args = []
        
        # Check if first argument is a channel mention or ID
        if args:
            # Try to convert first argument to channel
            try:
                if args[0].startswith('<#') and args[0].endswith('>'):
                    channel_id = int(args[0][2:-1])
                    channel = ctx.guild.get_channel(channel_id)
                elif args[0].startswith('#'):
                    channel_name = args[0][1:]
                    channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)
                elif args[0].isdigit():
                    channel = ctx.guild.get_channel(int(args[0]))
                
                if channel:
                    options_args = args[1:]  # Rest are options
                else:
                    options_args = args  # All are options, use current channel
            except (ValueError, IndexError):
                options_args = args  # All are options, use current channel
        
        # If no channel found and no options, show help
        if not channel and not options_args:
            embed = discord.Embed(
                title="Welcome Configuration",
                description="Usage: `!setwelcome #channel [options]` or `!setwelcome [options]` (uses current channel)\n\n"
                           "**Options:**\n"
                           "• `color=#hexcode` - Set embed color\n"
                           "• `message=\"text\"` - Custom message\n"
                           "• `gif=\"url\"` - Add GIF\n"
                           "• `thumbnail=avatar|server|none` - Thumbnail type\n\n"
                           "**Placeholders:**\n"
                           "• `{mention}` - Mention user\n"
                           "• `{user}` - Username\n"
                           "• `{server}` - Server name\n\n"
                           "**Examples:**\n"
                           "`!setwelcome #welcome color=#095fdf message=\"Hello {mention}, welcome to {server}!\"`\n"
                           "`!setwelcome color=#095fdf message=\"Hello {mention}!\"`",
                color=0x7289da
            )
            await ctx.send(embed=embed)
            return
        
        # Use current channel if no channel specified
        if not channel:
            channel = ctx.channel
        
        guild_id = str(ctx.guild.id)
        if guild_id not in self.bot.guild_configs:
            self.bot.guild_configs[guild_id] = {}
        
        if 'welcome' not in self.bot.guild_configs[guild_id]:
            self.bot.guild_configs[guild_id]['welcome'] = {}
        
        config = self.bot.guild_configs[guild_id]['welcome']
        options = self.parse_options(options_args)
        
        # Update configuration
        config['enabled'] = True
        config['channel_id'] = channel.id
        
        if 'color' in options:
            # Validate hex color
            color_value = options['color']
            if not color_value.startswith('#'):
                color_value = '#' + color_value
            try:
                int(color_value.replace('#', ''), 16)
                config['color'] = color_value
            except ValueError:
                await ctx.send("❌ Invalid color format! Use hex format like #095fdf")
                return
                
        if 'message' in options:
            config['message'] = options['message']
        if 'gif' in options:
            config['gif'] = options['gif']
        if 'thumbnail' in options:
            config['thumbnail'] = options['thumbnail']
        
        # Save configuration immediately
        self.bot.save_json("guild_configs.json", self.bot.guild_configs)
        
        embed = discord.Embed(
            title="✅ Welcome Messages Configured",
            description=f"Welcome messages will be sent to {channel.mention}",
            color=0x00ff00
        )
        
        if options:
            embed.add_field(name="Options Applied", value="\n".join([f"• {k}: {v}" for k, v in options.items()]), inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name='setgoodbye')
    @commands.has_permissions(manage_guild=True)
    async def set_goodbye(self, ctx, *args):
        """Configure goodbye messages"""
        # Parse arguments to find channel and options
        channel = None
        options_args = []
        
        # Check if first argument is a channel mention or ID
        if args:
            # Try to convert first argument to channel
            try:
                if args[0].startswith('<#') and args[0].endswith('>'):
                    channel_id = int(args[0][2:-1])
                    channel = ctx.guild.get_channel(channel_id)
                elif args[0].startswith('#'):
                    channel_name = args[0][1:]
                    channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)
                elif args[0].isdigit():
                    channel = ctx.guild.get_channel(int(args[0]))
                
                if channel:
                    options_args = args[1:]  # Rest are options
                else:
                    options_args = args  # All are options, use current channel
            except (ValueError, IndexError):
                options_args = args  # All are options, use current channel
        
        # If no channel found and no options, show help
        if not channel and not options_args:
            embed = discord.Embed(
                title="Goodbye Configuration",
                description="Usage: `!setgoodbye #channel [options]` or `!setgoodbye [options]` (uses current channel)\n\n"
                           "**Options:**\n"
                           "• `color=#hexcode` - Set embed color\n"
                           "• `message=\"text\"` - Custom message\n"
                           "• `gif=\"url\"` - Add GIF\n"
                           "• `thumbnail=avatar|server|none` - Thumbnail type\n\n"
                           "**Placeholders:**\n"
                           "• `{user}` - Username\n"
                           "• `{server}` - Server name\n\n"
                           "**Examples:**\n"
                           "`!setgoodbye #goodbye color=#ff0000 message=\"Goodbye {user}, thanks for being part of {server}!\"`\n"
                           "`!setgoodbye color=#ff0000 message=\"Goodbye {user}!\"`",
                color=0xff0000
            )
            await ctx.send(embed=embed)
            return
        
        # Use current channel if no channel specified
        if not channel:
            channel = ctx.channel
        
        guild_id = str(ctx.guild.id)
        if guild_id not in self.bot.guild_configs:
            self.bot.guild_configs[guild_id] = {}
        
        if 'goodbye' not in self.bot.guild_configs[guild_id]:
            self.bot.guild_configs[guild_id]['goodbye'] = {}
        
        config = self.bot.guild_configs[guild_id]['goodbye']
        options = self.parse_options(options_args)
        
        # Update configuration
        config['enabled'] = True
        config['channel_id'] = channel.id
        
        if 'color' in options:
            # Validate hex color
            color_value = options['color']
            if not color_value.startswith('#'):
                color_value = '#' + color_value
            try:
                int(color_value.replace('#', ''), 16)
                config['color'] = color_value
            except ValueError:
                await ctx.send("❌ Invalid color format! Use hex format like #ff0000")
                return
                
        if 'message' in options:
            config['message'] = options['message']
        if 'gif' in options:
            config['gif'] = options['gif']
        if 'thumbnail' in options:
            config['thumbnail'] = options['thumbnail']
        
        # Save configuration immediately
        self.bot.save_json("guild_configs.json", self.bot.guild_configs)
        
        embed = discord.Embed(
            title="✅ Goodbye Messages Configured",
            description=f"Goodbye messages will be sent to {channel.mention}",
            color=0x00ff00
        )
        
        if options:
            embed.add_field(name="Options Applied", value="\n".join([f"• {k}: {v}" for k, v in options.items()]), inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name='setleveling')
    @commands.has_permissions(manage_guild=True)
    async def set_leveling(self, ctx, action=None, channel: discord.TextChannel = None, *args):
        """Configure auto-leveling system"""
        if action not in ['enable', 'disable']:
            embed = discord.Embed(
                title="Leveling Configuration",
                description="Usage: `!setleveling enable #channel [options]` or `!setleveling disable`\n\n"
                           "**Options:**\n"
                           "• `color=#hexcode` - Set embed color\n"
                           "• `message=\"text\"` - Custom level-up message\n\n"
                           "**Placeholders:**\n"
                           "• `{mention}` - Mention user\n"
                           "• `{user}` - Username\n"
                           "• `{level}` - New level\n\n"
                           "**Example:**\n"
                           "`!setleveling enable #level-up color=#ffd700 message=\"🎉 {mention} reached level {level}!\"`",
                color=0xffd700
            )
            await ctx.send(embed=embed)
            return
        
        guild_id = str(ctx.guild.id)
        if guild_id not in self.bot.guild_configs:
            self.bot.guild_configs[guild_id] = {}
        
        if 'leveling' not in self.bot.guild_configs[guild_id]:
            self.bot.guild_configs[guild_id]['leveling'] = {}
        
        config = self.bot.guild_configs[guild_id]['leveling']
        
        if action == 'disable':
            config['enabled'] = False
            # Save configuration immediately
            self.bot.save_json("guild_configs.json", self.bot.guild_configs)
            embed = discord.Embed(
                title="✅ Leveling Disabled",
                description="Auto-leveling system has been disabled",
                color=0xff0000
            )
            await ctx.send(embed=embed)
            return
        
        if not channel:
            await ctx.send("❌ Please specify a channel for level-up announcements!")
            return
        
        options = self.parse_options(args)
        
        # Update configuration
        config['enabled'] = True
        config['channel_id'] = channel.id
        
        if 'color' in options:
            # Validate hex color
            color_value = options['color']
            if not color_value.startswith('#'):
                color_value = '#' + color_value
            try:
                int(color_value.replace('#', ''), 16)
                config['color'] = color_value
            except ValueError:
                await ctx.send("❌ Invalid color format! Use hex format like #ffd700")
                return
                
        if 'message' in options:
            config['message'] = options['message']
        
        # Save configuration immediately
        self.bot.save_json("guild_configs.json", self.bot.guild_configs)
        
        embed = discord.Embed(
            title="✅ Leveling System Configured",
            description=f"Level-up announcements will be sent to {channel.mention}",
            color=0x00ff00
        )
        
        if options:
            embed.add_field(name="Options Applied", value="\n".join([f"• {k}: {v}" for k, v in options.items()]), inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name='setwarnings')
    @commands.has_permissions(manage_guild=True)
    async def set_warnings(self, ctx, action=None, channel: discord.TextChannel = None, *args):
        """Configure warning system"""
        if action not in ['enable', 'disable']:
            embed = discord.Embed(
                title="Warning System Configuration",
                description="Usage: `!setwarnings enable #channel [options]` or `!setwarnings disable`\n\n"
                           "**Options:**\n"
                           "• `autokick=number` - Auto-kick after X warnings (1-10)\n"
                           "• `autoban=number` - Auto-ban after X warnings (1-15)\n\n"
                           "**Example:**\n"
                           "`!setwarnings enable #warnings autokick=3 autoban=5`",
                color=0xff8c00
            )
            await ctx.send(embed=embed)
            return
        
        guild_id = str(ctx.guild.id)
        if guild_id not in self.bot.guild_configs:
            self.bot.guild_configs[guild_id] = {}
        
        if 'warnings' not in self.bot.guild_configs[guild_id]:
            self.bot.guild_configs[guild_id]['warnings'] = {}
        
        config = self.bot.guild_configs[guild_id]['warnings']
        
        if action == 'disable':
            config['enabled'] = False
            # Save configuration immediately
            self.bot.save_json("guild_configs.json", self.bot.guild_configs)
            embed = discord.Embed(
                title="✅ Warning System Disabled",
                description="Warning system has been disabled",
                color=0xff0000
            )
            await ctx.send(embed=embed)
            return
        
        if not channel:
            await ctx.send("❌ Please specify a channel for warning logs!")
            return
        
        options = self.parse_options(args)
        
        # Update configuration
        config['enabled'] = True
        config['log_channel_id'] = channel.id
        
        if 'autokick' in options:
            if 1 <= options['autokick'] <= 10:
                config['autokick'] = options['autokick']
            else:
                await ctx.send("❌ Auto-kick value must be between 1 and 10!")
                return
        
        if 'autoban' in options:
            if 1 <= options['autoban'] <= 15:
                config['autoban'] = options['autoban']
            else:
                await ctx.send("❌ Auto-ban value must be between 1 and 15!")
                return
        
        # Save configuration immediately
        self.bot.save_json("guild_configs.json", self.bot.guild_configs)
        
        embed = discord.Embed(
            title="✅ Warning System Configured",
            description=f"Warning logs will be sent to {channel.mention}",
            color=0x00ff00
        )
        
        if options:
            embed.add_field(name="Options Applied", value="\n".join([f"• {k}: {v}" for k, v in options.items()]), inline=False)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ConfigCommands(bot))
