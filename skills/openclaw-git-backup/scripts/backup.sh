#!/bin/bash
# OpenClaw Git Backup - Quick Backup Script
# Usage: ./backup.sh [remote_url]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="$SCRIPT_DIR/backup_repo"
REMOTE_URL="$1"

echo "🚀 OpenClaw Git Backup"
echo "   Backup directory: $BACKUP_DIR"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Initialize git if needed
if [ ! -d "$BACKUP_DIR/.git" ]; then
    echo "📦 Initializing git repository..."
    cd "$BACKUP_DIR"
    git init
    git branch -M main
else
    cd "$BACKUP_DIR"
    echo "✅ Git repository already exists"
fi

# Add remote if provided
if [ -n "$REMOTE_URL" ]; then
    git remote get-url origin > /dev/null 2>&1 || git remote add origin "$REMOTE_URL"
    echo "✅ Remote configured: $REMOTE_URL"
fi

# Copy OpenClaw configuration
echo "📁 Syncing files..."

# Core configuration
cp -r ~/.openclaw/openclaw.json "$BACKUP_DIR/" 2>/dev/null || true
cp -r ~/.openclaw/agents "$BACKUP_DIR/" 2>/dev/null || true

# Workspace (personalization)
cp -r ~/.openclaw/workspace "$BACKUP_DIR/" 2>/dev/null || true

# Credentials (only non-sensitive files)
mkdir -p "$BACKUP_DIR/credentials"
for file in ~/.openclaw/credentials/*.json; do
    if [ -f "$file" ] && [[ ! "$file" =~ pairing ]]; then
        cp "$file" "$BACKUP_DIR/credentials/"
        echo "  📄 $(basename $file)"
    fi
done

# Devices & Identity
cp -r ~/.openclaw/devices "$BACKUP_DIR/" 2>/dev/null || true
cp -r ~/.openclaw/identity "$BACKUP_DIR/" 2>/dev/null || true

# Cron jobs
cp -r ~/.openclaw/cron "$BACKUP_DIR/" 2>/dev/null || true

# Custom skills
if [ -d ~/.openclaw/skills ]; then
    cp -r ~/.openclaw/skills "$BACKUP_DIR/custom_skills" 2>/dev/null || true
fi

# Create .gitignore if not exists
if [ ! -f "$BACKUP_DIR/.gitignore" ]; then
    cat > "$BACKUP_DIR/.gitignore" << 'EOF'
# OpenClaw Git Backup
# Track changes, not data

*.log
*.tmp
*.bak
.DS_Store

# Skip sensitive pairing files
*pairing*
EOF
fi

# Commit changes
echo ""
echo "📝 Committing changes..."
cd "$BACKUP_DIR"
git add -A

if git diff --cached --quiet; then
    echo "  ℹ️  No changes to commit"
else
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    git commit -m "OpenClaw backup: $TIMESTAMP"
    echo "  ✅ Changes committed"
fi

# Push if remote configured
if git remote get-url origin > /dev/null 2>&1; then
    echo ""
    echo "🚀 Pushing to remote..."
    git push -u origin main
    echo "  ✅ Pushed successfully"
else
    echo ""
    echo "ℹ️  No remote configured. To add remote:"
    echo "   cd $BACKUP_DIR"
    echo "   git remote add origin git@github.com:user/repo.git"
    echo "   git push -u origin main"
fi

echo ""
echo "✅ Backup complete!"
echo ""
echo "📊 Quick commands:"
echo "   cd $BACKUP_DIR"
echo "   git log                    # View history"
echo "   git diff HEAD              # View changes"
echo "   git status                 # Current status"
