# 2026-08-31 吴优全部8295模块UE语音覆盖完整执行记录

> 结论：此前记录不完整。本记录区分本轮实时测试、历史参考、规则禁止测试和筛选排除。通话中完全禁止语音操作。

## 统计

- 模块：10个；页面状态记录：48个。
- 本轮实时测试：45个功能、46条Query；通过39个，需申报6个。
- 历史参考：92个功能、208条Query；全部明确标记为2026-08-14历史证据。
- 通话中禁止：14组控件未测试；此前误测5个功能、8条Query已撤销能力结论。
- 其他明确排除：15组。

## 页面记录

| 页面ID | 页面 | 状态 | 证据类型 | 证据 |
| --- | --- | --- | --- | --- |
| drive:3d-desktop-v1.1.15 | 3D桌面&动效 / 当前交互文档 | active | current_page_state | Drive 当前文档全4页，背门、后视镜和车窗为有效直接控件 |
| 543:38855 | 情景模式 V1.9 / 当前版本主模式页 | active | current_page_state | MasterGo当前V1.9页面目录；主模式按各自名称在当前有效页审核 |
| 543:58241 | 情景模式 V1.9 / 小憩模式 | active | current_page_state | V1.9 当前有效页面 |
| 543:49168 | 情景模式 V1.9 / 睡眠空间 | active | current_page_state | V1.9 当前有效页面 |
| 543:54419 | 情景模式 V1.9 / 恒温座舱第3页 | deleted | current_page_state | 当前画布位于红色 v1.9删除区域 |
| 543:53811 | 情景模式 V1.9 / 恒温座舱第4页 | deleted | current_page_state | 当前画布位于红色 v1.9删除区域 |
| 543:48581 | 情景模式 V1.9 / 离车不下电模式 | shelved | current_page_state | 当前图层名称明确标注搁置 |
| 1335:21767 | 场景积木 V1.0 / 当前版本 | active | current_page_state | 场景空间、触发条件、前置条件和执行动作均属复杂配置，按筛选规则不纳入语音申报 |
| blocks:controls-do-not-use | 场景积木 / 控件（不要） | deprecated | current_page_state | 当前页面名称明确标注不要；V0.9、V0.8为历史版本 |
| 1020:64596 | 充放电 / 预约充电 | active | current_page_state | 车辆设置当前有效页面 |
| 202:4388 | 语音形象&GUI V0.9 | active | current_page_state | 当前内容为唤醒、收音、Loading和回复状态展示，无用户设置控件 |
| 818:038239 | 地图导航 850_V0.7 / 当前版本 | active | current_page_state | 草稿、废弃和未下发页面已排除；导航播报模式为当前有效设置 |
| map:draft-deprecated-unreleased | 地图导航 / 草稿、废弃、未下发页面 | deprecated | current_page_state | 当前画布状态明确标注草稿、废弃或未下发 |
| 94:05580 | 蓝牙电话 V0.4 / 1 / 封面 | active | current_page_state | MasterGo MCP 实时读取，页面仅为封面，无用户控件 |
| 94:05457 | 蓝牙电话 V0.4 / 2 / 修改记录 | active | current_page_state | MasterGo MCP 实时读取，记录 V0.4 于2026-05-26新增柔性桌面和桌面卡片隐私协议限制 |
| 94:05269 | 蓝牙电话 V0.4 / 3 / 隐私政策 | active | current_page_state | 同意、暂不同意、查看和撤回属于隐私授权复杂流程，按用户筛选规则不测试 |
| 94:04699 | 蓝牙电话 V0.4 / 4 / 蓝牙连接与数据同步 | active | current_page_state | 连接、授权、同步、CarPlay和HiCar切换依赖当前界面及外部状态，按用户筛选规则不测试 |
| 94:03907 | 蓝牙电话 V0.4 / 5 / 通话记录与通讯录 | active | current_page_state | 可从记录或联系人发起拨号；列表、筛选和字母定位优先可见交互 |
| 94:03153 | 蓝牙电话 V0.4 / 6 / 拨号键盘与更多设置 | active | current_page_state | 拨号属于高频直接操作；T9、数据同步、来电设置和隐私撤回依赖可见界面或复杂流程 |
| 94:02506 | 蓝牙电话 V0.4 / 7 / 通话状态-去电 | active | current_page_state | 当前页为通话中状态；挂断、麦克风静音、键盘、手机车机切换、缩小等全部规则禁止测试 |
| 94:01465 | 蓝牙电话 V0.4 / 8 / 通话状态-来电 | active | current_page_state | 来电接听、拒接和来电铃声静音可在通话建立前测试；接通后的麦克风、设备切换、键盘等禁止测试 |
| 94:00169 | 蓝牙电话 V0.4 / 9 / 通话状态-三方来电 | active | current_page_state | 通话中三方来电的挂断、结束并接听、保留并接听等全部规则禁止测试 |
| 94:9581 | 蓝牙电话 V0.4 / 10 / 通话状态-三方去电 | active | current_page_state | 通话中三方去电和切换通话全部规则禁止测试 |
| 94:9357 | 蓝牙电话 V0.4 / 11 / 语音聊天、Bcall、Ecall | active | current_page_state | 语音聊天、Bcall和Ecall均处于通话中，话筒和通话设备等全部规则禁止测试 |
| 94:9056 | 蓝牙电话 V0.4 / 12 / 电话卡片 | active | current_page_state | 最近通话、同步、蓝牙连接、隐私授权、拖动等依赖卡片可见状态，按用户筛选规则不测试 |
| 473:16202 | 创意画舫 AIGCv1.0 | active | current_page_state | 当前内容为文生图、上传和分享等复杂内容流程，按筛选规则不纳入 |
| art:aigcv0.1-8155 | 创意画舫 AIGCv0.1 8155 | backup | current_page_state | 默认打开页不是8295当前AIGCv1.0版本 |
| 2742:13434 | 车外语音 V0.9 | active | current_page_state | 当前主要为车外喊话入口、播放和音频优先级链路，未确认独立高频设置控件 |
| drive:voice-llm-v1.5 | 语音大模型 v1.5 | active | current_page_state | 工作表F列为空后按Drive回退，已枚举版本族并读取最新v1.5；暂停和关闭依赖当前弹窗可见上下文 |
| llm:deep-thinking-v1.4 | 大模型 / 深度思考 | deleted | current_page_state | v1.5修改记录及画布明确标注V1.4删除，C385-5/C673-7已删除 |
| 543:50288 | 8.情景模式-车内关怀（依赖OMS） | active | historical_page_reference | V1.9 当前有效页面 |
| 543:52488 | 4.情景模式-视听联动 | active | historical_page_reference | V1.9 当前有效页面 |
| 1335:32153 | 1.场景积木-场景空间 | active | historical_page_reference | V1.0 current page |
| 1335:29890 | 2.场景积木-我的场景 | active | historical_page_reference | V1.0 current page |
| 1335:28617 | 3.场景积木-触发条件 | active | historical_page_reference | V1.0 current page |
| 1335:23840 | 4.我的场景-前置条件 | active | historical_page_reference | V1.0 current page |
| 1335:22081 | 5.我的场景-执行动作 | active | historical_page_reference | V1.0 current page |
| 1335:24583 | 6.新手引导 | active | historical_page_reference | V1.0 current page |
| 1335:24996 | 7.场景分享 | active | historical_page_reference | V1.0 current page |
| 1335:27062 | 8.AI生成场景积木 | active | historical_page_reference | V1.0 current page |
| version-v0.9 | V0.9 | deprecated | historical_page_reference | MasterGo page list shows V0.9 below current V1.0 |
| version-v0.8 | V0.8 | deprecated | historical_page_reference | MasterGo page list shows V0.8 below current V1.0 |
| controls-do-not-use | 控件（不要） | deprecated | historical_page_reference | MasterGo page name explicitly marks the page as do not use |
| 854:77410 | 能源明细 V0.1 / 能源明细 | active | historical_page_reference | 当前有效页 |
| 1020:64372 | 车辆设置 V3.5 / 放电 | active | historical_page_reference | 当前有效页 |
| 1020:64168 | 车辆设置 V3.5 / 即时加热 | active | historical_page_reference | 当前有效页 |
| 1020:55689 | 车辆设置 V3.5 / 能量 | active | historical_page_reference | 当前有效页 |
| 345:28175 | D587-G车辆设置 V1.1 / 能量 | active | historical_page_reference | 当前有效页 |

