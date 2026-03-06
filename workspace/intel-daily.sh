#!/bin/bash
# intel-daily.sh - Daily AI Intelligence Briefing (6 Sources)
# 支持 Cookie 失效时的 Fallback 模式

COOKIE_FILE="$HOME/.bird_cookies.json"
TWITTER_SOURCE="[🔐 Cookie]"
FALLBACK_MODE=false
TWITTER_OK=true

# 检测 Cookie 是否有效
check_cookie() {
    if [ ! -f "$COOKIE_FILE" ]; then
        return 1
    fi
    
    AUTH=$(python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('auth_token',''))" < "$COOKIE_FILE" 2>/dev/null)
    CT0=$(python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('ct0',''))" < "$COOKIE_FILE" 2>/dev/null)
    
    if [ -z "$AUTH" ] || [ -z "$CT0" ]; then
        return 1
    fi
    return 0
}

load_cookies() {
    if [ -f "$COOKIE_FILE" ]; then
        AUTH=$(python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('auth_token',''))" < "$COOKIE_FILE" 2>/dev/null)
        CT0=$(python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('ct0',''))" < "$COOKIE_FILE" 2>/dev/null)
        echo "--auth-token $AUTH --ct0 $CT0"
    fi
}

echo "## 🌐 AI 情报日报 - $(date +%Y-%m-%d)"
echo ""

# 先检测 Cookie 状态
if ! check_cookie 2>/dev/null; then
    TWITTER_OK=false
    FALLBACK_MODE=true
    TWITTER_SOURCE="[⚠️ Cookie失效]"
fi

# ========== Twitter 抓取 ==========
echo "### 🐦 AI Agents 动态 $TWITTER_SOURCE"
if [ "$TWITTER_OK" = true ]; then
    COOKIE_ARGS=$(load_cookies)
    TWITTER_OUTPUT=$(python3 << PYEOF 2>&1
import subprocess, os, json, sys

cookie_file = os.path.expanduser('~/.bird_cookies.json')
if os.path.exists(cookie_file):
    with open(cookie_file) as f:
        cookies = json.load(f)
        auth = cookies.get('auth_token', '')
        ct0 = cookies.get('ct0', '')
else:
    auth = ct0 = ''

try:
    result = subprocess.run(
        ['bird', 'search', 'AI Agents', '-n', '8', '--auth-token', auth, '--ct0', ct0],
        capture_output=True, text=True, timeout=20
    )
    output = result.stdout + result.stderr
    if 'auth' in output.lower() or 'login' in output.lower() or 'credential' in output.lower() or result.returncode != 0:
        print('COOKIE_INVALID')
    else:
        print(result.stdout)
except Exception as e:
    print(f'ERROR: {e}')
PYEOF
)
    
    if echo "$TWITTER_OUTPUT" | grep -q "COOKIE_INVALID\|ERROR"; then
        echo "  ⚠️ Cookie 已过期或无效"
        TWITTER_OK=false
        FALLBACK_MODE=true
        TWITTER_SOURCE="[⚠️ Cookie失效]"
    elif [ -n "$TWITTER_OUTPUT" ]; then
        echo "$TWITTER_OUTPUT" | python3 -c "
import sys
lines = sys.stdin.read().strip().split('\n')
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
            print(f'  - **{handle}**: {content}')
            if url:
                print(f'    - 🔗 {url}')
            count += 1
    i += 1
" 2>/dev/null
    fi
fi

if [ "$TWITTER_OK" = false ]; then
    echo "  (Twitter 数据不可用 - 请更新 Cookie: bird-cookie-set)"
fi

# AI Tools
echo ""
echo "### 🛠️ AI Tools 新品 $TWITTER_SOURCE"
if [ "$TWITTER_OK" = true ]; then
    python3 << PYEOF 2>&1
import subprocess, os, json

cookie_file = os.path.expanduser('~/.bird_cookies.json')
if os.path.exists(cookie_file):
    with open(cookie_file) as f:
        cookies = json.load(f)
        auth = cookies.get('auth_token', '')
        ct0 = cookies.get('ct0', '')
else:
    auth = ct0 = ''

try:
    result = subprocess.run(
        ['bird', 'search', '"AI tools" -filter:retweets', '-n', '3', '--auth-token', auth, '--ct0', ct0],
        capture_output=True, text=True, timeout=20
    )
    output = result.stdout + result.stderr
    if 'auth' in output.lower() or 'login' in output.lower() or 'credential' in output.lower() or result.returncode != 0:
        print('COOKIE_INVALID')
    else:
        print(result.stdout)
except Exception as e:
    print(f'ERROR: {e}')
PYEOF
    if [ $? -ne 0 ]; then
        echo "  ⚠️ Cookie 已过期"
    fi
else
    echo "  (Twitter 数据不可用)"
fi

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
from datetime import date, timedelta
d=date.today()
week_ago = d - timedelta(days=7)
r=urllib.request.urlopen(f'https://api.github.com/search/repositories?q=language:python+created:>={week_ago.isoformat()}', timeout=10).read().decode()
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

# 输出提醒
if [ "$TWITTER_OK" = false ]; then
    echo ""
    echo "⚠️ **Twitter Cookie 已失效**，已使用备用数据源。请运行 `bird-cookie-set` 更新认证信息。"
fi

echo ""
echo "*🕐 $(date +%H:%M) | 每日 9:00 自动发送 | 6 数据源*"
