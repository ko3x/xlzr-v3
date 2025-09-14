import discord
from discord.ext import commands
import re

class ConfigCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def parse_options(self, args):
        """Parse command options from arguments"""
        options = {}
        i = 0
        while i < len(args):
            arg = args[i]
            if arg.startswith('color='):
                options['color'] = arg.split('=', 1)[1]
            elif arg.startswith('message='):
                # Handle quoted messages
                if arg.count('"') >= 2:
                    options['message'] = arg.split('=', 1)[1].strip('"')
                else:
                    # Multi-word message
                    message_parts = [arg.split('=', 1)[1]]
                    i += 1
                    while i < len(args) and not args[i].startswith(('color=', 'gif=', 'thumbnail=')):
                        message_parts.append(args[i])
                        i += 1
                    options['message'] = ' '.join(message_parts).strip('"')
                    i -= 1
            elif arg.startswith('gif='):
                options['gif'] = arg.split('=', 1)[1].strip('"')
            elif arg.startswith('thumbnail='):
                options['thumbnail'] = arg.split('=', 1)[1]
            elif arg.startswith('autokick='):
                options['autokick'] = int(arg.split('=', 1)[1])
            elif arg.startswith('autoban='):
                options['autoban'] = int(arg.split('=', 1)[1])
            i += 1
        return options
    
    @commands.command(name='setwelcome')
    @commands.has_permissions(manage_guild=True)
    async def set_welcome(self, ctx, channel: discord.TextChannel = None, *args):
        """Configure welcome messages"""
        if not channel:
            embed = discord.Embed(
                title="Welcome Configuration",
                description="Usage: `!setwelcome #channel [options]`\n\n"
                           "**Options:**\n"
                           "• `color=#hexcode` - Set embed color\n"
                           "• `message=\"text\"` - Custom message\n"
                           "• `gif=\"url\"` - Add GIF\n"
                           "• `thumbnail=avatar|server|none` - Thumbnail type\n\n"
                           "**Placeholders:**\n"
                           "• `{mention}` - Mention user\n"
                           "• `{user}` - Username\n"
                           "• `{server}` - Server name",
                color=0x7289da
            )
            await ctx.send(embed=embed)
            return
        
        guild_id = str(ctx.guild.id)
        if guild_id not in self.bot.guild_configs:
            self.bot.guild_configs[guild_id] = {}
        
        if 'welcome' not in self.bot.guild_configs[guild_id]:
            self.bot.guild_configs[guild_id]['welcome'] = {}
        
        config = self.bot.guild_configs[guild_id]['welcome']
        options = self.parse_options(args)
        
        # Update configuration
        config['enabled'] = True
        config['channel_id'] = channel.id
        
        if 'color' in options:
            config['color'] = options['color']
        if 'message' in options:
            config['message'] = options['message']
        if 'gif' in options:
            config['gif'] = options['gif']
        if 'thumbnail' in options:
            config['thumbnail'] = options['thumbnail']
        
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
    async def set_goodbye(self, ctx, channel: discord.TextChannel = None, *args):
        """Configure goodbye messages"""
        if not channel:
            embed = discord.Embed(
                title="Goodbye Configuration",
                description="Usage: `!setgoodbye #channel [options]`\n\n"
                           "**Options:**\n"
                           "• `color=#hexcode` - Set embed color\n"
                           "• `message=\"text\"` - Custom message\n"
                           "• `gif=\"url\"` - Add GIF\n"
                           "• `thumbnail=avatar|server|none` - Thumbnail type\n\n"
                           "**Placeholders:**\n"
                           "• `{user}` - Username\n"
                           "• `{server}` - Server name",
                color=0xff0000
            )
            await ctx.send(embed=embed)
            return
        
        guild_id = str(ctx.guild.id)
        if guild_id not in self.bot.guild_configs:
            self.bot.guild_configs[guild_id] = {}
        
        if 'goodbye' not in self.bot.guild_configs[guild_id]:
            self.bot.guild_configs[guild_id]['goodbye'] = {}
        
        config = self.bot.guild_configs[guild_id]['goodbye']
        options = self.parse_options(args)
        
        # Update configuration
        config['enabled'] = True
        config['channel_id'] = channel.id
        
        if 'color' in options:
            config['color'] = options['color']
        if 'message' in options:
            config['message'] = options['message']
        if 'gif' in options:
            config['gif'] = options['gif']
        if 'thumbnail' in options:
            config['thumbnail'] = options['thumbnail']
        
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
                           "• `{level}` - New level",
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
            config['color'] = options['color']
        if 'message' in options:
            config['message'] = options['message']
        
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
                           "• `autoban=number` - Auto-ban after X warnings (1-15)",
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
