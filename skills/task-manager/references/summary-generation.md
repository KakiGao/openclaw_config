# Summary Generation

## Overview

When user says "任务完成" in a task thread, automatically generate a comprehensive summary of the task execution.

## Trigger Detection

Monitor for exact phrase: `任务完成`

**Detection logic:**
- Exact match (case-insensitive)
- Must be in a task thread (thread name starts with `task-`)
- Ignore if in main channel

## Summary Components

### Required Fields

1. **Task Name** - Extracted from thread name
2. **Completion Time** - When "任务完成" was said
3. **Key Points** - 3-5 core takeaways
4. **Decisions Made** - Architectural/technical choices
5. **File Changes** - Created/modified files
6. **Lessons Learned** - For future reference

### Optional Fields

7. **Next Actions** - Follow-up items
8. **Related Tasks** - Spawned subtasks
9. **Open Questions** - Unresolved issues

## Extraction Strategy

### Key Points Extraction

Analyze conversation for:
- Problem statements
- Solution approaches
- Results achieved
- Trade-offs discussed

**Algorithm:**
1. Collect all user messages
2. Collect all AI responses
3. Extract sentences with action verbs
4. Prioritize: decisions > actions > observations
5. Limit to 3-5 most important points

### Decisions Extraction

Identify decision indicators:
- "决定" (decided)
- "选择" (chose)
- "采用" (adopted)
- "确定" (confirmed)
- "同意" (agreed)

### File Changes Extraction

Monitor for:
- File path mentions
- "创建" (created)
- "修改" (modified)
- "删除" (deleted)
- "更新" (updated)

### Lessons Extraction

Identify lessons:
- "学到" (learned)
- "注意" (note)
- "避免" (avoid)
- "下次" (next time)
- "经验" (experience)

## Summary Quality Guidelines

### Good Summary Example

```markdown
## 任务完成纪要

**任务名称:** 添加用户头像上传功能
**完成时间:** 2026-02-09 14:30

### 核心要点

- 实现了用户头像上传接口，支持JPG/PNG，最大2MB
- 集成阿里云OSS存储，生成CDN加速链接
- 前端添加图片压缩，减少上传时间50%

### 关键决策

1. 使用OSS而非本地存储 (可扩展性考虑)
2. 前端压缩而非后端 (节省带宽)
3. 保留原图和缩略图两种规格

### 文件变更

- `user/avatar.go` - 新增，头像上传逻辑
- `user/avatar_test.go` - 新增，单元测试
- `static/js/avatar.js` - 修改，前端压缩逻辑

### 后续行动

- 添加头像裁剪功能
- 实现批量上传

### 经验教训

- 前端压缩在低端机上可能性能不足
- OSS URL签名需要设置过期时间

---

*生成时间: 2026-02-09 14:30*
```

### Poor Summary Example (To Avoid)

```markdown
## 任务完成纪要

任务完成了。
做了些优化。
还可以。
```

**Problems:**
- Too vague
- No actionable details
- No file changes
- No lessons learned

## Context for Summary

When generating summary, consider:
- Task launch context (why this task?)
- Discussion flow (what was debated?)
- Outcome achieved (what was delivered?)

## Post-Summary Actions

1. Post summary in thread
2. Optionally pin summary
3. Optionally archive thread
4. Update memory with key lessons (future enhancement)
