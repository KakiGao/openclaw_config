---
name: xhs
description: |
  小红书 (Xiaohongshu) 内容工具 - 热点追踪、搜索、发布
  
  使用场景：
  - 搜索小红书内容并获取详情
  - 热点话题追踪和舆情分析
  - 获取帖子详情和热门评论
  - 导出帖子为长图
  - 点赞、收藏、评论
  - 用户主页查询
  
  MCP 服务地址: http://localhost:18060/mcp
  项目路径: /Users/kaki/Workspace/openclaw-xhs
---

# 🇨🇳 小红书工具 (XHS Tool)

基于 xiaohongshu-mcp 的能力封装。

## MCP 工具

| 工具名 | 描述 | 参数 |
|--------|------|------|
| `check_login_status` | 检查登录状态 | - |
| `search_feeds` | 搜索内容 | `{"keyword": "关键词"}` |
| `list_feeds` | 获取首页推荐 | - |
| `get_feed_detail` | 获取帖子详情和评论 | `{"feed_id": "id", "xsec_token": "token"}` |
| `post_comment_to_feed` | 发表评论 | `{"feed_id": "id", "xsec_token": "token", "content": "内容"}` |
| `user_profile` | 获取用户主页 | `{"user_id": "id"}` |
| `like_feed` | 点赞/取消 | `{"feed_id": "id", "xsec_token": "token", "like": true/false}` |
| `favorite_feed` | 收藏/取消 | `{"feed_id": "id", "xsec_token": "token", "favorite": true/false}` |
| `publish_content` | 发布图文笔记 | 参考 MCP 文档 |
| `publish_with_video` | 发布视频笔记 | 参考 MCP 文档 |

## 使用方式

### 1. 启动 MCP 服务（如未运行）
```bash
cd /Users/kaki/Workspace/openclaw-xhs/scripts
./start-mcp.sh
```

### 2. 调用 MCP 工具
通过 mcp-call.sh 调用：

```bash
# 搜索内容
./mcp-call.sh search_feeds '{"keyword": "AI教程"}'

# 获取帖子详情
./mcp-call.sh get_feed_detail '{"feed_id": "xxx", "xsec_token": "xxx"}'

# 检查登录状态
./mcp-call.sh check_login_status
```

### 3. Python 热点追踪
```bash
./track-topic.py "AI做海报" --limit 10
./track-topic.py "AI剪辑" --limit 5 --output report.md
```

### 4. 长图导出
```bash
./export-long-image.sh --posts-file posts.json -o output.jpg
```

## MCP 服务管理

| 命令 | 说明 |
|------|------|
| `./start-mcp.sh` | 启动 MCP 服务 |
| `./stop-mcp.sh` | 停止 MCP 服务 |
| `./status.sh` | 检查登录状态 |
| `./login.sh` | 扫码登录 |

## 环境要求

- xiaohongshu-mcp 二进制文件 (位于 ~/.local/bin/)
- Python 3.10+ (用于长图导出)
- jq 工具

## 快速开始

```bash
cd /Users/kaki/Workspace/openclaw-xhs/scripts

# 1. 启动服务
./start-mcp.sh

# 2. 检查状态
./status.sh

# 3. 搜索
./search.sh "关键词"

# 4. 追踪热点
./track-topic.sh "话题" --limit 10
```
