#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unified Intelligence Fetcher - 8 Data Sources
Combines news aggregation with local sensors.
Outputs: Discord-ready summary with links + summaries.

Sources:
- X/Twitter (bird CLI) ✅
- Hacker News
- GitHub Trending
- Product Hunt
- ArXiv AI
- V2EX
- XHS
- Chrome Web Store
"""

import sys
import os
import json
import subprocess
import argparse
from datetime import datetime
from typing import Dict, List, Any

# Add scripts directory for imports
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
SENSORS_DIR = os.path.join(SCRIPTS_DIR, 'sensors')

sys.path.insert(0, SCRIPTS_DIR)
sys.path.insert(0, SENSORS_DIR)

# --- Imports: Sensors ---
SENSORS = {}

try:
    from sensors.hacker_news import fetch_hackernews
    SENSORS['hacker_news'] = {'fn': fetch_hackernews, 'name': '📰 Hacker News'}
except ImportError:
    pass

try:
    from sensors.github_trending import fetch_github_trending
    SENSORS['github'] = {'fn': fetch_github_trending, 'name': '💻 GitHub Trending'}
except ImportError:
    pass

try:
    from sensors.product_hunt import fetch_trending_products
    SENSORS['product_hunt'] = {'fn': fetch_trending_products, 'name': '🐘 Product Hunt'}
except ImportError:
    pass

try:
    from sensors.arxiv_ai import fetch_ai_papers
    SENSORS['arxiv'] = {'fn': fetch_ai_papers, 'name': '🔬 ArXiv AI'}
except ImportError:
    pass

try:
    from sensors.v2ex_radar import fetch_v2ex
    SENSORS['v2ex'] = {'fn': fetch_v2ex, 'name': '🔧 V2EX'}
except ImportError:
    pass

try:
    from sensors.xhs_radar import XHSRadar
    SENSORS['xhs'] = {'fn': None, 'name': '📕 Xiaohongshu', 'class': XHSRadar}
except ImportError:
    pass


def load_bird_cookies() -> Dict[str, str]:
    """Load bird cookies from config file."""
    cookie_file = os.path.expanduser("~/.bird_cookies.json")
    if os.path.exists(cookie_file):
        try:
            with open(cookie_file, 'r') as f:
                data = json.load(f)
                return {
                    'auth_token': data.get('auth_token', ''),
                    'ct0': data.get('ct0', '')
                }
        except:
            pass
    return {}


def fetch_x_twitter(limit: int = 10) -> List[Dict]:
    """Fetch X/Twitter trends using bird CLI."""
    cookies = load_bird_cookies()
    
    if not cookies.get('auth_token') or not cookies.get('ct0'):
        return [{'title': '⚠️ X/Twitter 未配置', 'url': '#', 'posts': '请运行 bird-cookie-set'}]
    
    cmd = [
        'bird', 'news', '--ai-only', f'-n', str(limit),
        '--auth-token', cookies['auth_token'],
        '--ct0', cookies['ct0']
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return parse_bird_output(result.stdout)
    except Exception as e:
        return [{'title': f'❌ 获取失败: {e}', 'url': '#', 'posts': ''}]
    
    return [{'title': '⚠️ X/Twitter 趋势获取失败', 'url': '#', 'posts': '请检查 Cookie 是否有效'}]


def parse_bird_output(output: str) -> List[Dict]:
    """Parse bird CLI output to structured format."""
    items = []
    lines = output.strip().split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('[') and ']' in line:
            # Parse: [Category] Title | time | posts
            parts = line.split('|')
            title = parts[0].split(']')[1].strip() if ']' in parts[0] else line
            time = parts[1].strip() if len(parts) > 1 else ''
            posts = parts[2].strip() if len(parts) > 2 else ''
            
            # Extract trend ID from URL if present
            trend_id = ''
            if 'twitter://trending/' in line:
                trend_id = line.split('twitter://trending/')[-1].strip()
            
            items.append({
                'title': title,
                'url': f'https://x.com/i/trends/{trend_id}' if trend_id else '#',
                'posts': posts,
                'time': time
            })
        i += 1
    
    return items


class IntelCollector:
    """Unified intelligence collector."""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        
    def _load_config(self, path: str = None) -> Dict:
        if path is None:
            path = os.path.join(os.path.dirname(__file__), 'config.json')
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {}
    
    def fetch_all_sources(self, limit: int = 10) -> Dict[str, List[Any]]:
        """Fetch intelligence from all 8 sources."""
        intel = {}
        
        # 0. X/Twitter (bird CLI) ✅
        print("  🐦 Fetching X/Twitter Trends...")
        intel['twitter'] = fetch_x_twitter(limit)
        
        # 1-7. Other sensors
        for key, info in SENSORS.items():
            print(f"  {info['name']}...")
            try:
                if 'fn' in info and info['fn']:
                    intel[key] = info['fn'](limit)
                elif 'class' in info and self.config.get('XHS_COOKIE'):
                    sensor = info['class'](self.config.get('XHS_COOKIE'))
                    intel[key] = sensor.fetch_xhs_intel(limit)
                else:
                    intel[key] = [{'title': '⚠️ 未配置', 'url': '#'}]
            except Exception as e:
                intel[key] = [{'title': f'❌ 获取失败: {e}', 'url': '#'}]
        
        return intel
    
    def format_for_discord(self, intel: Dict, date_str: str = None) -> str:
        """Generate Discord-ready summary with links + summaries."""
        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        report = f"## 🌐 AI 情报日报 - {date_str}\n\n"
        
        # 🐦 X/Twitter - NEW!
        if 'twitter' in intel:
            report += "### 🐦 X/Twitter AI 趋势\n"
            for item in intel['twitter'][:5]:
                report += f"- **{item.get('title', 'N/A')}**\n"
                report += f"  - {item.get('time', '')} · {item.get('posts', '')}\n"
                if item.get('url') != '#':
                    report += f"  - 🔗 [查看趋势]({item['url']})\n"
            report += "\n"
        
        # 📰 Hacker News
        if 'hacker_news' in intel:
            report += "### 📰 Hacker News\n"
            for item in intel['hacker_news'][:5]:
                report += f"- [{item.get('title', 'N/A')}]({item.get('url', '#')})\n"
            report += "\n"
        
        # 💻 GitHub Trending
        if 'github' in intel:
            report += "### 💻 GitHub Trending\n"
            for item in intel['github'][:5]:
                report += f"- **{item.get('repo', 'N/A')}" + ("** 🔥" if item.get('stars', 0) > 100 else "**") + "\n"
                if item.get('description'):
                    report += f"  - {item['description'][:60]}...\n"
                if item.get('url'):
                    report += f"  - 🔗 [GitHub]({item['url']})\n"
            report += "\n"
        
        # 🐘 Product Hunt
        if 'product_hunt' in intel:
            report += "### 🐘 Product Hunt\n"
            for item in intel['product_hunt'][:5]:
                report += f"- **{item.get('name', 'N/A')}**\n"
                if item.get('tagline'):
                    report += f"  - {item['tagline'][:80]}\n"
                if item.get('url'):
                    report += f"  - 🔗 [查看]({item['url']})\n"
            report += "\n"
        
        # 🔬 ArXiv AI
        if 'arxiv' in intel:
            report += "### 🔬 ArXiv AI Papers\n"
            for item in intel['arxiv'][:5]:
                report += f"- [{item.get('title', 'N/A')}]({item.get('url', '#')})\n"
                if item.get('summary'):
                    report += f"  - {item['summary'][:100]}...\n"
            report += "\n"
        
        # 🔧 V2EX
        if 'v2ex' in intel:
            report += "### 🔧 V2EX 热门\n"
            for item in intel['v2ex'][:5]:
                report += f"- [{item.get('title', 'N/A')}]({item.get('url', '#')})\n"
            report += "\n"
        
        # 📕 Xiaohongshu
        if 'xhs' in intel:
            report += "### 📕 小红书\n"
            for item in intel['xhs'][:3]:
                report += f"- {item.get('title', 'N/A')}\n"
            report += "\n"
        
        report += f"---\n*🕐 更新于 {datetime.now().strftime('%H:%M')} | 8 数据源*"
        
        return report
    
    def generate_markdown_report(self, intel: Dict, date_str: str = None) -> str:
        """Generate full markdown report."""
        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        report = f"# 🌐 全球情报日报 (Global Intel Briefing)\n\n"
        report += f"**生成时间**: {date_str}\n"
        report += f"**数据源**: 8个 (X/Twitter, HN, GitHub, PH, ArXiv, V2EX, XHS, Chrome)\n\n"
        
        for source, items in intel.items():
            if items:
                source_name = SENSORS.get(source, {}).get('name', source)
                if source == 'twitter':
                    source_name = "🐦 X/Twitter AI 趋势"
                
                report += f"## {source_name}\n\n"
                for item in items[:5]:
                    if isinstance(item, dict):
                        title = item.get('title', 'N/A')
                        url = item.get('url', '#')
                        desc = item.get('description', item.get('summary', item.get('posts', '')))
                        report += f"- [{title}]({url})"
                        if desc:
                            report += f"\n  - {str(desc)[:80]}..."
                        report += "\n"
                    else:
                        report += f"- {item}\n"
                report += "\n"
        
        return report


def main():
    parser = argparse.ArgumentParser(description="AI Intelligence Collector - 8 Sources")
    parser.add_argument('--limit', type=int, default=10, help='Items per source')
    parser.add_argument('--output', type=str, help='Output file path (markdown)')
    parser.add_argument('--discord', action='store_true', help='Output for Discord')
    args = parser.parse_args()
    
    collector = IntelCollector()
    
    print("🚀 Starting Intel Collection (8 sources)...")
    intel = collector.fetch_all_sources(limit=args.limit)
    
    if args.discord:
        output = collector.format_for_discord(intel)
    else:
        output = collector.generate_markdown_report(intel)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"\n✅ Report saved to: {args.output}")
    else:
        print("\n" + output)


if __name__ == "__main__":
    main()
