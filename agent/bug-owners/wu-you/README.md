# 吴优 Bug 工作区

路由状态、Jira 显示名/账号、线上页、页签、gid 和本地索引只以 `../registry.yaml` 的 `wu-you` 条目为准，本文件不复制这些可变配置。

## 专属入口

- Jira 待处理查询：[吴优 PC Bug](http://jira.i-tetris.com/browse/PC-37264?jql=project%20%3D%20PC%20AND%20issuetype%20%3D%20Bug%20AND%20status%20in%20%28%22To%20Do%22%2C%20Reopened%2C%20%22In%20Progress%22%2C%20Pending%29%20AND%20assignee%20in%20%28membersOf%28product-ca%29%29%20AND%20assignee%20%3D%20you.wu)
- 公共流程：`../../workflows/bug.md`
- 表格契约：`../../sheet-contract.md`

同一 Jira 出现在李欣或冯智秀页时视为流转历史；保留其他页记录，只检查 `bug` 页内重复。
