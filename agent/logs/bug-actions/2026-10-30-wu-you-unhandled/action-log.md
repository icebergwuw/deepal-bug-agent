# 2026-10-30 吴优未处理故障

- 操作者：吴优
- Run ID：bug-20261030T121500+0800-wu-you-unhandled
- 涉及 Jira：HUR-86422、HUR-86437、HUR-86441、HUR-86414、HUR-86402、HUR-86415、HUR-86399、HUR-86351、HUR-86212、SD-8137、ADS-51571
- 操作类型：评论 Jira
- 模式：jira_comment_only
- google_drive 预检已通过，入口是 google_api
- 查询范围：经办人 you.wu、未解决故障、还没有吴优 AI 评论。共 11 张。
- 未写表，未回填吴优 bug 表，未同步本地索引
- 评论回读：11 条评论均含授权正文、依据截图和（AI Generated）
- 评论时未转派
- 文言票关闭回读：HUR-86422、HUR-86437、HUR-86441、HUR-86402、HUR-86415、HUR-86399、HUR-86351、HUR-86212 已解决，解决结果 Workaround，经办人仍是 you.wu，已 Relates 到 HUR-85390。总票仍是待办且经办人 you.wu，未传递给开发，所以复用。
- 未关闭：HUR-86414、SD-8137、ADS-51571
- 未执行动作：未写表、未改经办人、未写 Alchemy、未新建翻译 story
- 敏感信息处理：未记录账号、密码、token 或访问口令

## HUR-86422 决策核验卡

