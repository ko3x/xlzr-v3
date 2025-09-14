import discord
from discord.ext import commands

class PictureCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='getpicture', aliases=['getpfp', 'avatar'])
    async def get_picture(self, ctx, member: discord.Member = None):
        """Get Discord profile picture of a user"""
        if not member:
            member = ctx.author
        
        # Get user's avatar
        avatar_url = member.display_avatar.url
        
        # Create embed
        embed = discord.Embed(
            title=f"{member.display_name}'s Profile Picture",
            color=member.color if member.color != discord.Color.default() else 0x7289da
        )
        
        embed.set_image(url=avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)
        
        # Add user info
        embed.add_field(name="Username", value=f"{member.name}#{member.discriminator}", inline=True)
        embed.add_field(name="Display Name", value=member.display_name, inline=True)
        embed.add_field(name="User ID", value=str(member.id), inline=True)
        
        # Add join date
        if member.joined_at:
            embed.add_field(name="Joined Server", value=member.joined_at.strftime("%B %d, %Y"), inline=True)
        
        embed.add_field(name="Account Created", value=member.created_at.strftime("%B %d, %Y"), inline=True)
        
        # Add download link
        embed.add_field(name="Download Link", value=f"[Click here]({avatar_url})", inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='servericon')
    async def server_icon(self, ctx):
        """Get the server's icon"""
        if not ctx.guild.icon:
            embed = discord.Embed(
                title="❌ No Server Icon",
                description="This server doesn't have an icon set.",
                color=0xff0000
            )
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(
            title=f"{ctx.guild.name}'s Server Icon",
            color=0x7289da
        )
        
        embed.set_image(url=ctx.guild.icon.url)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)
        
        # Add server info
        embed.add_field(name="Server Name", value=ctx.guild.name, inline=True)
        embed.add_field(name="Server ID", value=str(ctx.guild.id), inline=True)
        embed.add_field(name="Member Count", value=str(ctx.guild.member_count), inline=True)
        
        # Add download link
        embed.add_field(name="Download Link", value=f"[Click here]({ctx.guild.icon.url})", inline=True)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(PictureCommands(bot))
