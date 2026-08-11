# 2026-08-03 吴优 Bug 表 156-206 正式证据复核

- 范围：`bug!156:206`，51 行，SLV-44265 至 BEO-8444。
- 模式：`recheck`；仅更新 C/D/G/I/J，A/B/E/F/H 保持不变。
- Jira：逐票读取描述和完整评论；未评论、未转派、未关闭、未变更 Jira 状态。
- 正式资料：按工作说明路由检索 C673 全功能清单、车辆设置 PRD、C673 地图 UE、J90A 场景 UE/PRD、J90A 蓝牙电话 UE、J90A LanguageList、D587G 文言表及关联票。
- 语音：在 BIGSUR、SLV、HUR 项目分别现测相关 query；评论中的历史 `meta_id` 未直接当作当前项目结果。

## 结果分布

- 待确认 17
- 待复核 7
- 待会诊 5
- 可转研发 4
- 可转语音 3
- 转需求 10
- 待回归 1
- 可关闭 4

## 关键收敛

- SLV-44216、SLV-44215、SLV-44210：C673 地图 UE 有精确目标，转地图/地图 UI 研发。
- SLV-44214、SLV-44212：一票混有已定义行为和未定义视觉/入口，拆分并待会诊。
- SLV-44209：现行 UE 无“评论最新优先”规则，且客户最新评论确认非问题，可关闭。
- PC-38626：BIGSUR 的地图缩放功能点存在，仅票面表达未覆盖，转语音配置。
- HUR-82401、HUR-80734、HUR-81596、HUR-81537、HUR-81536、HUR-81535、HUR-81534、HUR-81441：当前 LanguageList 输入本身仍含混语/换行/空格或旧文案，定义为文言变更，不归应用渲染缺陷。
- HUR-80107、HUR-80100：HUR 现测分别拒识/误命中音乐，与历史目标功能点偏离，转语音配置。
- HUR-78542：完整音频复测通过，定义为测试资料问题，可关闭。
- HUR-72810：荷兰语“能量管理”不等于“能量流”，定义为预期翻译错误，可关闭。
- BEO-8444：最新评论确认文言表已更新，保留待回归，回归通过后关闭并由 HUR-82127 跟踪后续。

## 写回校验

- 写入请求：首次 255 个单元格更新；J 列富文本规范化补写 50 个；语言映射纠正 3 个 C 单元格。
- 回读：`bug!A156:J206` 共 51 行；Jira Key 顺序全部匹配。
- 目标列：C/D/G/I/J 的可见文本及 J 列链接目标全部匹配。
- 保护列：A/B/E/F/H 的写入态与写前一致，0 处变化。
- 本地索引：`agent/bug-owners/wu-you/index.md` 已同步最终状态。

## 主要原始入口

- [Bug 清单](https://docs.google.com/spreadsheets/d/1niNVFbugK2443IFe06H8nvZRC-e_r2b83YRBqXKGkqs/edit?gid=2135747181#gid=2135747181)
- [C673 全功能清单](https://docs.google.com/spreadsheets/d/15Qxx8f9A-fJ2o99f_bCLm2twGVERAmA4H1VyoovW6Y8)
- [C673 地图 UE](https://mastergo.com/file/131302242181530)
- [J90A 场景 UE](https://mastergo.com/file/104392407833015)
- [J90A 蓝牙电话 UE](https://mastergo.com/file/105655102802021?fileOpenFrom=project&page_id=359%3A5451)
- [J90A LanguageList](https://docs.google.com/spreadsheets/d/1IBKk0OOYGzLwPeAPoO9cUWMXm_fjZAk8NQGjeNE5F2g)
- [D587G 文言表](https://docs.google.com/spreadsheets/d/1Hv2_mKeL0JqcSr8AaMXKnSDhjHTcDN3Y/edit?pli=1&gid=1567380826#gid=1567380826)
- [Alchemy 现测会话](https://alchemy.i-tetris.com/#/conversation/testing?id=27475f07-6fc5-47dc-bd3a-af07750b1683&env=)
