#!/bin/bash
# bird-wrapper.sh - Bird 命令 Wrapper，自动注入 Cookie

# Cookie 文件位置
COOKIE_FILE="$HOME/.bird_cookies.json"

# 读取保存的 cookie
get_cookies() {
    if [ -f "$COOKIE_FILE" ]; then
        cat "$COOKIE_FILE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('auth_token','')); print(d.get('ct0',''))" 2>/dev/null
    fi
}

# 检查 cookie 是否有效
check_cookie() {
    auth_token="$1"
    ct0="$2"
    
    if [ -z "$auth_token" ] || [ -z "$ct0" ]; then
        return 1
    fi
    
    result=$(bird whoami --auth-token "$auth_token" --ct0 "$ct0" 2>&1)
    echo "$result" | grep -q "@" && return 0 || return 1
}

# 更新 cookie
update_cookie() {
    echo "🔄 正在检测 X/Twitter 登录状态..."
    echo ""
    echo "❌ Cookie 无效或已过期"
    echo ""
    echo "请更新 Cookie:"
    echo "1. 确保 Chrome 已登录 x.com"
    echo "2. 运行以下命令:"
    echo ""
    echo "   bird-cookie-update"
    echo ""
    echo "或直接更新 Cookie:"
    echo "1. F12 → Application → Cookies → https://x.com"
    echo "2. 复制 auth_token 和 ct0"
    echo "3. 运行: bird-cookie-set"
}

# 主命令
case "$1" in
    refresh|update)
        echo "💡 请在 Chrome 中刷新 x.com 登录状态，然后运行: bird-cookie-set"
        ;;
    set)
        read -p "auth_token: " AUTH_TOKEN
        read -p "ct0: " CT0
        echo "{\"auth_token\": \"$AUTH_TOKEN\", \"ct0\": \"$CT0\"}" > "$COOKIE_FILE"
        chmod 600 "$COOKIE_FILE"
        echo "✅ 已保存 Cookie"
        
        # 验证
        if check_cookie "$AUTH_TOKEN" "$CT0"; then
            echo "✅ Cookie 有效！"
        else
            echo "❌ Cookie 无效，请检查"
        fi
        ;;
    status)
        cookies=$(get_cookies)
        if [ -n "$cookies" ]; then
            IFS=$'\n' read -r auth_token ct0 <<< "$cookies"
            if check_cookie "$auth_token" "$ct0"; then
                echo "✅ Cookie 有效"
            else
                echo "⚠️ Cookie 已过期，需要更新"
                echo "运行: bird-cookie-set"
            fi
        else
            echo "❌ 未找到保存的 Cookie"
            echo "运行: bird-cookie-set"
        fi
        ;;
    *)
        # 运行实际的 bird 命令
        cookies=$(get_cookies)
        if [ -z "$cookies" ]; then
            echo "❌ 未找到 Cookie"
            echo "请先运行: bird-cookie-set"
            exit 1
        fi
        
        IFS=$'\n' read -r auth_token ct0 <<< "$cookies"
        
        if ! check_cookie "$auth_token" "$ct0"; then
            update_cookie
            exit 1
        fi
        
        bird "$@" --auth-token "$auth_token" --ct0 "$ct0"
        ;;
esac
