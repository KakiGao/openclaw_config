# OpenClaw Configuration Backup

Version-controlled backup of OpenClaw configurations with full history tracking.

## 📁 Repository Structure

```
├── openclaw.json              # Main OpenClaw configuration
├── agents/                   # Agent configurations
│   └── main/
│       └── agent/            # Agent settings (models only, no auth)
├── workspace/                # Personalization
│   ├── SOUL.md              # AI persona
│   ├── USER.md              # User preferences
│   ├── MEMORY.md            # Long-term memory
│   ├── IDENTITY.md          # AI identity
│   ├── AGENTS.md            # Agent notes
│   └── *.md                 # Other workspace files
├── cron/                    # Scheduled tasks
├── custom_skills/           # Custom OpenClaw skills
├── SKILL.md                 # OpenClaw Git Backup skill documentation
├── backup.sh               # Backup script
└── restore.sh              # Restore script
```

## 🔐 Sensitive Data (Excluded)

The following are **NOT** tracked in Git to protect sensitive information:

- `credentials/` - Authentication tokens and pairing files
- `identity/` - Device authentication keys
- `devices/` - Paired device information
- `agents/main/sessions/*.jsonl` - Session history with API keys
- `*.jsonl.lock` - Session lock files
- `auth-profiles.json` - Authentication profiles
- Any file containing secrets or tokens

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
| Configuration | Main settings (tokens as placeholders) | ✅ |
| Skills | Custom skills | ✅ |
| Workspace | Personalization (SOUL, USER, MEMORY, etc.) | ✅ |
| Crons | Scheduled tasks | ✅ |
| Models Config | Agent model configurations | ✅ |
| Credentials | Sensitive tokens | ❌ |
| Identity | Device authentication | ❌ |
| Devices | Paired devices | ❌ |
| Sessions | API keys and history | ❌ |

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

Create a `.env` file for sensitive configuration (NOT tracked in Git):

```bash
# OpenClaw API Keys (DO NOT commit real values)
OPENAI_API_KEY=${OPENAI_API_KEY}
DISCORD_BOT_TOKEN=${DISCORD_BOT_TOKEN}
MINIMAX_API_KEY=${MINIMAX_API_KEY}
GITHUB_TOKEN=${GITHUB_TOKEN}
```

**Note**: The `openclaw.json` uses placeholders like `${API_KEY}` - replace these with real values when restoring.

### Custom Skills

Add custom skills to `custom_skills/` directory. They will be included in the backup.

## 📝 Notes

- **API Keys**: Use environment variables or `.env` file. Do not commit real keys.
- **Restoration**: After restore, restart OpenClaw Gateway to apply changes.
- **Verification**: Always verify critical configurations after restoration.
- **Security**: Sensitive directories (credentials, identity, devices) are excluded from Git tracking.

## 🔗 Related

- OpenClaw Documentation: https://docs.openclaw.ai
- GitHub: https://github.com/openclaw/openclaw
