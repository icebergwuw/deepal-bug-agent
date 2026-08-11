# Review And Meeting Workflow

这是会议纪要、可姐/leader 教学、Bug 复盘和客户后续反馈的唯一流程文件。

## 执行权限

- 首先按 `agent/onboarding.md` 和 `agent/scripts/bug_project_preflight.py` 核验本机身份、目标负责人写入范围及 Jira/Google Drive 权限；未通过时只整理复盘事实和权限引导，不写表。
- 先提炼结论更新、当前操作者待办、Agent 准确率和可沉淀规则。
- 用户给出会议纪要、可姐/leader 教学、客户复盘或明确复盘材料时，可按 `agent/config/sheet-update-modes.json` 的 `review` 模式更新对应负责人原行，并同步会议文件、待办和必要知识库。
- Jira 外部动作遵守 `AGENTS.md` 的全局权限边界；写 H 列不代表已执行 Jira 动作。

## 标准输出

1. `结论更新`：逐个 Jira 写最终产品结论、责任方、与旧判断的差异。
2. `当前操作者待办`：写可直接执行的评论、转派、建需求、拉群或补资料动作。
3. `准确率标注`：Agent 旧判断为对、错或待定，并说明关键原因；E 列仍由人工勾选。
4. `规则沉淀`：只沉淀可复用、证据明确的方法。
5. `待补信息`：列出仍会改变判断的未知项。

每个 Bug 的证据复核按 `agent/evidence-contract.md`；复盘同样形成当前要求的 `schema_version=3` manifest，使用 `agent/config/evidence-requirements.json` 完成全部画像和必查资料，并在写 H 前通过 `agent/scripts/validate_bug_evidence_gate.py`。标准结论、Jira 草稿和聊天复用按 `agent/output-contract.md`。

## Bug 表更新

- 先按 Jira 和负责人定位原行，不新增重复行。
- 后续反馈会改变原判断时，按证据契约重新读取当前 Jira 和决定性正式资料，重新判断全部证据画像并完成必查资料；不能仅凭一句研发或客户转述覆盖原结论。
- 复盘 manifest 的 `decision.text` 使用本轮 `final_decision_text`，确定性和待定状态均须通过同一证据门禁后才能写 G/H；客户或 leader 的明确最终结论可作为 `customer_final_decision`，但不能替代与结论有关的当前实现事实。
- 保留 D 列原始 Agent 判断和 F 列人工判断，最终处理写 H 列。
- H 写入 `agent/output-contract.md` 定义的 `final_decision_text`。
- 客户接受现有方案时，H 写“接受现状/结束跟进”，不能写成“已修复”。
- G 按复盘后的实际下一步更新为对应短状态；修改表格 G 不等于修改 Jira 状态，E 仍由人工勾选。
- H 列内容和链接按 `agent/sheet-contract.md` 写入并回读。
- I 写复盘后仍存在的唯一风险或门槛；J 汇总支撑 H 的原始可访问入口。C/D 保留普通处理阶段记录，详细复盘过程留在会议文件和操作日志。
- 复盘指出此前漏识别客户问题编号或漏收客户测试用例时，按证据契约将 G 改为 `待确认`，H 写向客户收集完整用例后复核；保留原 D/F 作为初次判断记录。

## 会议文件

- 每次会议在 `agent/meetings/` 新建 `YYYY-MM-DD-主题.md`。
- 同步更新 `agent/meetings/action-items.md`，待办必须有来源、负责人、状态和下一步。
- 原始长文本、旧表结构和历史颜色说明放 `agent/archive/`；现行证据、输出、流程和表格规则分别以对应权威契约为准。
- 规则变化更新对应权威文件或 `agent/product-kb/`，同时写操作日志。

## 会议纪要结构

1. 会议信息
2. 一句话结论
3. 结论更新
4. 当前操作者待办
5. Jira 注释草稿
6. 准确率标注
7. 规则沉淀
8. 待补信息

## 转需求记录

- 标题与原 Bug 对齐；按不同系统责任边界拆票。
- 背景写 `bug转需求`，描述附功能点、query、当前行为和目标行为。
- 关联原 Bug；多张需求票互相关联。
- 修复版本、合同/AP Link 和评审计划按当前项目规则填写，不沿用历史样例猜测。
