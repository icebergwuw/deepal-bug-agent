# HUR-81074 证据位置补正

- 日期：2026-08-06
- 线上目标：`吴优工作说明 > bug!A84:J84`
- 触发：用户要求说明第 84 行结论在文档中的具体位置，并要求以后固定写明。
- Key 核对：用户文字写为 `HUR-80174`，线上第 84 行和本地索引实际均为 `HUR-81074`；本次按第 84 行处理。

## 原问题

- 上次 C/D/J 只列出资料名称和链接，没有写 Sheet、序号、页码、区域或附件时间码。
- 现行 `agent/evidence-contract.md` 原本已要求定位到具体章节、条款、图层、配置项或功能点；本次属于执行不合规，不是规则没有要求。

## 精确证据位置

- [J90A EU&EU PI座舱功能清单V3.1](https://drive.google.com/file/d/1t-A3jeXPJOwuR4-CUZBuGdOBsNWoJ6uK)：Sheet「J90A EU座舱功能清单」序号 938（系统需求编号 `I2-F70-00-00`，需求备注“0222：需求和国内保持一致”）与序号 939（`I2-F70-SF01-00`，小憩模式）。该来源只建立 EU PI 车型继承/搭载链。
- [J90A情景模式PRD V2.4](https://drive.google.com/file/d/1uf6I3DPvjm7r0_bABI3TDYTHLsUGzm7y)：第 13 页，章节「情景模式-小憩模式」；“小憩模式专属页面”区域写明专属页，“页面层级”写明“全屏显示，屏蔽 Dock 栏和状态栏”，“小憩模式异常提示/其他情况”写明“离开小憩页面：小憩模式自动退出”。
- [J90A情景模式交互 V2.6](https://drive.google.com/file/d/1XD8lJA0Pe5UcD7mdpTk1j3QtBCqkAIiL)：第 13 页，同一章节与区域再次明确专属全屏页、屏蔽 Dock/状态栏、离页自动退出。
- [Jira视频](http://jira.i-tetris.com/secure/attachment/4014693/video%2848%29.mp4)：总时长 10.42 秒；`00:02` 仍显示小憩专属页，`00:05` 已进入本地应用列表，关键复现段为 `00:02-00:06`。

## 规则修正

- 规则升级为 `v1.6.0-trial.1`，结构化资料新增必填 `source_location`。
- `validate_bug_evidence_gate.py` 会在任何资料缺少 `source_location` 时失败；C、D/H、J 同步要求展示精确位置。
- 未执行 Jira 评论、转派、关闭或状态变更。

## 写后回读

- 已按 `recheck` 定向更新 `bug!C84:D84`、`bug!I84:J84`；A/B/E/F/G/H 未提交且写后值保持不变，G 仍为 `可转研发`。
- C/D/I/J 可见文本与补正输入逐字一致；C 的 5 个、D 的 4 个、J 的 5 个短标签链接目标逐项一致。
- E 列 BOOLEAN 校验保留；C/D/I/J 仍为 Arial 10、垂直居中、自动换行。Chrome 正常缩放下已检查第 84 行，未见截断或样式破坏。
- 结构化证据门禁、单元测试、规则架构校验和 `git diff --check` 均通过。
