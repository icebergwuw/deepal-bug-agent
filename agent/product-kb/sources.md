# Sources

最后整理：2026-07-17。来源表记录可复用入口和读取边界，不以文件修改时间代替资料核验。

## 当前业务主数据与平台

| 来源 | 类型 | 用途 | 读取状态 / 边界 |
| --- | --- | --- | --- |
| [bug](https://docs.google.com/spreadsheets/d/1niNVFbugK2443IFe06H8nvZRC-e_r2b83YRBqXKGkqs/edit?gid=2135747181#gid=2135747181) / [深蓝8155](https://docs.google.com/spreadsheets/d/1niNVFbugK2443IFe06H8nvZRC-e_r2b83YRBqXKGkqs/edit?gid=717876892#gid=717876892) | Google Sheet | 当前 bug 主数据、模块背景、资料入口 | 可用 Sheets API 读取；`bug` 页为当前 bug 主数据源 |
| [罗稚钦bug](https://docs.google.com/spreadsheets/d/1niNVFbugK2443IFe06H8nvZRC-e_r2b83YRBqXKGkqs/edit?gid=99343087#gid=99343087) | Google Sheet | 罗稚钦当前 Bug 主数据 | 2026-07-16 已读取，A:J 共 134 条 Jira，页内无重复 |
| [Jira](http://jira.i-tetris.com) | Jira | Jira 字段、描述、评论时间线、附件和当前流转 | 需当前登录态；每个 bug 必须完整读取 |
| [Alchemy 在线对话](https://alchemy.i-tetris.com/#/conversation/testing?id=27475f07-6fc5-47dc-bd3a-af07750b1683&env=) / [功能分类](https://alchemy.i-tetris.com/#/functional/classify) | Web 平台 | 语音原话测试、`meta_id`、标准功能、项目继承和执行策略 | 需当前平台登录态；本地缓存不能替代实时读取 |
| Google Drive 项目资料 | Drive / Docs / Sheets / Office 文件 | PRD、UE、需求说明、组织架构、项目资料 | 每个问题按模块和版本检索；Office 文件按可用方式读取 |
| MasterGo 设计链接 | 设计平台 | UE/UI 证据和页面行为核对 | MasterGo Magic MCP v0.2.4 的启动、鉴权和工具发现已于 2026-07-17 验证；设计读取需 `fileId + layerId` 或 MasterGo 短链。只有 `page_id` 的工作说明链接不能算已读 UE；账号还需具备团队版及团队项目访问条件。`.mastergo/` 缓存不是正式来源 |

## 项目 / 产品资料

| 来源 | 类型 | 用途 | 读取状态 |
| --- | --- | --- | --- |
| `长安 C673&C385-Components.xlsx` | Office-backed spreadsheet | 组件、FO、包名、问题分析方法 | Sheets API 不支持；可通过 Drive 原始下载解析 |
| `深蓝项目经理和驻场工程师分工及安排` | Google Sheet | 项目经理、FAE、车型、平台 | 可用 Sheets API 读取 |
| `J90A_AllKey_静态补齐多语言_最终检查版` | Google Sheet | 多语言 key、页面文本、3D Control、All Key | 可用 Sheets API 读取 |
| `深蓝情景模式车型配置_20250516` | Google Sheet | 情景模式前置条件、TTS、车型支持 | 可用 Sheets API 读取 |
| [罗稚钦工作说明.xlsx](https://docs.google.com/spreadsheets/d/1VPXk6D0yPRZpMb9_dlLWd2RfHcPqp0Yz/edit?gid=2017792747#gid=2017792747) | Office-backed spreadsheet | 历史 Bug 处理方法、Jira 种子和模块资料入口 | 2026-07-16 已用 Drive 全文读取；118 个 Jira 链接、112 个唯一 Jira，混有历史记录和资料票，不视为当前在办清单 |

## 注意

- Components 表内含测试账号类信息，知识库只记录模块 / FO / 包名 / 责任边界，不记录账号密码。
- `罗稚钦bug` 是当前在办清单；旧 `罗稚钦工作说明.xlsx` 只作为方法和历史资料校准。处理 Bug 时仍需读当前 Jira 和正式资料。
- 资料是否“未找到”必须写明检索时间、资料入口和限制；详细规则见 `rules/source-freshness.md`。

## 历史检索基线

以下内容只记录当时检索结果，不代表当前仍无其他资料：

| 模块 | 核验日期 | 当时结果 | 下次处理要求 |
| --- | --- | --- | --- |
| 语音形象与 GUI | 2026-07-03 | 工作说明中只定位到 MasterGo UE 入口 | 重新检索 Drive 和当前需求资料，并读取可用目标图层 |
| 地图 | 2026-07-03 | 工作说明中只定位到 MasterGo UE 入口 | 按当前 query、功能和交互阶段检索专项资料 |
| 蓝牙电话 | 2026-07-03 | 工作说明中只定位到 MasterGo UE 入口；历史对接线索为雷磊 | 重新核对当前 Jira、正式资料和当前责任映射 |
| 场景积木 | 2026-07-03 | 工作说明中存在需求资料；单一版本未明确某些弹窗位置 | 按当前版本、功能点和交互阶段核对，不外推为永久规则 |
