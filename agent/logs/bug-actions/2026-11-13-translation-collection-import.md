# 2026-11-13 翻译需求收集表导入正式清单

- 操作类型：把收集表里能安全对应的条目写入两张正式 xlsx，并回写导入状态
- 收集表：`海外项目翻译需求收集表（一代+在研）` `1v06-QX9nwIgSn1FmAXd4nFuvNMhETOr2dRABzCYAewc`
- 一代正式表：`海外一代项目全量翻译正式版（产品维护）260928.xlsx` `190R0ysvAWAUlGr2JjKBxl_XJBunJ2Okz`
- 在研正式表：`C673-G/D587G翻译清单261015.xlsx` `1Hv2_mKeL0JqcSr8AaMXKnSDhjHTcDN3Y`
- 写入方式：Drive API 下载 xlsx，只改目标工作表 XML，保留 drawings，上传后按 SHA-256 回读一致
- 已写入：
  - 在研 `IC` 1086-1090：`TipInfo/BdcTpmsErrHintReq` 1-5，来源收集表 UI（在研）899-903。kk/uz 无列，未写。
  - 在研 `IC` 303、一代 `IC_TEXT` 1055：`C385/NDATextOne` / 2 改为「领航辅助即将退出，请控制车辆」。
  - 一代 `CarPlay` 9-10：`siri_voice_channel_used_localvr_tip`、`voice_disable_tip_by_cp_call`。
- 收集表变更记录 E13、E15 已标「已导入」，E15 橙色已清。
- 未导入：收集表里模块名对不上、Key 写成中文、标了待校验，或早于正式表后续修订的历史行。不整表覆盖。

- 2026-11-13 补充：按吴优确认，写入在研 `AndesCarModel-D587` 第149-150行 `settings_system_reset_charging_tip`、`settings_system_reset_discharging_tip`。只写该页已有的 10 个语种。收集表变更记录第6行已标已导入。3D 缺的 `,CA24A68C...` 和 `,D59C03DB...` 收集表没有译文行，未写。
