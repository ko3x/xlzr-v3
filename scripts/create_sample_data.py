import json
import os

def create_sample_data():
    """Create sample data files for testing"""
    
    # Ensure data directory exists
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Sample guild configuration
    guild_configs = {
        "123456789012345678": {  # Replace with your guild ID
            "welcome": {
                "enabled": True,
                "channel_id": 987654321098765432,  # Replace with your channel ID
                "color": "#7289da",
                "message": "Welcome {mention} to {server}! 🎉",
                "thumbnail": "avatar"
            },
            "goodbye": {
                "enabled": True,
                "channel_id": 987654321098765432,
                "color": "#ff0000",
                "message": "Goodbye {user}! Thanks for being part of {server}. 👋"
            },
            "leveling": {
                "enabled": True,
                "channel_id": 987654321098765432,
                "color": "#ffd700",
                "message": "Congratulations {mention}! You reached level {level}! 🎉"
            },
            "warnings": {
                "enabled": True,
                "log_channel_id": 987654321098765432,
                "autokick": 3,
                "autoban": 5
            }
        }
    }
    
    # Sample user levels
    user_levels = {
        "123456789012345678": {
            "987654321098765432": {
                "xp": 150,
                "level": 2,
                "last_message": 1640995200
            }
        }
    }
    
    # Sample verification data
    verification_data = {
        "123456789012345678": {
            "987654321098765432": {
                "roblox_username": "testuser123",
                "display_name": "TestUserOG",
                "verified_at": "2024-01-01T12:00:00",
                "discord_user": "TestUser#1234"
            }
        }
    }
    
    # Sample keyword configuration
    keyword_config = {
        "123456789012345678": {
            "keyword": "OG",
            "role_name": "OG member"
        }
    }
    
    # Save sample data
    with open("data/guild_configs.json", "w") as f:
        json.dump(guild_configs, f, indent=2)
    
    with open("data/user_levels.json", "w") as f:
        json.dump(user_levels, f, indent=2)
    
    with open("data/user_warnings.json", "w") as f:
        json.dump({}, f, indent=2)
    
    with open("data/verification_data.json", "w") as f:
        json.dump(verification_data, f, indent=2)
    
    with open("data/keyword_config.json", "w") as f:
        json.dump(keyword_config, f, indent=2)
    
    print("✅ Sample data files created successfully!")
    print("📝 Remember to update the IDs in the sample data with your actual Discord server and channel IDs")

if __name__ == "__main__":
    create_sample_data()
