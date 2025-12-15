# Gitinsky Support Bot - Setup Guide

## Prerequisites

Before setting up the bot, ensure you have:

- Python 3.9 or higher installed
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- DeepSeek API key
- SMTP email server access (e.g., Gmail, company email server)
- Company email domain for user verification

## Installation Steps

### 1. Clone or Download the Project

```bash
cd gitinsky-supportbot-tg
```

### 2. Create Virtual Environment

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file with your configuration:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather

# DeepSeek API Configuration
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_API_URL=https://api.deepseek.com/v1
OPENROUTER_API_KEY=your_openrouter_api_key

# Database Configuration
DATABASE_URL=sqlite:///./gitinsky_bot.db

# Email Configuration (SMTP)
# For Gmail, use: smtp.gmail.com port 587
# For custom server, use your SMTP settings
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@company.com
SMTP_PASSWORD=your_app_password
SMTP_FROM_EMAIL=your_email@company.com
SMTP_FROM_NAME=Gitinsky Support Bot

# Company Email Domain
COMPANY_EMAIL_DOMAIN=yourcompany.com

# Admin Configuration
# Comma-separated list of Telegram user IDs
ADMIN_TELEGRAM_IDS=123456789,987654321
```

### 5. Initialize Knowledge Base

Populate the knowledge base with technology documentation:

```bash
python populate_knowledge.py
```

This will add documentation for all 19 technology stacks to the database.

### 6. Run the Bot

```bash
python main.py
```

You should see:
```
╔═══════════════════════════════════════╗
║   Gitinsky Support Bot                ║
║   Technical Support Assistant         ║
╚═══════════════════════════════════════╝

Loading configuration...
Initializing database...
Starting Telegram bot...
Bot is running. Press Ctrl+C to stop.
```

## Configuration Details

### Getting Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token provided

### Getting DeepSeek API Key

1. Visit [DeepSeek Platform](https://platform.deepseek.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

### Email Configuration

#### Using Gmail

1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password:
   - Go to Google Account → Security
   - Select "App passwords"
   - Generate password for "Mail"
3. Use this app password in `SMTP_PASSWORD`

#### Using Custom SMTP Server

Configure your company's SMTP server settings:
- `SMTP_HOST`: Your SMTP server hostname
- `SMTP_PORT`: Usually 587 (TLS) or 465 (SSL)
- `SMTP_USER`: Your email username
- `SMTP_PASSWORD`: Your email password

### Finding Your Telegram User ID

To add yourself as an admin:

1. Start a chat with [@userinfobot](https://t.me/userinfobot)
2. The bot will send you your user ID
3. Add this ID to `ADMIN_TELEGRAM_IDS` in `.env`

## Database

The bot uses SQLite by default, which creates a file `gitinsky_bot.db` in the project directory.

For production, you can use PostgreSQL:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/gitinsky_bot
```

## Testing the Bot

### 1. Start the Bot in Telegram

Search for your bot in Telegram by the username you set with BotFather.

### 2. Test Verification Flow

1. Send `/start` to the bot
2. Send `/verify`
3. Enter your company email
4. Check your email for verification code
5. Enter the code in Telegram
6. You should be verified!

### 3. Ask a Technical Question

Try asking:
- "How do I deploy an application with Kubernetes?"
- "What are Ansible best practices?"
- "Help me with Docker troubleshooting"

### 4. Test Admin Commands (if configured)

If your Telegram ID is in `ADMIN_TELEGRAM_IDS`:
- `/admin_list_users` - View all verified users

## Troubleshooting

### Bot doesn't respond

- Check if the bot is running (`python main.py`)
- Verify `TELEGRAM_BOT_TOKEN` is correct
- Check bot logs in `bot.log`

### Email verification not working

- Verify SMTP settings are correct
- Check if email is being blocked by firewall
- Try using Gmail with app password
- Check `bot.log` for email errors

### DeepSeek API errors

- Verify `OPENROUTER_API_KEY` is correct
- Check API quota/limits
- Verify internet connectivity
- Review `bot.log` for specific errors

### Database errors

- Ensure write permissions in project directory
- For PostgreSQL, verify connection string
- Check database server is running

## Running as a Service

### Linux (systemd)

Create `/etc/systemd/system/gitinsky-bot.service`:

```ini
[Unit]
Description=Gitinsky Support Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/gitinsky-supportbot-tg
Environment="PATH=/path/to/gitinsky-supportbot-tg/venv/bin"
ExecStart=/path/to/gitinsky-supportbot-tg/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable gitinsky-bot
sudo systemctl start gitinsky-bot
sudo systemctl status gitinsky-bot
```

### Windows (NSSM)

1. Download [NSSM](https://nssm.cc/)
2. Install as service:
   ```powershell
   nssm install GitinskyBot "C:\path\to\venv\Scripts\python.exe" "C:\path\to\main.py"
   nssm set GitinskyBot AppDirectory "C:\path\to\gitinsky-supportbot-tg"
   nssm start GitinskyBot
   ```

## Updating the Bot

1. Stop the bot
2. Pull latest changes (if using Git)
3. Activate virtual environment
4. Update dependencies: `pip install -r requirements.txt --upgrade`
5. Run database migrations if needed
6. Restart the bot

## Adding New Technologies

To add new technology documentation:

1. Edit `populate_knowledge.py`
2. Add new entry to `knowledge_entries` list
3. Run: `python populate_knowledge.py`

Or use the admin interface (if implemented).

## Security Recommendations

1. **Never commit `.env` file** - It contains sensitive credentials
2. **Use strong passwords** for email and API keys
3. **Restrict admin access** - Only add trusted user IDs
4. **Keep dependencies updated** - Run `pip install -r requirements.txt --upgrade` regularly
5. **Monitor logs** - Check `bot.log` for suspicious activity
6. **Use HTTPS** - All API communications use HTTPS by default
7. **Backup database** - Regularly backup `gitinsky_bot.db`

## Support

For issues or questions:
1. Check `bot.log` for error messages
2. Review this setup guide
3. Check the design document
4. Contact your system administrator

## Next Steps

After setup:
1. Populate knowledge base with company-specific information
2. Add verified users
3. Monitor bot performance
4. Gather user feedback
5. Continuously improve knowledge base
