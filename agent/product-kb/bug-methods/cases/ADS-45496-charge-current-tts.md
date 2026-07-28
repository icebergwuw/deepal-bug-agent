# ADS-45496 Charge Current TTS

## 基本信息

- Jira：`http://jira.i-tetris.com/browse/ADS-45496`
- 模块：语音 / 车控 / 能量 / 充放电
- 在线原话：`充电电流设置为8A`
- 在线结果：`meta_id=1495`，`energy:charging:setting:charge_current`
- 标准功能：`1494 调节充电电流限值-指定`
- 深蓝项目功能点：`24599`，继承未修改

## 正式功能定义

- 深蓝国内取值范围：`8A / 10A / 16A / 32A`。
- 项目功能点当前成功 TTS：`已把$FUNC$调到$VALUE$`，其中 `$FUNC$=充电电流限值`。

## 产品结论

实际播报“掉到”是 TTS 实现或资源错误，不是 NLU 映射错误。转 TTS 实现/资源，将实际播报修正为项目功能点当前正式 TTS；不改标准 meta、slot 或意图。
