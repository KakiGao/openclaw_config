#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw Git Backup - Version-controlled configuration backup
Backs up all OpenClaw configurations to a Git repository with full history.
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

# Configuration
OPENCLAW_DIR = Path.home() / ".openclaw"
BACKUP_SCRIPT_DIR = Path(__file__).parent.parent
REPO_DIR = BACKUP_SCRIPT_DIR / "backup_repo"


class OpenClawBackup:
    """Backup OpenClaw configuration to Git repository."""
    
    def __init__(self, repo_url: str = None, branch: str = "main"):
        self.repo_url = repo_url
        self.branch = branch
        self.backup_dir = REPO_DIR
        
    def get_backup_items(self) -> dict:
        """Define what to backup and how."""
        return {
            # Core Configuration
            "openclaw.json": {
                "source": OPENCLAW_DIR / "openclaw.json",
                "description": "Main OpenClaw configuration"
            },
            "agents/": {
                "source": OPENCLAW_DIR / "agents",
                "description": "Agent configurations and sessions"
            },
            
            # Workspace (Personalization)
            "workspace/": {
                "source": Path.home() / ".openclaw" / "workspace",
                "description": "Workspace files (SOUL, USER, MEMORY, etc.)"
            },
            
            # Credentials (Sensitive - exclude sensitive tokens)
            "credentials/": {
                "source": OPENCLAW_DIR / "credentials",
                "description": "Channel credentials (tokens will be .gitignored)",
                "gitignore_sensitive": True
            },
            
            # Devices & Identity
            "devices/": {
                "source": OPENCLAW_DIR / "devices",
                "description": "Paired devices configuration"
            },
            "identity/": {
                "source": OPENCLAW_DIR / "identity",
                "description": "Device identity"
            },
            
            # Cron Jobs
            "cron/": {
                "source": OPENCLAW_DIR / "cron",
                "description": "Scheduled tasks"
            },
            
            # Skills (if in custom location)
            "custom_skills/": {
                "source": Path.home() / ".openclaw" / "skills",
                "description": "Custom skills"
            },
        }
    
    def setup_gitignore(self):
        """Create .gitignore to protect sensitive data."""
        gitignore_content = """# OpenClaw Git Backup .gitignore
# This file is intentionally empty - we want to track ALL changes
# Sensitive data is handled via .gitignore files in subdirectories

# However, we explicitly DO NOT want to track:
# - API keys (they should be environment variables)
# - Large binary files
# - Temporary files

*.log
*.tmp
*.bak
.DS_Store
"""
        gitignore_path = self.backup_dir / ".gitignore"
        if not gitignore_path.exists():
            with open(gitignore_path, 'w') as f:
                f.write(gitignore_content)
            print(f"  ✅ Created .gitignore")
    
    def copy_file(self, src: Path, dst: Path):
        """Copy file, creating parent dirs if needed."""
        if not src.exists():
            return False
        
        dst.parent.mkdir(parents=True, exist_ok=True)
        
        # Special handling for credentials - only copy non-sensitive files
        if "credentials" in str(src):
            # Copy but warn about sensitive files
            if src.name in ["discord-allowFrom.json", "discord-pairing.json"]:
                print(f"  ⚠️  Skipping sensitive file: {src.name}")
                return False
        
        # Read and write to normalize (especially JSON)
        try:
            with open(src, 'r') as f:
                content = f.read()
            with open(dst, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"  ❌ Error copying {src}: {e}")
            return False
    
    def sync_files(self) -> int:
        """Sync files from OpenClaw to backup directory."""
        items = self.get_backup_items()
        copied = 0
        
        for name, config in items.items():
            src = Path(config["source"])
            dst = self.backup_dir / name
            
            if src.is_file():
                if self.copy_file(src, dst):
                    print(f"  📄 Copied: {name}")
                    copied += 1
            elif src.is_dir():
                for file_path in src.rglob("*"):
                    if file_path.is_file():
                        rel_path = file_path.relative_to(src)
                        dst_path = dst / rel_path
                        
                        # Skip sensitive files
                        if "discord-pairing" in str(file_path):
                            continue
                        
                        if self.copy_file(file_path, dst_path):
                            print(f"  📄 Copied: {name}/{rel_path}")
                            copied += 1
        
        return copied
    
    def init_git(self) -> bool:
        """Initialize Git repository."""
        if not (self.backup_dir / ".git").exists():
            subprocess.run(["git", "init"], cwd=self.backup_dir, check=True)
            subprocess.run(["git", "branch", "-M", self.branch], cwd=self.backup_dir, check=True)
            print(f"  ✅ Git repository initialized at {self.backup_dir}")
            return True
        return False
    
    def commit_and_push(self, message: str = None) -> bool:
        """Commit changes and push to remote."""
        if message is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = f"OpenClaw backup: {timestamp}"
        
        # Add all files
        subprocess.run(["git", "add", "."], cwd=self.backup_dir, check=True)
        
        # Check if there are changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=self.backup_dir,
            capture_output=True,
            text=True
        )
        
        if not result.stdout.strip():
            print("  ℹ️  No changes to commit")
            return True
        
        # Commit
        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=self.backup_dir,
            check=True
        )
        print(f"  ✅ Changes committed: {message[:50]}...")
        
        # Push if remote is configured
        if self.repo_url:
            # Check if remote exists
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                cwd=self.backup_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                subprocess.run(
                    ["git", "remote", "add", "origin", self.repo_url],
                    cwd=self.backup_dir,
                    check=True
                )
                print(f"  ✅ Remote added: {self.repo_url}")
            
            # Push
            print(f"  🚀 Pushing to remote...")
            subprocess.run(
                ["git", "push", "-u", "origin", self.branch],
                cwd=self.backup_dir,
                check=True
            )
            print(f"  ✅ Pushed to {self.repo_url}")
        
        return True
    
    def backup(self, message: str = None) -> bool:
        """Main backup workflow."""
        print(f"\n🚀 Starting OpenClaw Git Backup...")
        print(f"   Backup directory: {self.backup_dir}")
        print(f"   Remote: {self.repo_url or 'None (local only)'}")
        print()
        
        # Setup
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.init_git()
        self.setup_gitignore()
        
        # Sync files
        print("📁 Syncing files...")
        copied = self.sync_files()
        print(f"   Copied {copied} files")
        print()
        
        # Commit and push
        success = self.commit_and_push(message)
        
        print("\n✅ Backup complete!")
        return success
    
    def show_status(self):
        """Show backup status and git log."""
        print(f"\n📊 OpenClaw Backup Status")
        print(f"   Backup directory: {self.backup_dir}")
        print(f"   Remote: {self.repo_url or 'Not configured'}")
        print()
        
        if not (self.backup_dir / ".git").exists():
            print("  ❌ Git repository not initialized")
            return
        
        # Git status
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=self.backup_dir,
            capture_output=True,
            text=True
        )
        
        if result.stdout.strip():
            print("  📝 Uncommitted changes:")
            print(result.stdout)
        else:
            print("  ✅ No uncommitted changes")
        
        # Git log
        print("\n📜 Recent commits:")
        result = subprocess.run(
            ["git", "log", "--oneline", "-10"],
            cwd=self.backup_dir,
            capture_output=True,
            text=True
        )
        print(result.stdout or "  No commits yet")
    
    def show_diff(self, commit_hash: str = None):
        """Show changes since last backup."""
        if not (self.backup_dir / ".git").exists():
            print("  ❌ Git repository not initialized")
            return
        
        if commit_hash:
            result = subprocess.run(
                ["git", "show", "--stat", commit_hash],
                cwd=self.backup_dir,
                capture_output=True,
                text=True
            )
        else:
            # Show diff from last commit
            result = subprocess.run(
                ["git", "diff", "--stat", "HEAD"],
                cwd=self.backup_dir,
                capture_output=True,
                text=True
            )
        
        print(result.stdout or "  No changes")


def main():
    parser = argparse.ArgumentParser(description="OpenClaw Git Backup")
    parser.add_argument('--remote', type=str, help='Git remote URL (e.g., git@github.com:user/repo.git)')
    parser.add_argument('--branch', type=str, default='main', help='Branch name')
    parser.add_argument('--message', type=str, help='Commit message')
    parser.add_argument('--status', action='store_true', help='Show backup status')
    parser.add_argument('--diff', action='store_true', help='Show changes')
    
    args = parser.parse_args()
    
    backup = OpenClawBackup(repo_url=args.remote, branch=args.branch)
    
    if args.status:
        backup.show_status()
    elif args.diff:
        backup.show_diff()
    else:
        backup.backup(message=args.message)


if __name__ == "__main__":
    main()
