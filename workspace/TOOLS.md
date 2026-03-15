# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## XHS (小红书)

**Skill 位置**: `/Users/kaki/.openclaw/workspace/skills/xhs/`

**MCP 服务**: http://localhost:18060/mcp (需要先运行 `./start-mcp.sh`)

**快捷命令**:
```bash
# 搜索
xhs-search() { cd /Users/kaki/.openclaw/workspace/skills/xhs/scripts && ./search.sh "$1"; }

# 追踪热点
xhs-track() { cd /Users/kaki/.openclaw/workspace/skills/xhs/scripts && ./track-topic.py "$1" --limit ${2:-10}; }

# 获取详情
xhs-detail() { cd /Users/kaki/.openclaw/workspace/skills/xhs/scripts && ./mcp-call.sh get_feed_detail "{\"feed_id\":\"$1\",\"xsec_token\":\"$2\"}"; }

# 检查状态
xhs-status() { cd /Users/kaki/.openclaw/workspace/skills/xhs/scripts && ./status.sh; }
```

**常用调用**:
```bash
cd /Users/kaki/.openclaw/workspace/skills/xhs/scripts
./search.sh "关键词"
./track-topic.py "AI" --limit 10
./mcp-call.sh search_feeds '{"keyword": "AI"}'
```

---

Add whatever helps you do your job. This is your cheat sheet.

<!-- antfarm:workflows -->
# Antfarm Workflows

Antfarm CLI (always use full path to avoid PATH issues):
`node ~/.openclaw/workspace/antfarm/dist/cli/cli.js`

Commands:
- Install: `node ~/.openclaw/workspace/antfarm/dist/cli/cli.js workflow install <name>`
- Run: `node ~/.openclaw/workspace/antfarm/dist/cli/cli.js workflow run <workflow-id> "<task>"`
- Status: `node ~/.openclaw/workspace/antfarm/dist/cli/cli.js workflow status "<task title>"`
- Logs: `node ~/.openclaw/workspace/antfarm/dist/cli/cli.js logs`

Workflows are self-advancing via per-agent cron jobs. No manual orchestration needed.
<!-- /antfarm:workflows -->

