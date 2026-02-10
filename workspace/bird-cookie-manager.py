#!/usr/bin/env python3
"""
bird-cookie-manager.py - 自动刷新 X/Twitter Cookie

功能：
1. 从 Chrome 自动读取最新的 auth_token 和 ct0
2. 保存到 ~/.bird_cookies.json
3. 提供 bird 命令 wrapper，自动注入最新 cookie
"""

import os
import json
import subprocess
import sqlite3
import sys
from pathlib import Path

# 配置
COOKIE_DB = os.path.expanduser(
    "~/Library/Application Support/Google/Chrome/Default/Cookies"
)
COOKIE_FILE = os.path.expanduser("~/.bird_cookies.json")

def get_chrome_cookies():
    """从 Chrome 读取 X/Twitter cookie"""
    if not os.path.exists(COOKIE_DB):
        return None

    try:
        conn = sqlite3.connect(COOKIE_DB)
        cursor = conn.cursor()

        # Chrome cookie 表结构: creation_utc, host_key, name, value, path, expires_utc, etc.
        # value 可能在多个列中
        cursor.execute("""
            SELECT host_key, name, value, encrypted_value
            FROM cookies
            WHERE host_key LIKE '%twitter.com' OR host_key LIKE '%x.com'
        """)

        cookies = {}
        for host, name, value, encrypted in cursor.fetchall():
            if value:
                cookies[name] = value
            elif encrypted:
                # 解密encrypted_value - 简化版，实际需要 keychain
                pass

        conn.close()

        auth_token = cookies.get('auth_token')
        ct0 = cookies.get('ct0')

        if auth_token and ct0:
            return {'auth_token': auth_token, 'ct0': ct0}

    except Exception as e:
        print(f"⚠️ 读取 Chrome cookies 失败: {e}")
        print("   尝试备用方法...")

    return None


def get_cookies_from_json():
    """从保存的文件读取 cookie"""
    if os.path.exists(COOKIE_FILE):
        try:
            with open(COOKIE_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return None


def save_cookies(cookies):
    """保存 cookie 到文件"""
    with open(COOKIE_FILE, 'w') as f:
        json.dump(cookies, f, indent=2)
    os.chmod(COOKIE_FILE, 0o600)  # 仅用户可读写


def test_cookies(auth_token, ct0):
    """测试 cookie 是否有效"""
    cmd = [
        'bird', 'whoami',
        '--auth-token', auth_token,
        '--ct0', ct0
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except:
        return False


def refresh_cookies():
    """刷新 cookie"""
    print("🔄 正在刷新 X/Twitter cookie...")

    # 方法1: 从 Chrome 读取
    chrome_cookies = get_chrome_cookies()

    if chrome_cookies:
        # 测试是否有效
        if test_cookies(chrome_cookies['auth_token'], chrome_cookies['ct0']):
            print("✅ 从 Chrome 获取到有效 cookie")
            save_cookies(chrome_cookies)
            return chrome_cookies
        else:
            print("⚠️ Chrome cookie 已过期")

    # 方法2: 检查保存的 cookie
    saved = get_cookies_from_json()
    if saved and test_cookies(saved['auth_token'], saved['ct0']):
        print("✅ 使用保存的 cookie (仍有效)")
        return saved

    print("❌ Cookie 无效或已过期")
    print("\n请更新 cookie:")
    print("1. 打开 Chrome → x.com → F12 → Application → Cookies → x.com")
    print("2. 复制 auth_token 和 ct0 的值")
    print("3. 运行: bird-cookie-update")
    return None


def run_bird(args):
    """运行 bird 命令，自动注入 cookie"""
    # 尝试刷新 cookie
    cookies = refresh_cookies()

    if not cookies:
        print("\n💡 提示: 运行 'bird-cookie-update' 更新 cookie 后重试")
        sys.exit(1)

    # 构建命令
    cmd = ['bird'] + list(args) + [
        '--auth-token', cookies['auth_token'],
        '--ct0', cookies['ct0']
    ]

    # 运行
    os.execvp('bird', cmd)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法:")
        print("  bird-wrap news --ai-only          # 运行 bird 命令")
        print("  bird-cookie-refresh                # 手动刷新 cookie")
        print("  bird-cookie-status                 # 检查 cookie 状态")
        sys.exit(1)

    if sys.argv[1] == 'refresh':
        refresh_cookies()
    elif sys.argv[1] == 'status':
        saved = get_cookies_from_json()
        if saved:
            if test_cookies(saved['auth_token'], saved['ct0']):
                print("✅ Cookie 有效")
            else:
                print("⚠️ Cookie 已过期，需要刷新")
        else:
            print("❌ 未找到保存的 cookie")
    else:
        run_bird(sys.argv[1:])
