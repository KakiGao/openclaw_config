#!/usr/bin/env python3
"""
bird-auto-cookie.py - 自动从 Chrome 获取最新 X/Twitter Cookie

使用 OpenClaw browser 工具注入脚本来读取 cookie
"""

import subprocess
import json
import os

def get_cookies_via_browser():
    """通过 browser 工具获取 cookie"""
    # 使用 browser 工具的 evaluate 功能执行 JavaScript
    # 读取 document.cookie
    
    # 注意：这只对同源页面有效
    # X cookie 可能有 HttpOnly 标志，无法通过 JS 读取
    
    # 备选方案：使用 browser dump cookies 功能
    pass


def create_update_script():
    """创建一键更新脚本"""
    script = '''#!/bin/bash
# bird-cookie-refresh.sh - 一键刷新 X/Twitter Cookie

echo "🔄 正在从 Chrome 获取最新 Cookie..."

# 方法1: 使用 bird 自带的 cookie 检查
if bird check --cookie-source chrome 2>/dev/null | grep -q "auth_token.*found"; then
    echo "✅ 从 Chrome 获取成功"
    bird whoami
    exit 0
fi

# 方法2: 提示用户
echo ""
echo "⚠️ 无法自动从 Chrome 读取 Cookie"
echo ""
echo "请手动更新:"
echo "1. 确保 Chrome 已登录 https://x.com"
echo "2. 打开 F12 → Application → Cookies → https://x.com"
echo "3. 复制 auth_token 和 ct0 的 Value"
echo "4. 运行: bird-cookie-set"
echo ""
echo "或者运行以下命令，粘贴 Cookie:"
echo "bird-cookie-set"
'''
    
    with open('/Users/kaki/.openclaw/workspace/bird-cookie-refresh.sh', 'w') as f:
        f.write(script)
    os.chmod('/Users/kaki/.openclaw/workspace/bird-cookie-refresh.sh', 0o755)


if __name__ == '__main__':
    create_update_script()
    print("✅ 已创建 bird-cookie-refresh.sh")
