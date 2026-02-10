#!/bin/bash
# OpenClaw Git Restore - Restore from Git backup
# Usage: ./restore.sh [branch]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="$SCRIPT_DIR/backup_repo"
BRANCH="${1:-main}"

echo "🔄 OpenClaw Git Restore"
echo "   Source: $BACKUP_DIR"
echo "   Branch: $BRANCH"

# Check if backup exists
if [ ! -d "$BACKUP_DIR/.git" ]; then
    echo "❌ Error: No git repository found at $BACKUP_DIR"
    echo "   Please run backup.sh first"
    exit 1
fi

# Pull latest changes
cd "$BACKUP_DIR"
echo ""
echo "📥 Pulling latest changes..."
git pull origin "$BRANCH" || git pull

# Confirm before restoring
echo ""
echo "⚠️  This will OVERWRITE the following files:"
echo "   - ~/.openclaw/openclaw.json"
echo "   - ~/.openclaw/agents/"
echo "   - ~/.openclaw/workspace/"
echo "   - ~/.openclaw/devices/"
echo "   - ~/.openclaw/identity/"
echo "   - ~/.openclaw/cron/"
echo "   - ~/.openclaw/skills/ (custom only)"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled"
    exit 0
fi

# Restore files
echo ""
echo "📦 Restoring files..."

# Core configuration
cp -f "$BACKUP_DIR/openclaw.json" ~/.openclaw/ 2>/dev/null && echo "  ✅ openclaw.json" || true
cp -rf "$BACKUP_DIR/agents/" ~/.openclaw/ 2>/dev/null && echo "  ✅ agents/" || true
cp -rf "$BACKUP_DIR/workspace/" ~/.openclaw/ 2>/dev/null && echo "  ✅ workspace/" || true

# Devices & Identity
cp -rf "$BACKUP_DIR/devices/" ~/.openclaw/ 2>/dev/null && echo "  ✅ devices/" || true
cp -rf "$BACKUP_DIR/identity/" ~/.openclaw/ 2>/dev/null && echo "  ✅ identity/" || true

# Cron jobs
cp -rf "$BACKUP_DIR/cron/" ~/.openclaw/ 2>/dev/null && echo "  ✅ cron/" || true

# Custom skills
if [ -d "$BACKUP_DIR/custom_skills" ]; then
    mkdir -p ~/.openclaw/skills
    cp -rf "$BACKUP_DIR/custom_skills/"* ~/.openclaw/skills/ 2>/dev/null && echo "  ✅ custom_skills/" || true
fi

echo ""
echo "✅ Restore complete!"
echo ""
echo "⚠️  Important:"
echo "   - Restart OpenClaw Gateway to apply changes"
echo "   - Some services may require re-authentication"
echo "   - API keys may need to be reconfigured"