## 本轮实时Query

| 模块 | 页面 | 功能 | Query | operation证据 | 结论 | 是否申报 |
| --- | --- | --- | --- | --- | --- | --- |
| 情景模式 | 情景模式 V1.9 / 小憩模式 | 设置小憩模式结束时间 | 设置小憩模式结束时间为20点30分 | classification=chat；meta_id=3189，仅返回 llm:scenario_block session_id，无可执行的结束时间设置 operation | blocked | 是 |
| 情景模式 | 情景模式 V1.9 / 小憩模式 | 设置小憩模式音效 | 设置小憩模式音效为夜阑听雨 | meta_id=1919，返回 common:func:not:supported / nlu_intent_others | unsupported | 是 |
| 情景模式 | 情景模式 V1.9 / 睡眠空间 | 调节睡眠空间音量 | 调低睡眠空间音量 | meta_id=1186，vehicle:audio:volume:adjust 的 scale_offset=lower，但 channel canonical 为空 | empty_required_slot | 是 |
| 情景模式 | 情景模式 V1.9 / 睡眠空间 | 设置睡眠空间不限时 | 设置睡眠空间为不限时 | meta_id=1146，mode=sleep_space、op=set，但 duration 只有 literal=不限时，没有 canonical | empty_required_slot | 是 |
| 充放电 | 充放电 / 预约充电 | 设置预约充电结束方式 | 设置预约充电结束方式为充满后停止 | meta_id=1919，返回 common:func:not:supported / nlu_intent_others | unsupported | 是 |
| 3D桌面&动效 | 3D桌面&动效 / 当前交互文档 | 打开后备箱 | 打开后备箱 | meta_id=1097，vehicle:ctrl:back_door，op=open | pass | 否 |
| 3D桌面&动效 | 3D桌面&动效 / 当前交互文档 | 关闭后备箱 | 关闭后备箱 | meta_id=1098，vehicle:ctrl:back_door，op=close | pass | 否 |
| 3D桌面&动效 | 3D桌面&动效 / 当前交互文档 | 折叠后视镜 | 折叠后视镜 | meta_id=1095，vehicle:ctrl:rear_mirror:side_mirror，op=fold | pass | 否 |
| 3D桌面&动效 | 3D桌面&动效 / 当前交互文档 | 展开后视镜 | 展开后视镜 | meta_id=1094，vehicle:ctrl:rear_mirror:side_mirror，op=unfold | pass | 否 |
| 3D桌面&动效 | 3D桌面&动效 / 当前交互文档 | 打开主驾车窗 | 打开主驾车窗 | meta_id=1263，vehicle:ctrl:window，op=open，position=main_driver | pass | 否 |
| 3D桌面&动效 | 3D桌面&动效 / 当前交互文档 | 关闭主驾车窗 | 关闭主驾车窗 | meta_id=1264，vehicle:ctrl:window，op=close，position=main_driver | pass | 否 |
| 3D桌面&动效 | 3D桌面&动效 / 当前交互文档 | 调节主驾车窗开度 | 主驾车窗开度调到50% | meta_id=1266，vehicle:ctrl:window，position=main_driver，scale_percent=50% | pass | 否 |
| 3D桌面&动效 | 3D桌面&动效 / 当前交互文档 | 打开全部车窗 | 打开全部车窗 | meta_id=1263，vehicle:ctrl:window，op=open，position=all | pass | 否 |
| 3D桌面&动效 | 3D桌面&动效 / 当前交互文档 | 关闭全部车窗 | 关闭全部车窗 | meta_id=1264，vehicle:ctrl:window，op=close，position=all | pass | 否 |
| 3D桌面&动效 | 3D桌面&动效 / 当前交互文档 | 设置全部车窗为通风状态 | 将全部车窗调到通风状态 | meta_id=1266，vehicle:ctrl:window，mode=overall_ventilation，position=all | pass | 否 |
| 地图 | 地图导航 850_V0.7 / 当前版本 | 设置导航播报模式为详细播报 | 设置导航播报模式为详细播报 | meta_id=1023，navi:setting，target=map_broadcast_mode，value=exhaustive | pass | 否 |
| 地图 | 地图导航 850_V0.7 / 当前版本 | 设置导航播报模式为简洁播报 | 设置导航播报模式为简洁播报 | meta_id=1023，navi:setting，target=map_broadcast_mode，value=simple | pass | 否 |
| 地图 | 地图导航 850_V0.7 / 当前版本 | 设置导航播报模式为静音 | 设置导航播报模式为静音 | meta_id=1023，navi:setting，target=map_broadcast_mode，value=mute | pass | 否 |
| 蓝牙电话 | 蓝牙电话 V0.4 / 6 / 拨号键盘与更多设置 | 拨打电话号码 | 拨打10086 | meta_id=1061，phone:call，with_number=10086 | pass | 否 |
| 蓝牙电话 | 蓝牙电话 V0.4 / 8 / 通话状态-来电 | 接听电话 | 接听电话 | meta_id=1065，phone:call:ctrl，op=answer_call | pass | 否 |
| 蓝牙电话 | 蓝牙电话 V0.4 / 8 / 通话状态-来电 | 拒接电话 | 拒接电话 | meta_id=1065，phone:call:ctrl，op=reject_call | pass | 否 |
| 蓝牙电话 | 蓝牙电话 V0.4 / 8 / 通话状态-来电 | 打开来电铃声静音 | 打开铃声静音 | meta_id=1188，vehicle:audio:volume:mute，op=open，channel=ringtone | pass | 否 |
| 蓝牙电话 | 蓝牙电话 V0.4 / 8 / 通话状态-来电 | 关闭来电铃声静音 | 关闭铃声静音<br>关闭来电铃声静音 | 两个Query均返回 meta_id=1919、common:func:not:supported | unsupported | 是 |
| 情景模式 | 情景模式 V1.9 / 当前版本主模式页 | 打开露营模式 | 打开露营模式 | classification=task；meta_id=1127；vehicle:scenario:ctrl；mode=camp；op=open | pass | 否 |
| 情景模式 | 情景模式 V1.9 / 当前版本主模式页 | 关闭露营模式 | 关闭露营模式 | classification=task；meta_id=1126；vehicle:scenario:ctrl；mode=camp；op=close | pass | 否 |
| 情景模式 | 情景模式 V1.9 / 当前版本主模式页 | 打开舒享模式 | 打开舒享模式 | classification=task；meta_id=1127；vehicle:scenario:ctrl；mode=comfort；op=open | pass | 否 |
| 情景模式 | 情景模式 V1.9 / 当前版本主模式页 | 关闭舒享模式 | 关闭舒享模式 | classification=task；meta_id=1126；vehicle:scenario:ctrl；mode=comfort；op=close | pass | 否 |
| 情景模式 | 情景模式 V1.9 / 当前版本主模式页 | 打开小憩模式 | 打开小憩模式 | classification=task；meta_id=1127；vehicle:scenario:ctrl；mode=rest；op=open | pass | 否 |
| 情景模式 | 情景模式 V1.9 / 当前版本主模式页 | 关闭小憩模式 | 关闭小憩模式 | classification=task；meta_id=1126；vehicle:scenario:ctrl；mode=rest；op=close | pass | 否 |
| 情景模式 | 情景模式 V1.9 / 当前版本主模式页 | 打开睡眠空间 | 打开睡眠空间 | classification=task；meta_id=1127；vehicle:scenario:ctrl；mode=sleep_space；op=open | pass | 否 |
| 情景模式 | 情景模式 V1.9 / 当前版本主模式页 | 关闭睡眠空间 | 关闭睡眠空间 | classification=task；meta_id=1126；vehicle:scenario:ctrl；mode=sleep_space；op=close | pass | 否 |
| 情景模式 | 情景模式 V1.9 / 当前版本主模式页 | 打开隐私模式 | 打开隐私模式 | classification=task；meta_id=1127；vehicle:scenario:ctrl；mode=privacy；op=open | pass | 否 |
| 情景模式 | 情景模式 V1.9 / 当前版本主模式页 | 关闭隐私模式 | 关闭隐私模式 | classification=task；meta_id=1126；vehicle:scenario:ctrl；mode=privacy；op=close | pass | 否 |
| 情景模式 | 情景模式 V1.9 / 当前版本主模式页 | 打开吸烟模式 | 打开吸烟模式 | classification=task；meta_id=1127；vehicle:scenario:ctrl；mode=smoking；op=open | pass | 否 |
| 情景模式 | 情景模式 V1.9 / 当前版本主模式页 | 关闭吸烟模式 | 关闭吸烟模式 | classification=task；meta_id=1126；vehicle:scenario:ctrl；mode=smoking；op=close | pass | 否 |
| 情景模式 | 情景模式 V1.9 / 当前版本主模式页 | 打开车内关怀 | 打开车内关怀 | classification=task；meta_id=1127；vehicle:scenario:ctrl；mode=rear_care_mode；op=open | pass | 否 |
| 情景模式 | 情景模式 V1.9 / 当前版本主模式页 | 关闭车内关怀 | 关闭车内关怀 | classification=task；meta_id=1126；vehicle:scenario:ctrl；mode=rear_care_mode；op=close | pass | 否 |
| 情景模式 | 情景模式 V1.9 / 当前版本主模式页 | 打开冬季模式 | 打开冬季模式 | classification=task；meta_id=1127；vehicle:scenario:ctrl；mode=winter；op=open | pass | 否 |
| 情景模式 | 情景模式 V1.9 / 当前版本主模式页 | 关闭冬季模式 | 关闭冬季模式 | classification=task；meta_id=1126；vehicle:scenario:ctrl；mode=winter；op=close | pass | 否 |
| 情景模式 | 情景模式 V1.9 / 当前版本主模式页 | 打开洗车模式 | 打开洗车模式 | classification=task；meta_id=1127；vehicle:scenario:ctrl；mode=car_wash_mode；op=open | pass | 否 |
| 情景模式 | 情景模式 V1.9 / 当前版本主模式页 | 关闭洗车模式 | 关闭洗车模式 | classification=task；meta_id=1126；vehicle:scenario:ctrl；mode=car_wash_mode；op=close | pass | 否 |
| 情景模式 | 情景模式 V1.9 / 当前版本主模式页 | 打开宠物模式 | 打开宠物模式 | classification=task；meta_id=1127；vehicle:scenario:ctrl；mode=pet；op=open | pass | 否 |
| 情景模式 | 情景模式 V1.9 / 当前版本主模式页 | 关闭宠物模式 | 关闭宠物模式 | classification=task；meta_id=1126；vehicle:scenario:ctrl；mode=pet；op=close | pass | 否 |
| 情景模式 | 情景模式 V1.9 / 当前版本主模式页 | 打开音乐灯光秀 | 打开音乐灯光秀 | classification=task；meta_id=1127；vehicle:scenario:ctrl；mode=music_light_show；op=open | pass | 否 |
| 情景模式 | 情景模式 V1.9 / 当前版本主模式页 | 关闭音乐灯光秀 | 关闭音乐灯光秀 | classification=task；meta_id=1126；vehicle:scenario:ctrl；mode=music_light_show；op=close | pass | 否 |

