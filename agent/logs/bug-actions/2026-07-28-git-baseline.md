# Bug 工作区 Git 基线

- 日期：2026-07-28
- 操作类型：版本治理 / Git 初始化
- 涉及 Jira：无
- Jira 动作：未评论、未转派、未关闭、未修改状态
- 线上表格动作：未读取、未写入

## 操作

- 初始化本地 Git 仓库，默认分支为 `main`。
- 建立当前 `v1.1.0-trial.3` 规则、索引、知识库、历史证据和日志基线。
- 使用仓库本地提交身份 `Codex <codex@local>`，不修改用户全局 Git 配置。
- `.gitignore` 明确排除 `.env`、`.env.*`、`.mastergo/`、`.DS_Store`、`__pycache__/` 和 `*.pyc`；保留 `.env.example`。
- 敏感模式只做文件名级扫描，未发现私钥、Bearer token 或 `sk-` 密钥模式。

## 安全边界

- `.env` 中存在 Jira 连接变量，因此保持 ignored，未进入暂存区或提交。
- `.mastergo/` 是本地设计缓存，保持 ignored。
- 不在日志中记录任何凭据值。

## 验证

- 当前分支必须为 `main`。
- 架构校验必须返回 `ok: true`。
- 基线提交后工作区必须 clean；ignored 文件仍保持未跟踪。
