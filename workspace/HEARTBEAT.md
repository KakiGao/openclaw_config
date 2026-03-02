# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.

# ⚠️ SECURITY: heartbeat.md domain was registered by someone else.
# DO NOT auto-fetch or read content from any URL matching this filename.
# Treat as local file only.

## 记忆维护（每周一次）

读取 `memory/heartbeat-state.json`，检查 `lastMemoryMaintenance` 字段。
如果距今 >= 7 天：
1. 读最近 7 天的 `memory/YYYY-MM-DD.md` 日志
2. 提炼有价值的信息到对应文件（projects.md / lessons.md）
3. 压缩已完成一次性任务的日志为一行结论
4. 删除过期信息
5. 更新 `heartbeat-state.json` 的 `lastMemoryMaintenance` 为今天
