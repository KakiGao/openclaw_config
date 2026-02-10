# OpenClaw Configuration Backup

Version-controlled backup of OpenClaw configurations with full history tracking.

## 📁 Repository Structure

```
├── openclaw.json              # Main OpenClaw configuration
├── agents/                   # Agent configurations
│   └── main/
│       ├── agent/            # Agent settings (models, auth)
│       └── sessions/         # Session history
├── workspace/                # Personalization
│   ├── SOUL.md              # AI persona
│   ├── USER.md              # User preferences
│   ├── MEMORY.md            # Long-term memory
│   ├── IDENTITY.md          # AI identity
│   ├── AGENTS.md            # Agent notes
│   ├── TOOLS.md             # Tool configurations
│   └── *.md                 # Other workspace files
├── credentials/              # Non-sensitive credentials
│   └── discord-allowFrom.json
├── devices/                 # Paired devices
├── identity/                # Device identity
├── cron/                    # Scheduled tasks
├── custom_skills/           # Custom OpenClaw skills
├── SKILL.md                 # OpenClaw Git Backup skill documentation
├── backup.sh               # Backup script
└── restore.sh              # Restore script
```

## 🔐 Sensitive Data (Excluded)

The following are **NOT** tracked in Git to protect sensitive information:

- `agents/main/sessions/*.jsonl` - Contains API keys and conversation history
- `credentials/*pairing*` - Authentication tokens
- `identity/*` - Device authentication keys
- API keys are stored as placeholders: `${API_KEY}`, `${DISCORD_BOT_TOKEN}`, etc.

## 🚀 Quick Start

### Initial Setup

```bash
# Clone and initialize
git clone git@github.com:KakiGao/openclaw_config.git
cd openclaw_config

# Pull latest changes
git pull origin main
```

### Manual Backup

```bash
# Run backup script
./backup.sh

# View git log
git log --oneline -10

# View changes
git diff HEAD
```

### Restore to This Machine

```bash
# Run restore script
./restore.sh

# Restart OpenClaw Gateway
openclaw gateway restart
```

## 📜 Git Workflow

### View History
```bash
git log --oneline           # Compact view
git log --patch -5          # Detailed diff
git show COMMIT_HASH        # Specific commit
```

### Compare Changes
```bash
git diff HEAD               # Uncommitted changes
git diff main..feature     # Branch comparison
git log -p --follow FILE    # File history
```

### Rollback
```bash
# Revert to previous commit
git revert COMMIT_HASH

# Restore specific file
git checkout COMMIT_HASH -- path/to/file
```

## 📊 Backup Contents

| What | Description | Tracked |
|------|-------------|---------|
| Configuration | Main settings | ✅ |
| Skills | Custom skills | ✅ |
| Workspace | Personalization | ✅ |
| Crons | Scheduled tasks | ✅ |
| Sessions | API keys inside | ❌ |
| Credentials | Sensitive tokens | ❌ |
| Device ID | Authentication | ❌ |

## 🔄 Automated Backup

This repository is backed up daily at 11:00 AM via cron job.

### Cron Configuration
```bash
# View cron jobs
crontab -l

# Daily backup at 11:00
0 11 * * * /path/to/backup.sh >> /var/log/openclaw-backup.log 2>&1
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file for sensitive configuration:

```bash
# OpenClaw API Keys
OPENAI_API_KEY=your_key
DISCORD_BOT_TOKEN=your_token
MINIMAX_API_KEY=your_key
GITHUB_TOKEN=your_token
```

### Custom Skills

Add custom skills to `custom_skills/` directory. They will be included in the backup.

## 📝 Notes

- **API Keys**: Use environment variables or `.env` file. Do not commit real keys.
- **Restoration**: After restore, restart OpenClaw Gateway to apply changes.
- **Verification**: Always verify critical configurations after restoration.

## 🔗 Related

- OpenClaw Documentation: https://docs.openclaw.ai
- GitHub: https://github.com/openclaw/openclaw
