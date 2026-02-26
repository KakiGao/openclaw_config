# Trigger Patterns and Examples

## Task Launch Triggers

### Primary Trigger
```regex
^开启任务：(.+)$
```

**Matches:**
- `开启任务：优化首页` ✅
- `开启任务：重构用户模块` ✅
- `开启任务：修复登录bug` ✅

**Does NOT match:**
- `我想开启任务：xxx` ❌ (has prefix)
- `开启任务：` ❌ (empty task name)
- `任务开启` ❌ (different wording)

### Task Completion Trigger
```regex
^任务完成$
```

**Usage:**
- User types exactly `任务完成` in the task thread
- Bot generates summary from thread conversation
- Summary includes key decisions, actions, files

## Thread Naming Convention

Format: `task-<task-name>-<timestamp>`

**Examples:**
- Task: "优化数据库查询" → `task-优化数据库查询-202602091200`
- Task: "添加用户验证" → `task-添加用户验证-202602091215`
- Task: "修复支付流程" → `task-修复支付流程-202602091230`

**Timestamp format:** YYYYMMDDHHMM (local time)

## Context Injection Format

When creating thread, first message format:

```markdown
## 任务背景

**任务名称:** {task_name}
**创建时间:** {timestamp}

### 相关上下文

{context_from_memory}

### 相关文件

{files}

---

💡 **提示:** 所有任务讨论请在此thread中进行，主区保持干净。
```

## Summary Generation Format

When user says "任务完成", generate:

```markdown
## 任务完成纪要

**任务名称:** {task_name}
**完成时间:** {timestamp}

### 核心要点

- {key_point_1}
- {key_point_2}
- {key_point_3}

### 关键决策

1. {decision_1}
2. {decision_2}

### 文件变更

- `{file_1}` - {description}
- `{file_2}` - {description}

### 后续行动

- {action_1}
- {action_2}

### 经验教训

- {lesson_1}
- {lesson_2}

---

*生成时间: {timestamp}*
```

## Complete Usage Example

**Main Channel:**
```
[10:00] User: 开启任务：重构登录模块
```

**Bot Actions:**
1. Detects trigger → extracts "重构登录模块"
2. Searches memory for context
3. Creates thread: `task-重构登录模块-202602091000`
4. Posts in thread:
   ```
   ## 任务背景
   
   **任务名称:** 重构登录模块
   **创建时间:** 2026-02-09 10:00
   
   ### 相关上下文
   
   - 相关任务：用户认证优化 (2026-02-05)
   - 决策：采用JWT方案替代session
   
   ### 相关文件
   
   - auth/login.go
   - auth/session.go
   
   ---
   
   💡 提示: 所有任务讨论请在此thread中进行，主区保持干净。
   ```

**Thread Discussion:**
```
[10:05] AI: 开始分析现有登录逻辑...
[10:15] User: 改成JWT后需要处理token刷新
[10:20] AI: 了解，加入token刷新机制
[10:30] User: 任务完成
```

**Bot Summary:**
```
## 任务完成纪要

**任务名称:** 重构登录模块
**完成时间:** 2026-02-09 10:30

### 核心要点

- 现有session认证改用JWT
- 实现token刷新机制
- 移除session相关代码

### 关键决策

1. JWT方案使用RS256签名
2. Token有效期设为24小时
3. 刷新窗口期为7天

### 文件变更

- `auth/login.go` - 重构登录逻辑，JWT实现
- `auth/token.go` - 新增，JWT生成和验证
- `auth/session.go` - 标记为废弃

### 后续行动

- 更新API文档
- 添加单元测试

### 经验教训

- Token刷新需要考虑并发场景
- 旧session清理需要迁移脚本

---

*生成时间: 2026-02-09 10:30*
```