## 通话中禁止测试

| 页面 | 控件 | Query | 结论 | 原因 |
| --- | --- | --- | --- | --- |
| 蓝牙电话 V0.4 / 7 / 通话状态-去电 | 缩小或展开通话浮窗 | 未执行 | do_not_test_or_report | 通话中完全禁止语音操作 |
| 蓝牙电话 V0.4 / 7 / 通话状态-去电 | 打开通话键盘 | 未执行 | do_not_test_or_report | 通话中完全禁止语音操作 |
| 蓝牙电话 V0.4 / 7 / 通话状态-去电 | 关闭通话键盘 | 未执行 | do_not_test_or_report | 通话中完全禁止语音操作 |
| 蓝牙电话 V0.4 / 7 / 通话状态-去电 | 结束通话 | 未执行 | do_not_test_or_report | 通话中完全禁止语音操作 |
| 蓝牙电话 V0.4 / 7 / 通话状态-去电 | 打开通话麦克风静音 | 未执行 | do_not_test_or_report | 通话中完全禁止语音操作 |
| 蓝牙电话 V0.4 / 7 / 通话状态-去电 | 关闭通话麦克风静音 | 未执行 | do_not_test_or_report | 通话中完全禁止语音操作 |
| 蓝牙电话 V0.4 / 7 / 通话状态-去电 | 设置通话设备为手机 | 未执行 | do_not_test_or_report | 通话中完全禁止语音操作 |
| 蓝牙电话 V0.4 / 7 / 通话状态-去电 | 设置通话设备为车机 | 未执行 | do_not_test_or_report | 通话中完全禁止语音操作 |
| 蓝牙电话 V0.4 / 8 / 通话状态-来电 | 接通后的通话键盘、话筒、设备切换及挂断 | 未执行 | do_not_test_or_report | 通话中完全禁止语音操作 |
| 蓝牙电话 V0.4 / 9 / 通话状态-三方来电 | 三方来电挂断 | 未执行 | do_not_test_or_report | 通话中完全禁止语音操作 |
| 蓝牙电话 V0.4 / 9 / 通话状态-三方来电 | 三方来电结束当前通话并接听 | 未执行 | do_not_test_or_report | 通话中完全禁止语音操作 |
| 蓝牙电话 V0.4 / 9 / 通话状态-三方来电 | 三方来电保留当前通话并接听 | 未执行 | do_not_test_or_report | 通话中完全禁止语音操作 |
| 蓝牙电话 V0.4 / 10 / 通话状态-三方去电 | 三方通话去电与切换通话 | 未执行 | do_not_test_or_report | 通话中完全禁止语音操作 |
| 蓝牙电话 V0.4 / 11 / 语音聊天、Bcall、Ecall | 语音聊天、Bcall、Ecall中的话筒与设备切换 | 未执行 | do_not_test_or_report | 通话中完全禁止语音操作 |

