---
name: skill-vetter
author: "Kaki"
version: 1.0.0
description: Security-first vetting protocol for AI agent skills. Automatically reviews any skill before installation, checking for red flags, permission scope, and suspicious patterns.
---

# Skill Vetter 🔒

**安装任何技能前自动触发安全审查**

## 触发条件

当用户要求安装/创建新技能时，**自动触发**，无需额外命令：

- "安装 XXX skill"
- "创建一个 XXX 技能"
- "从 GitHub 安装 XXX"
- "运行 XXX skill"

## 工作流程

```
用户要求安装技能
          │
          ▼
    自动触发审查
          │
          ▼
    1. 来源分析 (GitHub/ClawHub/本地)
    2. 代码审查 (检查危险模式)
    3. 权限分析 (文件/命令/网络)
    4. 风险分类 (LOW/MEDIUM/HIGH/EXTREME)
          │
          ▼
    生成审查报告
          │
          ├─→ EXTREME → ❌ 拒绝安装
          ├─→ HIGH → ⚠️ 需用户批准
          └─→ LOW/MEDIUM → ✅ 提示后安装
```

## 使用方式

### 自动触发（推荐）

用户只需要说：
```
"安装天气技能"
"创建一个笔记技能"
"从 GitHub 安装 openai-skill"
```

Skill 会自动：
1. 获取技能来源
2. 下载并审查 SKILL.md
3. 检查代码危险模式
4. 生成报告
5. 建议下一步操作

### 手动触发

```bash
python3 /openclaw/skills/skill-vetter/vetter.py <skill-name> <source> [repo-url]
```

## 危险红 Flag（自动检测）

```
🚨 发现立即拒绝:
• curl/wget 下载未知脚本
• 发送数据到外部服务器
• 请求 credentials/tokens/API keys
• 读取 ~/.ssh, ~/.aws, ~/.config
• 访问 MEMORY.md, USER.md, SOUL.md
• 使用 base64 decode
• 使用 eval() 或 exec()
• 修改系统文件权限
• 代码混淆/加密
```

## 风险分类

| 级别 | 标准 | 操作 |
|------|------|------|
| 🟢 LOW | 无红 Flag | ✅ 提示后可安装 |
| 🟡 MEDIUM | 低风险 Flag | ✅ 建议审查后安装 |
| 🔴 HIGH | 敏感权限请求 | ⚠️ **需用户批准** |
| ⛔ EXTREME | 危险操作检测 | ❌ **拒绝安装** |

## 输出示例

```
🔍 Vetting skill: example-skill
   Source: github

📄 Analyzing SKILL.md...
⚠️  RED FLAGS DETECTED:
   - Uses curl to download external script
   - Accesses credentials pattern found

───────────────────────────────────────
RISK LEVEL: 🔴 HIGH

VERDICT: ⚠️ HUMAN APPROVAL REQUIRED
NOTES: High risk detected. Review carefully before installation.

建议: 请用户确认是否继续安装。
```

## 集成说明

这个 skill 应该在 OpenClaw 消息处理入口集成：

```python
# 当用户要求安装技能时
if user_message.startswith(("安装", "create", "install")):
    skill_name = extract_skill_name(user_message)
    source = detect_source(user_message)  # github/clawhub/local
    
    # 自动触发审查
    report = vet_skill(skill_name, source, repo_url)
    await send_message(user_channel, report)
    
    # EXTREME/HIGH 风险时，询问用户
    if "HIGH" in report or "EXTREME" in report:
        await send_message(user_channel, "⚠️ 高风险！是否继续安装？(yes/no)")
```

## 信任等级

| 来源 | 信任度 | 审查强度 |
|------|--------|---------|
| OpenClaw 官方 | 高 | 基础审查 |
| 高星 GitHub (1000+) | 中 | 标准审查 |
| 已知作者 | 中 | 标准审查 |
| 未知来源 | 低 | **严格审查** |
| 要求凭据访问 | **零信任** | **拒绝** |

## 文件结构

```
skill-vetter/
├── SKILL.md           # 此文档
├── vetter.py          # 审查核心脚本
└── README.md          # 快速参考
```

## 注意事项

- ⚠️ 此 skill 仅提供审查建议，最终安装决策由用户做出
- 🔒 对于 HIGH/EXTREME 风险，始终要求人工确认
- 📝 建议记录每次审查结果供后续参考

---

_"Paranoia is a feature."_ 🔒🦀
