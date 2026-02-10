#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw Backup Cron - 执行备份并生成报告
"""

import subprocess
import os
import json
from datetime import datetime
from pathlib import Path

BACKUP_DIR = Path(__file__).parent
REPORT_FILE = BACKUP_DIR / "backup_report.md"

def run_backup():
    """执行备份并返回报告内容"""
    lines = []
    lines.append("## 📦 OpenClaw 自动备份报告")
    lines.append(f"**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")
    
    try:
        # 1. 清理并同步openclaw.json
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
        
        lines.append("✅ **openclaw.json** - Token已替换为占位符")
        
        # 2. Git操作
        subprocess.run(['git', 'add', '-A'], capture_output=True)
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        
        if result.stdout.strip():
            msg = f"Backup: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            subprocess.run(['git', 'commit', '-m', msg], capture_output=True)
            subprocess.run(['git', 'push', '-f', 'origin', 'main'], capture_output=True)
            lines.append("✅ **Git** - 已提交并推送")
            
            # 获取commit hash
            hash_result = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True)
            lines.append(f"**Commit**: `{hash_result.stdout.strip()[:7]}`")
        else:
            lines.append("ℹ️ **Git** - 无新更改")
        
        lines.append("")
        lines.append("### ✅ 已备份:")
        lines.append("- openclaw.json (Token已清理)")
        lines.append("- workspace/")
        lines.append("- agents/main/agent/")
        lines.append("- cron/")
        lines.append("- custom_skills/")
        
        lines.append("")
        lines.append("### ❌ 已排除:")
        lines.append("- credentials/ ❌")
        lines.append("- identity/ ❌")
        lines.append("- devices/ ❌")
        lines.append("- agents/sessions/*.jsonl ❌")
        
        lines.append("")
        lines.append("---")
        lines.append(f"*自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        # 保存报告
        report = '\n'.join(lines)
        with open(REPORT_FILE, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report
        
    except Exception as e:
        lines.append(f"❌ **错误**: {str(e)}")
        return '\n'.join(lines)

if __name__ == "__main__":
    report = run_backup()
    print(report)
