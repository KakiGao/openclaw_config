#!/usr/bin/env python3
"""
Skill Vetter - 技能安装前安全审查工具
"""

import json
import re
import subprocess
from dataclasses import dataclass
from typing import Optional, List
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


@dataclass
class VetResult:
    """审查结果"""
    skill_name: str
    source: str
    author: str
    version: str
    downloads: int = 0
    stars: int = 0
    updated: str = ""
    files_reviewed: int = 0
    red_flags: List[str] = None
    permissions_files: List[str] = None
    permissions_network: List[str] = None
    permissions_commands: List[str] = None
    risk_level: str = "UNKNOWN"
    verdict: str = "UNKNOWN"
    notes: str = ""

def fetch_github_repo_info(owner: str, repo: str) -> dict:
    """获取 GitHub 仓库信息"""
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}"
        req = Request(url, headers={"User-Agent": "Skill-Vetter"})
        with urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return {
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0),
                "updated": data.get("updated_at", "")[:10],
                "author": data.get("owner", {}).get("login", "unknown"),
            }
    except Exception as e:
        print(f"  ⚠️ 无法获取仓库信息: {e}")
        return {"stars": 0, "forks": 0, "updated": "", "author": ""}


def check_source(skill_info: dict) -> List[str]:
    """检查来源"""
    flags = []
    
    # 检查未知来源
    if not skill_info.get("author"):
        flags.append("Unknown author")
    
    # 检查 stars 过少
    if skill_info.get("stars", 0) < 10 and skill_info.get("source") == "github":
        flags.append("Low star count (potential untrusted source)")
    
    return flags


# 危险代码模式
RED_FLAGS = [
    (r"curl\s+|wget\s+", "External download (curl/wget)"),
    (r"requests\s*\([^)]*credential", "Requests credentials"),
    (r"api[_-]?key|auth[_-]?token|password|secret", "Accesses credentials/API keys"),
    (r"~\/\.ssh|~\/\.aws|~\/\.config", "Accesses sensitive directories"),
    (r"MEMORY\.md|USER\.md|SOUL\.md|IDENTITY\.md", "Accesses personal/agent files"),
    (r"base64\.(decode|encode|decoding)", "Base64 encoding/decoding"),
    (r"\beval\s*\(|\bexec\s*\(|\bos\.system", "Dynamic code execution"),
    (r"chmod\s+[4677]|chown\s+|sudo", "System permission changes"),
    (r"\bps\s+aux\b.*\bgrep\b.*\bkill\b", "Process listing/killing"),
    (r"\.ssh|\.aws|credentials|secrets|keys", "Credential/access patterns"),
    (r"obfuscated|encoded|encrypted", "Obfuscated/encoded code"),
    (r"<script[^>]*>.*?document\.cookie", "Cookie access"),
    (r"spawn\s*\([^)]*\bexec\b|child_process", "Child process spawning"),
    (r"os\.remove|fs\.unlink|rm\s+-", "File deletion"),
    (r">\s*\/etc\/|>~\/\.|>>\s*~", "System file modification"),
]


def analyze_code(content: str) -> List[str]:
    """分析代码内容，检查危险模式"""
    flags = []
    for pattern, desc in RED_FLAGS:
        if re.search(pattern, content, re.IGNORECASE):
            flags.append(desc)
    return flags


def classify_risk(red_flags: List[str], files: List[str], network: List[str]) -> str:
    """分类风险等级"""
    if not red_flags:
        if not files and not network:
            return "🟢 LOW"
        return "🟢 LOW"
    
    high_risk = ["credential", "password", "secret", "token", "sudo", "eval", "exec"]
    extreme_risk = ["~/.ssh", "~/.aws", "~/.config", "credentials", "secrets", "keys"]
    
    for flag in red_flags:
        flag_lower = flag.lower()
        if any(r in flag_lower for r in extreme_risk):
            return "⛔ EXTREME"
        if any(r in flag_lower for r in high_risk):
            return "🔴 HIGH"
    
    return "🟡 MEDIUM"


