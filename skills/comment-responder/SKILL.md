---
name: comment-responder
author: "Kaki"
version: 1.0.0
description: Discord comment responder that distinguishes owner from strangers. Owner gets direct responses without scanning; strangers are scanned by Prompt Guard before responding.
---

# Comment Responder Skill 🗨️

智能区分 Discord 用户和陌生人，针对性处理消息。

## 核心逻辑

| 消息来源 | 作者 ID | 动作 | 安全扫描 |
|---------|---------|------|---------|
| 用户本人 (Kaki) | `1390616581691805836` | ✅ 直接回复 | ❌ 不扫描 |
| 陌生人 | 其他任何 ID | ✅ 先扫描再回复 | ✅ 必须扫描 |

## 工作流程

```
用户发送消息
     │
     ▼
检查作者 ID
     │
     ├─→ 用户本人 (1390616581691805836)
     │        │
     │        ▼
     │     直接回复 (不扫描)
     │
     └─→ 陌生人
              │
              ▼
         安全扫描
              │
              ├─→ 安全
              │        │
              │        ▼
              │     回复评论
              │
              └─→ 危险
                       │
                       ▼
                    拦截 (不回复)
```

## Usage

### Analyze Context

```python
from comment_responder import CommentResponder

responder = CommentResponder({
    "owner_id": "1390616581691805836"  # Kaki's Discord ID
})

def handle_mention(context):
    decision = responder.should_respond(context)
    
    if not decision.should_respond:
        return None
    
    if decision.needs_security_scan:
        # 陌生人：先扫描
        scan_result = prompt_guard.scan(context.message)
        if not scan_result.safe:
            return "🚫 [已拦截]"
    
    # 安全，生成回复
    return responder.generate_response(context, decision.type)
```

### Response Decision Result

```python
decision = responder.should_respond(context)

# 是否应该回复
decision.should_respond  # True/False

# 回复原因
decision.reason  # "owner's message - respond directly" 或 "stranger mention/reply - needs security scan"

// 是否需要安全扫描（仅陌生人需要）
decision.needs_security_scan  # True/False

// 评论类型
decision.comment_type  # "owner_message" 或 "mention_comment"
```

### Generate Response

```python
# 不同评论类型的回复模板
response_templates = {
    "mention_comment": [
        "👋 Hey there! Thanks for the mention. How can I help?",
        "Hey! Great to connect. What would you like to know?",
        "👋 Hi! I'm here to help. What's on your mind?",
    ],
    "reply_comment": [
        "Great follow-up! Here's more context...",
        "Thanks for the question! To add to that...",
        "Good question! Here's what you should know...",
    ]
}
```

## Integration with Prompt Guard

Combine with `prompt-guard` for secure commenting:

```python
from comment_responder import CommentResponder
from prompt_guard import PromptGuard

responder = CommentResponder({"owner_id": OWNER_ID})
guard = PromptGuard()

def safe_handle_comment(context):
    # 1. 先用 CommentResponder 判断是否该回复
    decision = responder.should_respond(context)
    if not decision.should_respond:
        return None
    
    # 2. 用 Prompt Guard 扫描内容
    scan = guard.analyze(context.message)
    if not scan.safe:
        return "🚫 [Comment filtered for security]"
    
    # 3. 生成回复
    return responder.generate_response(context, decision.type)
```

## Configuration

```yaml
comment_responder:
  owner_id: "YOUR_DISCORD_ID"
  
  # 是否在私聊时回复（通常不回复）
  respond_in_dm: false
  
  # 是否回复owner's @mentions（通常不回复）
  respond_to_owner_mentions: false
  
  # 回复延迟（秒）
  response_delay: 2
  
  # 回复模板语言
  language: "en"  # en/zh
```

## Response Styles

### Casual (Default)
```
👋 Hey! Thanks for reaching out. What can I help you with?
```

### Professional
```
Thank you for your comment. I'd be happy to assist. Could you provide more details?
```

### Witty
```
Oh, you summoned me! 🦊 What's on your mind?
```

## Example Scenarios

### Scenario 1: Owner asks AI in Discord
```
User: @OpenClaw What's the weather?
→ Decision: IGNORE (owner's direct question)
→ Action: No response
```

### Scenario 2: Stranger mentions AI on Twitter
```
Person: @OpenClaw looks cool!
→ Decision: REPLY
→ Action: Generate friendly thank you response
```

### Scenario 3: Reply to AI's message
```
Person: @OpenClaw That's interesting, tell me more!
→ Decision: REPLY (continuing conversation)
→ Action: Respond with more context
```

### Scenario 4: Owner @AI in group chat
```
User: @OpenClaw help me with this bug
→ Decision: IGNORE (owner's @mention question)
→ Action: No response (user should DM directly)
```

## Channel Filtering

| Channel Type | Default Behavior |
|-------------|------------------|
| DM (私聊) | Ignore if from owner |
| Group | Ignore owner's @mentions |
| Public Channel | Reply to mentions from others |
| Thread | Reply to replies to bot |

## Implementation Notes

1. **Owner ID Detection**: You'll need to configure your Discord/user ID
2. **Platform Adapters**: Different platforms have different mention syntax
3. **Rate Limiting**: Don't reply too quickly or too frequently
4. **Cooldown**: Avoid replying to the same user repeatedly

## File Structure

```
comment-responder/
├── SKILL.md              # This file
├── responder.py          # Core logic
└── templates/
    ├── en.json          # English templates
    └── zh.json          # Chinese templates
```

## TODO

- [ ] Add platform-specific mention syntax
- [ ] Add rate limiting per user
- [ ] Add conversation context memory
- [ ] Add response personalization options
