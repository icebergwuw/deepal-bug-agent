# 2026-11-19 长马文言 Bug 转需求

- 操作者：吴优
- Run ID：bug-20261119T182253+0800-hur-87144-wording-close
- 涉及 Jira：HUR-87579、HUR-87500、HUR-87496、HUR-87497、HUR-87486、HUR-87481、HUR-87472、HUR-87460、HUR-87459、HUR-87458、HUR-87306、HUR-87356、HUR-87355
- 承接需求：HUR-87144，待办，经办人 you.wu。复用，关联类型 Blocks。
- 授权：吴优要求按流程关联 HUR-87144 并关票。
- 预检：jira 与 google_drive 均通过。Drive 文件通过 google_api 检索并下载，MD5 为 dcd17082ff0981166875594cfed5c5a3。只使用 V1.2.3 的 01–21 页。
- 未写表，未回填吴优 Bug 表，未转派。
- 流转字段：解决结果 Workaround，Root Cause 为需求问题_需求变更，保留修复版本、QA、严重程度和经办人。
- 首张 HUR-87579 的试跑关联方向反了，已删除本次创建的反向关联并按总票向外 Blocks 重建，双向回读通过。

| 原 Bug | 评论回读 | 依据附件 | 关联 | 回读状态 | 解决结果 |
|---|---|---|---|---|---|
| HUR-87579 | 8930944 | 4713364 | Blocks | 已解决 | Workaround |
| HUR-87500 | 8930951 | 4713378 | Blocks | 已解决 | Workaround |
| HUR-87496 | 8930952 | 4713379 | Blocks | 已解决 | Workaround |
| HUR-87497 | 8930953 | 4713380 | Blocks | 已解决 | Workaround |
| HUR-87486 | 8930954 | 4713381 | Blocks | 已解决 | Workaround |
| HUR-87481 | 8930956 | 4713382 | Blocks | 已解决 | Workaround |
| HUR-87472 | 8930957 | 4713383 | Blocks | 已解决 | Workaround |
| HUR-87460 | 8930958 | 4713384 | Blocks | 已解决 | Workaround |
| HUR-87459 | 8930959 | 4713387 | Blocks | 已解决 | Workaround |
| HUR-87458 | 8930960 | 4713389 | Blocks | 已解决 | Workaround |
| HUR-87306 | 8930961 | 4713390 | Blocks | 已解决 | Workaround |
| HUR-87356 | 8930963 | 4713393 | Blocks | 已解决 | Workaround |
| HUR-87355 | 8930964 | 4713394 | Blocks | 已解决 | Workaround |

- 回读校验：当前已核验 Workaround 及 Blocks 13/13 张。最终回读使用每张原票的 close-readback.json。
- 总票回读：已确认。

## HUR-87579 决策核验卡

- 备注因果链：0507 匈牙利语后排安全带报警在快捷栏出现单字母换行，研发已定位到 rear_seat_belt_alarm。
- 客户问题识别：Jira 实车测试提报。
- 关联票：已回读 HUR-87144，待办，经办人 you.wu。
- 证据画像与必查资料：general，读取原票和当前 J90A 海外文言表。
- 资料适用范围：02_Launcher AA21，0507 / 0109 / 0904 的 V1.2.3 导入源。
- 冲突处理：agent/context.md 指定 2026-11-17 中科返回 V1.2.3 用于 0507、0109、0904 三分支导入。Drive 源文件校验值与已下载文件一致。V1.3_261014 是另一文件，当前口径按指定导入版。
- 唯一结论：以下为该票授权正文。

