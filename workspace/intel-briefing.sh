#!/bin/bash
# intel-briefing.sh - AI Intelligence Daily Briefing (8 Sources)

# Cookie for bird
COOKIE_FILE="$HOME/.bird_cookies.json"
load_cookies() {
    if [ -f "$COOKIE_FILE" ]; then
        AUTH_TOKEN=$(python3 -c "import json,sys; print(json.load(sys.stdin).get('auth_token',''))" < "$COOKIE_FILE" 2>/dev/null)
        CT0=$(python3 -c "import json,sys; print(json.load(sys.stdin).get('ct0',''))" < "$COOKIE_FILE" 2>/dev/null)
        BIRD_AUTH="--auth-token $AUTH_TOKEN --ct0 $CT0"
    else
        BIRD_AUTH=""
    fi
}

echo "🚀 Starting AI Intelligence Collection (8 sources)..."
echo ""

# === 🐦 X/Twitter (bird CLI) ===
echo "🐦 Fetching X/Twitter AI Trends..."
load_cookies
TWITTER_DATA=$(bird news --ai-only -n 10 $BIRD_AUTH 2>/dev/null | grep -E "^\[" | head -5)

# === 📰 Hacker News ===
echo "📰 Fetching Hacker News..."
HN_DATA=$(curl -s "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty" | head -10 | grep -E "^\s*[0-9]" | tr -d ' ,' | while read id; do
    curl -s "https://hacker-news.firebaseio.com/v0/item/$id.json?print=pretty" | python3 -c "
import json,sys,html
d=json.load(sys.stdin)
if d:
    title=d.get('title','')
    url=d.get('url','')
    if url:
        print(f'- [{title}]({url})')
" 2>/dev/null
done | head -5)

# === 💻 GitHub Trending ===
echo "💻 Fetching GitHub Trending..."
GH_DATA=$(curl -s "https://github.com/trending/python?since=daily" 2>/dev/null | grep -E 'class="Repo|class="Link' | head -20 | awk '
/class="Repo/{repo=$0; gsub(/.*href="|".*/, "", repo); printf "https://github.com%s ", repo}
/class="Link/{gsub(/.*">|</.*/, "", $0); print $0}
' | head -5 | while read url desc; do
    echo "- **[$(basename $url)]** - $desc"
    echo "  - 🔗 $url"
done)

# === 🐘 Product Hunt ===
echo "🐘 Fetching Product Hunt..."
PH_DATA=$(curl -s "https://www.producthunt.com/" 2>/dev/null | grep -oE '"name":"[^"]+"|"tagline":"[^"]+"' | head -12 | paste - - | head -5 | sed 's/"name":"//g;s/"tagline":"//g;s/"/ /g')

# === 🔬 ArXiv AI ===
echo "🔬 Fetching ArXiv AI Papers..."
ARXIV_DATA=$(curl -s "http://export.arxiv.org/api/query?search_query=cat:cs.AI&start=0&max_results=10" 2>/dev/null | grep -E "<title>|<id>|<summary>" | head -15 | paste - - - | head -5 | sed 's/<[^>]*>//g')

# === 🔧 V2EX ===
echo "🔧 Fetching V2EX..."
V2EX_DATA=$(curl -s "https://www.v2ex.com/?tab=hot" 2>/dev/null | grep -oE 'href="/t/[0-9]+[^"]*"' | head -5 | while read link; do
    id=$(echo $link | grep -oE '[0-9]+')
    title=$(curl -s "https://www.v2ex.com/t/$id.json" 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('title',''))" 2>/dev/null)
    echo "- $title"
    echo "  - 🔗 https://v2ex.com$link"
done)

# === 📕 Xiaohongshu (optional) ===
echo "📕 Fetching Xiaohongshu..."
XHS_DATA=$(echo "- ⚠️ 需要配置 XHS_COOKIE (可选)")

# === Generate Report ===
DATE=$(date +%Y-%m-%d)

cat << EOF
## 🌐 AI 情报日报 - $DATE

### 🐦 X/Twitter AI 趋势
$TWITTER_DATA

### 📰 Hacker News Top Stories
$HN_DATA

### 💻 GitHub Trending
$GH_DATA

### 🐘 Product Hunt
$PH_DATA

### 🔬 ArXiv AI Papers
$ARXIV_DATA

### 🔧 V2EX 热门讨论
$V2EX_DATA

### 📕 Xiaohongshu
$XHS_DATA

---
*🕐 $(date +%H:%M) | 8 数据源 | 使用 bird CLI, HN, GH, PH, ArXiv, V2EX*
EOF
