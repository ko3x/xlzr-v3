# XLZR-v3 Discord Bot

A powerful, feature-rich Discord bot with configurable welcome messages, auto-leveling system, comprehensive moderation tools, Roblox verification, and profile picture utilities. Built with discord.py and designed for easy customization.

## 🌟 Features

### 📋 Core Features (from xlzr-v2)
- **Welcome Messages**: Customizable embeds with colors, GIFs, and thumbnails
- **Goodbye Messages**: Personalized farewell messages
- **Auto-Leveling**: XP-based leveling system with announcements
- **Warning System**: Automated moderation with auto-kick and auto-ban
- **Configurable Commands**: Extensive customization options

### 🆕 New Features in v3
- **Roblox Verification System**: Verify users with Roblox accounts and auto-assign roles
- **Profile Picture Fetch**: Get Discord profile pictures with detailed user information
- **Daily Verification Checks**: Automatic updates for verified users
- **Admin Verification**: Manual verification by administrators

### 🎨 Customization Options
- **Colors**: Hex color codes for embed styling
- **Messages**: Custom text with placeholder variables
- **GIFs**: Add animated images to embeds
- **Thumbnails**: Avatar or server icon options
- **Channels**: Designate specific channels for different features
- **Keywords**: Configurable keywords for role assignment

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- A Discord bot token ([Create one here](https://discord.com/developers/applications))

### Installation

1. **Clone the repository**
   \`\`\`bash
   git clone https://github.com/yourusername/xlzr-v3
   cd xlzr-v3
   \`\`\`

2. **Install Python dependencies**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Set up environment variables**
   \`\`\`bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your Discord bot token
   # DISCORD_TOKEN=your_bot_token_here
   \`\`\`

4. **Create sample data (optional)**
   \`\`\`bash
   python scripts/create_sample_data.py
   \`\`\`

5. **Run the bot**
   \`\`\`bash
   python main.py
   \`\`\`

   If you didn't set up the .env file, the bot will prompt you to enter your token.

### Bot Permissions

Make sure your bot has the following permissions in your Discord server:
- Read Messages
- Send Messages
- Embed Links
- Attach Files
- Read Message History
- Manage Nicknames
- Manage Roles
- Kick Members (for auto-kick)
- Ban Members (for auto-ban)

## 📚 Commands

### ⚙️ Configuration Commands

#### Welcome Messages
\`\`\`
!setwelcome #channel [options]
\`\`\`

**Options:**
- `color=#hexcode` - Set embed color (e.g., `color=#ff0000`)
- `message="text"` - Custom welcome message
- `gif="url"` - Add animated GIF
- `thumbnail=avatar|server|none` - Set thumbnail type

**Examples:**
\`\`\`
!setwelcome #general
!setwelcome #welcome color=#00ff00 message="Welcome {mention} to {server}!"
!setwelcome #welcome gif="https://example.com/welcome.gif" thumbnail=avatar
\`\`\`

#### Goodbye Messages
\`\`\`
!setgoodbye #channel [options]
\`\`\`

**Options:**
- `color=#hexcode` - Set embed color
- `message="text"` - Custom goodbye message
- `gif="url"` - Add animated GIF
- `thumbnail=avatar|server|none` - Set thumbnail type

#### Auto-Leveling
\`\`\`
!setleveling enable #channel [options]
!setleveling disable
\`\`\`

**Options:**
- `color=#hexcode` - Set level-up announcement color
- `message="text"` - Custom level-up message

**Examples:**
\`\`\`
!setleveling enable #level-ups
!setleveling enable #general color=#ffff00 message="GG {mention}! Level {level}!"
!setleveling disable
\`\`\`

#### Warning System
\`\`\`
!setwarnings enable #log-channel [options]
!setwarnings disable
\`\`\`

**Options:**
- `autokick=number` - Auto-kick after X warnings (1-10)
- `autoban=number` - Auto-ban after X warnings (1-15)

**Examples:**
\`\`\`
!setwarnings enable #mod-logs
!setwarnings enable #logs autokick=3 autoban=5
!setwarnings disable
\`\`\`

### 🛡️ Moderation Commands

#### Warn Users
\`\`\`
!warn @user [reason]
\`\`\`

#### View Warnings
\`\`\`
!warnings @user
\`\`\`

### 🆕 Roblox Verification Commands

#### Verify Roblox Account
\`\`\`
!verify <roblox_username>
\`\`\`
**Example:** `!verify lazir1st`

This command will:
- Fetch the Roblox display name
- Update Discord nickname to match display name
- Assign roles based on keywords in display name
- Store verification data for daily checks

#### Set Verification Keyword (Admin Only)
\`\`\`
!setkeyword <keyword> <role_name>
\`\`\`
**Example:** `!setkeyword OG "OG member"`

#### Admin Manual Verification (Admin Only)
\`\`\`
!adminverify <roblox_username> @discord_user
\`\`\`

#### Check Verification Status (Admin Only)
\`\`\`
!verificationstatus
\`\`\`

### 🖼️ Profile Picture Commands

#### Get User Profile Picture
\`\`\`
!getpicture [@user]
!getpfp [@user]
!avatar [@user]
\`\`\`

If no user is mentioned, shows your own profile picture.

#### Get Server Icon
\`\`\`
!servericon
\`\`\`

### 📊 Utility Commands

#### Check Level/XP
\`\`\`
!level [@user]
\`\`\`

#### Help
\`\`\`
!help [command]
\`\`\`

## 🔧 Configuration

### Message Placeholders

Use these placeholders in custom messages:
- `{mention}` - Mention the user (@user)
- `{user}` - Username without mention
- `{server}` - Server name
- `{level}` - User's current level (leveling only)

### Data Storage

The bot uses JSON files for data storage:
- `data/guild_configs.json` - Server configurations
- `data/user_levels.json` - User XP and levels
- `data/user_warnings.json` - Warning records
- `data/verification_data.json` - Roblox verification data
- `data/keyword_config.json` - Keyword and role configuration

Data is automatically saved every 5 minutes and when the bot shuts down.

### Roblox Verification System

The verification system works as follows:

1. **User Verification**: Users run `!verify <username>` to link their Roblox account
2. **Display Name Fetch**: Bot fetches current Roblox display name via API
3. **Nickname Update**: Discord nickname is updated to match Roblox display name
4. **Role Assignment**: If display name contains configured keyword, special role is assigned
5. **Daily Checks**: Bot automatically checks all verified users daily for display name changes
6. **Auto Role Management**: Roles are added/removed based on current display name

### Permissions

Commands require appropriate Discord permissions:
- **Configuration commands**: `Manage Server`
- **Moderation commands**: `Moderate Members`
- **Auto-kick/ban**: `Kick Members` / `Ban Members`
- **Admin verification**: `Administrator`

## 🎨 Design Examples

### Welcome Message Setup
\`\`\`bash
# Basic setup
!setwelcome #welcome

# Advanced setup with styling
!setwelcome #welcome color=#7289da message="🎉 Welcome {mention} to **{server}**! We're glad you're here!" gif="https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif" thumbnail=avatar
\`\`\`

### Leveling System
\`\`\`bash
# Enable with custom styling
!setleveling enable #level-ups color=#ffd700 message="🎉 Congratulations {mention}! You've reached **Level {level}**! Keep it up! 🚀"
\`\`\`

### Roblox Verification Setup
\`\`\`bash
# Set up keyword and role
!setkeyword OG "OG member"

# Users can then verify
!verify lazir1st
\`\`\`

## 📁 Project Structure

\`\`\`
xlzr-v3/
├── main.py                 # Main bot file
├── commands/               # Command modules
│   ├── __init__.py
│   ├── config_commands.py      # Configuration commands
│   ├── moderation_commands.py  # Moderation commands
│   ├── utility_commands.py     # Utility commands
│   ├── verification_commands.py # Roblox verification
│   └── picture_commands.py     # Profile picture commands
├── data/                   # Data storage (auto-created)
│   ├── guild_configs.json
│   ├── user_levels.json
│   ├── user_warnings.json
│   ├── verification_data.json
│   └── keyword_config.json
├── scripts/                # Utility scripts
│   └── create_sample_data.py
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables example
└── README.md              # This file
\`\`\`

## 🔧 Troubleshooting

### Common Issues

1. **Bot doesn't respond to commands**
   - Check if bot has "Read Messages" and "Send Messages" permissions
   - Verify the bot token is correct
   - Make sure the bot is online

2. **Cannot change nicknames**
   - Bot needs "Manage Nicknames" permission
   - Bot's role must be higher than the user's highest role
   - Server owner nicknames cannot be changed

3. **Role assignment not working**
   - Bot needs "Manage Roles" permission
   - Bot's role must be higher than the role it's trying to assign
   - Check if the role name matches exactly (case-sensitive)

4. **Roblox verification fails**
   - Check if the Roblox username is spelled correctly
   - Roblox API might be temporarily unavailable
   - User might have privacy settings that block API access

### Debug Mode

Set `DEBUG=True` in your `.env` file to enable detailed logging.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check this README for troubleshooting steps
2. Create an issue on GitHub with detailed information
3. Join our support server: [Discord Invite Link]

## 🔮 Upcoming Features

- Custom reaction roles
- Advanced moderation tools
- Music commands
- Economy system
- Custom command creation
- Multiple language support
- Web dashboard
- Slash commands support

## 📊 API Information

### Roblox API Endpoints Used

- `POST https://users.roblox.com/v1/usernames/users` - Get user ID from username
- `GET https://users.roblox.com/v1/users/{userId}` - Get user details including display name

### Rate Limiting

The bot implements proper rate limiting for Roblox API calls to avoid being blocked.

## 🔄 Migration from xlzr-v2

If you're migrating from the Node.js version (xlzr-v2), note that:

1. **Data format is different** - You'll need to reconfigure your settings
2. **Commands are the same** - All existing commands work identically
3. **New features added** - Roblox verification and profile picture commands
4. **Performance improved** - Python version with better error handling

---

⭐ **Star this repository if you found it helpful!**

Made with ❤️ for the Discord community
