# 2026-11-12 长马语料写回在线文件

- 操作者：吴优
- Run ID：20261112T1147+0800-corpus-drive
- 涉及 Jira：HUR-87169
- 操作类型：规则维护
- 读取证据：吴优指出应使用 Google API。Drive API 回读在线文件是 xlsx，Sheets API 返回 Office file 不能直接改。未打印凭证。
- 表格位置：Drive 文件 `1ny5OwV4Jrnjl1xFKxV-O16YiAWuv8L--`，变更履历第 2 行
- 写入摘要：补上长马语料必须写回在线 xlsx 的规则。线上变更履历写入 V1.3，并替换法语、挪威语、英语、阿语 8 句。
- Jira 动作：未评论，未流转
- 回读校验：Drive API 重新下载，V1.3 和 8 句与写入一致。`python3 agent/scripts/validate_rule_architecture.py` 通过。
- 未执行动作：未发飞书，未写 bug 表
- 敏感信息处理：未记录账号、密码、token 或访问口令