def generate_report(result: VetResult) -> str:
    """生成审查报告"""
    report = f"""
SKILL VETTING REPORT
═══════════════════════════════════════
Skill: {result.skill_name}
Source: {result.source}
Author: {result.author}
Version: {result.version}
───────────────────────────────────────
METRICS:
• Stars/Downloads: ⭐ {result.stars}
• Last Updated: {result.updated}
• Files Reviewed: {result.files_reviewed}
───────────────────────────────────────
"""
    
    if result.red_flags:
        report += f"RED FLAGS:\n⚠️  " + "\n⚠️  ".join(result.red_flags) + "\n"
    else:
        report += "RED FLAGS: ✅ None\n"
    
    report += f"""
PERMISSIONS NEEDED:
• Files: {', '.join(result.permissions_files) if result.permissions_files else 'None'}
• Network: {', '.join(result.permissions_network) if result.permissions_network else 'None'}
• Commands: {', '.join(result.permissions_commands) if result.permissions_commands else 'None'}
───────────────────────────────────────
RISK LEVEL: {result.risk_level}

VERDICT: {result.verdict}
NOTES: {result.notes}
═══════════════════════════════════════
"""
    return report


def vet_skill(skill_name: str, source: str, repo_url: str = None) -> str:
    """
    主函数：审查技能
    
    Args:
        skill_name: 技能名称
        source: 来源 (github/clawhub/local)
        repo_url: GitHub 仓库URL (可选)
    
    Returns:
        审查报告
    """
    result = VetResult(
        skill_name=skill_name,
        source=source,
        author="Unknown",
        version="1.0.0",
        red_flags=[],
        permissions_files=[],
        permissions_network=[],
        permissions_commands=[],
    )
    
    print(f"\n🔍 Vetting skill: {skill_name}")
    print(f"   Source: {source}")
    
    # Step 1: 获取来源信息
    if source == "github" and repo_url:
        # 解析 GitHub URL
        match = re.match(r"github\.com/([^/]+)/([^/]+)", repo_url)
        if match:
            owner, repo = match.groups()
            repo = repo.replace(".git", "").replace("/tree/main", "").replace("/tree/master", "")
            info = fetch_github_repo_info(owner, repo)
            result.author = info.get("author", "unknown")
            result.stars = info.get("stars", 0)
            result.updated = info.get("updated", "")
    
    # Step 2: 检查来源风险
    source_flags = check_source({
        "source": source,
        "author": result.author,
        "stars": result.stars,
    })
    result.red_flags.extend(source_flags)
    
    # Step 3: 分析 SKILL.md
    print(f"\n📄 Analyzing SKILL.md...")
    
    # 获取 SKILL.md 内容
    skill_md_url = None
    if source == "github" and repo_url:
        skill_md_url = repo_url.replace("github.com", "raw.githubusercontent.com")
        if not skill_md_url.endswith("/"):
            skill_md_url += "/"
        skill_md_url += "main/skills/" + skill_name + "/SKILL.md"
    
    if skill_md_url:
        try:
            req = Request(skill_md_url, headers={"User-Agent": "Skill-Vetter"})
            with urlopen(req, timeout=10) as resp:
                content = resp.read().decode()
                result.files_reviewed = 1
                
                # 分析内容
                flags = analyze_code(content)
                result.red_flags.extend(flags)
                
        except Exception as e:
            print(f"  ⚠️ 无法获取 SKILL.md: {e}")
            result.notes += f"Warning: Could not fetch SKILL.md from {skill_md_url}. "
    
    # Step 4: 风险分类
    result.risk_level = classify_risk(
        result.red_flags, 
        result.permissions_files, 
        result.permissions_network
    )
    
    # Step 5: 判定
    if "EXTREME" in result.risk_level:
        result.verdict = "❌ DO NOT INSTALL"
        result.notes += "Extreme risk detected. This skill requests access to critical system areas."
    elif "HIGH" in result.risk_level:
        result.verdict = "⚠️ HUMAN APPROVAL REQUIRED"
        result.notes += "High risk detected. Review carefully before installation."
    else:
        result.verdict = "✅ REVIEW REQUIRED"
        result.notes += "Basic review passed, but manual review still recommended."
    
    # 生成报告
    return generate_report(result)


# CLI 接口
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python skill-vetter.py <skill-name> <source> [repo-url]")
        print("\nExamples:")
        print("  python skill-vetter.py weather github https://github.com/user/weather-skill")
        print("  python skill-vetter.py notes local /path/to/skill")
        sys.exit(1)
    
    skill_name = sys.argv[1]
    source = sys.argv[2]
    repo_url = sys.argv[3] if len(sys.argv) > 3 else None
    
    report = vet_skill(skill_name, source, repo_url)
    print(report)
