---
name: product-marketing-context
description: "创建和维护产品营销上下文文档。用于捕获基础定位和信息，其他营销技能会引用此文档，避免用户重复回答相同问题。"
---

# 产品营销上下文 (Product Marketing Context)

帮助用户创建和维护产品营销上下文文档。这会捕获基础定位和信息，供其他营销技能引用，这样用户就不用重复回答相同问题。

文档保存在 `.agents/product-marketing-context.md`。

## 工作流程

### 步骤 1：检查现有上下文

首先，检查 `.agents/product-marketing-context.md` 是否已存在。也检查 `.claude/product-marketing-context.md`（旧设置）——如果在那里找到但不在 `.agents/` 中，可以迁移。

**如果存在：**
- 阅读并总结已捕获的内容
- 询问用户想更新哪些部分
- 只收集那些部分的信息

**如果不存在，提供两个选项：**

1. **自动起草（推荐）：** 你会研究代码库——README、落地页、营销文案、package.json 等——然后起草 V1 上下文文档。用户然后审查、纠正和填补空白。这比从头开始更快。

2. **从零开始：** 逐步对话每个部分，一次收集一个部分的信息。

大多数用户偏好选项 1。展示草稿后问："什么需要纠正？缺少什么？"

### 步骤 2：收集信息

**如果自动起草：**
- 阅读代码库：README、落地页、营销文案、关于页面、元描述、package.json、任何现有文档
- 根据你找到的起草所有部分
- 展示草稿并问什么需要纠正或遗漏
- 迭代直到用户满意

**如果从零开始：** 逐步对话每个部分，一次一个。不要一次抛出所有问题。

**对于每个部分：**
- 简要解释你正在捕获什么
- 问相关问题
- 确认准确性
- 进入下一个

推动使用客户的原话—— exact phrases 比精炼的描述更有价值，因为它们反映了客户实际的思考和说话方式，这使文案更能引起共鸣。

## 要捕获的部分

### 1. 产品概览
- 一句话描述
- 它做什么（2-3 句）
- 产品类别（你所在的"货架"——客户如何搜索你）
- 产品类型（SaaS、市场、电商、服务等）
- 商业模式和定价

### 2. 目标受众
- 目标公司类型（行业、规模、阶段）
- 目标决策者（角色、部门）
- 主要用例（你解决的主要问题）
- 要完成的工作（客户"雇佣"你做的 2-3 件事）
- 具体用例或场景

### 3. 人物角色（B2B only）
如果涉及多个购买决策者，为每个捕获：
- 用户、Champion、决策者、财务买家、技术影响者
- 每个关心什么，他们的挑战，以及你承诺的价值

### 4. 问题与痛点
- 客户找到你之前面临的核心挑战
- 为什么现有解决方案不足
- 这让他们付出了什么（时间、金钱、机会）
- 情绪紧张（压力、恐惧、疑虑）

### 5. 竞争格局
- **直接竞争对手：** 相同解决方案，相同问题（如 Calendly vs SavvyCal）
- **次要竞争对手：** 不同解决方案，相同问题（如 Calendly vs Superhuman 调度）
- **间接竞争对手：** 冲突方法（如 Calendly vs 个人助理）
- 每个如何对客户不足

### 6. 差异化
- 关键差异化（替代方案缺乏的能力）
- 你如何不同地解决它
- 为什么这更好（收益）
- 为什么客户选择你而不是替代方案

### 7. 反对意见与反人物角色
- 销售中听到的 3 大反对意见以及如何应对
- 谁不是合适的人选（反人物角色）

### 8. 切换 dynamics

JTBD 四力：
- **Push（推）：** 什么挫折促使他们离开当前解决方案
- **Pull（拉）：** 什么吸引他们到你这里
- **Habit（习惯）：** 什么让他们坚持当前方法
- **Anxiety（焦虑）：** 什么让他们担心切换

### 9. 客户语言
- 客户如何描述问题（原文）
- 他们如何描述你的解决方案（原文）
- 要使用的词/短语
- 要避免的词/短语
- 产品特定术语表

### 10. 品牌调性
- 语气（专业、随意、活泼等）
- 沟通风格（直接、对话、技术）
- 品牌个性（3-5 个形容词）

### 11. 证明点
- 要引用的关键指标或结果
- 知名客户/logo
- 推荐语片段
- 主要价值主题和支持证据

### 12. 目标
- 主要商业目标
- 关键转化行动（你希望人们做什么）
- 当前指标（如果知道）

## 步骤 3：创建文档

收集信息后，创建 `.agents/product-marketing-context.md`，使用以下结构：

```markdown
# Product Marketing Context

*Last updated: [date]*

## Product Overview

**One-liner:**
**What it does:**
**Product category:**
**Product type:**
**Business model:**

## Target Audience

**Target companies:**
**Decision-makers:**
**Primary use case:**
**Jobs to be done:**
- 
**Use cases:**
- 

## Personas

| Persona | Cares about | Challenge | Value we promise |
|---------|-------------|-----------|------------------|
| | | | |

## Problems & Pain Points

**Core problem:**
**Why alternatives fall short:**
- 
**What it costs them:**
**Emotional tension:**

## Competitive Landscape

**Direct:** [Competitor] — falls short because...
**Secondary:** [Approach] — falls short because...
**Indirect:** [Alternative] — falls short because...

## Differentiation

**Key differentiators:**
- 
**How we do it differently:**
**Why that's better:**
**Why customers choose us:**

## Objections

| Objection | Response |
|-----------|----------|
| | |

**Anti-persona:**

## Switching Dynamics

**Push:**
**Pull:**
**Habit:**
**Anxiety:**

## Customer Language

**How they describe the problem:**
- "[verbatim]"
**How they describe us:**
- "[verbatim]"
**Words to use:**
**Words to avoid:**
**Glossary:**

| Term | Meaning |
|------|---------|
| | |

## Brand Voice

**Tone:**
**Style:**
**Personality:**

## Proof Points

**Metrics:**
**Customers:**
**Testimonials:**
> "[quote]" — [who]
**Value themes:**

| Theme | Proof |
|-------|-------|
| | |

## Goals

**Business goal:**
**Conversion action:**
**Current metrics:**
```

## 步骤 4：确认和保存

- 展示完成的文档
- 问是否需要调整
- 保存到 `.agents/product-marketing-context.md`
- 告诉他们："其他营销技能现在会自动使用此上下文。运行 /product-marketing-context 可以随时更新。"

## 技巧

- **具体：** 问"什么 #1 挫折让他们来找你？"而不是"他们解决什么问题？"
- **捕获原话：** 客户语言胜过精炼描述
- **要例子：** "能给我一个例子吗？"能解锁更好的答案
- **验证：** 总结每个部分并在继续之前确认
- **跳过不适用的：** 不是每个产品都需要所有部分（如 B2C 的人物角色）
