# MEMORY.md

## 创建 Skills 的成功方式

### Task Manager 技能创建经验 (2026-02-09)

**成功创建步骤：**

1. **使用 skill-creator 技能** - 这是创建新技能的标准化方式
   - 通过 `openclaw sessions spawn agentId=skill-creator` 启动
   - 或直接说"创建一个新技能"让系统自动处理

2. **创建命令**：
   ```bash
   # 在正确的skills目录下创建
   scripts/init_skill.py task-manager --path /Users/kaki/.nvm/versions/node/v22.14.0/lib/node_modules/openclaw/skills/ --resources references
   ```

3. **关键要点**：
   - skill名称用小写字母和连字符（kebab-case）
   - 路径要指向 OpenClaw 的 skills 目录
   - 创建后需要编辑 SKILL.md 添加实际内容
   - skill-creator 技能的 SKILL.md 里有完整的创建指南

4. **创建后的验证**：
   - 检查 SKILL.md 格式正确
   - 确认 frontmatter 包含 name 和 description
   - 技能会自动出现在可用技能列表中

**重要教训**：
- skill-creator 技能的 SKILL.md 文档非常详细，包含步骤1-6
- 不要自己摸索创建方式，直接遵循 skill-creator 的指导
- 每次创建新技能时都应该参考 skill-creator 的文档

## 可用技能列表

当前已安装的技能：
- `coding-agent` - 运行 Codex CLI 等编程代理
- `gemini` - Gemini CLI 问答和生成
- `github` - GitHub 交互（issue, PR, run, api）
- `healthcheck` - 主机安全加固和风险配置
- `imsg` - iMessage/SMS CLI
- `obsidian` - Obsidian 笔记交互
- `skill-creator` - 创建和更新 AgentSkills ✅ (用于创建其他技能)
- `task-manager` - Discord 任务隔离和管理 ✅ (刚创建)
- `video-frames` - 视频帧提取
- `weather` - 天气查询

## Discord 集成

### Task Manager 工作流程 (2026-02-09 更新)

1. **触发条件**：在主频道发送 `/new <任务名称>`
2. **自动创建线程**：bot 自动创建专用线程
3. **注入上下文**：自动搜索相关记忆注入背景信息
4. **任务执行**：在线程中进行讨论
5. **完成总结**：说 `/done` 后自动生成总结报告

**示例**：
```
用户：/new 优化数据库查询性能
→ 创建线程：task-优化数据库查询性能-时间戳
→ 注入背景：搜索 memory 找到相关上下文
→ 开始执行
→ 用户：/done
→ 生成任务总结报告
```

---

## intel-collector 每日 AI 情报 (2026-02-09)

### 配置完成

**6 大数据源**：
- 🐦 X/Twitter AI 趋势 (bird CLI)
- 📰 Hacker News Top 5
- 💻 GitHub Trending (Python repos)
- 🔬 ArXiv AI Papers
- ⏸️ V2EX (暂停)
- ⏸️ Xiaohongshu (暂停)

**文件位置**：
- `/Users/kaki/.openclaw/workspace/intel-daily.sh` - 主脚本
- `~/.bird_cookies.json` - X/Twitter Cookie
- `/Users/kaki/.nvm/.../skills/intel-collector/SKILL.md` - 技能文档

**使用方式**：
```bash
# 手动运行
bash /Users/kaki/.openclaw/workspace/intel-daily.sh

# 设置/更新 X Cookie
bird-cookie-set
```

### Cron 定时任务

- **任务名**: daily-intel
- **时间**: 每天 9:00
- **动作**: 执行 intel-daily.sh → 发送情报到 Discord

### bird CLI 认证

X/Twitter 使用 Cookie 认证（无需 API Key）：
- Cookie 保存在 `~/.bird_cookies.json`
- 过期时运行 `bird-cookie-set` 更新

---

## ⚠️ 安全提醒 (2026-02-09)

### HEARTBEAT.md 域名风险

**事件**: heartbeat.md 域名被他人注册

**风险**: 恶意网站可能利用文件名进行钓鱼或攻击

**防范措施**:
1. HEARTBEAT.md 只读本地文件，**永不自动访问任何 URL**
2. 文件中添加安全警告注释
3. 所有 URL 访问必须经过用户明确授权
4. 定期检查文件名是否可能被恶意利用

**规则**:
- 不自动抓取任何 URL
- URL 必须来自可信来源
- 敏感文件名永不作为 URL 处理

