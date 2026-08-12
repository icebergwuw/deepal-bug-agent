# 2026-08-12 运行证据与日志闭环门禁

- Run ID：20260812T105609+0800-daily-bug-recheck
- 操作者：Codex（本机绑定 wu-you）
- 涉及 Jira：无（本文件记录规则维护；11票复查详见独立逐Key日志）
- 操作类型：规则维护 / 本地索引修复 / 普通复查
- 读取证据：项目全部权威规则、现有校验脚本与测试；Google Drive真实检索结果及候选正文；线上负责人清单；写后A:J回读
- 表格位置：吴优 `bug!A321:J331`；李欣线上清单与本地索引一致性校验
- 写入摘要：manifest升级schema v4；新增Drive检索回执、run_context、run bundle与final回读门禁；自动化强制每次留日志；修正李欣本地索引多出的HUR-80041和ADS-45249；11条只更新C/D/I/J并保留待复核
- Jira 动作：未评论 Jira / 未转派 Jira / 未关闭 Jira / 未变更状态
- 回读校验：run bundle final通过；A:J、B公式、C/D/J链接、E列BOOLEAN、保护列、WRAP格式和11个目标Key唯一性均通过；历史重复SLV-44272仍为2条，非本次产生
- run bundle：agent/logs/bug-actions/2026-08-12-daily-new-bugs-run.json
- readback_sha256：64025e54b811fd6f64107b54f29cbb4cb38525d4fd3ec8a309d9705a347d7d4a
- 未执行动作：未补造历史缺失日志；未执行任何Jira外部动作；Alchemy仍停在SSO登录页
- 敏感信息处理：未记录账号、密码、token 或访问口令

## 规则验证

- `validate_rule_architecture.py`：通过。
- `test_bug_evidence_gate.py`：28项通过；覆盖假零结果、缺回执和候选漏审。
- `test_bug_run.py`：3项通过；覆盖写前、写后哈希和无新增日志。
- `test_bug_sheet_contract.py`：16项通过。
- `test_bug_project_preflight.py`：7项通过。
- `git diff --check`：通过。

## 未完成项

- 11条语音相关Bug均因Alchemy当前原话、标准功能点和项目功能点不可访问而保持`待复核`；恢复登录后再形成确定性产品判断。
- HUR-77192与HUR-72809在最新J90A海外LanguageList V1.1指定Sheet/范围均精确零命中，仍需取得MRE当前语料条目。
- PC-38471/38472/38473仍缺当前生效的可见配置和完整UE节点/图层；已读8295页面开启需求v2.6只部分覆盖新增唤醒词页面。
- 历史日志覆盖不足不伪造补录；以后触及旧票时从当次开始按完整run闭环留痕。
