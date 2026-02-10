#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw Git Backup - 完整备份脚本
确保每次都完整同步所有文件
"""

import subprocess
import os
import json
import shutil
from datetime import datetime
from pathlib import Path

BACKUP_DIR = Path(__file__).parent.parent

def clean_openclaw_json():
    """清理openclaw.json中的敏感信息"""
    with open('openclaw.json', 'r') as f:
        config = json.load(f)
    
    for provider in ['minimax', 'openai', 'anthropic', 'minimax-portal']:
        if 'models' in config and 'providers' in config['models']:
            if provider in config['models']['providers']:
                config['models']['providers'][provider]['apiKey'] = '${API_KEY}'
    if 'channels' in config and 'discord' in config['channels']:
        config['channels']['discord']['token'] = '${DISCORD_BOT_TOKEN}'
    
    with open('openclaw.json', 'w') as f:
        json.dump(config, f, indent=2)
    print("✅ 清理 openclaw.json (Token替换为占位符)")

def sync_workspace():
    """完整同步workspace目录"""
    src_workspace = Path(os.path.expanduser('~/.openclaw/workspace'))
    dst_workspace = BACKUP_DIR / 'workspace'
    
    # 删除旧的workspace
    if dst_workspace.exists():
        shutil.rmtree(dst_workspace)
    
    # 递归复制整个目录
    shutil.copytree(src_workspace, dst_workspace, dirs_exist_ok=True)
    
    # 删除.git目录
    git_dir = dst_workspace / '.git'
    if git_dir.exists():
        shutil.rmtree(git_dir)
    
    # 删除.gitignore
    gitignore_file = dst_workspace / '.gitignore'
    if gitignore_file.exists():
        gitignore_file.unlink()
    
    print(f"✅ 同步 workspace/ ({len(list(dst_workspace.rglob('*')))} 个文件)")

def sync_agents():
    """同步agents配置"""
    agents_dir = BACKUP_DIR / 'agents'
    
    # 删除旧的agents
    if agents_dir.exists():
        shutil.rmtree(agents_dir)
    
    # 重新创建
    os.makedirs('agents/main/agent', exist_ok=True)
    
    # 复制models.json
    shutil.copy(
        os.path.expanduser('~/.openclaw/agents/main/agent/models.json'),
        'agents/main/agent/'
    )
    
    # 删除sessions目录（包含敏感信息）
    sessions_dir = agents_dir / 'main' / 'sessions'
    if sessions_dir.exists():
        shutil.rmtree(sessions_dir)
    
    print("✅ 同步 agents/ (仅models.json，排除sessions)")

def sync_cron():
    """同步cron"""
    src_cron = Path(os.path.expanduser('~/.openclaw/cron'))
    dst_cron = BACKUP_DIR / 'cron'
    
    if dst_cron.exists():
        shutil.rmtree(dst_cron)
    
    shutil.copytree(src_cron, dst_cron, dirs_exist_ok=True)
    print("✅ 同步 cron/")

def git_commit_push():
    """Git提交和推送"""
    # 添加所有更改
    subprocess.run(['git', 'add', '-A'], check=True)
    
    # 检查状态
    result = subprocess.run(
        ['git', 'status', '--porcelain'],
        capture_output=True,
        text=True
    )
    
    if not result.stdout.strip():
        print("ℹ️  无更改需要提交")
        return False
    
    # 提交
    msg = f"Backup: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    subprocess.run(['git', 'commit', '-m', msg], check=True)
    print(f"✅ 提交: {msg}")
    
    # 获取commit hash
    hash_result = subprocess.run(
        ['git', 'rev-parse', 'HEAD'],
        capture_output=True,
        text=True
    )
    commit_hash = hash_result.stdout.strip()[:7]
    
    # 推送
    subprocess.run(['git', 'push', '-f', 'origin', 'main'], check=True)
    print(f"✅ 推送到 GitHub (commit: {commit_hash})")
    
    return True

def main():
    print("="*60)
    print("🚀 开始完整备份 - 严格排除所有ID信息")
    print("="*60)
    print()
    
    os.chdir(BACKUP_DIR)
    
    # 1. 清理并同步
    clean_openclaw_json()
    sync_workspace()
    sync_agents()
    sync_cron()
    
    print()
    
    # 2. Git操作
    changed = git_commit_push()
    
    print()
    print("="*60)
    print("📦 备份完成！")
    print()
    print("✅ 已备份:")
    print("  • openclaw.json (Token已清理)")
    print("  • workspace/ (完整同步)")
    print("  • agents/main/agent/models.json")
    print("  • cron/")
    print()
    print("❌ 已排除:")
    print("  • credentials/")
    print("  • identity/")
    print("  • devices/")
    print("  • agents/sessions/*.jsonl")
    print("  • workspace/.git")
    print("="*60)

if __name__ == "__main__":
    main()
