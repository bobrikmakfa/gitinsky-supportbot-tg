# Gitinsky Support Bot

🤖 **AI-Powered Technical Support Assistant for IT Teams**

Gitinsky Support Bot is an intelligent Telegram bot designed to provide instant technical support to company employees. Powered by DeepSeek AI and equipped with comprehensive knowledge about your technology stack, it helps answer questions, troubleshoot issues, and provide best practices guidance.

## 🌟 Features

- **🔐 Secure Email Verification**: Company domain email verification ensures only authorized employees can access the bot
- **🧠 AI-Powered Responses**: Leverages DeepSeek API for intelligent, context-aware technical assistance
- **📚 Comprehensive Knowledge Base**: Pre-loaded with documentation for 19 technology areas
- **💬 Natural Conversation**: Simple Telegram interface for easy interaction
- **📊 Interaction Logging**: Tracks queries and responses for analytics and improvement
- **👍 Feedback System**: Collect user feedback to continuously improve response quality
- **🔧 Admin Tools**: Administrative commands for user management and knowledge base updates

## 🛠️ Technology Stack Coverage

### Orchestration
- Ansible
- Kubernetes
- OpenShift
- Puppet

### Containerization
- Docker
- Docker Swarm
- Docker Compose

### Infrastructure as Code
- Terraform

### CI/CD
- Argo CD
- GitLab CI

### Monitoring & Logging
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Zabbix
- Grafana
- Prometheus

### Databases
- MySQL
- PostgreSQL

### Networking
- Cisco
- MikroTik
- Keenetic

### Operating Systems
- Linux Administration
- Windows Administration

### Programming
- Python

### System Administration
- General sysadmin practices and best practices

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Telegram bot token from [@BotFather](https://t.me/BotFather)
- DeepSeek API key
- SMTP email server access

### Installation

1. **Clone the repository**
   ```bash
   cd gitinsky-supportbot-tg
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

5. **Initialize knowledge base**
   ```bash
   python populate_knowledge.py
   ```

6. **Run the bot**
   ```bash
   python main.py
   ```

For detailed setup instructions, see [SETUP.md](SETUP.md).

## 📖 Usage

### User Commands

- `/start` - Initialize bot and see welcome message
- `/verify` - Start email verification process
- `/help` - Display available commands and usage guide
- `/status` - Check your verification status
- `/feedback` - Rate the last response

### Admin Commands

- `/admin_list_users` - View all verified users

### Asking Questions

Once verified, simply send your technical question:

**Examples:**
- "How do I deploy an application with Kubernetes?"
- "What are Ansible best practices?"
- "Help me troubleshoot Docker container issues"
- "How to set up MySQL replication?"
- "What's the best way to configure Prometheus alerts?"

## 🔒 Security Features

- **Email Domain Verification**: Only company domain emails allowed
- **Time-Limited Verification Codes**: Codes expire after 15 minutes
- **Session Management**: Auto-logout after 30 days of inactivity
- **Secure Credential Storage**: Environment-based configuration
- **Admin Access Control**: Restricted administrative functions
- **Rate Limiting**: Protection against API abuse

## 🏗️ Architecture

The bot follows a modular architecture:

```
├── main.py                 # Application entry point
├── config.py              # Configuration management
├── models.py              # Database models
├── database.py            # Database connection
├── auth.py                # Authentication service
├── email_service.py       # Email verification
├── deepseek_client.py     # DeepSeek API integration
├── knowledge_base.py      # Knowledge management
├── query_processor.py     # Query analysis and processing
├── bot.py                 # Telegram bot handler
└── populate_knowledge.py  # Knowledge base initialization
```

## 📊 Database Schema

- **Users**: Verified user profiles and sessions
- **Knowledge Entries**: Technology documentation
- **Interaction Logs**: Query/response history and analytics

## 🔧 Configuration

Key environment variables:

```env
TELEGRAM_BOT_TOKEN=your_bot_token
DEEPSEEK_API_KEY=your_api_key
SMTP_HOST=smtp.gmail.com
SMTP_USER=your_email@company.com
COMPANY_EMAIL_DOMAIN=yourcompany.com
ADMIN_TELEGRAM_IDS=123456789
```

See [.env.example](.env.example) for all options.

## 📈 Monitoring

The bot logs:
- All user interactions
- API calls and response times
- Authentication events
- Errors and warnings

Logs are stored in `bot.log` and can be integrated with your monitoring system.

## 🤝 Contributing

### Adding New Technologies

1. Edit `populate_knowledge.py`
2. Add entry to `knowledge_entries` list
3. Run `python populate_knowledge.py`

### Improving Knowledge Base

- Update existing entries with more detailed information
- Add company-specific best practices
- Include troubleshooting tips from real incidents

## 📝 License

Proprietary - Internal use only for Gitinsky employees.

## 🆘 Support

For issues:
1. Check [SETUP.md](SETUP.md) for troubleshooting
2. Review `bot.log` for errors
3. Contact your system administrator

## 🎯 Roadmap

- [ ] Multi-language support
- [ ] Integration with ticketing system
- [ ] Advanced analytics dashboard
- [ ] Voice message support
- [ ] Multimedia content in knowledge base
- [ ] Conversation context memory
- [ ] Proactive maintenance alerts

## 👥 Authors

Developed for Gitinsky IT company to enhance technical support and knowledge sharing.

---

**Made with ❤️ using Python, Telegram Bot API, and DeepSeek AI**
