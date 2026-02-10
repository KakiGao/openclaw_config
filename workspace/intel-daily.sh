#!/bin/bash
# intel-daily.sh - Daily AI Intelligence Briefing (6 Sources)

COOKIE_FILE="$HOME/.bird_cookies.json"

load_cookies() {
    if [ -f "$COOKIE_FILE" ]; then
        AUTH=$(python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('auth_token',''))" < "$COOKIE_FILE" 2>/dev/null)
        CT0=$(python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('ct0',''))" < "$COOKIE_FILE" 2>/dev/null)
        echo "--auth-token $AUTH --ct0 $CT0"
    fi
}

echo "## 🌐 AI 情报日报 - $(date +%Y-%m-%d)"
echo ""

# X/Twitter Part 1: AI Agents
echo "### 🐦 AI Agents 动态"
python3 << 'PYEOF' 2>/dev/null
import subprocess, os, re, json

cookie_file = os.path.expanduser('~/.bird_cookies.json')
if os.path.exists(cookie_file):
    with open(cookie_file) as f:
        cookies = json.load(f)
        auth = cookies.get('auth_token', '')
        ct0 = cookies.get('ct0', '')
else:
    auth = ct0 = ''

result = subprocess.run(
    ['bird', 'search', 'AI Agents', '-n', '8', '--auth-token', auth, '--ct0', ct0],
    capture_output=True, text=True, timeout=30
)

lines = result.stdout.strip().split('\n')
i = 0
count = 0
while i < len(lines) and count < 8:
    line = lines[i].strip()
    if line.startswith('@') and '(' in line:
        handle = line.split('(')[0].strip()
        i += 1
        content = ''
        url = ''
        while i < len(lines):
            next_line = lines[i].strip()
            if next_line.startswith('---'):
                break
            if '🔗' in next_line:
                url = next_line.replace('🔗', '').strip()
                break
            if next_line and not content:
                content = next_line[:150] + ('...' if len(next_line) > 150 else '')
            i += 1
        if content:
            print(f"  - **{handle}**: {content}")
            if url:
                print(f"    - 🔗 {url}")
            count += 1
    i += 1
PYEOF

# X/Twitter Part 2: AI Tools
echo ""
echo "### 🛠️ AI Tools 新品"
python3 << 'PYEOF' 2>/dev/null
import subprocess, os, re, json

cookie_file = os.path.expanduser('~/.bird_cookies.json')
if os.path.exists(cookie_file):
    with open(cookie_file) as f:
        cookies = json.load(f)
        auth = cookies.get('auth_token', '')
        ct0 = cookies.get('ct0', '')
else:
    auth = ct0 = ''

result = subprocess.run(
    ['bird', 'search', '"AI tools" -filter:retweets', '-n', '3', '--auth-token', auth, '--ct0', ct0],
    capture_output=True, text=True, timeout=30
)

lines = result.stdout.strip().split('\n')
i = 0
count = 0
while i < len(lines) and count < 3:
    line = lines[i].strip()
    if line.startswith('@') and '(' in line:
        handle = line.split('(')[0].strip()
        i += 1
        content = ''
        url = ''
        while i < len(lines):
            next_line = lines[i].strip()
            if next_line.startswith('---'):
                break
            if '🔗' in next_line:
                url = next_line.replace('🔗', '').strip()
                break
            if next_line and not content:
                content = next_line[:150] + ('...' if len(next_line) > 150 else '')
            i += 1
        if content:
            print(f"  - **{handle}**: {content}")
            if url:
                print(f"    - 🔗 {url}")
            count += 1
    i += 1
PYEOF

echo ""
echo "### 📰 Hacker News"
python3 -c "
import json,urllib.request
for i in json.load(urllib.request.urlopen('https://hacker-news.firebaseio.com/v0/topstories.json'))[:5]:
    d=json.load(urllib.request.urlopen(f'https://hacker-news.firebaseio.com/v0/item/{i}.json'))
    u=d.get('url',f'https://news.ycombinator.com/item?id={i}')
    print(f'  - [{d.get(\"title\",\"\")}]({u})')
"
echo ""
echo "### 💻 GitHub Trending (Python)"
python3 -c "
import urllib.request,json
d=__import__('datetime').date.today()
r=urllib.request.urlopen(f'https://api.github.com/search/repositories?q=language:python+created:>={d.year}-{d.month:02d}-{d.day-7:02d}', timeout=10).read().decode()
for item in json.loads(r)['items'][:5]:
    print(f'  - [{item[\"full_name\"]}]({item[\"html_url\"]})')
    desc=item.get('description','')
    lang=item.get('language','')
    stars=item.get('stargazers_count',0)
    if desc: print(f'    - {desc[:80]}' + ('...' if len(desc)>80 else ''))
    print(f'    - ⭐ {stars} | 🐍 {lang}')
"
echo ""
echo "### 🔬 ArXiv AI Papers"
python3 -c "
import urllib.request,xml.etree.ElementTree as ET
r=urllib.request.urlopen('http://export.arxiv.org/api/query?search_query=cat:cs.AI&start=0&max_results=5', timeout=10).read().decode()
for e in ET.fromstring(r).findall('{http://www.w3.org/2005/Atom}entry')[:5]:
    t=e.find('{http://www.w3.org/2005/Atom}title').text.strip().replace(chr(10),' ')
    l=e.find('{http://www.w3.org/2005/Atom}id').text
    print('  - [' + t[:55] + '...](' + l + ')')
"
echo ""
echo "---"
echo "*🕐 $(date +%H:%M) | 每日 9:00 自动发送 | 6 数据源*"
