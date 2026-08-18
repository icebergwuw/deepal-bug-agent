# 2026-08-18 每日新增 Bug 运行记录

- Run ID：`bug-20260818T010508Z-3613f6b1-439e-46c6-b63f-c1de83fe8502`
- 运行时间：2026-08-18 09:05（Asia/Shanghai）
- 操作者 / 目标负责人：吴优（`wu-you`）
- Jira 查询：`assignee = "you.wu" AND project in (SD,HUR,ADS,BGS,BEO,PC,SM,SLV) AND issuetype = Bug AND status in ("To Do",Reopened,"In Progress",Pending) ORDER BY key ASC`
- Jira 命中：107 个唯一 Key。
- 本地负责人索引：351 个唯一登记 Key；线上原始 A:J 本轮无法读取，因此仅以最近一次已验证索引做去重基线。
- 本次新增且尚未登记：`ADS-47844`、`ADS-48790`、`ADS-48837`、`ADS-48847`、`HUR-83121`、`HUR-83232`、`HUR-83268`、`HUR-83269`、`HUR-83271`、`HUR-83275`、`SM-17768`。

## Jira 完整读取

已逐票读取上述 11 个 Jira 的字段、描述、附件元数据、全部评论和直接关联票；每票评论/附件/关联数量、更新时间、完整响应 SHA-256 和字节数保存在 `2026-08-18-daily-new-bugs-evidence-receipts.json`。未执行 Jira 评论、转派、关闭或状态变更。

## 产品处理状态

本轮仅完成新增 Key 发现与 Jira 证据读取，未形成可写入的产品结论。11 票均需继续补齐正式 Drive 资料、引用追查和适用版本枚举；语音/车外语音票还需逐票重测 Alchemy 当前原话、标准功能点和深蓝项目功能点；涉及可见交互的票需刷新 MasterGo。客户提报票缺完整可比对用例时保持待确认并由吴优收集完整客户测试用例。

## 写入与阻塞

- 未更新吴优线上 bug 清单、未更新本地索引，不产生写入行号。
- 当前工具面没有 schema v5 `search_completion` 所需的 Drive 结构化搜索回执，也没有 Sheets 原始 A:J 元数据写回/回读能力；按 fail-closed 禁止生成 manifest、prewrite 请求和线上写入。
- 未执行 Alchemy 逐票复测；MasterGo回执过期，相关票据按证据门禁降级。
- 本轮 run bundle 状态为 `blocked`，不可表述为 Bug 已完成处理。

## 未完成项

1. 恢复 Drive 结构化检索并逐项打开/排除全部候选，完成引用文档追查和版本族枚举。
2. 对语音相关票据逐票核验 Alchemy 原话、MetaId、标准功能点和项目功能点。
3. 生成并通过 11 份 schema v5 manifest、决策核验卡与 prewrite run bundle。
4. 使用结构化 Sheets 接口写入实际行并完成 A:J 原始回读、校验 JSON、`readback_sha256` 和 final run 校验。
