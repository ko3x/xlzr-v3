#!/usr/bin/env python3
"""
Setup script for XLZR-v3 Discord Bot
This script helps with initial bot setup and configuration.
"""

import os
import json
import sys

def create_directories():
    """Create necessary directories"""
    directories = ['data', 'logs']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        token = input("Enter your Discord bot token: ").strip()
        if token:
            with open('.env', 'w') as f:
                f.write(f"DISCORD_TOKEN={token}\n")
                f.write("DEBUG=False\n")
            print("✅ Created .env file")
        else:
            print("❌ No token provided, skipping .env creation")
    else:
        print("📄 .env file already exists")

def create_default_configs():
    """Create default configuration files"""
    configs = {
        'guild_configs.json': {},
        'user_levels.json': {},
        'user_warnings.json': {},
        'verification_data.json': {},
        'keyword_config.json': {
            "keyword": "OG",
            "role_name": "OG member"
        }
    }
    
    for filename, default_data in configs.items():
        filepath = os.path.join('data', filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                json.dump(default_data, f, indent=2)
            print(f"✅ Created config file: {filename}")
        else:
            print(f"📄 Config file already exists: {filename}")

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import discord
        import aiohttp
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def main():
    """Main setup function"""
    print("🤖 XLZR-v3 Discord Bot Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version}")
    
    # Create directories
    create_directories()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install dependencies first:")
        print("pip install -r requirements.txt")
        return
    
    # Create configuration files
    create_default_configs()
    
    # Create .env file
    create_env_file()
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Make sure your bot has the required permissions in your Discord server")
    print("2. Run the bot with: python main.py")
    print("3. Use !help to see available commands")
    print("\nFor detailed instructions, see README.md")

if __name__ == "__main__":
    main()
