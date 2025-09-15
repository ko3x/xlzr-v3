import discord
from discord.ext import commands
from datetime import datetime
import json

class ModerationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load_warnings()
    
    def load_warnings(self):
        try:
            with open("user_warnings.json", "r") as file:
                self.bot.user_warnings = json.load(file)
        except FileNotFoundError:
            self.bot.user_warnings = {}
    
    def save_json(self, filename, data):
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
    
    @commands.command(name='warn')
    @commands.has_permissions(moderate_members=True)
    async def warn_user(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Warn a user"""
        if member.bot:
            await ctx.send("❌ Cannot warn bots!")
            return
        
        if member == ctx.author:
            await ctx.send("❌ You cannot warn yourself!")
            return
        
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ You cannot warn someone with equal or higher role!")
            return
        
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)
        
        # Initialize warning data
        if guild_id not in self.bot.user_warnings:
            self.bot.user_warnings[guild_id] = {}
        
        if user_id not in self.bot.user_warnings[guild_id]:
            self.bot.user_warnings[guild_id][user_id] = []
        
        # Add warning
        warning_data = {
            'reason': reason,
            'moderator': ctx.author.name,
            'timestamp': datetime.now().isoformat(),
            'id': len(self.bot.user_warnings[guild_id][user_id]) + 1
        }
        
        self.bot.user_warnings[guild_id][user_id].append(warning_data)
        warning_count = len(self.bot.user_warnings[guild_id][user_id])
        
        self.save_json("user_warnings.json", self.bot.user_warnings)
        
        # Create warning embed
        embed = discord.Embed(
            title="⚠️ User Warned",
            color=0xff8c00
        )
        embed.add_field(name="User", value=member.mention, inline=True)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
        embed.add_field(name="Warning Count", value=str(warning_count), inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=f"Warning ID: {warning_data['id']}")
        
        await ctx.send(embed=embed)
        
        # Send to log channel if configured
        config = self.bot.guild_configs.get(guild_id, {}).get('warnings', {})
        if config.get('enabled', False):
            log_channel_id = config.get('log_channel_id')
            if log_channel_id:
                log_channel = ctx.guild.get_channel(log_channel_id)
                if log_channel:
                    try:
                        await log_channel.send(embed=embed)
                    except discord.Forbidden:
                        pass
        
        # Check for auto-kick/ban
        autokick = config.get('autokick')
        autoban = config.get('autoban')
        
        try:
            if autoban and warning_count >= autoban:
                await member.ban(reason=f"Auto-ban: {autoban} warnings reached")
                ban_embed = discord.Embed(
                    title="🔨 Auto-Ban Executed",
                    description=f"{member.mention} has been banned for reaching {autoban} warnings",
                    color=0xff0000
                )
                await ctx.send(embed=ban_embed)
            elif autokick and warning_count >= autokick:
                await member.kick(reason=f"Auto-kick: {autokick} warnings reached")
                kick_embed = discord.Embed(
                    title="👢 Auto-Kick Executed",
                    description=f"{member.mention} has been kicked for reaching {autokick} warnings",
                    color=0xff8c00
                )
                await ctx.send(embed=kick_embed)
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to kick/ban this user!")
    
    @commands.command(name='warnings')
    @commands.has_permissions(moderate_members=True)
    async def view_warnings(self, ctx, member: discord.Member):
        """View warnings for a user"""
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)
        
        warnings = self.bot.user_warnings.get(guild_id, {}).get(user_id, [])
        
        if not warnings:
            embed = discord.Embed(
                title="📋 User Warnings",
                description=f"{member.mention} has no warnings",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(
            title="📋 User Warnings",
            description=f"{member.mention} has {len(warnings)} warning(s)",
            color=0xff8c00
        )
        
        for warning in warnings[-5:]:  # Show last 5 warnings
            embed.add_field(
                name=f"Warning #{warning['id']}",
                value=f"**Reason:** {warning['reason']}\n"
                      f"**Moderator:** {warning['moderator']}\n"
                      f"**Date:** {warning['timestamp'][:10]}",
                inline=False
            )
        
        if len(warnings) > 5:
            embed.set_footer(text=f"Showing last 5 of {len(warnings)} warnings")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ModerationCommands(bot))
