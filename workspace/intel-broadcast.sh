#!/bin/bash
# intel-broadcast.sh - 发送到多个 Discord 服务器

# 读取配置文件
CONFIG_FILE="$HOME/.openclaw/intel-broadcast.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo '{"servers": {}}' > "$CONFIG_FILE"
fi

# 运行 intel-daily.sh 获取情报
INTEL_OUTPUT=$(bash /Users/kaki/.openclaw/workspace/intel-daily.sh 2>/dev/null)

# 读取服务器配置
SERVERS=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['servers'].keys())" 2>/dev/null)

# 遍历发送
for guild_id in $SERVERS; do
    channel_id=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['servers']['$guild_id']['channel_id'])" 2>/dev/null)
    if [ -n "$channel_id" ]; then
        echo "📤 发送到服务器 $guild_id 频道 $channel_id"
        # 这里调用 OpenClaw message API
    fi
done
