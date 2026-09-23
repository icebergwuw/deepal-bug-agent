# 2026-09-23 页面 /save 写表通道

- 操作者：Codex
- Run ID：20260923T-page-save
- 涉及 Jira：SD-7944
- 操作类型：规则维护
- 读取证据：吴优 bug 页当前 Chrome 登录态；页面 `/save` 与 `/bind` 请求形态
- 表格位置：bug!K426，仅作通道试写；A426:J426 不作为试写目标
- 写入摘要：新增 `sheet_page_save.py`。API 阻断后先写纯文本、单个 `=` 公式或清空；富文本、复选框验证和锚点格式仍走界面兜底
- Jira 动作：未评论 Jira / 未流转 Jira
- 回读校验：K426 写入 `pipeprobe` 后公式栏回读一致；`=2+2` 被公式栏按公式着色。清空并重新加载后 K426 为空。A426 仍是 `2026-09-23`，B426 仍是 SD-7944 链接
- run bundle：不适用
- readback_sha256：不适用。页面 `/save` 未通过 API final
- 未执行动作：未评论 Jira、未流转 Jira、未改 SD-7944 的 A:J、未改 Text ID 或 LanguageList
- 敏感信息处理：未记录账号、密码、token、sid、ouid 或访问口令

## 通道结论

- `sheets.googleapis.com` 的 `batchUpdate` 仍被阻断。gviz 返回 ACCESS_DENIED。
- 页面 `/save` 可以提交纯文本 opcode `132274236`、清空 opcode `132274237`，以及以 `=` 开头的用户输入公式。
- 富文本链接的页面命令没有带上 URI，本轮不把它做成可复用写入。
- 一次只提交一个单元格。修订号取响应中的新修订号，不写死。