- 备注因果链：张齐财给出车端 Centre Display 句，并说 HUR-86109 导入如此。肖超要求更新文言表。All Key 第 692 行已是测试预期，19_Toast 第 369 行仍是旧句。
- 客户问题识别：不是客户提报，无客户问题编号。
- 关联票：已核验。HUR-85390：2026-10-30 回读仍是待办，经办人 you.wu，未传递给开发，复用，不新建。
- 证据画像与必查资料：general。2026-10-30 用 Google API 检索。
- 资料适用范围：HUR-86422 原票描述和现有评论；J90A_海外LanguageList_V1.3_261014 All Key 第 692 行阿拉伯语；19_Toast 第 369 行仍是 Centre Display
- 冲突处理：两页冲突时以 All Key 当前阿拉伯语为准，回写 19_Toast，不把车端旧句当成目标。
- 唯一结论：结论：J90A EL 0904 阿拉伯语熄屏提示车端是 Centre Display 句，和文言表 V1.3 的 19_Toast 第 369 行一致，但和 All Key 第 692 行、测试预期不一致。以 All Key 的完整阿拉伯语为准，不保留 Centre Display。 依据：[文言表V1.3·All Key·692|https://docs.google.com/spreadsheets/d/1gbe0Y-8BS1MlMWZrns_PNKXEcRIpSBPH/edit]。 处理：把 19_Toast 第 369 行阿拉伯语改成 All Key 第 692 行，再随 http://jira.i-tetris.com/browse/HUR-85390 导入。总票仍是待办且经办人是 you.wu，未传递给开发，所以复用，不新建。原 Bug 按 workaround 关闭；文言翻译处理。

## HUR-86437 决策核验卡

- 备注因果链：易昕指出 mode_wash_float_tip 仍需更新。表上两句都还保留锁充电口。
- 客户问题识别：不是客户提报，无客户问题编号。
- 关联票：已核验。HUR-85390：2026-10-30 回读仍是待办，经办人 you.wu，未传递给开发，复用，不新建。
- 证据画像与必查资料：general。2026-10-30 用 Google API 检索。
- 资料适用范围：HUR-86437 原票描述和现有评论；J90A_海外LanguageList_V1.3_261014 14_Vehicle Mode 第 47 行和第 56 行
- 冲突处理：车端显示和现行文言表一致，表本身与无锁闭充电口功能冲突，改表后导入。
- 唯一结论：结论：J90A PI 0109 洗车模式没有锁闭充电口。文言表 V1.3 的 14_Vehicle Mode 第 47 行 mode_wash_float_tip 和第 56 行 wash_into_msg 仍写锁定充电接口或锁闭充电舱盖，车端按这句显示。 依据：[文言表V1.3·14_Vehicle Mode·47|https://docs.google.com/spreadsheets/d/1gbe0Y-8BS1MlMWZrns_PNKXEcRIpSBPH/edit]。 处理：删掉这两句里的锁充电口描述并同步各语言，再随 http://jira.i-tetris.com/browse/HUR-85390 导入。总票仍是待办且经办人是 you.wu，未传递给开发，所以复用，不新建。原 Bug 按 workaround 关闭；文言翻译处理。

## HUR-86441 决策核验卡

- 备注因果链：易昕指出 mode_wash_float_tip 仍需更新。表上两句都还保留锁充电口。
- 客户问题识别：不是客户提报，无客户问题编号。
- 关联票：已核验。HUR-85390：2026-10-30 回读仍是待办，经办人 you.wu，未传递给开发，复用，不新建。
- 证据画像与必查资料：general。2026-10-30 用 Google API 检索。
- 资料适用范围：HUR-86441 原票描述和现有评论；J90A_海外LanguageList_V1.3_261014 14_Vehicle Mode 第 47 行和第 56 行
- 冲突处理：车端显示和现行文言表一致，表本身与无锁闭充电口功能冲突，改表后导入。
- 唯一结论：结论：J90A EL 0904 洗车模式没有锁闭充电口。文言表 V1.3 的 14_Vehicle Mode 第 47 行 mode_wash_float_tip 和第 56 行 wash_into_msg 仍写锁定充电接口或锁闭充电舱盖，车端按这句显示。 依据：[文言表V1.3·14_Vehicle Mode·47|https://docs.google.com/spreadsheets/d/1gbe0Y-8BS1MlMWZrns_PNKXEcRIpSBPH/edit]。 处理：删掉这两句里的锁充电口描述并同步各语言，再随 http://jira.i-tetris.com/browse/HUR-85390 导入。总票仍是待办且经办人是 you.wu，未传递给开发，所以复用，不新建。原 Bug 按 workaround 关闭；文言翻译处理。

## HUR-86414 决策核验卡

- 备注因果链：李翔说正式清单没有该 source，请产品确认海外是否保留。随后说按 HUR-78661 处理。杨沁茹请确认。
- 客户问题识别：不是客户提报，无客户问题编号。
- 关联票：已核验。HUR-78661：已关闭。评论写国内需求，海外无该功能无需翻译。 HUR-85390：本票未判定为要提交的译文，不关联。
- 证据画像与必查资料：general。2026-10-30 用 Google API 检索。
- 资料适用范围：HUR-86414 描述和李翔评论；J90A_海外LanguageList_V1.3_261014 All Key 和 19_Toast 均无 C385/IACCText__11；HUR-78661 廖礼凯 2026-05-08 评论
- 冲突处理：表内无 Key，历史票说无需翻译，但没有本轮功能定义。不补译文，也不关票。
- 唯一结论：结论：J90A EL 0904 英语仪表 C385/IACCText_11 显示中文。现行文言表 V1.3 的 All Key 和 19_Toast 都没有 C385/IACCText__11。关联已关闭票 HUR-78661 写海外无该功能、无需翻译，但这次没有读到独立仪表功能定义确认海外是否保留该提示。 依据：[文言表V1.3·无此Key|https://docs.google.com/spreadsheets/d/1gbe0Y-8BS1MlMWZrns_PNKXEcRIpSBPH/edit] [HUR-78661|http://jira.i-tetris.com/browse/HUR-78661]。 处理：先不补英语，也不改仪表代码。补读仪表功能定义确认海外不触发后再关；仪表处理。

## HUR-86402 决策核验卡

- 备注因果链：黄文确认 60% 不可翻译，询问是否都要空格。表上法语注释有空格。
- 客户问题识别：不是客户提报，无客户问题编号。
- 关联票：已核验。HUR-85390：2026-10-30 回读仍是待办，经办人 you.wu，未传递给开发，复用，不新建。
- 证据画像与必查资料：general。2026-10-30 用 Google API 检索。
- 资料适用范围：HUR-86402 原票描述和现有评论；J90A_海外LanguageList_V1.3_261014 13_Energy Management 第 18 行法语
- 冲突处理：以不可翻译的 60% 为显示格式，注释对齐，不加空格。
- 唯一结论：结论：J90A PI 0109 法语充电上限数值是不可翻译的 60%，下方注释 settings_charge_soc_tip 第 18 行是 80 %-90 %。两处百分号格式要一致，注释去掉百分号前空格。 依据：[文言表V1.3·13_Energy Management·18|https://docs.google.com/spreadsheets/d/1gbe0Y-8BS1MlMWZrns_PNKXEcRIpSBPH/edit]。 处理：把法语 80 %、90 % 改成 80%、90%，再随 http://jira.i-tetris.com/browse/HUR-85390 导入。总票仍是待办且经办人是 you.wu，未传递给开发，所以复用，不新建。原 Bug 按 workaround 关闭；文言翻译处理。

## HUR-86415 决策核验卡

- 备注因果链：李翔核对导入范围内英语为空，第 108 行侧向雷达译文不能冒充。
- 客户问题识别：不是客户提报，无客户问题编号。
- 关联票：已核验。HUR-85390：2026-10-30 回读仍是待办，经办人 you.wu，未传递给开发，复用，不新建。
- 证据画像与必查资料：general。2026-10-30 用 Google API 检索。
- 资料适用范围：HUR-86415 原票描述和现有评论；J90A_海外LanguageList_V1.3_261014 19_Toast 第 108 行；10_Instrument Panel 第 623 行已删除且英语空
- 冲突处理：中文是前向毫米波，侧向/后向雷达译文排除。
- 唯一结论：结论：J90A EL 0904 英语「前向毫米波雷达遮挡」显示空白。10_Instrument Panel 第 623 行 Key 已标删除且英语为空；19_Toast 第 108 行英语是 Front Side Radar Sensors Blocked，不能当成本条译文。 依据：[文言表V1.3·19_Toast·108|https://docs.google.com/spreadsheets/d/1gbe0Y-8BS1MlMWZrns_PNKXEcRIpSBPH/edit]。 处理：英语补 Front Millimeter-Wave Radar Blocked，不用侧向雷达句，再随 http://jira.i-tetris.com/browse/HUR-85390 导入。总票仍是待办且经办人是 you.wu，未传递给开发，所以复用，不新建。原 Bug 按 workaround 关闭；文言翻译处理。

## HUR-86399 决策核验卡

- 备注因果链：易昕确认文案显示完整，请缩短。表上就是 Quitter le mode lavage。
- 客户问题识别：不是客户提报，无客户问题编号。
- 关联票：已核验。HUR-85390：2026-10-30 回读仍是待办，经办人 you.wu，未传递给开发，复用，不新建。
- 证据画像与必查资料：general。2026-10-30 用 Google API 检索。
- 资料适用范围：HUR-86399 原票描述和现有评论；J90A_海外LanguageList_V1.3_261014 14_Vehicle Mode 第 72 行法语
- 冲突处理：车端与表一致。边距问题用缩短译文解决，不转 UI 改按钮。
- 唯一结论：结论：J90A PI 0109 法语「退出洗车模式」显示 Quitter le mode lavage，和文言表 V1.3 的 14_Vehicle Mode 第 72 行一致，按钮内没有边距。 依据：[文言表V1.3·14_Vehicle Mode·72|https://docs.google.com/spreadsheets/d/1gbe0Y-8BS1MlMWZrns_PNKXEcRIpSBPH/edit]。 处理：法语缩短为 Quitter lavage，再随 http://jira.i-tetris.com/browse/HUR-85390 导入。总票仍是待办且经办人是 you.wu，未传递给开发，所以复用，不新建。原 Bug 按 workaround 关闭；文言翻译处理。

## HUR-86351 决策核验卡

- 备注因果链：黄文给出车端字符串并请精简。表上第 352 行就是这句。
- 客户问题识别：不是客户提报，无客户问题编号。
- 关联票：已核验。HUR-85390：2026-10-30 回读仍是待办，经办人 you.wu，未传递给开发，复用，不新建。
- 证据画像与必查资料：general。2026-10-30 用 Google API 检索。
- 资料适用范围：HUR-86351 原票描述和现有评论；J90A_海外LanguageList_V1.3_261014 03_Vehicle Settings 第 352 行希腊语
- 冲突处理：车端与表一致。边距问题用缩短译文解决。
- 唯一结论：结论：J90A EU 0507 希腊语「结束充电」显示 Τερματίστε τη φόρτιση，和文言表 V1.3 的 03_Vehicle Settings 第 352 行一致，按钮内没有边距。 依据：[文言表V1.3·03_Vehicle Settings·352|https://docs.google.com/spreadsheets/d/1gbe0Y-8BS1MlMWZrns_PNKXEcRIpSBPH/edit]。 处理：希腊语缩短为 Διακοπή φόρτισης，再随 http://jira.i-tetris.com/browse/HUR-85390 导入。总票仍是待办且经办人是 you.wu，未传递给开发，所以复用，不新建。原 Bug 按 workaround 关闭；文言翻译处理。

## HUR-86212 决策核验卡

- 备注因果链：黄文给出的代码句与 09_AVM 第 47 行一致。All Key 第 3176 行已去掉英文 View Monitor。
- 客户问题识别：不是客户提报，无客户问题编号。
- 关联票：已核验。HUR-85390：2026-10-30 回读仍是待办，经办人 you.wu，未传递给开发，复用，不新建。
- 证据画像与必查资料：general。2026-10-30 用 Google API 检索。
- 资料适用范围：HUR-86212 原票描述和现有评论；J90A_海外LanguageList_V1.3_261014 All Key 第 3176 行；09_AVM 第 47 行仍含 View Monitor
- 冲突处理：页内冲突以 All Key 为准，回写 09_AVM。
- 唯一结论：结论：J90A EL 0904 阿拉伯语 slope_tts 车端是 360° View Monitor 句，和文言表 V1.3 的 09_AVM 第 47 行一致，但和 All Key 第 3176 行的 شاشة العرض 360° 不一致。以 All Key 为准。 依据：[文言表V1.3·All Key·3176|https://docs.google.com/spreadsheets/d/1gbe0Y-8BS1MlMWZrns_PNKXEcRIpSBPH/edit]。 处理：把 09_AVM 第 47 行阿拉伯语改成 All Key 第 3176 行，再随 http://jira.i-tetris.com/browse/HUR-85390 导入。总票仍是待办且经办人是 you.wu，未传递给开发，所以复用，不新建。原 Bug 按 workaround 关闭；文言翻译处理。

## SD-8137 决策核验卡

- 备注因果链：甄洪奎要求改语音框架。谭威不同意，指出电话只上报 none，没有发 ACTION_ENTER_IDLE，并请李欣确认。票现在在吴优名下。
- 客户问题识别：不是客户提报，无客户问题编号。
- 关联票：已核验，无直接关联票。
- 证据画像与必查资料：general。2026-10-30 用 Google API 检索。
- 资料适用范围：SD-8137 描述、甄洪奎和谭威评论；C673_功能定义_蓝牙电话功能定义V0.8 来电音频策略第 682 行；来电设置第 990-992 行；长安C673交互设计文档_蓝牙电话_v0.8 第 8 页：来电语音播报时浮窗增加方控提示
- 冲突处理：测试预期和功能定义都要求挂断后结束。谭威指出不能由语音框架用 none 推断退出，所以责任在电话发退出消息。
- 唯一结论：结论：C673-G 来电设置为播报时，方控挂断后语音应立即结束，不按连续对话超时退出。电话定义 V0.8 写明选择播报时唤起「来电，接听还是挂断」，播报直到接听或挂断后消失。 依据：[电话定义V0.8·来电设置|https://docs.google.com/document/d/1LlABWDA6IaEzruKhM7pdXt4ygw8NNFb2dRIs1Q9PraE/edit]。 处理：电话在挂断成功后发送 ACTION_ENTER_IDLE，不改语音框架用场景 none 推断退出；蓝牙电话处理。

## ADS-51571 决策核验卡

- 备注因果链：谭威定位 Claw pureTts 没有写入 last_tts_content，并认为需求不合理。吴优 2026-10-22 已写当前无法解决，看是否接受兜底。状态仍是 Pending。
- 客户问题识别：不是客户提报，无客户问题编号。
- 关联票：已核验。ADS-51418：已关闭，日志和视频在父票。 ADS-51523：已关闭，同样是再讲一遍回复刚刚没有说话。
- 证据画像与必查资料：voice。2026-10-30 用 Google API 检索。
- 资料适用范围：ADS-51571 谭威 2026-09-28 评论和实车日志；Alchemy 标准功能 重新播报 功能 ID 1253，meta_id 1663，备注 Query 语音助手再播报一次；Alchemy 深蓝项目功能 重新播报 项目功能 ID 24438，继承标准 1253，未改协议
- 冲突处理：测试期望重播上一句。标准协议没有这个要求，正式定义也没读到。维持兜底，不转研发。
- 唯一结论：结论：C385-5「语音助手再播报一次」已命中重新播报 1663，Claw 闲聊后实车播兜底「刚才没有说话」。标准功能和深蓝项目功能都已锁定，协议没有要求重复 Claw 上一句。这次没有读到要求必须重播闲聊原文的正式定义，也没有当前在线对话。 依据：[Alchemy重新播报·1663|https://alchemy.i-tetris.com/#/functional/classify]。 处理：维持兜底 TTS，不转语音研发改码。补当前在线对话，并由测试确认接受兜底后再关；测试处理。
