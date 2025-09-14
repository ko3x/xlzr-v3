import discord
from discord.ext import commands
import aiohttp
import logging

logger = logging.getLogger(__name__)

class VerificationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='verify')
    async def verify_roblox(self, ctx, username: str):
        """Verify Roblox account and update Discord nickname"""
        # Send initial message
        embed = discord.Embed(
            title="🔄 Verifying Roblox Account...",
            description=f"Looking up Roblox user: `{username}`",
            color=0xffa500
        )
        message = await ctx.send(embed=embed)
        
        # Fetch Roblox display name
        display_name = await self.bot.get_roblox_display_name(username)
        
        if not display_name:
            embed = discord.Embed(
                title="❌ Verification Failed",
                description=f"Could not find Roblox user: `{username}`\n\nPlease check the username and try again.",
                color=0xff0000
            )
            await message.edit(embed=embed)
            return
        
        # Update Discord nickname
        try:
            await ctx.author.edit(nick=display_name)
            nickname_updated = True
        except discord.Forbidden:
            nickname_updated = False
        
        # Store verification data
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        
        if guild_id not in self.bot.verification_data:
            self.bot.verification_data[guild_id] = {}
        
        self.bot.verification_data[guild_id][user_id] = {
            'roblox_username': username,
            'display_name': display_name,
            'verified_at': discord.utils.utcnow().isoformat(),
            'discord_user': ctx.author.name
        }
        
        # Handle role assignment
        await self.bot.handle_role_assignment(ctx.author, display_name, guild_id)
        
        # Create success embed
        embed = discord.Embed(
            title="✅ Verification Successful",
            color=0x00ff00
        )
        embed.add_field(name="Roblox Username", value=username, inline=True)
        embed.add_field(name="Display Name", value=display_name, inline=True)
        embed.add_field(name="Discord User", value=ctx.author.mention, inline=True)
        
        if nickname_updated:
            embed.add_field(name="Nickname Updated", value="✅ Yes", inline=True)
        else:
            embed.add_field(name="Nickname Updated", value="❌ No (Missing permissions)", inline=True)
        
        # Check if role was assigned
        guild_config = self.bot.keyword_config.get(guild_id, self.bot.keyword_config)
        keyword = guild_config.get("keyword", "OG")
        role_name = guild_config.get("role_name", "OG member")
        
        if keyword.lower() in display_name.lower():
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role and role in ctx.author.roles:
                embed.add_field(name="Special Role", value=f"✅ {role_name} assigned", inline=True)
            else:
                embed.add_field(name="Special Role", value=f"❌ {role_name} (role not found or no permissions)", inline=True)
        else:
            embed.add_field(name="Special Role", value=f"No special role (keyword '{keyword}' not found)", inline=True)
        
        embed.set_footer(text="Your verification will be automatically checked daily for updates")
        
        await message.edit(embed=embed)
    
    @commands.command(name='setkeyword')
    @commands.has_permissions(manage_guild=True)
    async def set_keyword(self, ctx, keyword: str, *, role: discord.Role):
        """Set the keyword and role for verification system"""
        guild_id = str(ctx.guild.id)
        
        # Update keyword configuration
        if guild_id not in self.bot.keyword_config:
            self.bot.keyword_config[guild_id] = {}
        
        self.bot.keyword_config[guild_id]['keyword'] = keyword
        self.bot.keyword_config[guild_id]['role_name'] = role.name
        self.bot.keyword_config[guild_id]['role_id'] = role.id  # Store role ID for better reliability
        
        embed = discord.Embed(
            title="✅ Keyword Configuration Updated",
            color=0x00ff00
        )
        embed.add_field(name="Keyword", value=f"`{keyword}`", inline=True)
        embed.add_field(name="Role", value=role.mention, inline=True)
        embed.add_field(name="How it works", value=f"Users with `{keyword}` in their Roblox display name will automatically get the {role.mention} role", inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='adminverify')
    @commands.has_permissions(administrator=True)
    async def admin_verify(self, ctx, roblox_username: str, discord_user: discord.Member):
        """Admin command to manually verify a user"""
        # Send initial message
        embed = discord.Embed(
            title="🔄 Admin Verification in Progress...",
            description=f"Verifying `{roblox_username}` for {discord_user.mention}",
            color=0xffa500
        )
        message = await ctx.send(embed=embed)
        
        # Fetch Roblox display name
        display_name = await self.bot.get_roblox_display_name(roblox_username)
        
        if not display_name:
            embed = discord.Embed(
                title="❌ Admin Verification Failed",
                description=f"Could not find Roblox user: `{roblox_username}`",
                color=0xff0000
            )
            await message.edit(embed=embed)
            return
        
        # Update Discord nickname
        try:
            await discord_user.edit(nick=display_name)
            nickname_updated = True
        except discord.Forbidden:
            nickname_updated = False
        
        # Store verification data
        guild_id = str(ctx.guild.id)
        user_id = str(discord_user.id)
        
        if guild_id not in self.bot.verification_data:
            self.bot.verification_data[guild_id] = {}
        
        self.bot.verification_data[guild_id][user_id] = {
            'roblox_username': roblox_username,
            'display_name': display_name,
            'verified_at': discord.utils.utcnow().isoformat(),
            'discord_user': discord_user.name,
            'verified_by_admin': ctx.author.name
        }
        
        # Handle role assignment
        await self.bot.handle_role_assignment(discord_user, display_name, guild_id)
        
        # Create success embed
        embed = discord.Embed(
            title="✅ Admin Verification Successful",
            color=0x00ff00
        )
        embed.add_field(name="Roblox Username", value=roblox_username, inline=True)
        embed.add_field(name="Display Name", value=display_name, inline=True)
        embed.add_field(name="Discord User", value=discord_user.mention, inline=True)
        embed.add_field(name="Verified by Admin", value=ctx.author.mention, inline=True)
        
        if nickname_updated:
            embed.add_field(name="Nickname Updated", value="✅ Yes", inline=True)
        else:
            embed.add_field(name="Nickname Updated", value="❌ No (Missing permissions)", inline=True)
        
        await message.edit(embed=embed)
    
    @commands.command(name='verificationstatus')
    @commands.has_permissions(manage_guild=True)
    async def verification_status(self, ctx):
        """Show verification system status and statistics"""
        guild_id = str(ctx.guild.id)
        
        # Get verification data
        verified_users = self.bot.verification_data.get(guild_id, {})
        keyword_config = self.bot.keyword_config.get(guild_id, self.bot.keyword_config)
        
        embed = discord.Embed(
            title="📊 Verification System Status",
            color=0x7289da
        )
        
        # Configuration info
        embed.add_field(name="Keyword", value=f"`{keyword_config.get('keyword', 'OG')}`", inline=True)
        embed.add_field(name="Role", value=keyword_config.get('role_name', 'OG member'), inline=True)
        embed.add_field(name="Verified Users", value=str(len(verified_users)), inline=True)
        
        # Show some verified users
        if verified_users:
            user_list = []
            for user_id, data in list(verified_users.items())[:5]:
                member = ctx.guild.get_member(int(user_id))
                if member:
                    user_list.append(f"• {member.mention} → `{data['display_name']}`")
            
            if user_list:
                embed.add_field(name="Recent Verifications", value="\n".join(user_list), inline=False)
            
            if len(verified_users) > 5:
                embed.set_footer(text=f"Showing 5 of {len(verified_users)} verified users")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(VerificationCommands(bot))