## 通话中历史误测

| 页面 | 功能 | 误测Query | 处理 |
| --- | --- | --- | --- |
| 蓝牙电话 V0.4 / 7 / 通话状态-去电 | 结束通话 | 挂断电话<br>结束通话 | withdrawn_no_capability_conclusion |
| 蓝牙电话 V0.4 / 7 / 通话状态-去电 | 打开通话麦克风静音 | 打开麦克风静音 | withdrawn_no_capability_conclusion |
| 蓝牙电话 V0.4 / 7 / 通话状态-去电 | 关闭通话麦克风静音 | 关闭麦克风静音 | withdrawn_no_capability_conclusion |
| 蓝牙电话 V0.4 / 7 / 通话状态-去电 | 设置通话设备为手机 | 切换到手机接听<br>设置通话设备为手机 | withdrawn_no_capability_conclusion |
| 蓝牙电话 V0.4 / 7 / 通话状态-去电 | 设置通话设备为车机 | 切换到车机接听<br>设置通话设备为车机 | withdrawn_no_capability_conclusion |

## 其他未执行项

| 模块 | 页面 | 功能 | Query | 排除原因 |
| --- | --- | --- | --- | --- |
| 3D桌面&动效 | 3D桌面&动效 / 当前交互文档 | 设置3D车身颜色 | 未执行 | 低频且依赖可见界面 |
| 3D桌面&动效 | 3D桌面&动效 / 当前交互文档 | 设置3D轮毂样式 | 未执行 | 低频且依赖可见界面 |
| 3D桌面&动效 | 3D桌面&动效 / 当前交互文档 | 胎压和车灯逻辑 | 未执行 | 状态展示或联动逻辑，不是独立用户设置控件 |
| 语音形象&GUI | 语音形象&GUI V0.9 | 唤醒、收音、Loading、回复和形象动效 | 未执行 | 系统状态展示，无用户可操作设置控件 |
| 地图 | 地图导航 850_V0.7 / 当前版本 | 设置手动限速或道路限速 | 未执行 | 依赖当前页面与行车条件，复杂且可见交互优先 |
| 创意画舫 | 创意画舫 AIGCv1.0 | 进入或退出创意画舫 | 未执行 | 页面导航动作，不属于当前12类高频直接执行 |
| 创意画舫 | 创意画舫 AIGCv1.0 | 文生图生成、重试、保存或分享 | 未执行 | 复杂内容流程，依赖当前页面和生成状态 |
| 创意画舫 | 创意画舫 AIGCv1.0 | 车机分享手机图片 | 未执行 | 跨设备复杂内容流程 |
| 车外语音 | 车外语音 V0.9 | 进入车外喊话 | 未执行 | 页面入口，依赖可见交互 |
| 车外语音 | 车外语音 V0.9 | 播放或试听车外喊话 | 未执行 | 播放链路受导航、音乐、通话优先级影响，不是独立简单设置 |
| 车外语音 | 车外语音 V0.9 | 取消或打断车外喊话 | 未执行 | 依赖当前播放状态，可见交互优先 |
| 大模型 | 语音大模型 v1.5 | 暂停大模型回复 | 未执行 | 依赖当前弹窗和生成状态，不看界面无法确定目标 |
| 大模型 | 语音大模型 v1.5 | 关闭大模型回复 | 未执行 | 依赖当前弹窗和生成状态，不看界面无法确定目标 |
| 大模型 | 大模型 / 深度思考 | 打开深度思考 | 未执行 | V1.4删除，当前UE无效 |
| 大模型 | 大模型 / 深度思考 | 关闭深度思考 | 未执行 | V1.4删除，当前UE无效 |

## 历史Query逐项记录

> 以下均为2026-08-14历史证据，仅用于说明当时查过哪些功能、页面和Query，不等同本轮实时测试。

