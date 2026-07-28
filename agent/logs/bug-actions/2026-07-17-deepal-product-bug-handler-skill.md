# Deepal Product Bug Handler Skill

- 日期：2026-07-17
- 类型：Skill 与流程入口维护
- Jira：无；本次未处理具体 Bug

## 变更

- 新建全局 Skill：`/Users/you.wu/.codex/skills/deepal-product-bug-handler/`。
- Skill 不复制负责人名单、表格列定义和易变化资料链接；每次先读取 Bug 项目的权威文件。
- 固化默认 Jira 意图、负责人路由、完整评论时间线、Drive 直查、Alchemy 必查链路、MasterGo 条件读取、产品视角判断、线上表/索引/日志回读和复盘 H 列规则。
- MasterGo 只在运行时鉴权可用且提供 `layerId` 或短链时作为已读 UE；只有 `page_id` 或返回空结构时记录限制。
- 凭证不得写入 Skill、项目文件、日志、Sheet、Jira 或回复。

## 外部动作

- 未修改线上 Sheet、Jira、Drive、Alchemy 或 MasterGo 数据。

## 校验

- 使用 Skill Creator 的 `quick_validate.py` 校验通过：`Skill is valid!`
- 已回读 `SKILL.md` 与 `agents/openai.yaml`，触发描述、默认提示和项目权威入口一致。
- 已检查 Skill 与本次日志，未写入 MasterGo 凭证。
