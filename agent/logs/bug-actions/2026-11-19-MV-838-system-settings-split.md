# 2026-11-19 MV-838 拆分语音设置和能量管理分屏

- 操作者：吴优（本机预检绑定 `wu-you`）
- 读取证据：Jira MCP 回读 MV-838、MV-839、MV-921、MV-7。MV-838 到 MV-921 的既有关系为 Issue split。查重未发现同名分屏故事及 UI Task。MV-7 标题为 `ECR_待签署`，状态待办。
- UE：用户提供《长安深蓝518&857交互设计文档_系统设置分屏_v0.1.pdf》，共 11 页。通过 `google_api` 上传到系统设置 UE 既有共享目录。回读大小 46119223 字节、MD5 `1eb191d61ea955d56755ae2dd2ec353b` 与本地一致，域内 reader 权限与此前系统设置 UE 一致。https://drive.google.com/file/d/1mAEVsnK0af5YlOBcWW6INPLbQItVvJnr/view
- Jira 写入：创建语音设置分屏故事 MV-1019、UI Task MV-1020，能量管理分屏故事 MV-1021、UI Task MV-1022。两故事从 MV-838 按 Issue split 拆分，各与对应 UI Task 建立 Relates。四票描述均使用同一新版 UE。
- 字段：两故事沿用 MV-838 的经办人明逸智、P1、Android - SystemSettings、修复版本 `SW01-C518_1&C857_3_VS_20261230`。UI Task 与对应故事的描述及上述字段一致。四票 Epic Link 为 MV-7。
- 回读：用 `get_jira_issue` 逐票确认标题、类型、状态、经办人、优先级、模块、Epic、描述及关联双向一致，REST 回读修复版本一致。MV-838 原描述、经办人、状态和附件保持原值。
- 操作范围：未评论、未发飞书、未更新变更管理表，未修改已有 UI Task MV-839。
