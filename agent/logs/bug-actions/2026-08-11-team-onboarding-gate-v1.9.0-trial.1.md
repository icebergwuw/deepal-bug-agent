# 2026-08-11 团队首次运行与权限门禁

- 操作者：Codex
- 涉及 Jira：无
- 操作类型：规则维护 / Skill维护 / 团队交接能力
- 原因：项目通过Git迁移到其他成员电脑时仍固定吴优身份，Skill安装路径写死，且缺少Jira、Drive、Alchemy、MasterGo首次登录与权限引导。
- 修改摘要：新增本机私有身份、负责人写入范围、短期平台访问回执、首次运行文档和机器预检；将输出视角改为已绑定操作者；Skill和校验脚本改为可移植路径；`bug_sheet_contract.py build/patch` 已绑定身份、负责人范围和平台预检，不能绕过生成写表请求。
- 安全处理：未保存或使用任何密码、Token、Cookie、测试账号或平台访问口令；本机身份文件与 `outputs/` 已加入 `.gitignore`；本地 `.env` 保持忽略并收紧为 `0600`；仅允许推送私有仓库。
- 外部动作：未评论或流转Jira，未修改线上Bug表；已在GitHub账号 `icebergwuw` 创建私有仓库 `deepal-bug-agent`，等待本地提交与推送。
- 验证：onboarding预检7项、证据门禁26项、写表契约16项测试全部通过；规则架构、Skill同步、Python语法、越权只读、敏感信息和Git历史扫描、`git diff --check` 均通过。
- 回读：已回读新增入口、Skill模板、预检脚本、规则版本和本日志。