| 模块 | 页面 | 功能 | 历史Query | 历史operation证据 | 历史结论 | 当前处理 |
| --- | --- | --- | --- | --- | --- | --- |
| 情景模式 | 10.情景模式-睡眠空间 | 睡眠空间座椅设置入口 | 打开睡眠空间座椅设置 | 返回 app:ctrl，但没有座椅 target canonical | empty_required_slot | excluded_by_user_filter：虽有历史失败证据，但不满足当前简单、高频、离屏可记忆和12类筛选规则 |
| 情景模式 | 小憩模式 | 小憩模式座椅位置选择 | 小憩模式设置为主驾 | 返回 common:func:not:supported | unsupported | excluded_by_user_filter：虽有历史失败证据，但不满足当前简单、高频、离屏可记忆和12类筛选规则 |
| 情景模式 | 小憩模式 | 小憩模式结束时间设置 | 小憩模式结束时间设置为20点30分 | 误生成充电预约操作 | misrouted | superseded_by_current_live_test：本轮已用当前Query重新测试，见 nap-end-time |
| 情景模式 | 小憩模式 | 小憩模式不限时开关 | 打开小憩模式不限时 | 返回 llm:scenario_block | blocked | excluded_by_user_filter：虽有历史失败证据，但不满足当前简单、高频、离屏可记忆和12类筛选规则 |
| 情景模式 | 小憩模式 | 小憩模式音效选择 | 小憩模式音效切换为夜阑听雨 | 未形成可执行的小憩音效选择操作 | unsupported | superseded_by_current_live_test：本轮已用当前Query重新测试，见 nap-sound |
| 情景模式 | 小憩模式 | 小憩模式熄屏 | 小憩模式熄屏 | 熄屏同时被解析为关闭小憩模式 | misrouted | excluded_by_user_filter：虽有历史失败证据，但不满足当前简单、高频、离屏可记忆和12类筛选规则 |
| 情景模式 | 小憩模式 | 小憩模式音乐切换 | 小憩模式切换音乐 | 未形成可执行的小憩音乐切换操作 | unsupported | excluded_by_user_filter：虽有历史失败证据，但不满足当前简单、高频、离屏可记忆和12类筛选规则 |
| 情景模式 | 10.情景模式-睡眠空间 | 睡眠空间音量调节 | 睡眠空间音量调高 | vehicle:audio:volume:adjust 的 channel canonical 为空 | empty_required_slot | superseded_by_current_live_test：本轮已用当前Query重新测试，见 sleep-volume-lower |
| 情景模式 | 10.情景模式-睡眠空间 | 睡眠空间跳过人声 | 睡眠空间跳过人声 | vehicle:scenario:theme_adjust 的 operation canonical 为空 | empty_required_slot | excluded_by_user_filter：虽有历史失败证据，但不满足当前简单、高频、离屏可记忆和12类筛选规则 |
| 情景模式 | 10.情景模式-睡眠空间 | 打开睡眠问诊 | 打开睡眠问诊 | classification=chat，仅返回已打开的文本，无 operation | chat_only | excluded_by_user_filter：虽有历史失败证据，但不满足当前简单、高频、离屏可记忆和12类筛选规则 |
| 情景模式 | 10.情景模式-睡眠空间 | 睡眠空间不限时设置 | 睡眠空间设置为不限时 | duration 仅有 literal=不限时，canonical 为空 | empty_required_slot | superseded_by_current_live_test：本轮已用当前Query重新测试，见 sleep-unlimited |
| 情景模式 | 8.情景模式-车内关怀（依赖OMS） | 车内关怀窗口模式切换 | 车内关怀切换为小窗 | 小窗指令返回 common:func:not:supported；全屏可执行 | unsupported | excluded_by_user_filter：虽有历史失败证据，但不满足当前简单、高频、离屏可记忆和12类筛选规则 |
| 情景模式 | 4.情景模式-视听联动 | 下载音乐灯光秀 | 下载音乐灯光秀 | 误生成打开音乐灯光秀操作，未执行下载/打开应用商城 | misrouted | excluded_by_user_filter：虽有历史失败证据，但不满足当前简单、高频、离屏可记忆和12类筛选规则 |
| 情景模式 | 10.情景模式-睡眠空间 | 睡眠空间熄屏 | 睡眠空间熄屏 | 返回 vehicle:display:ctrl:screen_off，target_screen=default_screen | pass | not_add_historical_pass：历史Alchemy操作匹配；本轮未重复测试，不作为本轮实时证据 |
| 情景模式 | 10.情景模式-睡眠空间 | 睡眠空间空调设置入口 | 打开睡眠空间空调设置 | 返回 app:ctrl open，target=air_conditioner | pass | not_add_historical_pass：历史Alchemy操作匹配；本轮未重复测试，不作为本轮实时证据 |
| 场景积木 | 1.场景积木-场景空间 | 场景空间与我的场景页签切换 | 打开场景积木的场景空间<br>打开场景积木的我的场景 | app:ctrl lacked a target or custom scenario control was returned instead of the requested tab | misrouted | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 1.场景积木-场景空间 | 推荐场景详情打开 | 打开第一个推荐场景详情 | common:func:not:supported | unsupported | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 1.场景积木-场景空间 | 推荐场景添加到我的场景 | 把第一个推荐场景添加到我的场景 | common:func:not:supported | unsupported | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 2.场景积木-我的场景 | 创建自定义场景 | 创建一个场景积木 | llm:scenario_block returned instead of creating a scene | blocked | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 2.场景积木-我的场景 | 编辑自定义场景 | 编辑第一个场景积木 | misrouted to media:music:play and llm:draw:image | misrouted | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 2.场景积木-我的场景 | 自定义场景重命名 | 把第一个场景积木重命名为下班回家 | misrouted to navigation favorite home | misrouted | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 2.场景积木-我的场景 | 自定义场景删除与批量删除 | 删除第一个场景积木 | common:func:not:supported | unsupported | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 2.场景积木-我的场景 | 自定义场景排序 | 把第一个场景积木排到第二个 | common:func:not:supported | unsupported | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 2.场景积木-我的场景 | 执行场景与跳过前置条件执行 | 执行第一个场景积木<br>跳过前置条件执行第一个场景积木 | both queries returned common:func:not:supported | unsupported | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 2.场景积木-我的场景 | 场景自动执行开关 | 打开第一个场景积木自动执行<br>关闭第一个场景积木自动执行 | opened or closed the sceneblock app instead of changing the selected scene auto-execute switch | misrouted | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 1.场景积木-场景空间 | 场景试用与暂停 | 试用第一个场景积木<br>暂停试用场景积木 | opened or closed the app instead of starting or pausing scene trial | misrouted | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 6.新手引导 | 新手引导进入、翻页、跳过、完成与关闭 | 打开场景积木新手引导<br>场景积木新手引导下一步<br>场景积木新手引导上一步<br>跳过场景积木新手引导<br>开始体验场景积木<br>关闭场景积木新手引导 | guide target canonical was empty; step actions were unsupported or misrouted to navigation | misrouted | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 7.场景分享 | 场景分享、分享码生成与复制 | 分享第一个场景积木<br>生成第一个场景积木的分享码<br>复制第一个场景积木的分享码 | chat text claimed sharing, generation, or copy success but no executable operation was returned | chat_only | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 7.场景分享 | 输入分享码添加场景 | 输入分享码123456789添加场景积木 | common:func:not:supported | unsupported | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 8.AI生成场景积木 | AI生成场景积木 | 用AI生成一个下班回家场景积木 | chat text described a generated scene but no executable scene-generation operation was returned | chat_only | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 8.AI生成场景积木 | AI生成暂停与卡片关闭 | 暂停AI生成场景积木<br>关闭AI生成场景积木卡片 | both queries returned common:func:not:supported | unsupported | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 8.AI生成场景积木 | 保存AI生成场景 | 保存AI生成的场景积木 | common:func:not:supported | unsupported | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 8.AI生成场景积木 | 编辑AI生成场景 | 去编辑AI生成的场景积木 | common:func:not:supported | unsupported | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 3.场景积木-触发条件 | 触发条件-时间 | 把场景积木的触发条件设置为每天8点 | common:func:not:supported | unsupported | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 3.场景积木-触发条件 | 触发条件-驾驶与能量 | 把场景积木的触发条件设置为P挡<br>把场景积木的触发条件设置为车速大于30公里每小时<br>把场景积木的触发条件设置为舒适驾驶模式<br>把场景积木的触发条件设置为强制纯电<br>把场景积木的触发条件设置为电池电量低于20% | queries were unsupported or immediately changed driving/energy functions; battery query navigated to a charging station | misrouted | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 3.场景积木-触发条件 | 触发条件-车门车窗 | 把场景积木的触发条件设置为主驾车门打开<br>把场景积木的触发条件设置为左侧儿童锁开启<br>把场景积木的触发条件设置为主驾车窗降下<br>把场景积木的触发条件设置为遮阳帘打开<br>把场景积木的触发条件设置为全车门锁上锁 | door, child-lock, window, and sunshade actions executed immediately; door-lock condition was unsupported | misrouted | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 3.场景积木-触发条件 | 触发条件-乘员 | 把场景积木的触发条件设置为主驾有人<br>把场景积木的触发条件设置为主驾安全带系上 | both queries returned common:func:not:supported | unsupported | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 3.场景积木-触发条件 | 触发条件-环境 | 把场景积木的触发条件设置为空气质量重度污染<br>把场景积木的触发条件设置为车内温度高于30度<br>把场景积木的触发条件设置为环境光昏暗<br>把场景积木的触发条件设置为雨天 | air-quality query became a weather query, temperature changed AC immediately, and light/weather conditions were unsupported | misrouted | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 3.场景积木-触发条件 | 触发条件-导航 | 把场景积木的触发条件设置为预计到达时间早于20点<br>场景积木触发条件设为距离目的地小于3公里 | returned journey query/charging booking or immediate navigation search instead of storing a trigger | misrouted | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 3.场景积木-触发条件 | 触发条件-充电状态 | 把场景积木的触发条件设置为开始充电 | common:func:not:supported | unsupported | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 4.我的场景-前置条件 | 前置条件-时间与位置 | 把场景积木的前置条件设置为每天8点到9点<br>把场景积木的前置条件设置为距离家2公里以内 | both queries returned common:func:not:supported | unsupported | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 4.我的场景-前置条件 | 前置条件-车辆状态 | 把场景积木的前置条件设置为未充电<br>把场景积木的前置条件设置为四门车窗全关 | charging state was unsupported and window state immediately closed all windows | misrouted | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 4.我的场景-前置条件 | 前置条件-导航与媒体状态 | 把场景积木的前置条件设置为导航中<br>把场景积木的前置条件设置为媒体播放中 | misrouted to navigation favorite control or media playback | misrouted | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 4.我的场景-前置条件 | 前置条件-连接状态 | 把场景积木的前置条件设置为蓝牙已连接<br>把场景积木的前置条件设置为WLAN已连接<br>把场景积木的前置条件设置为无线充电中 | all connection-state queries returned common:func:not:supported | unsupported | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 5.我的场景-执行动作 | 执行动作-车身 | 把场景积木的执行动作设置为打开门把手<br>把场景积木的执行动作设置为全车门锁上锁<br>把场景积木的执行动作设置为开启左侧儿童锁<br>把场景积木的执行动作设置为四门车窗开度50%<br>把场景积木的执行动作设置为主驾车窗开度30%<br>把场景积木的执行动作设置为后视镜折叠<br>把场景积木的执行动作设置为前雨刮低速<br>把场景积木的执行动作设置为后雨刮开启<br>把场景积木的执行动作设置为升起电动尾翼 | underlying body controls executed immediately or were unsupported; no scenario action was stored | misrouted | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 5.我的场景-执行动作 | 执行动作-座椅 | 把场景积木的执行动作设置为主驾座椅位置向前<br>把场景积木的执行动作设置为副驾座椅位置向后<br>把场景积木的执行动作设置为开启主驾座椅加热<br>把场景积木的执行动作设置为开启主驾座椅通风<br>把场景积木的执行动作设置为主驾按摩高强度波浪模式 | seat operations executed immediately; no scenario action was stored | misrouted | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 5.我的场景-执行动作 | 执行动作-灯光 | 把场景积木的执行动作设置为打开左转向灯<br>把场景积木的执行动作设置为打开大灯<br>把场景积木的执行动作设置为打开后雾灯 | returned immediate light control or light clarification instead of storing a scenario action | misrouted | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 5.我的场景-执行动作 | 执行动作-空调 | 把场景积木的执行动作设置为打开空调<br>把场景积木的执行动作设置为主驾空调25度<br>把场景积木的执行动作设置为空调内循环<br>把场景积木的执行动作设置为打开空气净化<br>把场景积木的执行动作设置为空调风量5级<br>把场景积木的执行动作设置为空调吹脸<br>把场景积木的执行动作设置为打开自动空调<br>把场景积木的执行动作设置为空调制冷 | all climate operations controlled the current vehicle immediately instead of storing a scenario action | misrouted | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 5.我的场景-执行动作 | 执行动作-媒体与应用 | 把场景积木的执行动作设置为播放蓝牙音乐<br>把场景积木的执行动作设置为播放网易云音乐今日推荐<br>把场景积木的执行动作设置为播放QQ音乐我的收藏<br>把场景积木的执行动作设置为播放周杰伦的晴天<br>把场景积木的执行动作设置为媒体暂停 | media operations played or paused content immediately instead of storing a scenario action | misrouted | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 5.我的场景-执行动作 | 执行动作-导航 | 把场景积木的执行动作设置为导航回家 | immediate navigation to home was returned instead of storing a scenario action | misrouted | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 5.我的场景-执行动作 | 执行动作-驾驶与能量 | 把场景积木的执行动作设置为舒适驾驶模式<br>把场景积木的执行动作设置为强制纯电 | driving or energy mode changed immediately instead of storing a scenario action | misrouted | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 5.我的场景-执行动作 | 执行动作-连接与车辆设置 | 把场景积木的执行动作设置为打开低速提示音<br>把场景积木的执行动作设置为打开蓝牙<br>把场景积木的执行动作设置为打开无线热点<br>把场景积木的执行动作设置为打开无线充电<br>把场景积木的执行动作设置为打开WLAN<br>把场景积木的执行动作设置为打开离车记录<br>把场景积木的执行动作设置为打开智能钥匙感应闭锁<br>把场景积木的执行动作设置为打开蓝牙钥匙感应闭锁<br>把场景积木的执行动作设置为打开智能钥匙感应解锁<br>把场景积木的执行动作设置为打开蓝牙钥匙感应解锁<br>把场景积木的执行动作设置为打开闭锁音<br>把场景积木的执行动作设置为打开后排安全带未系提示 | settings were controlled immediately or unsupported; no scenario action was stored | misrouted | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 5.我的场景-执行动作 | 执行动作-语音播报与延时 | 把场景积木的执行动作设置为语音播报欢迎回家<br>把场景积木的执行动作设置为延时30秒 | both queries returned common:func:not:supported | unsupported | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 5.我的场景-执行动作 | 执行动作-屏幕与HUD | 把场景积木的执行动作设置为中控旋转屏10度<br>把场景积木的执行动作设置为副驾屏展开<br>把场景积木的执行动作设置为中控屏旋转<br>把场景积木的执行动作设置为中控屏熄屏<br>把场景积木的执行动作设置为中控屏亮度60%<br>把场景积木的执行动作设置为打开自动亮度<br>把场景积木的执行动作设置为中控屏深色背景模式<br>把场景积木的执行动作设置为打开HUD<br>把场景积木的执行动作设置为HUD标准模式 | screen/HUD controls executed immediately, were unsupported, or had empty canonical; no scenario action was stored | misrouted | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 5.我的场景-执行动作 | 执行动作-音量 | 把场景积木的执行动作设置为多媒体音量16<br>把场景积木的执行动作设置为通话音量16<br>把场景积木的执行动作设置为导航播报音量16<br>把场景积木的执行动作设置为语音播报音量16 | volume operations ran immediately and some channels were empty or polluted by sceneblock | misrouted | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 5.我的场景-执行动作 | 执行动作-冷暖箱 | 把场景积木的执行动作设置为冷暖箱制冷5度 | cold-box temperature changed immediately instead of storing a scenario action | misrouted | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 场景积木 | 1.场景积木-场景空间 | 打开场景积木 | 打开场景积木 | app:ctrl open target=sceneblock | pass | excluded_by_user_filter：复杂配置或内容流程；能走可见交互优先可见，不纳入当前语音申报 |
| 充放电 | 车辆设置 V3.5 / 充电桌面 | 立即充电 | 立即充电 | BIGSUR returned navi:dest:search for a charging station instead of starting vehicle charging | misrouted | excluded_by_user_filter：虽有历史失败证据，但不满足当前简单、高频、离屏可记忆和12类筛选规则 |
| 充放电 | 车辆设置 V3.5 / 充电桌面 | 结束充电 | 结束充电 | BIGSUR returned energy:charging:ctrl close charge | pass | not_add_historical_pass：历史Alchemy操作匹配；本轮未重复测试，不作为本轮实时证据 |
| 充放电 | 车辆设置 V3.5 / 充电桌面 | 预约充电开关 | 打开预约充电<br>关闭预约充电 | BIGSUR returned charge_book open and close operations | pass | not_add_historical_pass：历史Alchemy操作匹配；本轮未重复测试，不作为本轮实时证据 |
| 充放电 | 车辆设置 V3.5 / 充电桌面 | 预约充电开始与结束时间 | 把预约充电开始时间设置为晚上10点<br>把预约充电结束时间设置为早上6点 | BIGSUR returned booking start and end time operations with canonical values | pass | not_add_historical_pass：历史Alchemy操作匹配；本轮未重复测试，不作为本轮实时证据 |
| 充放电 | 车辆设置 V3.5 / 充电桌面 | 预约充电充满后停止 | 预约充电设置为充满后停止<br>预约充电结束方式设置为充满后停止 | BIGSUR closed charge_book instead of setting the completion mode | misrouted | superseded_by_current_live_test：本轮已用当前Query重新测试，见 charge-book-full-stop |
| 充放电 | 车辆设置 V3.5 / 充电桌面 | 预约充电设置确认 | 确认预约充电设置 | BIGSUR returned navi:dest:via:add with empty params | misrouted | excluded_by_user_filter：虽有历史失败证据，但不满足当前简单、高频、离屏可记忆和12类筛选规则 |
| 充放电 | 车辆设置 V3.5 / 充电桌面 | 充电电流限值 | 把充电电流限值设置为8A<br>把充电电流限值设置为10A<br>把充电电流限值设置为16A<br>把充电电流限值设置为32A | BIGSUR returned charge_current with 8, 10, 16 and 32 amp values | pass | not_add_historical_pass：历史Alchemy操作匹配；本轮未重复测试，不作为本轮实时证据 |
| 充放电 | 车辆设置 V3.5 / 放电 | 对外放电开关 | 打开对外放电<br>关闭对外放电 | BIGSUR returned open/close for canonical discharge_outward | pass | not_add_historical_pass：历史Alchemy操作匹配；本轮未重复测试，不作为本轮实时证据 |
| 充放电 | 车辆设置 V3.5 / 即时加热 | 脉冲加热 | 开启脉冲加热 | BIGSUR returned vehicle:energy:battery:ctrl open pulse_heat | pass | not_add_historical_pass：历史Alchemy操作匹配；本轮未重复测试，不作为本轮实时证据 |
| 充放电 | 车辆设置 V3.5 / 能量 | 慢充口自动解锁 | 打开慢充口自动解锁<br>关闭慢充口自动解锁 | BIGSUR returned charge_gun_auto_unlock open and close | pass | not_add_historical_pass：历史Alchemy操作匹配；本轮未重复测试，不作为本轮实时证据 |
| 充放电 | 车辆设置 V3.5 / 能量 | 能耗计量方式 | 能耗计量方式设置为CLTC工况<br>能耗计量方式设置为WLTC工况 | BIGSUR returned cltc and wltc consumption_method modes | pass | not_add_historical_pass：历史Alchemy操作匹配；本轮未重复测试，不作为本轮实时证据 |
| 充放电 | 车辆设置 V3.5 / 能量 | 能量显示方式 | 能量显示设置为剩余里程<br>能量显示设置为剩余电量 | BIGSUR returned mileage and energy display_method modes | pass | not_add_historical_pass：历史Alchemy操作匹配；本轮未重复测试，不作为本轮实时证据 |
| 充放电 | 车辆设置 V3.5 / 能量 | 直流充电VIN授权 | 打开直流充电VIN授权<br>关闭直流充电VIN授权 | BIGSUR returned energy:charging:ctrl but setting_item canonical was empty for both directions | empty_required_slot | excluded_by_user_filter：虽有历史失败证据，但不满足当前简单、高频、离屏可记忆和12类筛选规则 |
| 充放电 | 车辆设置 V3.5 / 能量 | 超级省电开关 | 打开超级省电<br>关闭超级省电<br>确认开启超级省电 | BIGSUR returned super_power_saving open/close operations | pass | not_add_historical_pass：历史Alchemy操作匹配；本轮未重复测试，不作为本轮实时证据 |
| 充放电 | 车辆设置 V3.5 / 能量 | 充电桩连接开关 | 打开充电桩连接<br>关闭充电桩连接 | BIGSUR returned charge_pile_connection open and close | pass | not_add_historical_pass：历史Alchemy操作匹配；本轮未重复测试，不作为本轮实时证据 |
| 充放电 | 车辆设置 V3.5 / 能量 | 充电桩设备连接、断开、忘记、重试与取消配对 | 断开已连接的充电桩<br>忘记已连接的充电桩<br>连接第一个充电桩<br>重试连接充电桩<br>取消充电桩配对 | BIGSUR either returned unsupported or only toggled the global charge_pile_connection switch without the selected device operation | misrouted | excluded_by_user_filter：虽有历史失败证据，但不满足当前简单、高频、离屏可记忆和12类筛选规则 |
| 充放电 | 车辆设置 V3.5 / 能量 | 燃油补电开关 | 打开燃油补电<br>关闭燃油补电<br>确认开启燃油补电 | BIGSUR returned charge_with_fuel open and close | pass | not_add_historical_pass：历史Alchemy操作匹配；本轮未重复测试，不作为本轮实时证据 |
| 充放电 | 车辆设置 V3.5 / 能量 | 燃油补电档位 | 燃油补电档位设置为低<br>燃油补电档位设置为中<br>燃油补电档位设置为高 | BIGSUR returned low, medium and high fuel charging power values | pass | not_add_historical_pass：历史Alchemy操作匹配；本轮未重复测试，不作为本轮实时证据 |
| 充放电 | 车辆设置 V3.5 / 能量 | 燃油补电SOC上限 | 燃油补电SOC上限设置为60% | BIGSUR returned common:func:not:supported | unsupported | excluded_by_user_filter：虽有历史失败证据，但不满足当前简单、高频、离屏可记忆和12类筛选规则 |
| 充放电 | 车辆设置 V3.5 / 能量 | 国内能量管理模式 | 能量管理设置为市区模式<br>能量管理设置为高速模式<br>能量管理设置为山地模式 | BIGSUR returned urban, highway and mountain management modes | pass | not_add_historical_pass：历史Alchemy操作匹配；本轮未重复测试，不作为本轮实时证据 |
| 充放电 | 车辆设置 V3.5 / 能量 | 强制纯电开关 | 打开强制纯电<br>关闭强制纯电<br>确认开启强制纯电 | BIGSUR returned forced_pure_electricity open and close | pass | not_add_historical_pass：历史Alchemy操作匹配；本轮未重复测试，不作为本轮实时证据 |
| 充放电 | 车辆设置 V3.5 / 能量 | 电量保持目标 | 电量保持目标设置为60% | BIGSUR returned soc_target scale_percent 60% | pass | not_add_historical_pass：历史Alchemy操作匹配；本轮未重复测试，不作为本轮实时证据 |
| 充放电 | 车辆设置 V3.5 / 能量 | 能量管理记忆开关 | 打开能量管理记忆<br>关闭能量管理记忆 | BIGSUR returned energy_management_memory open and close | pass | not_add_historical_pass：历史Alchemy操作匹配；本轮未重复测试，不作为本轮实时证据 |
| 充放电 | 车辆设置 V3.5 / 能量 | 电池保温开关 | 打开电池保温<br>关闭电池保温 | BIGSUR returned battery_insulation open and close | pass | not_add_historical_pass：历史Alchemy操作匹配；本轮未重复测试，不作为本轮实时证据 |
| 充放电 | 能源明细 V0.1 / 能源明细 | 能源明细入口 | 打开能源明细 | BIGSUR returned common:func:not:supported | unsupported | excluded_by_user_filter：虽有历史失败证据，但不满足当前简单、高频、离屏可记忆和12类筛选规则 |
| 充放电 | 能源明细 V0.1 / 能源明细 | 能源明细页签切换 | 能源明细切换到能耗曲线<br>切换能源明细到能耗曲线<br>能源明细切换到行程信息 | BIGSUR returned common:func:not:supported for both tabs | unsupported | excluded_by_user_filter：虽有历史失败证据，但不满足当前简单、高频、离屏可记忆和12类筛选规则 |
| 充放电 | 能源明细 V0.1 / 能源明细 | 能耗曲线筛选 | 能耗曲线选择全部<br>能耗曲线选择电耗<br>能耗曲线选择油耗 | BIGSUR returned statistical/curve mode operations with empty params for all three values | empty_required_slot | excluded_by_user_filter：虽有历史失败证据，但不满足当前简单、高频、离屏可记忆和12类筛选规则 |
| 充放电 | 能源明细 V0.1 / 能源明细 | 小计行程清零及确认取消 | 清零小计行程<br>确认清除小计行程<br>取消清除小计行程 | BIGSUR returned an empty energy curve mode operation or unsupported responses instead of trip reset | misrouted | excluded_by_user_filter：虽有历史失败证据，但不满足当前简单、高频、离屏可记忆和12类筛选规则 |
| 充放电 | 车辆设置 V3.5 / 充电桌面 | 充电信息弹窗入口 | 打开充电信息 | BIGSUR returned app:ctrl open without a target | empty_required_slot | excluded_by_user_filter：虽有历史失败证据，但不满足当前简单、高频、离屏可记忆和12类筛选规则 |
| 充放电 | 车辆设置 V3.5 / 放电 | 放电信息弹窗入口 | 打开放电信息 | BIGSUR returned app:ctrl open with an empty target canonical | empty_required_slot | excluded_by_user_filter：虽有历史失败证据，但不满足当前简单、高频、离屏可记忆和12类筛选规则 |
| 充放电 | 车辆设置 V3.5 / 充电桌面 | 动力电池提醒关闭 | 关闭动力电池提醒 | BIGSUR returned common:func:not:supported | unsupported | excluded_by_user_filter：虽有历史失败证据，但不满足当前简单、高频、离屏可记忆和12类筛选规则 |
| 充放电 | D587-G车辆设置 V1.1 / 能量 | D587-G充电枪自动解锁 | 打开充电枪自动解锁<br>关闭充电枪自动解锁 | D587-G returned charge_gun_auto_unlock open and close | pass | not_add_historical_pass：历史Alchemy操作匹配；本轮未重复测试，不作为本轮实时证据 |
| 充放电 | D587-G车辆设置 V1.1 / 能量 | D587-G能耗计量方式 | 能耗计量方式设置为NEDC工况<br>能耗计量方式设置为WLTP工况 | D587-G returned nedc and wltp modes | pass | not_add_historical_pass：历史Alchemy操作匹配；本轮未重复测试，不作为本轮实时证据 |
| 充放电 | D587-G车辆设置 V1.1 / 能量 | D587-G燃油优先与纯电优先 | 能量管理设置为燃油优先<br>能量管理设置为纯电优先 | D587-G returned pv and ev energy modes | pass | not_add_historical_pass：历史Alchemy操作匹配；本轮未重复测试，不作为本轮实时证据 |
| 充放电 | D587-G车辆设置 V1.1 / 能量 | D587-G电量保持模式 | 能量管理设置为电量保持 | D587-G returned common:func:not:supported | unsupported | excluded_by_user_filter：虽有历史失败证据，但不满足当前简单、高频、离屏可记忆和12类筛选规则 |

## 最终申报

1. 设置小憩模式结束时间
2. 设置小憩模式音效
3. 调节睡眠空间音量
4. 设置睡眠空间不限时
5. 设置预约充电结束方式
6. 关闭来电铃声静音

当前申报表共6条；4条通话中错误申报已删除。
