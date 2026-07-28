# MasterGo Magic MCP 渠道验证

- 日期：2026-07-17
- 类型：资料渠道与规则维护
- Jira：无；本次未处理具体 Bug

## 验证内容

- 查阅 MasterGo Magic MCP 官方仓库，确认设计读取需要 `fileId + layerId` 或 MasterGo 短链，并受团队版、团队项目访问范围限制。
- 从线上 `深蓝8155` 工作说明定位到语音形象&GUI、地图等模块的现有 MasterGo 链接。
- 使用 MasterGo Magic MCP v0.2.4 完成服务启动、运行时鉴权和工具列表读取。
- 以两个工作说明中的真实链接测试；链接仅提供 `page_id`，按页面编号尝试读取均返回空结构，未取得可引用的 UE 内容。

## 结论与规则变更

- MasterGo 纳入条件可用的正式资料渠道。
- 有 `layer_id` 或 MasterGo 短链时直接通过 MCP 读取；只有 `page_id` 时不能声称已读 UE，需补图层链接或短链。
- 已更新 `agent/product-kb/sources.md`、`agent/context.md` 和 `agent/workflows/bug.md`。
- 本次未修改线上表、Jira 或 MasterGo 文件；运行时凭证未写入项目文件和日志。
