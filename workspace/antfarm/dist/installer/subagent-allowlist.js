function normalizeAllow(value) {
    if (!Array.isArray(value)) {
        return [];
    }
    return value.filter((entry) => typeof entry === "string");
}
function uniq(values) {
    return Array.from(new Set(values));
}
function ensureAgentToAgent(config) {
    if (!config.tools) {
        config.tools = {};
    }
    if (!config.tools.agentToAgent) {
        config.tools.agentToAgent = { enabled: true };
    }
    return config.tools.agentToAgent;
}
export function addSubagentAllowlist(config, agentIds) {
    if (agentIds.length === 0) {
        return;
    }
    const agentToAgent = ensureAgentToAgent(config);
    const existing = normalizeAllow(agentToAgent.allow);
    // If "*" is in the list, all agents are already allowed
    if (existing.includes("*")) {
        return;
    }
    agentToAgent.allow = uniq([...existing, ...agentIds]);
}
export function removeSubagentAllowlist(config, agentIds) {
    if (agentIds.length === 0) {
        return;
    }
    const agentToAgent = ensureAgentToAgent(config);
    const existing = normalizeAllow(agentToAgent.allow);
    if (existing.includes("*")) {
        return;
    }
    const next = existing.filter((entry) => !agentIds.includes(entry));
    agentToAgent.allow = next.length > 0 ? next : undefined;
}
