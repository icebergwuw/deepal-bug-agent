# SM-18475 意大利语界面文案与语料不一致

- 操作者：吴优
- Run ID：bug-20261104T105200+0800-SM-18475
- 涉及 Jira：SM-18475
- 操作类型：评论 Jira
- 读取证据：评论前预检 google_drive 为 google_api 且 fresh，jira 与 alchemy 已验证。Jira 当前字段、评论；Google API 读取深蓝语料表、C673 车辆设置功能定义 V2.3、C673-G/D587G翻译清单261015。Alchemy 读了后雾灯和后追尾预警标准/项目功能点。未重跑在线对话。
- 写入摘要：评论 8805827，并挂语料与界面词截图 4636070。未回填吴优 bug 表。
- Jira 动作：评论 SM-18475。状态仍为待办，经办人仍为吴优。未转派、未关闭。
- 回读校验：评论回读包含授权正文、（AI Generated）和 SM-18475-corpus-ui.png。未转派。
- 未执行动作：未写表、未关闭、未改状态、未改经办人、未写 Alchemy、未改语料表。
- 敏感信息处理：未记录账号、密码、token 或访问口令。

## SM-18475 决策核验卡

- 备注因果链：测试说五条意大利语功能都能执行，只报文案和语料不一致。聂汉维要求确认语料。
- 客户问题识别：不是外部客户票。内测记录有原话、时间和日志名。
- 关联票：无直接关联票。
- 证据画像与必查资料：适用 voice。2026-11-04 用 Google API 检索并读 C673 车辆设置 V2.3；语料表和翻译清单已读到对应行。Alchemy 在线对话未重跑。
- 资料适用范围：语料表第205行打开后雾灯与关闭句用词不一致；第263行拖车模式写成 rimorchio；第283行后追尾预警是 tamponamento。V2.3 把拖车模式和拖挂模式分成两项。翻译清单第481、727、659行给出界面意大利语。
- 冲突处理：播放句和现行语料一致。后雾灯、拖车模式按翻译清单和 V2.3 改语料。后追尾预警不采用车上 Collisione postesteriore，因为翻译清单没有这个词。
- 唯一结论：结论：Saguaro 意大利语这五条功能都能执行，不是车端没按语料执行。后雾灯打开句和拖车模式的意大利语要改；后追尾预警不要按车上现在的词改语料。现行深蓝语料表标题仍是 V0.3.2.17，版本记录已到 V0.3.2.19，这三句没有后续改写。打开后雾灯是 Accendi la luce posteriore per nebbia，关闭句是 Spegni il fendinebbia posteriore。C673 翻译清单 BigsurCarSettings 第481行 settings_light_fog 意大利语是 Fari Fendinebbia Posteriori。打开句应改成 Accendi i fari fendinebbia posteriori。打开/关闭拖车模式现在写成 modalità rimorchio。C673 车辆设置 V2.3 把拖车模式定义成驻车维护里的平板拖车功能，语音指令就是开启/关闭拖车模式；拖挂模式是另一项，触发写的是开关，不是这句语料。翻译清单第727行 preference_trail_mode 是 Modalita traino d'emergenza，第756行拖挂模式才是 Modalità traino。车上显示 Modalità Traino di Emergenza，和拖车模式一致。语料里的 rimorchio 会和拖挂模式混，应改成 traino di emergenza。后追尾预警语料是 avviso di tamponamento posteriore。翻译清单第659行是 Avviso di collisione posteriore。车上的 Collisione postesteriore 不在这份清单里，不能当成目标词。这句语料先不改。依据：[深蓝语料表 深蓝-删减版 第205-206、263-264、283-284行|https://docs.google.com/spreadsheets/d/159bd_jBCou9dmXZNEH8y_cQQiMKmUj7rJoVHMl2d1SI/edit?gid=1845215852#gid=1845215852]、[C673车辆设置功能定义V2.3 拖车模式/后雾灯|https://drive.google.com/file/d/1WwGNLStCOD3MPX00VOzWLkDGQseSHxt9/view]、[C673-G/D587G翻译清单261015 BigsurCarSettings 第481、659、727、756行|https://drive.google.com/file/d/1Hv2_mKeL0JqcSr8AaMXKnSDhjHTcDN3Y/view]。处理：后雾灯打开句改为 Accendi i fari fendinebbia posteriori；拖车模式改为 Modalità traino di emergenza，不要写成 rimorchio。后追尾预警先不改语料，车上 Collisione postesteriore 先按翻译清单核对是不是旧词。语音语料维护处理。
