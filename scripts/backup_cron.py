#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw Git Backup - Cron Job Script
Automatically backs up OpenClaw configs and posts report to Discord.
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

# Configuration
BACKUP_SCRIPT_DIR = Path(__file__).parent.parent
BACKUP_DIR = BACKUP_SCRIPT_DIR
REPORT_FILE = BACKUP_SCRIPT_DIR / "backup_report.md"
LOG_FILE = BACKUP_SCRIPT_DIR / "backup.log"


class BackupCron:
    """Automated backup job for cron."""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def run_backup(self) -> dict:
        """Run git backup and capture output."""
        result = {
            "success": False,
            "files_changed": 0,
            "commit_hash": None,
            "error": None
        }
        
        try:
            # Run git add
            subprocess.run(["git", "add", "-A"], cwd=BACKUP_DIR, check=True, capture_output=True)
            
            # Check for changes
            diff_result = subprocess.run(
                ["git", "diff", "--cached", "--stat"],
                cwd=BACKUP_DIR,
                capture_output=True,
                text=True
            )
            
            if not diff_result.stdout.strip():
                result["success"] = True
                result["message"] = "No changes to commit"
                return result
            
            # Count files changed
            lines = diff_result.stdout.strip().split('\n')
            for line in lines:
                if 'changed' in line or 'insertion' in line or 'deletion' in line:
                    try:
                        result["files_changed"] = int(line.split()[0])
                    except:
                        pass
            
            # Commit
            commit_msg = f"Auto backup: {self.timestamp}"
            subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=BACKUP_DIR,
                check=True,
                capture_output=True
            )
            
            # Get commit hash
            hash_result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=BACKUP_DIR,
                capture_output=True,
                text=True
            )
            result["commit_hash"] = hash_result.stdout.strip()[:7]
            result["success"] = True
            
            # Push
            push_result = subprocess.run(
                ["git", "push", "origin", "main"],
                cwd=BACKUP_DIR,
                capture_output=True,
                text=True
            )
            
            if push_result.returncode != 0:
                result["error"] = push_result.stderr
                
        except subprocess.CalledProcessError as e:
            result["error"] = str(e)
            
        return result
    
    def generate_report(self, result: dict) -> str:
        """Generate Discord-formatted report."""
        lines = [
            "## 📦 OpenClaw 自动备份报告",
            f"**时间**: {self.timestamp}",
            ""
        ]
        
        if result["success"]:
            lines.append("✅ **状态**: 备份成功")
            
            if result["files_changed"] > 0:
                lines.append(f"📁 **更改文件数**: {result['files_changed']}")
            else:
                lines.append("ℹ️ **状态**: 无新更改")
            
            if result["commit_hash"]:
                lines.append(f"🔗 **Commit**: `{result['commit_hash']}`")
            
            # Git log
            log_result = subprocess.run(
                ["git", "log", "--oneline", "-5"],
                cwd=BACKUP_DIR,
                capture_output=True,
                text=True
            )
            
            if log_result.stdout.strip():
                lines.append("")
                lines.append("📜 **最近提交**:")
                for line in log_result.stdout.strip().split('\n')[:5]:
                    lines.append(f"> {line}")
            
        else:
            lines.append("❌ **状态**: 备份失败")
            if result["error"]:
                lines.append(f"**错误**: {result['error'][:200]}")
        
        # Git diff summary
        lines.append("")
        lines.append("📊 **更改统计**:")
        
        diff_result = subprocess.run(
            ["git", "diff", "--stat", "HEAD~1"],
            cwd=BACKUP_DIR,
            capture_output=True,
            text=True
        )
        
        if diff_result.stdout.strip():
            lines.append("```")
            lines.append(diff_result.stdout.strip())
            lines.append("```")
        
        return '\n'.join(lines)
    
    def save_report(self, report: str):
        """Save report to file."""
        with open(REPORT_FILE, 'w', encoding='utf-8') as f:
            f.write(f"# OpenClaw Backup Report - {self.timestamp}\n\n")
            f.write(report)
    
    def run(self):
        """Execute cron job."""
        # Log start
        with open(LOG_FILE, 'a') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Backup started: {self.timestamp}\n")
        
        # Run backup
        result = self.run_backup()
        
        # Generate report
        report = self.generate_report(result)
        self.save_report(report)
        
        # Print for Discord webhook
        print(report)
        
        # Log end
        status = "SUCCESS" if result["success"] else "FAILED"
        with open(LOG_FILE, 'a') as f:
            f.write(f"Backup completed: {status}\n")
            f.write(f"Files changed: {result['files_changed']}\n")
        
        return result["success"]


if __name__ == "__main__":
    cron = BackupCron()
    success = cron.run()
    sys.exit(0 if success else 1)
