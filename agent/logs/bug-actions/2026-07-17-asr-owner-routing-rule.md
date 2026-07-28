# ASR 识别错误责任路由

- 日期：2026-07-17
- 类型：产品规则与责任人沉淀
- 来源：吴优当前确认
- Jira：无；本次未处理具体 Bug

## 规则

- 确认属于 ASR 语音识别错误，即用户原话被识别成错误文本时，统一转汪文菁处理。
- 该规则是语音问题的研发处理人路由，不改变产品负责人线上页的负责人注册表。
- NLU、功能点、项目配置、TTS、VUI 或车端执行问题仍按各自证据分流，不能仅因属于语音问题就转汪文菁。

## 变更位置

- `agent/product-kb/modules/voice-vui.md`
- `agent/product-kb/org/component-owner-map.md`
- `agent/workflows/bug.md`

## 外部动作

- 未修改线上 Sheet、Jira、Drive、Alchemy 或 MasterGo 数据。
