import discord
from discord.ext import commands, tasks
import json
import os
import asyncio
import aiohttp
from datetime import datetime, timedelta
import logging
from typing import Optional, Dict, Any

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class XLZRBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )
        
        # Initialize data storage
        self.data_dir = "data"
        self.ensure_data_directory()
        
        # Load configurations
        self.guild_configs = self.load_json("guild_configs.json", {})
        self.user_levels = self.load_json("user_levels.json", {})
        self.user_warnings = self.load_json("user_warnings.json", {})
        self.verification_data = self.load_json("verification_data.json", {})
        self.keyword_config = self.load_json("keyword_config.json", {
            "keyword": "OG",
            "role_name": "OG member"
        })
        
        # Auto-save task
        self.auto_save.start()
        
        # Daily verification check
        self.daily_verification_check.start()
    
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def load_json(self, filename: str, default: Any = None) -> Any:
        """Load JSON data from file"""
        filepath = os.path.join(self.data_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return default if default is not None else {}
    
    def save_json(self, filename: str, data: Any):
        """Save JSON data to file"""
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @tasks.loop(minutes=5)
    async def auto_save(self):
        """Auto-save all data every 5 minutes"""
        try:
            self.save_json("guild_configs.json", self.guild_configs)
            self.save_json("user_levels.json", self.user_levels)
            self.save_json("user_warnings.json", self.user_warnings)
            self.save_json("verification_data.json", self.verification_data)
            self.save_json("keyword_config.json", self.keyword_config)
            logger.info("Auto-saved all data")
        except Exception as e:
            logger.error(f"Error during auto-save: {e}")
    
    @tasks.loop(hours=24)
    async def daily_verification_check(self):
        """Daily check for verified users' Roblox display names"""
        logger.info("Starting daily verification check...")
        
        for guild_id, users in self.verification_data.items():
            guild = self.get_guild(int(guild_id))
            if not guild:
                continue
                
            for user_id, user_data in users.items():
                try:
                    member = guild.get_member(int(user_id))
                    if not member:
                        continue
                    
                    # Fetch current Roblox display name
                    current_display_name = await self.get_roblox_display_name(user_data['roblox_username'])
                    
                    if current_display_name and current_display_name != user_data.get('display_name'):
                        # Update stored display name
                        user_data['display_name'] = current_display_name
                        
                        # Update Discord nickname
                        try:
                            await member.edit(nick=current_display_name)
                        except discord.Forbidden:
                            logger.warning(f"Cannot change nickname for {member.name}")
                        
                        # Check keyword and role assignment
                        await self.handle_role_assignment(member, current_display_name, guild_id)
                        
                        logger.info(f"Updated verification for {member.name}: {current_display_name}")
                
                except Exception as e:
                    logger.error(f"Error checking verification for user {user_id}: {e}")
    
    async def get_roblox_display_name(self, username: str) -> Optional[str]:
        """Fetch Roblox display name from username using Roblox API"""
        try:
            async with aiohttp.ClientSession() as session:
                # First, get user ID from username
                async with session.post(
                    "https://users.roblox.com/v1/usernames/users",
                    json={"usernames": [username]}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("data") and len(data["data"]) > 0:
                            user_id = data["data"][0]["id"]
                            
                            # Then get user details including display name
                            async with session.get(f"https://users.roblox.com/v1/users/{user_id}") as user_response:
                                if user_response.status == 200:
                                    user_data = await user_response.json()
                                    return user_data.get("displayName")
            return None
        except Exception as e:
            logger.error(f"Error fetching Roblox data for {username}: {e}")
            return None
    
    async def handle_role_assignment(self, member: discord.Member, display_name: str, guild_id: str):
        """Handle role assignment based on keyword in display name"""
        guild_config = self.keyword_config.get(guild_id, self.keyword_config)
        keyword = guild_config.get("keyword", "OG")
        role_name = guild_config.get("role_name", "OG member")
        
        # Find the role
        role = discord.utils.get(member.guild.roles, name=role_name)
        if not role:
            return
        
        has_keyword = keyword.lower() in display_name.lower()
        has_role = role in member.roles
        
        try:
            if has_keyword and not has_role:
                await member.add_roles(role)
                logger.info(f"Added {role_name} role to {member.name}")
            elif not has_keyword and has_role:
                await member.remove_roles(role)
                logger.info(f"Removed {role_name} role from {member.name}")
        except discord.Forbidden:
            logger.warning(f"Cannot manage roles for {member.name}")
    
    async def on_ready(self):
        """Bot ready event"""
        logger.info(f'{self.user} has connected to Discord!')
        logger.info(f'Bot is in {len(self.guilds)} guilds')
        
        # Ensure auto-save task is running
        if not self.auto_save.is_running():
            self.auto_save.start()
        
        # Ensure daily check is running
        if not self.daily_verification_check.is_running():
            self.daily_verification_check.start()
    
    async def on_member_join(self, member):
        """Handle member join events for welcome messages"""
        guild_id = str(member.guild.id)
        config = self.guild_configs.get(guild_id, {}).get('welcome', {})
        
        if not config.get('enabled', False):
            return
        
        channel_id = config.get('channel_id')
        if not channel_id:
            return
        
        channel = member.guild.get_channel(channel_id)
        if not channel:
            return
        
        # Create welcome embed
        embed = discord.Embed(
            title="Welcome!",
            description=config.get('message', 'Welcome {mention} to {server}!').format(
                mention=member.mention,
                user=member.name,
                server=member.guild.name
            ),
            color=int(config.get('color', '0x7289da').replace('#', '0x'), 16)
        )
        
        # Add thumbnail
        thumbnail_type = config.get('thumbnail', 'avatar')
        if thumbnail_type == 'avatar':
            embed.set_thumbnail(url=member.display_avatar.url)
        elif thumbnail_type == 'server':
            embed.set_thumbnail(url=member.guild.icon.url if member.guild.icon else None)
        
        # Add GIF if specified
        gif_url = config.get('gif')
        if gif_url:
            embed.set_image(url=gif_url)
        
        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            logger.warning(f"Cannot send welcome message in {channel.name}")
    
    async def on_member_remove(self, member):
        """Handle member leave events for goodbye messages"""
        guild_id = str(member.guild.id)
        config = self.guild_configs.get(guild_id, {}).get('goodbye', {})
        
        if not config.get('enabled', False):
            return
        
        channel_id = config.get('channel_id')
        if not channel_id:
            return
        
        channel = member.guild.get_channel(channel_id)
        if not channel:
            return
        
        # Create goodbye embed
        embed = discord.Embed(
            title="Goodbye!",
            description=config.get('message', 'Goodbye {user}! Thanks for being part of {server}.').format(
                user=member.name,
                server=member.guild.name
            ),
            color=int(config.get('color', '0xff0000').replace('#', '0x'), 16)
        )
        
        # Add thumbnail
        thumbnail_type = config.get('thumbnail', 'avatar')
        if thumbnail_type == 'avatar':
            embed.set_thumbnail(url=member.display_avatar.url)
        elif thumbnail_type == 'server':
            embed.set_thumbnail(url=member.guild.icon.url if member.guild.icon else None)
        
        # Add GIF if specified
        gif_url = config.get('gif')
        if gif_url:
            embed.set_image(url=gif_url)
        
        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            logger.warning(f"Cannot send goodbye message in {channel.name}")
    
    async def on_message(self, message):
        """Handle message events for XP system"""
        if message.author.bot:
            return
        
        # XP System
        guild_id = str(message.guild.id)
        user_id = str(message.author.id)
        
        # Initialize user data if not exists
        if guild_id not in self.user_levels:
            self.user_levels[guild_id] = {}
        
        if user_id not in self.user_levels[guild_id]:
            self.user_levels[guild_id][user_id] = {'xp': 0, 'level': 1, 'last_message': 0}
        
        user_data = self.user_levels[guild_id][user_id]
        current_time = datetime.now().timestamp()
        
        # Check cooldown (1 minute between XP gains)
        if current_time - user_data.get('last_message', 0) >= 60:
            # Add XP (15-25 random)
            import random
            xp_gain = random.randint(15, 25)
            user_data['xp'] += xp_gain
            user_data['last_message'] = current_time
            
            # Check for level up
            required_xp = user_data['level'] * 100
            if user_data['xp'] >= required_xp:
                user_data['level'] += 1
                user_data['xp'] = 0
                
                # Send level up message if enabled
                config = self.guild_configs.get(guild_id, {}).get('leveling', {})
                if config.get('enabled', False):
                    channel_id = config.get('channel_id')
                    if channel_id:
                        channel = message.guild.get_channel(channel_id)
                        if channel:
                            embed = discord.Embed(
                                title="Level Up!",
                                description=config.get('message', 'Congratulations {mention}! You reached level {level}!').format(
                                    mention=message.author.mention,
                                    user=message.author.name,
                                    level=user_data['level']
                                ),
                                color=int(config.get('color', '0xffd700').replace('#', '0x'), 16)
                            )
                            try:
                                await channel.send(embed=embed)
                            except discord.Forbidden:
                                pass
        
        await self.process_commands(message)

# Load cogs/commands
async def load_extensions(bot):
    """Load all command extensions"""
    extensions = [
        'commands.config_commands',
        'commands.moderation_commands',
        'commands.utility_commands',
        'commands.verification_commands',
        'commands.picture_commands'
    ]
    
    for extension in extensions:
        try:
            await bot.load_extension(extension)
            logger.info(f"Loaded extension: {extension}")
        except Exception as e:
            logger.error(f"Failed to load extension {extension}: {e}")

async def main():
    """Main function to run the bot"""
    bot = XLZRBot()
    
    # Load extensions
    await load_extensions(bot)
    
    # Get token from environment or user input
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        token = input("Please enter your Discord bot token: ").strip()
        if not token:
            print("No token provided!")
            return
    
    try:
        await bot.start(token)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot error: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
