# 2026-11-19 MV 情景模式 UE 更新

- 操作者：吴优（本机预检绑定 `wu-you`）
- 涉及 Jira：MV-28、MV-818（关联 UI Task）、MV-526（拆分开发任务）
- 读取证据：用户提供的《长安C518&C857交互设计文档_情景模式_v0.1.pdf》，共 14 页。Jira MCP 回读三票均引用同一份 WT 8155 平台旧版 UE。
- Drive 写入：通过 `google_api` 上传到旧版所在共享目录「深蓝8155平台UE文档」，保留旧版。新版链接 https://drive.google.com/file/d/1CKARw59YJM-FZd0ttqGy4hwVQT5k2LAJ/view
- Drive 回读：新版大小 39260299 字节，MD5 `9b68e1c12f3323aa662bd33dfc7746c7`，与本地一致。新旧文件继承权限一致。
- Jira 写入与回读：REST 仅替换三票 UE 段的文件名和链接。通过 `get_jira_issue` 逐票回读，完整描述与预期一致，PRD、其他需求描述、标题、状态、经办人、关联和 Epic 保持原值。
- 操作范围：沿用 MV-818，未新建 Jira 或评论，未写表或发飞书，未更改 MasterGo。
