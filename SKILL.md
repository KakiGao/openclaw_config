---
name: openclaw-git-backup
description: Git-based version control backup for OpenClaw configurations, workspaces, and skills. Tracks all changes with full history, supports SSH authentication, and enables easy recovery and rollback.
---

# OpenClaw Git Backup

Version-controlled configuration backup for OpenClaw with full history tracking.

## 🎯 核心功能

- **完整备份**: 配置、记忆、技能、工作区
- **版本控制**: 每次备份都是一次commit，可追溯更改历史
- **SSH支持**: 通过SSH密钥自动认证
- **快速恢复**: 一键恢复到任意历史版本
- **敏感数据保护**: 自动跳过敏感凭据文件

## 📋 可用指令

### 执行备份
**触发词**: "备份" / "backup" / "git backup"

```bash
# 本地备份（无远程）
python scripts/backup.py

# 备份并推送到远程
python scripts/backup.py --remote git@github.com:user/openclaw_config.git

# 自定义commit信息
python scripts/backup.py --remote git@github.com:user/repo.git --message "更新配置"
```

**或使用快捷脚本**:
```bash
./scripts/backup.sh
./scripts/backup.sh git@github.com:KakiGao/openclaw_config.git
```

### 查看状态
**触发词**: "备份状态" / "backup status"

```bash
python scripts/backup.py --status
```

**显示**:
- 未提交的更改
- 最近commit历史
- 远程同步状态

### 查看差异
**触发词**: "备份差异" / "backup diff"

```bash
# 查看未提交的更改
python scripts/backup.py --diff

# 查看特定commit的更改
python scripts/backup.py --diff --show-ref
```

### 恢复备份
**触发词**: "恢复备份" / "restore"

```bash
./scripts/restore.sh           # 从main分支恢复
./scripts/restore.sh main      # 从指定分支恢复
```

**恢复流程**:
1. 从Git拉取最新代码
2. 确认覆盖现有文件
3. 恢复到以下位置:
   - `~/.openclaw/openclaw.json`
   - `~/.openclaw/agents/`
   - `~/.openclaw/workspace/`
   - `~/.openclaw/devices/`
   - `~/.openclaw/identity/`
   - `~/.openclaw/cron/`

## 📁 备份内容

### ✅ 会备份的内容

| 目录/文件 | 描述 | 敏感？ |
|----------|------|--------|
| `openclaw.json` | 主配置 | ✅ |
| `agents/` | Agent配置和会话 | ✅ |
| `workspace/` | 工作区文件 | ❌ |
| `devices/` | 配对设备 | ⚠️ |
| `identity/` | 设备身份 | ⚠️ |
| `cron/` | 定时任务 | ❌ |
| `custom_skills/` | 自定义技能 | ❌ |

### ❌ 不会备份的内容

- **凭据文件**: `*pairing*`, `discord-*`（敏感令牌）
- **临时文件**: `*.log`, `*.tmp`, `*.bak`
- **二进制缓存**: `node_modules/`, `__pycache__/`

## 🔐 SSH配置

### 1. 检查SSH密钥
```bash
ls -la ~/.ssh/
```

### 2. 添加SSH密钥到GitHub
1. 复制公钥:
```bash
cat ~/.ssh/id_rsa.pub
```
2. 添加到GitHub: Settings → SSH and GPG keys → New SSH key

### 3. 测试连接
```bash
ssh -T git@github.com
```

## 🚀 快速开始

### 首次设置（备份到GitHub）

```bash
# 1. 进入技能目录
cd /Users/kaki/.nvm/versions/node/v22.14.0/lib/node_modules/openclaw/skills/openclaw-git-backup

# 2. 执行备份（首次会自动创建本地仓库）
./scripts/backup.sh git@github.com:KakiGao/openclaw_config.git

# 3. 推送到GitHub
cd backup_repo
git push -u origin main
```

### 日常使用

```bash
# 每日备份（添加到cron）
crontab -e
# 添加: 0 9 * * * /path/to/backup.sh

# 或手动备份
./scripts/backup.sh --message "每日备份"
```

### 恢复到新机器

```bash
# 1. 克隆仓库
git clone git@github.com:KakiGao/openclaw_config.git openclaw-git-backup/backup_repo

# 2. 恢复文件
cd openclaw-git-backup
./scripts/restore.sh

# 3. 重启Gateway
openclaw gateway restart
```

## 📊 Git工作流

### 查看历史
```bash
cd backup_repo
git log --oneline -20          # 简洁历史
git log --patch -5             # 详细diff
git show COMMIT_HASH           # 特定commit详情
```

### 回滚到历史版本
```bash
cd backup_repo
git revert COMMIT_HASH         # 创建新commit回滚
# 或
git checkout COMMIT_HASH -- path/to/file  # 恢复特定文件
```

### 分支管理
```bash
cd backup_repo
git branch -a                  # 查看所有分支
git checkout -b backup-2024-01  # 创建备份分支
git push origin backup-2024-01  # 推送到远程
```

## ⚠️ 注意事项

1. **API密钥**: 敏感凭据不会备份到Git，请使用环境变量或 `.env` 文件
2. **大文件**: 避免备份大型二进制文件（如模型权重）
3. **频率**: 建议每日或每次重大更改后备份
4. **恢复后**: 可能需要重新认证某些服务
5. **验证**: 恢复后检查关键配置是否正确

## 🔧 故障排除

### SSH权限被拒绝
```bash
# 检查SSH代理
ssh-add -l

# 添加密钥
ssh-add ~/.ssh/id_rsa

# 使用完整路径
git remote add origin git@github.com:user/repo.git
```

### 合并冲突
```bash
# 拉取远程更改
git pull origin main --rebase

# 或手动解决冲突后
git add .
git commit -m "解决合并冲突"
```

### 文件权限
```bash
# 确保脚本可执行
chmod +x scripts/*.sh
```

## 📂 文件结构

```
openclaw-git-backup/
├── SKILL.md                   # 本文档
├── scripts/
│   ├── backup.py             # Python备份脚本（完整功能）
│   ├── backup.sh             # Bash快捷脚本
│   └── restore.sh            # 恢复脚本
└── backup_repo/              # Git仓库（首次备份后创建）
    ├── .git/
    ├── openclaw.json
    ├── agents/
    ├── workspace/
    ├── devices/
    ├── identity/
    ├── cron/
    └── custom_skills/
```

## 💡 使用示例

### 场景1：每日自动备份

```bash
# 添加到crontab
crontab -e

# 每天早上9点自动备份
0 9 * * * cd /path/to/openclaw-git-backup && ./scripts/backup.sh >> /var/log/openclaw-backup.log 2>&1
```

### 场景2：手动触发备份

```bash
cd /path/to/openclaw-git-backup

# 备份并推送到远程
./scripts/backup.sh git@github.com:KakiGao/openclaw_config.git

# 查看状态
python scripts/backup.py --status
```

### 场景3：恢复到特定版本

```bash
cd /path/to/openclaw-git-backup/backup_repo

# 查看历史
git log --oneline -10

# 恢复到某个commit
git checkout abc1234

# 恢复文件
./scripts/restore.sh

# 重启Gateway
openclaw gateway restart
```
