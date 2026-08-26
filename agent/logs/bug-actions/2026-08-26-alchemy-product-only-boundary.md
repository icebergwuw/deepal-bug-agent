# Alchemy 产品专属修改边界

- 日期：2026-08-26
- 触发问题：PC-38902 语音切换音色，平台已命中 `meta_id=1402`，但 `mode_type=女` 的 canonical 为空。
- 项目审查：现有规则要求语音 Bug 查 Alchemy、标准功能点和项目功能点，但未明确 Alchemy 修改权限只属于产品。
- 本次规则：Alchemy 的意图、query/泛化、slot、literal/canonical、功能点继承、项目执行策略、TTS 话术和下发发布均由语音产品负责人操作；Agent 只读、测试、定位、提出操作清单、验收和回读。
- 分流边界：产品完成配置并下发且 canonical 正确后，仍执行失败，才转车端/语音服务研发。
- 未执行：未修改 Alchemy、未评论/转派/关闭 Jira，未写 Bug 表。