结论：0507 匈牙利语后排安全带报警在快捷栏出现单字母换行，研发已定位到 rear_seat_belt_alarm。
依据：[Text ID V1.2.3 · 02_Launcher AA21|https://docs.google.com/spreadsheets/d/1e6OJUwu2YOYxAOFb16exX4rjpbYyv6GC/edit]、[现场现象和研发定位|http://jira.i-tetris.com/browse/HUR-87579]。
处理：请中科提供可在快捷栏完整显示的短译，与 0109 的 HUR-87027 共用同一 Key 的匈牙利语修改项。 当前翻译需求尚未交付开发，复用 [HUR-87144|http://jira.i-tetris.com/browse/HUR-87144] 追踪，原 Bug 按 Workaround / bug转需求关闭。中科处理。

## HUR-87500 决策核验卡

- 备注因果链：0507 小憩设置页英语提示的 20% 在源文里也缺少半角空格。
- 客户问题识别：Jira 实车测试提报。
- 关联票：已回读 HUR-87144，待办，经办人 you.wu。
- 证据画像与必查资料：general，读取原票和当前 J90A 海外文言表。
- 资料适用范围：14_Vehicle Mode O10、O138，0507 / 0109 / 0904 的 V1.2.3 导入源。
- 冲突处理：agent/context.md 指定 2026-11-17 中科返回 V1.2.3 用于 0507、0109、0904 三分支导入。Drive 源文件校验值与已下载文件一致。V1.3_261014 是另一文件，当前口径按指定导入版。
- 唯一结论：以下为该票授权正文。

结论：0507 小憩设置页英语提示的 20% 在源文里也缺少半角空格。
依据：[Text ID V1.2.3 · 14_Vehicle Mode O10、O138|https://docs.google.com/spreadsheets/d/1e6OJUwu2YOYxAOFb16exX4rjpbYyv6GC/edit]、[现场现象和研发定位|http://jira.i-tetris.com/browse/HUR-87500]。
处理：请中科将小憩设置提示中的 20% 改为 20 %，与 0109 已收录的小憩话术共用文言修改项。 当前翻译需求尚未交付开发，复用 [HUR-87144|http://jira.i-tetris.com/browse/HUR-87144] 追踪，原 Bug 按 Workaround / bug转需求关闭。中科处理。

## HUR-87496 决策核验卡

- 备注因果链：0507 俄语「播放」在蓝牙音乐按钮内断词。研发回读的 Воспроизведение 与文言表一致，需缩短译文。
- 客户问题识别：Jira 实车测试提报。
- 关联票：已回读 HUR-87144，待办，经办人 you.wu。
- 证据画像与必查资料：general，读取原票和当前 J90A 海外文言表。
- 资料适用范围：05_Media AH17，0507 / 0109 / 0904 的 V1.2.3 导入源。
- 冲突处理：agent/context.md 指定 2026-11-17 中科返回 V1.2.3 用于 0507、0109、0904 三分支导入。Drive 源文件校验值与已下载文件一致。V1.3_261014 是另一文件，当前口径按指定导入版。
- 唯一结论：以下为该票授权正文。

结论：0507 俄语「播放」在蓝牙音乐按钮内断词。研发回读的 Воспроизведение 与文言表一致，需缩短译文。
依据：[Text ID V1.2.3 · 05_Media AH17|https://docs.google.com/spreadsheets/d/1e6OJUwu2YOYxAOFb16exX4rjpbYyv6GC/edit]、[现场现象和研发定位|http://jira.i-tetris.com/browse/HUR-87496]。
处理：请中科给 common_play_text 提供能在一行完整显示的俄语短译。 当前翻译需求尚未交付开发，复用 [HUR-87144|http://jira.i-tetris.com/browse/HUR-87144] 追踪，原 Bug 按 Workaround / bug转需求关闭。中科处理。

## HUR-87497 决策核验卡

- 备注因果链：0109 匈牙利语「氛围灯」出现单字母换行。研发回读的 Hangulatvilágítás 与文言表一致，需缩短译文。
- 客户问题识别：Jira 实车测试提报。
- 关联票：已回读 HUR-87144，待办，经办人 you.wu。
- 证据画像与必查资料：general，读取原票和当前 J90A 海外文言表。
- 资料适用范围：02_Launcher AA45，0507 / 0109 / 0904 的 V1.2.3 导入源。
- 冲突处理：agent/context.md 指定 2026-11-17 中科返回 V1.2.3 用于 0507、0109、0904 三分支导入。Drive 源文件校验值与已下载文件一致。V1.3_261014 是另一文件，当前口径按指定导入版。
- 唯一结论：以下为该票授权正文。

结论：0109 匈牙利语「氛围灯」出现单字母换行。研发回读的 Hangulatvilágítás 与文言表一致，需缩短译文。
依据：[Text ID V1.2.3 · 02_Launcher AA45|https://docs.google.com/spreadsheets/d/1e6OJUwu2YOYxAOFb16exX4rjpbYyv6GC/edit]、[现场现象和研发定位|http://jira.i-tetris.com/browse/HUR-87497]。
处理：请中科给 ambient_light_title 提供能在一行完整显示的匈牙利语短译。 当前翻译需求尚未交付开发，复用 [HUR-87144|http://jira.i-tetris.com/browse/HUR-87144] 追踪，原 Bug 按 Workaround / bug转需求关闭。中科处理。

## HUR-87486 决策核验卡

- 备注因果链：0109 波兰语热管理系统通讯异常提示保留强制换行，第一段超出仪表宽度后再次折行。V1.2.3 仪表页已去掉该译文换行，但后导入的 Toast 页仍有换行。
- 客户问题识别：Jira 实车测试提报。
- 关联票：已回读 HUR-87144，待办，经办人 you.wu。
- 证据画像与必查资料：general，读取原票和当前 J90A 海外文言表。
- 资料适用范围：19_Toast X253、10_Instrument Panel AE338，0507 / 0109 / 0904 的 V1.2.3 导入源。
- 冲突处理：agent/context.md 指定 2026-11-17 中科返回 V1.2.3 用于 0507、0109、0904 三分支导入。Drive 源文件校验值与已下载文件一致。V1.3_261014 是另一文件，当前口径按指定导入版。
- 唯一结论：以下为该票授权正文。

结论：0109 波兰语热管理系统通讯异常提示保留强制换行，第一段超出仪表宽度后再次折行。V1.2.3 仪表页已去掉该译文换行，但后导入的 Toast 页仍有换行。
依据：[Text ID V1.2.3 · 19_Toast X253、10_Instrument Panel AE338|https://docs.google.com/spreadsheets/d/1e6OJUwu2YOYxAOFb16exX4rjpbYyv6GC/edit]、[现场现象和研发定位|http://jira.i-tetris.com/browse/HUR-87486]。
处理：请中科将 19_Toast 的波兰语译文改为单行，由弹窗按宽度自动换行。 当前翻译需求尚未交付开发，复用 [HUR-87144|http://jira.i-tetris.com/browse/HUR-87144] 追踪，原 Bug 按 Workaround / bug转需求关闭。中科处理。

## HUR-87481 决策核验卡

- 备注因果链：0109 荷兰语低电下电提示仍带强制换行，第一段超出弹窗宽度后导致额外折行。
- 客户问题识别：Jira 实车测试提报。
- 关联票：已回读 HUR-87144，待办，经办人 you.wu。
- 证据画像与必查资料：general，读取原票和当前 J90A 海外文言表。
- 资料适用范围：19_Toast W213，0507 / 0109 / 0904 的 V1.2.3 导入源。
- 冲突处理：agent/context.md 指定 2026-11-17 中科返回 V1.2.3 用于 0507、0109、0904 三分支导入。Drive 源文件校验值与已下载文件一致。V1.3_261014 是另一文件，当前口径按指定导入版。
- 唯一结论：以下为该票授权正文。

结论：0109 荷兰语低电下电提示仍带强制换行，第一段超出弹窗宽度后导致额外折行。
依据：[Text ID V1.2.3 · 19_Toast W213|https://docs.google.com/spreadsheets/d/1e6OJUwu2YOYxAOFb16exX4rjpbYyv6GC/edit]、[现场现象和研发定位|http://jira.i-tetris.com/browse/HUR-87481]。
处理：请中科去掉 19_Toast 荷兰语译文中的强制换行，由弹窗按宽度自动换行。 当前翻译需求尚未交付开发，复用 [HUR-87144|http://jira.i-tetris.com/browse/HUR-87144] 追踪，原 Bug 按 Workaround / bug转需求关闭。中科处理。

## HUR-87472 决策核验卡

- 备注因果链：0109 波兰语智驾辅助重新认证提示在源表保留强制换行，导致仪表显示额外折行。
- 客户问题识别：Jira 实车测试提报。
- 关联票：已回读 HUR-87144，待办，经办人 you.wu。
- 证据画像与必查资料：general，读取原票和当前 J90A 海外文言表。
- 资料适用范围：19_Toast X131、10_Instrument Panel AE461，0507 / 0109 / 0904 的 V1.2.3 导入源。
- 冲突处理：agent/context.md 指定 2026-11-17 中科返回 V1.2.3 用于 0507、0109、0904 三分支导入。Drive 源文件校验值与已下载文件一致。V1.3_261014 是另一文件，当前口径按指定导入版。
- 唯一结论：以下为该票授权正文。

结论：0109 波兰语智驾辅助重新认证提示在源表保留强制换行，导致仪表显示额外折行。
依据：[Text ID V1.2.3 · 19_Toast X131、10_Instrument Panel AE461|https://docs.google.com/spreadsheets/d/1e6OJUwu2YOYxAOFb16exX4rjpbYyv6GC/edit]、[现场现象和研发定位|http://jira.i-tetris.com/browse/HUR-87472]。
处理：请中科同步移除这两处波兰语译文中的强制换行，由弹窗按宽度自动换行。 当前翻译需求尚未交付开发，复用 [HUR-87144|http://jira.i-tetris.com/browse/HUR-87144] 追踪，原 Bug 按 Workaround / bug转需求关闭。中科处理。

## HUR-87460 决策核验卡

- 备注因果链：0109 生命体征雷达故障提示的仪表中文匹配列丢了换行，导致波兰语沿用旧资源。
- 客户问题识别：Jira 实车测试提报。
- 关联票：已回读 HUR-87144，待办，经办人 you.wu。
- 证据画像与必查资料：general，读取原票和当前 J90A 海外文言表。
- 资料适用范围：10_Instrument Panel F565、N565、AE565，0507 / 0109 / 0904 的 V1.2.3 导入源。
- 冲突处理：agent/context.md 指定 2026-11-17 中科返回 V1.2.3 用于 0507、0109、0904 三分支导入。Drive 源文件校验值与已下载文件一致。V1.3_261014 是另一文件，当前口径按指定导入版。
- 唯一结论：以下为该票授权正文。

结论：0109 生命体征雷达故障提示的仪表中文匹配列丢了换行，导致波兰语沿用旧资源。
依据：[Text ID V1.2.3 · 10_Instrument Panel F565、N565、AE565|https://docs.google.com/spreadsheets/d/1e6OJUwu2YOYxAOFb16exX4rjpbYyv6GC/edit]、[现场现象和研发定位|http://jira.i-tetris.com/browse/HUR-87460]。
处理：请中科恢复 N565 在逗号后的原始换行，保留 AE565 的波兰语译文，使其能按实际中文重新匹配导入。 当前翻译需求尚未交付开发，复用 [HUR-87144|http://jira.i-tetris.com/browse/HUR-87144] 追踪，原 Bug 按 Workaround / bug转需求关闭。中科处理。

## HUR-87459 决策核验卡

- 备注因果链：0109 生命体征雷达故障提示的仪表中文匹配列丢了换行，影响意大利语资源匹配。
- 客户问题识别：Jira 实车测试提报。
- 关联票：已回读 HUR-87144，待办，经办人 you.wu。
- 证据画像与必查资料：general，读取原票和当前 J90A 海外文言表。
- 资料适用范围：10_Instrument Panel F565、N565、AB565，0507 / 0109 / 0904 的 V1.2.3 导入源。
- 冲突处理：agent/context.md 指定 2026-11-17 中科返回 V1.2.3 用于 0507、0109、0904 三分支导入。Drive 源文件校验值与已下载文件一致。V1.3_261014 是另一文件，当前口径按指定导入版。
- 唯一结论：以下为该票授权正文。

结论：0109 生命体征雷达故障提示的仪表中文匹配列丢了换行，影响意大利语资源匹配。
依据：[Text ID V1.2.3 · 10_Instrument Panel F565、N565、AB565|https://docs.google.com/spreadsheets/d/1e6OJUwu2YOYxAOFb16exX4rjpbYyv6GC/edit]、[现场现象和研发定位|http://jira.i-tetris.com/browse/HUR-87459]。
处理：请中科恢复 N565 在逗号后的原始换行，保留 AB565 的意大利语译文。该中文源文与同 Key 的其他语种票合并处理。 当前翻译需求尚未交付开发，复用 [HUR-87144|http://jira.i-tetris.com/browse/HUR-87144] 追踪，原 Bug 按 Workaround / bug转需求关闭。中科处理。

## HUR-87458 决策核验卡

- 备注因果链：0109 生命体征雷达故障提示的仪表中文匹配列丢了换行，导致西班牙语沿用旧资源。
- 客户问题识别：Jira 实车测试提报。
- 关联票：已回读 HUR-87144，待办，经办人 you.wu。
- 证据画像与必查资料：general，读取原票和当前 J90A 海外文言表。
- 资料适用范围：10_Instrument Panel F565、N565、W565，0507 / 0109 / 0904 的 V1.2.3 导入源。
- 冲突处理：agent/context.md 指定 2026-11-17 中科返回 V1.2.3 用于 0507、0109、0904 三分支导入。Drive 源文件校验值与已下载文件一致。V1.3_261014 是另一文件，当前口径按指定导入版。
- 唯一结论：以下为该票授权正文。

结论：0109 生命体征雷达故障提示的仪表中文匹配列丢了换行，导致西班牙语沿用旧资源。
依据：[Text ID V1.2.3 · 10_Instrument Panel F565、N565、W565|https://docs.google.com/spreadsheets/d/1e6OJUwu2YOYxAOFb16exX4rjpbYyv6GC/edit]、[现场现象和研发定位|http://jira.i-tetris.com/browse/HUR-87458]。
处理：请中科恢复 N565 在逗号后的原始换行，保留 W565 的西班牙语译文。该中文源文与同 Key 的其他语种票合并处理。 当前翻译需求尚未交付开发，复用 [HUR-87144|http://jira.i-tetris.com/browse/HUR-87144] 追踪，原 Bug 按 Workaround / bug转需求关闭。中科处理。

## HUR-87306 决策核验卡

- 备注因果链：0109 充电电流限值介绍的英语源文将数字和 A 连写，且 10A 前的不定冠词有误。
- 客户问题识别：Jira 实车测试提报。
- 关联票：已回读 HUR-87144，待办，经办人 you.wu。
- 证据画像与必查资料：general，读取原票和当前 J90A 海外文言表。
- 资料适用范围：13_Energy Management O55–O56，0507 / 0109 / 0904 的 V1.2.3 导入源。
- 冲突处理：agent/context.md 指定 2026-11-17 中科返回 V1.2.3 用于 0507、0109、0904 三分支导入。Drive 源文件校验值与已下载文件一致。V1.3_261014 是另一文件，当前口径按指定导入版。
- 唯一结论：以下为该票授权正文。

结论：0109 充电电流限值介绍的英语源文将数字和 A 连写，且 10A 前的不定冠词有误。
依据：[Text ID V1.2.3 · 13_Energy Management O55–O56|https://docs.google.com/spreadsheets/d/1e6OJUwu2YOYxAOFb16exX4rjpbYyv6GC/edit]、[现场现象和研发定位|http://jira.i-tetris.com/browse/HUR-87306]。
处理：请中科将 limit_summy_8 和 limit_summy_13 英语里的 10A、16A 分别改为 10 A、16 A，同步把 an 10A 改为 a 10 A。 当前翻译需求尚未交付开发，复用 [HUR-87144|http://jira.i-tetris.com/browse/HUR-87144] 追踪，原 Bug 按 Workaround / bug转需求关闭。中科处理。

## HUR-87356 决策核验卡

- 备注因果链：0904 充电电流限值介绍的英语源文把 10A 连写，且不定冠词写成 an。
- 客户问题识别：Jira 实车测试提报。
- 关联票：已回读 HUR-87144，待办，经办人 you.wu。
- 证据画像与必查资料：general，读取原票和当前 J90A 海外文言表。
- 资料适用范围：13_Energy Management O55，0507 / 0109 / 0904 的 V1.2.3 导入源。
- 冲突处理：agent/context.md 指定 2026-11-17 中科返回 V1.2.3 用于 0507、0109、0904 三分支导入。Drive 源文件校验值与已下载文件一致。V1.3_261014 是另一文件，当前口径按指定导入版。
- 唯一结论：以下为该票授权正文。

结论：0904 充电电流限值介绍的英语源文把 10A 连写，且不定冠词写成 an。
依据：[Text ID V1.2.3 · 13_Energy Management O55|https://docs.google.com/spreadsheets/d/1e6OJUwu2YOYxAOFb16exX4rjpbYyv6GC/edit]、[现场现象和研发定位|http://jira.i-tetris.com/browse/HUR-87356]。
处理：请中科将 limit_summy_8 英语的 an 10A power socket 改为 a 10 A power socket，与 0109 共用同一文言修改项。 当前翻译需求尚未交付开发，复用 [HUR-87144|http://jira.i-tetris.com/browse/HUR-87144] 追踪，原 Bug 按 Workaround / bug转需求关闭。中科处理。

## HUR-87355 决策核验卡

- 备注因果链：0904 充电电流限值介绍的英语源文把 16A 连写。
- 客户问题识别：Jira 实车测试提报。
- 关联票：已回读 HUR-87144，待办，经办人 you.wu。
- 证据画像与必查资料：general，读取原票和当前 J90A 海外文言表。
- 资料适用范围：13_Energy Management O56，0507 / 0109 / 0904 的 V1.2.3 导入源。
- 冲突处理：agent/context.md 指定 2026-11-17 中科返回 V1.2.3 用于 0507、0109、0904 三分支导入。Drive 源文件校验值与已下载文件一致。V1.3_261014 是另一文件，当前口径按指定导入版。
- 唯一结论：以下为该票授权正文。

结论：0904 充电电流限值介绍的英语源文把 16A 连写。
依据：[Text ID V1.2.3 · 13_Energy Management O56|https://docs.google.com/spreadsheets/d/1e6OJUwu2YOYxAOFb16exX4rjpbYyv6GC/edit]、[现场现象和研发定位|http://jira.i-tetris.com/browse/HUR-87355]。
处理：请中科将 limit_summy_13 英语的 16A 改为 16 A，与 0109 共用同一文言修改项。 当前翻译需求尚未交付开发，复用 [HUR-87144|http://jira.i-tetris.com/browse/HUR-87144] 追踪，原 Bug 按 Workaround / bug转需求关闭。中科处理。
