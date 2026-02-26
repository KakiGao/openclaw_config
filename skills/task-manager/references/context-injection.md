# Context Injection Strategy

## Overview

When a task is launched, automatically search and inject relevant background context to provide the AI with necessary context without requiring manual paste.

## Context Sources

### 1. Memory Search (Primary)

Use `memory_search` to find:
- Recent task discussions
- Related decisions made
- Previous similar tasks
- Project-wide conventions

**Search query strategy:**
```
<task-name> related context decisions
```

**Example:** For "优化数据库查询", search:
```
数据库 查询 优化 相关 上下文 决策
```

### 2. Session History (Secondary)

Check recent message history in:
- Main channel (last 20 messages)
- Related threads

### 3. File System (Tertiary)

Check for relevant files:
- Project documentation
- Configuration files
- Recent changes

## Context Priority

| Priority | Source | When to Use |
|----------|--------|-------------|
| 1 | memory_search | Always |
| 2 | Session history | If memory empty |
| 3 | File system | If both above empty |

## Injection Timing

**Immediately after thread creation**, as the first message in the thread.

## Context Filtering

Only inject information that is:
- ✅ Relevant to current task
- ✅ Recent (within 7 days)
- ✅ Not already mentioned in task name
- ✅ Actionable (can inform decisions)

**Skip:**
- ❌ Unrelated historical events
- ❌ Very old decisions (>30 days)
- ❌ Sensitive/personal information
- ❌ Generic project descriptions

## Example Context Assembly

### Input
- Task name: "优化API响应速度"
- Time: 2026-02-09 10:00

### Memory Search Query
```
API 响应 速度 优化 性能 相关 决策
```

### Memory Results (Example)
```
- 2026-02-05: 决定使用gRPC替代REST (from MEMORY.md)
- 2026-01-28: API网关方案确定 (from memory/2026-01-28.md)
- 2026-01-15: 性能优化优先级设定 (from MEMORY.md)
```

### Filtered Context
```
### 相关上下文

- **技术选型**: 已决定使用gRPC替代REST (2026-02-05)
- **基础设施**: API网关已部署 (2026-01-28)
- **性能目标**: API响应时间 < 200ms (2026-01-15)

### 相关文件

- api/gateway/main.go
- api/grpc/server.go
```

## No Context Found

If no relevant context found, inject minimal placeholder:

```markdown
### 相关上下文

暂无历史上下文。这是新任务，请从头开始记录关键信息。

### 提示

请在任务过程中记录：
- 关键决策
- 文件变更
- 经验教训
```
