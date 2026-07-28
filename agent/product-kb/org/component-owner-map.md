# Component Owner Map

来源：`长安 C673&C385-Components.xlsx`。该文件是 Office-backed 表，不能直接用 Google Sheets API 读取；已通过 Drive 原始下载读取样例。

## 常用模块分流

| 模块 | Jira Component / 系统 | FO / 负责人 | 备注 | 包名 |
| --- | --- | --- | --- | --- |
| 地图 | Android -Map | 程云 | 导航 DA 车型也涉及陈中兴 | `com.android.launcher3` |
| SystemUI & Launcher | Android -Launcher&SystemUI | 谢重任 / 曾爽 | SystemUI 含顶部状态栏、底部 dock、AppList、下拉快捷中心；Launcher / 3D 桌面偏曾爽 | `com.android.systemui`, `com.android.launcher3` |
| 控制中心 | Android -SystemUI | 谢重任 | 快捷中心 / 控制中心类问题 | `com.android.systemui` |
| 媒体音乐 | Android -Music | 龙学卫 / 吴松泽 | 三方音乐、视频类语音接入、桌面音乐 widget 等需拆责任 | `com.mega.media` |
| 蓝牙电话 | Android -BTPhone | 雷磊02 | 隐私授权、拨打电话、通话记录等 | `com.mega.btphone` |
| 语音 - VUI | Android -VUI | 甘杰 | 含可见即可说、APP 页面交互控制不执行 / 执行错误 | `com.mega.assist.vui` |
| 语音服务 | 语音服务 | 谭威 | 语音服务 / TTS 相关需区分 | `com.mega.assistant.service` |
| AIS | Apps - AI | 刘双龙 | ASR、语音服务 SDK、算法类能力 |  |
| ASR 识别错误 | Apps - AI / ASR | 汪文菁 | 用户原话被识别成错误文本时，按 2026-07-17 吴优确认的规则直接转汪文菁 |  |
| 情景模式 | Android -SceneMode | 丁黎 | backup 明逸智 |  |
| 场景积木 |  | 谢重任 / 曾爽 | 页面 / Launcher / 场景链路需拆责任 |  |
| TTS | TTS | 谭威 | TTS 规范和播报文案 | `com.mega.tts` |
| 美行地图 |  | 陈中兴 | C385 / C673 DA 车型导航由美行开发 |  |
| 华为应用相关 |  | 钟奇江 / 易积勇 | 花瓣地图、华为 AVM、华为 APA、华为哨兵等 |  |

## 使用规则

- 表格中的 FO 用于初步分流，不替代 Jira 当前评论和项目实际分工。
- 页面层级、AppList、状态栏、dock、快捷中心优先查 SystemUI / Launcher。
- 语音问题要拆：VUI、语音服务、AIS、TTS、应用执行侧，不要笼统写“语音处理”。
- AIS 的通用模块负责人信息不覆盖具体路由规则；确认是 ASR 识别错误时统一转汪文菁。
