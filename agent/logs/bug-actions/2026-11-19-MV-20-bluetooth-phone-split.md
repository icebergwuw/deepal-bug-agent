# 2026-11-19 MV-20 拆票：蓝牙电话分屏

- 操作者：吴优（本机预检绑定 `wu-you`）
- 读取证据：Jira MCP 回读 MV-20、MV-532、MV-7。MV-20 已有 Issue split 拆票关系，MV-532 定义非华为分屏框架并将蓝牙电话分屏适配排除在该票范围之外。Jira 查重未发现同名分屏故事和 UI Task。
- Jira 写入：创建 MV-1024「[分屏]蓝牙电话分屏」故事，按 Issue split 挂在 MV-20 下；创建 MV-1025「[分屏]蓝牙电话分屏-UI」任务，按 Relates 关联 MV-1024。
- 字段：两票均沿用 MV-20 的经办人舒万里、优先级 P1、模块「产品需求」和修复版本 `SW01-C518_1&C857_3_VS_20261230`。Epic Link 为未关闭的 MV-7「ECR_待签署」。
- 描述：以 MV-20 的蓝牙电话 PRD 作为功能基线，引用 MV-532 的分屏框架。Jira、Drive 和本地资料未定位到 C518&C857 蓝牙电话分屏交互稿，UE 段写待补充。
- 回读：用 `get_jira_issue` 核对两票描述、字段和关联方向，REST 核对修复版本。MV-20 原描述、经办人、状态和附件与建票前一致。
- 操作范围：未评论、未发飞书、未改变更管理表。

## 补充蓝牙电话 UE

- 吴优提供《长安C518&C857交互设计文档_蓝牙电话_v0.1.pdf》，共 13 页。通过 `google_api` 上传到 C518&C857 当前共享 UE 目录，域内 reader 权限与系统设置分屏 UE 一致。回读大小 7080112 字节、MD5 `da429b69584fdd2fe5c3ea6fbf1aa63c` 与本地一致。https://drive.google.com/file/d/1AEdSLt5etF3G4WwEOYx5j43w-KlZmMxy/view
- Jira REST 更新 MV-1024 和已关联的 UI Task MV-1025 的 UE 段。通过 `get_jira_issue` 逐票回读，两票完整描述与预期一致，其余业务字段和关联与更新前一致。
