# BEO-10339 未评论故障补评

- 操作者：吴优
- Run ID：bug-20261113T162500+0800-BEO-10339
- 涉及 Jira：BEO-10339
- 操作类型：评论 Jira
- 读取证据：评论前预检 jira、google_drive 均为 fresh，入口 google_api。已下载 C673-G/D587G翻译清单261015 并读取对应 sheet。
- 写入摘要：评论 8881732，挂依据截图。未回填吴优 bug 表。
- Jira 动作：评论 BEO-10339。状态仍为待办，经办人仍为 you.wu。未转派、未关闭。
- 回读校验：评论回读包含授权正文和（AI Generated）。
- 未执行动作：未写表、未关闭、未改状态、未改经办人。
- 敏感信息处理：未记录账号、密码、token 或访问口令。

## BEO-10339 决策核验卡

- 备注因果链：俄语快捷车窗、全开、全关用了单数，客户预期是复数。
- 客户问题识别：否，无外部客户编号。
- 关联票：已检查，无直接关联票。
- 证据画像与必查资料：general。Google Drive API 已检索翻译清单。
- 资料适用范围：C673-G/D587G翻译清单261015，BigsurCarSettings car_window、car_settings_window_open、car_settings_window_close。
- 冲突处理：俄语快捷车窗、全开、全关用了单数，客户预期是复数。
- 唯一结论：结论：D587-G 欧亚快捷界面的车窗、全开、全关应按复数改俄语。现行 C673-G/D587G翻译清单261015 的 BigsurCarSettings 里，car_window「车窗」是「Окно」，car_settings_window_open「全开」是「Полностью открыто」，car_settings_window_close「全关」是「Полностью закрыто」。这三个控件作用的是多个车窗，单数和客户预期不一致。表里另有复数「Окна」，不能用单数句覆盖这里。
依据：[C673-G/D587G翻译清单261015 车窗俄语|https://docs.google.com/spreadsheets/d/1Hv2_mKeL0JqcSr8AaMXKnSDhjHTcDN3Y/edit]。
处理：这三个 Key 的俄语改成「Окна」「Полностью открыты」「Полностью закрыты」。不要改描述单个车窗状态的句子。翻译处理。
