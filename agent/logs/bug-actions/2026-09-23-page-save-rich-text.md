# 2026-09-23 页面 /save 富文本链接

- 操作者：吴优
- Run ID：20260923T-page-save-rich-text
- 涉及 Jira：SD-7944
- 操作类型：规则维护
- 读取证据：已登录 Chrome 中的吴优 bug 页；此前页面 `/save` 对 K426 的两链接试写在重载后的编辑态读到了 URL
- 表格位置：bug!K426，仅作通道试写；A426:J426 不作为试写目标
- 写入摘要：`sheet_page_save.py` 现在可以生成 http(s) 富文本短标签命令。复选框验证和锚点格式仍走界面兜底
- Jira 动作：未评论 Jira / 未流转 Jira
- 回读校验：本轮只核对清空结果。K426 公式栏为空。A426 仍是 `2026-09-23`，B426 仍是 SD-7944 链接。试写当时的编辑态链接已在上一轮确认，本轮没有再次写入
- run bundle：不适用
- readback_sha256：不适用。页面 `/save` 未通过 API final
- 未执行动作：未评论 Jira、未流转 Jira、未改 SD-7944 的 A:J、未改 Text ID 或 LanguageList
- 敏感信息处理：未记录账号、密码、token、sid、ouid 或访问口令

## 通道结论

- 纯文本和清空仍用外层 opcode `21299578`。
- 富文本短标签用外层 opcode `25813757`。单元格命令有 27 个字段，格式和链接按短标签起止位置成对写入。
- 写后不能只看空闲公式栏。富文本必须进编辑态读 `data-sheets-formula-bar-text-link`，然后按 Esc 退出。
