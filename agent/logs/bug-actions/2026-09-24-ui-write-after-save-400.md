# 2026-09-24 页面保存 400 后改走界面

- 操作者：吴优 / `wu-you`
- Run ID：`rules-20260924T-ui-write-after-save-400`
- 涉及 Jira：ADS-50547
- 操作类型：规则维护
- 读取证据：ADS-50547 第427行的 Chrome 界面写入，以及页面 `/save` 富文本返回 HTTP 400、没有新修订号
- 表格位置：吴优 bug 页第427行，本轮不改单元格
- 写入摘要：同一张表记录 `/save` HTTP 400 后，下一票直接走 Chrome 界面。取消必须按 Esc 退出；编辑态读到短标签 URL 且退出后链接仍在才算核对完成
- Jira 动作：未评论 Jira / 未流转 Jira
- 回读校验：`python3 agent/scripts/test_bug_run.py`。未通过 API final，本轮也没有新的界面写表
- run bundle：不适用
- readback_sha256：不适用
- 未执行动作：未改 ADS-50547 第427行，未改 SD-7944 第426行，未改 Jira、Text ID、LanguageList 或 Alchemy
- 敏感信息处理：未记录账号、密码、token、sid、ouid 或访问口令

## 规则变化

- API 阻断后，没有 `/save` HTTP 400 记录时仍先试页面 `/save`。
- 已有 HTTP 400 且没有新修订号时，不再重试 `/save`。
- 界面顺序是名称框跳格、编辑态粘贴、插入短标签，编辑中途不点表格空白。
- Esc 清掉链接标记时重新加载并放弃编辑，不得提交纯文本。
