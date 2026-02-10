#!/usr/bin/env python3
"""
OpenClaw Security Gateway - Prompt Guard CLI Wrapper
拦截恶意消息，保护 AI 代理
"""

import sys
import json
from prompt_guard import PromptGuard

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "safe": True,
            "error": "No message provided"
        }))
        sys.exit(0)
    
    # 获取消息（支持 stdin）
    if len(sys.argv) > 2 and sys.argv[1] == "--stdin":
        message = sys.stdin.read()
    else:
        message = sys.argv[1]
    
    guard = PromptGuard()
    result = guard.analyze(message)
    
    # 输出 JSON 供 Node.js 解析
    output = {
        "safe": result.action.value in ["allow", "log"],
        "severity": result.severity.value,
        "severity_name": result.severity.name,
        "action": result.action.value,
        "action_name": result.action.name,
        "reasons": result.reasons,
        "patterns_matched": result.patterns_matched,
        "confidence": getattr(result, 'confidence', None),
        "shield": result.to_shield_format() if hasattr(result, 'to_shield_format') else None
    }
    
    print(json.dumps(output, ensure_ascii=False))

if __name__ == "__main__":
    main()
