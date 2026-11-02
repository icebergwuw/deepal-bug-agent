# 2026-11-02 StoryID 回写改为超链接

- 操作者：吴优
- 操作类型：变更表回写修正
- 读取：Google API 回读 G74、G80、G94。原值为纯文本。
- 写入：三格改为超链接，显示票号，指向对应 Jira。G74 SD-8239，G80 SD-8240，G94 SD-8241。
- 回读校验：三格 hyperlink 分别为 http://jira.i-tetris.com/browse/SD-8239、SD-8240、SD-8241。显示文本仍是票号。
- 规则：变更表 StoryID/TaskID 以后回写必须是超链接。已写入建票 Skill 和 context。
- 未执行：未改其他行，未改 Jira，未发飞书。
- 敏感信息处理：未记录账号、密码、token 或 App Secret。
