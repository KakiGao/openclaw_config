#!/usr/bin/env python3
"""OpenClaw Git Backup - 完整备份脚本"""

import subprocess
import os
import json
import shutil
from datetime import datetime
from pathlib import Path

BACKUP_DIR = Path(__file__).parent.parent
SKILLS_DIR = Path("/Users/kaki/.nvm/versions/node/v22.14.0/lib/node_modules/openclaw/skills")

def clean_openclaw_json():
    """清理openclaw.json中的敏感信息"""
    with open('openclaw.json', 'r') as f:
        config = json.load(f)
    
    # 清理 API keys
    for provider in ['minimax', 'openai', 'anthropic', 'minimax-portal']:
        if 'models' in config and 'providers' in config['models']:
            if provider in config['models']['providers']:
                config['models']['providers'][provider]['apiKey'] = '${API_KEY}'
    if 'channels' in config and 'discord' in config['channels']:
        config['channels']['discord']['token'] = '${DISCORD_BOT_TOKEN}'
    
    with open('openclaw.json', 'w') as f:
        json.dump(config, f, indent=2)
    print("✅ 清理 openclaw.json")

def sync_workspace():
    """同步workspace目录"""
    src = Path(os.path.expanduser('~/.openclaw/workspace'))
    dst = BACKUP_DIR / 'workspace'
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, dirs_exist_ok=True)
    
    # 删除.git
    for f in dst.rglob('.git*'):
        f.unlink() if f.is_file() else shutil.rmtree(f)
    print(f"✅ 同步 workspace/ ({len(list(dst.rglob('*')))} 个文件)")

def sync_skills():
    """同步所有skills"""
    dst = BACKUP_DIR / 'skills'
    if dst.exists():
        shutil.rmtree(dst)
    
    # 只复制有SKILL.md的目录
    os.makedirs(dst, exist_ok=True)
    count = 0
    for item in SKILLS_DIR.iterdir():
        if item.is_dir() and (item / 'SKILL.md').exists():
            # 排除一些大文件
            if item.name not in ['node_modules', '.git']:
                shutil.copytree(item, dst / item.name, dirs_exist_ok=True)
                count += 1
    
    print(f"✅ 同步 skills/ ({count} 个技能)")

def sync_cron():
    """同步cron"""
    src = Path(os.path.expanduser('~/.openclaw/cron'))
    dst = BACKUP_DIR / 'cron'
    if dst.exists():
        shutil.rmtree(dst)
    if src.exists():
        shutil.copytree(src, dst, dirs_exist_ok=True)
    print("✅ 同步 cron/")

def git_commit_push():
    """Git提交和推送"""
    subprocess.run(['git', 'add', '-A'], check=True)
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    
    if not result.stdout.strip():
        print("ℹ️  无更改")
        return False
    
    msg = f"Backup: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    subprocess.run(['git', 'commit', '-m', msg], check=True)
    hash_result = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True)
    commit_hash = hash_result.stdout.strip()[:7]
    subprocess.run(['git', 'push', '-f', 'origin', 'main'], check=True)
    print(f"✅ 提交: {msg} ({commit_hash})")
    return True

def main():
    print("="*50)
    print("🚀 OpenClaw 完整备份")
    print("="*50)
    
    os.chdir(BACKUP_DIR)
    
    clean_openclaw_json()
    sync_workspace()
    sync_skills()
    sync_cron()
    git_commit_push()
    
    print("="*50)
    print("✅ 备份完成！")

if __name__ == "__main__":
    main()
