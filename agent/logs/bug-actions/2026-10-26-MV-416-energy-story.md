# 2026-10-26 MV 车辆设置能量管理建票

- 操作者：吴优
- Run ID：20261026T162841+0800-MV-416
- 涉及 Jira：MV-416
- 操作类型：新建需求
- 读取证据：吴优指定 Changan MountainView（MV）车辆设置-能量管理，并给出三份 PRD，UE 为未锁定。Jira 项目 createmeta 核对故事必填项：模块、描述、修复版本、优先级。项目只有修复版本 `无发版计划`。Epic `MV-7` 标题为 `ECR_待签署`。同项目无「能量管理 / 外接充放电 / 充电电流 / 充电电量上限」既有故事。Chrome 已登录态打开三份指定文档。未打印凭证。
- 表格位置：不适用。本次不是变更表行，未回写变更管理表，未填 PJM 列。
- 写入摘要：新建 MV Story `MV-416`。
- Jira 动作：项目 MV，类型故事，经办人 `you.wu`，Epic Link `MV-7`，修复版本 `无发版计划`，模块 `Android - CarSettings`，优先级 `P1->High`。未评论，未流转，未关联，未改其他票经办人。
- 回读校验：REST 与 `get_jira_issue` 回读标题、经办人、Epic、模块、修复版本、优先级和描述一致。飞书通知返回 `message_id=om_x100b62c4bb983ca8cf62a082957bc1d`，群 `oc_c3692001480b0aac7825bafab90989b3`。未声称已艾特。
- run bundle：不适用
- readback_sha256：不适用
- 未执行动作：未写变更管理表，未写吴优 bug 表，未关闭，未转派，未写 Alchemy
- 敏感信息处理：未记录账号、密码、token、App Secret 或访问口令

## 字段与资料

- 经办人按当前操作者吴优设置为 `you.wu`，创建时显式指定。
- Epic 使用 MV 项目内的 `ECR_待签署`（`MV-7`），没有复用 ADS-7。
- 车型不是 MV 故事创建必填项，未猜车型。
- PRD：
  - `P13项目外接充放电功能显性化功能定义文档V1.3-10.7_20231106200934A503`，`https://docs.google.com/document/d/1h8M_F-thabHLAj3gH5UG8eFr67j4CqC9/edit`
  - `充电电流挡位设置功能定义文档_20250306165413A654`，`https://drive.google.com/file/d/12FA6P2bLXbKs6qvHXpACd9kcIVgFsVcA/view`
  - `2- 充电电量上限设置功能定义文档V1.6_20260104183012A030`，`https://drive.google.com/file/d/1voBYOsbxdqmDebOSeGrIY6mZ8501mmEG/view`
- UE：按吴优指定写未锁定。对接人未给出，通知写待指定。
- 同目录另见 `C857&C518-EV能量管理相关需求文档会签版-0626-V6.0`，本次未写入票内，避免把未指定文档当成需求依据。
