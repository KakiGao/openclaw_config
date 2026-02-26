---
name: task-manager
description: Task isolation and context management for Discord channels. Automatically creates dedicated threads for tasks initiated with "/new <task-name>", injects relevant background context, and generates summary reports upon "/done".
---

# Task Manager

> **创建记录**：此技能于 2026-02-09 使用 `skill-creator` 技能成功创建。
> 创建命令：`scripts/init_skill.py task-manager --path <skills-dir> --resources references`

## Overview

This skill manages task isolation and context persistence for Discord channels. It ensures:
- Clean main channel (only task launches)
- Isolated task execution in threads
- Automatic context injection
- Auto-generated task summaries

## Workflow

### 1. Task Launch Trigger

Monitor the main channel for messages matching pattern:
```
/new <task-name>
```

**Example:** `/new 优化首页性能`

### 2. Thread Creation

When trigger detected:
1. Extract task name from message (format: `/new <task-name>`)
2. Create a Discord thread in the main channel
3. Thread naming convention: `task-<task-name>-<timestamp>`
4. Post task launch confirmation in thread

### 3. Context Injection

Before task execution, automatically:
1. Search memory for recent relevant context using `memory_search`
2. Inject background information as first thread message
3. Reference any related previous tasks or decisions

### 4. Task Execution

All task discussion happens in the dedicated thread:
- Main channel remains clean
- AI maintains task focus
- All relevant context is available in thread

### 5. Task Completion

When user says `/done` in the thread:
1. Extract key discussion points from thread history
2. Generate summary with:
   - Task name
   - Key decisions made
   - Actions taken
   - Files created/modified
   - Lessons learned
3. Post summary in thread
4. Optionally archive thread

## Implementation

### Triggers
- **Start Task**: Message matching regex `^/new\s+(.+)$` in main channel
- **Complete Task**: Message exactly `/done` in task thread

### Actions
1. **Thread Creation**: Use `message` tool with `action=thread-create`
2. **Context Search**: Use `memory_search` for relevant background
3. **Summary Generation**: Use conversation context to extract key points

### Example Flow

**Main Channel:**
```
User: /new 优化数据库查询性能
```

**Bot Actions:**
1. Creates thread: `task-优化数据库查询性能-202602091200`
2. Injects context:
   ```
   [任务背景]
   - 近期相关讨论：...
   - 相关文件：...
   - 历史决策：...
   ```
3. Thread ready for execution

**Thread (Execution):**
```
[讨论优化方案...]
User: /done
```

**Bot Summary:**
```
[任务完成纪要]
任务：优化数据库查询性能

要点：
- 识别慢查询...
- 添加索引...
- 查询重写...

文件变更：
- schema.sql
- query_builder.go

下次参考：
- 优先检查查询计划...
```

## Integration Points

- **Memory**: Uses `memory_search` to find context
- **Discord**: Uses `message` for thread creation and posting
- **Sessions**: Optionally spawns sub-agent for complex tasks
