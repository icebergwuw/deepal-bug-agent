# 2026-11-24 MV-1117 荣耀车联任意门建票

- 操作者：吴优（本机预检绑定 `wu-you`）。
- 来源：用户指定《EPA1平台化-荣耀车联功能定义 V1.1.docx》和《C385&673交互设计文档_地图导航（高德）_850_V0.8.pdf》。取 PRD 4.2.19「特色功能-荣耀任意门」及连接章节的回连顺序，整理手机端拖拽解析、已连接直达搜索、未连接缓存回连及搜索导航链路。
- Drive：通过 `google_api` 核对 MV-140 的现有 PRD 与本地文件 1641338 字节及 MD5 `e9c557d27e9544a0fd16d1e9d8ac8219` 一致，复用 https://drive.google.com/file/d/1eg78UdgQPCPEGSl5DOg4BJquuy3e3wMQ/view 。同名地图 UE 的旧在线文件内容不同，上传用户提供的 PDF 到 C518&C857 共享 UE 目录，使用继承权限。回读 19388346 字节、MD5 `4603b30fe0c40162cae9eede31f571e1` 与本地一致。https://drive.google.com/file/d/1AiMncxZmed3lcbJnBllPD5FL4Y7b1usC/view
- Jira：查重未发现同名故事；新建 MV-1117「【功能模块】荣耀车联-任意门」，经办人舒万里、优先级 P1、模块产品需求、修复版本 `SW01-C518_1&C857_3_VS_20261230` 沿用同模块 MV-140，Epic 使用未关闭的 MV-7「ECR_待签署」。两份 Drive 链接均写入描述，Relates 关联 MV-140。
- 回读：`get_jira_issue` 逐票回读确认新票标题、类型、描述、经办人、优先级、模块、Epic 与双向关联。REST 回读修复版本与参考票一致。已提示 UI Task 可另建。
