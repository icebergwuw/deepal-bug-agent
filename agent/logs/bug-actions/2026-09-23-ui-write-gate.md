# 2026-09-23 Chrome 界面写表门禁

- 操作者：吴优 / `wu-you`
- Run ID：`rules-20260923T-ui-write-gate`
- 涉及 Jira：SD-7944
- 操作类型：规则维护
- 读取证据：SD-7944 界面写入过程、公式栏逐列回读、F426/H426 串入 `PC-37245` 的事实
- 表格位置：吴优 bug 页 SD-7944 行426
- 写入摘要：新增 `chrome_ui` 兜底和 `validate_bug_run.py --phase ui`。API final 仍是默认收口，界面回读不能冒充。
- Jira 动作：未评论 Jira / 未流转 Jira
- 回读校验：规则测试见 `agent/scripts/test_bug_run.py`；SD-7944 使用界面回读，未通过 API final
- run bundle：`agent/logs/bug-actions/bug-20260923T141818+0800-SD-7944-run-bundle.json`
- readback_sha256：API 回读不适用。Chrome 界面兜底改为写 `ui_readback_sha256`
- 未执行动作：未改 Jira，未改 Text ID、LanguageList 或 Alchemy
- 敏感信息处理：未记录账号、密码、token 或访问口令

## 规则变化

- 截图不能代替逐列公式栏回读。
- 富文本链接进编辑态读取，按 Esc 退出，Enter 不作为换行或核对结束。
- 新增行 F/H 写后必须为空；串入其他票标题必须清空并标记 `contamination_cleared`。
- `ui_verified` 只通过 `--phase ui`，送进 `--phase final` 必须失败。
