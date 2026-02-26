---
name: intel-collector
description: AI Intelligence Collector - Daily intelligence gathering with 6 sources + X/Twitter (bird CLI). Uses AIA methodology.
---

# Intel Collector

AI行业情报收集系统，从多个源头采集商业情报。

## 🎯 核心能力 (6大数据源)

| 数据源 | 内容 | 状态 |
|--------|------|------|
| 🐦 X/Twitter | AI/技术趋势 (bird CLI) | ✅ |
| 📰 Hacker News | 技术趋势讨论 | ✅ |
| 💻 GitHub Trending | Python 开源项目 | ✅ |
| 🔬 ArXiv AI | AI 学术论文 | ✅ |
| 🔧 V2EX | 中文技术讨论 | ⏸️ 可选 |
| 📕 Xiaohongshu | 中文社交讨论 | ⏸️ 可选 |

## 📋 可用指令

### 🌞 每日情报 (Daily Briefing)
**触发词**: "今日情报" / "send intel" / "run intel"

**动作**: 运行 intel-daily.sh → 发送到 Discord

**输出格式**:
```
## 🌐 AI 情报日报 - YYYY-MM-DD

### 🐦 X/Twitter AI 趋势
  [AI · Category] Title
  - time · posts

### 📰 Hacker News
  - [Title](URL)

### 💻 GitHub Trending
  - [repo](URL)
    - description

### 🔬 ArXiv AI
  - [Title...](URL)
```

### 🐦 X/Twitter 独立命令
```bash
# 获取 AI 趋势
bird news --ai-only -n 10

# 搜索话题
bird search "AI agent" -n 10

# Cookie 管理
bird-cookie-set     # 设置/更新
bird-cookie-status  # 检查状态
```

## 🧠 AIA 方法论 (可选分析)

### 绝望指数 (Desperation Score) 🌡️
- **V2EX/XHS**: 识别"愿意直接掏钱的客户"
- **关键词**: 救命、有偿、急、崩溃、红包

### 丑陋现金牛 (Ugly Cash Cows) 🐮
- **Chrome 插件**: 用户数 > 5000, 评分 < 3.8
- **机会**: 1星差评 = 需求文档

### 卖铲子策略 ⛏️
- **Web3/AI**: 开源工具 → GUI 产品
- **过滤**: 排除 Airdrop 噪音

## 🔧 配置

### bird CLI 认证 (必需)
```bash
# 保存 Cookie
bird-cookie-set
# 输入 auth_token 和 ct0

# 验证
bird whoami
```

## ⏰ 定时任务

**每日 9:00** 自动执行:
1. 采集 6 个数据源
2. 生成情报摘要
3. 发送到 Discord

**手动触发**: 说 "发送情报" 或 "run intel"

## 📂 文件结构

```
/Users/kaki/.openclaw/workspace/
├── intel-daily.sh              # 主脚本 (6 sources)
├── intel-collector skill/     # SKILL.md
└── ~/.bird_cookies.json       # X/Twitter 认证
```

## ⚠️ 注意事项

1. **X/Twitter**: 需要先运行 `bird-cookie-set`
2. **V2EX/XHS**: 当前暂停，需要可手动启用
3. **GitHub API**: 无需认证，公开接口
4. **Cookie 过期**: 每周会检查提醒
