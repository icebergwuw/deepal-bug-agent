#!/usr/bin/env python3

from copy import deepcopy
from pathlib import Path
import tempfile
import unittest

from validate_bug_evidence_gate import validate_log, validate_manifest


def queries(*items: tuple[str, str]) -> list[dict[str, str]]:
    return [{"kind": kind, "text": text} for kind, text in items]


def hur_case() -> dict:
    return {
        "schema_version": 3,
        "jira_key": "HUR-82492",
        "comment_causality": (
            "拒绝麦克风权限后，手机/HFP 对端反复请求 eSCO；"
            "车机创建小窗后因无权限断开音频，形成闪烁循环。"
        ),
        "customer_issue": {"identified": False},
        "related_issues": {
            "checked": True,
            "items": [
                {
                    "key": "HUR-82490",
                    "relationship": "重复提交，指向 HUR-82492",
                    "read": True,
                    "outcome": "同一根因分组，不单独定义产品目标。",
                },
                {
                    "key": "HUR-82491",
                    "relationship": "共享日志且测试预期相关",
                    "read": True,
                    "outcome": "需以 J90A 专项定义判断设备兼容边界。",
                },
            ],
        },
        "scope_checks": [
            {
                "source_id": "j90a-formal",
                "source": "J90A 蓝牙电话功能定义 V0.5",
                "source_location": "第12页，微信电话权限处理/运行时拒绝麦克风权限",
                "source_type": "special_prd",
                "role": "formal_target",
                "project_model": "J90A",
                "trigger": "微信电话拒绝麦克风权限",
                "target_behavior": "页面是否出现取决于手机和应用行为",
                "match": "exact",
                "reason": "专项资料覆盖本票项目和交互。",
            },
            {
                "source_id": "jira-actual",
                "source": "HUR-82492 完整评论与复现日志",
                "source_location": "Jira评论时间线与复现日志附件，拒绝权限后的eSCO循环片段",
                "source_type": "implementation_log",
                "role": "implementation_actual",
                "project_model": "J90A",
                "trigger": "微信电话拒绝麦克风权限",
                "target_behavior": "手机持续请求 eSCO，车机反复建链和断链",
                "match": "exact",
                "reason": "当前 Jira 日志完整覆盖本票实际行为。",
            },
            {
                "source_id": "generic-prd",
                "source": "共通蓝牙电话 PRD V1.4",
                "source_location": "第8页，系统设置关闭授权场景",
                "source_type": "prd",
                "role": "context_only",
                "project_model": "非 J90A 专项",
                "trigger": "系统设置关闭授权",
                "target_behavior": "车机不显示",
                "match": "mismatch",
                "reason": "项目和触发方式均不相同，不能替代专项定义。",
            },
        ],
        "evidence_profiles": ["general"],
        "evidence_profile_assessment": {
            "general": {
                "applicable": True,
                "reason": "非语音、非地图、非可见交互，使用通用正式定义画像。",
            },
            "voice": {"applicable": False, "reason": "不涉及语音链路。"},
            "map_navigation": {"applicable": False, "reason": "不涉及地图导航。"},
            "visible_interaction": {
                "applicable": False,
                "reason": "结论判断蓝牙兼容链路，不定义页面控件交互。",
            },
        },
        "required_evidence_checks": [
            {
                "check_id": "formal_definition_search",
                "status": "read",
                "source_ids": ["j90a-formal"],
                "searched_at": "2026-08-06",
                "search_location": "Google Drive/J90A/蓝牙电话",
                "queries": queries(
                    ("jira_key", "HUR-82492"),
                    ("problem_concept", "拒绝麦克风权限后微信电话eSCO循环"),
                    ("module_artifact", "J90A 蓝牙电话 PRD UE"),
                ),
            }
        ],
        "inheritance_chains": [],
        "expected_behavior": {
            "trigger": "微信电话运行时拒绝麦克风权限",
            "target_state": "按手机与应用端实际建链状态展示",
            "intent_function_signal": "蓝牙 HFP/eSCO 链路；无语音意图",
            "ui_tts_vehicle_behavior": "车机不制造额外的持续建链请求",
            "boundary": "手机或应用持续请求时按兼容性问题处理",
            "source_ids": ["j90a-formal"],
        },
        "conflict_resolution": (
            "HUR-82491 的小窗预期不覆盖本票的拒绝权限闪烁场景，"
            "以 J90A 专项定义和完整因果链为准。"
        ),
        "voice_evidence": {"applicable": False},
        "decision": {
            "status": "Invalid",
            "owner": "手机端/蓝牙对端设备兼容责任方",
            "implementation_source_ids": ["jira-actual"],
            "text": (
                "结论：定义为手机/HFP 对端设备兼容行为。\n"
                "依据：J90A 专项定义与 Jira 完整评论因果链。\n"
                "处理：维持 Invalid，由手机端/蓝牙对端设备兼容责任方处理。"
            ),
        },
    }


def pc37681_case() -> dict:
    return {
        "schema_version": 3,
        "jira_key": "PC-37681",
        "comment_causality": (
            "模式1正常开启；模式2原话被路由到通用恒温座舱意图，"
            "未进入低功耗项目功能点。"
        ),
        "customer_issue": {"identified": False},
        "related_issues": {
            "checked": True,
            "items": [
                {
                    "key": "ST-63391",
                    "relationship": "语音算法关联排查票",
                    "read": True,
                    "outcome": "只提供排查分类，不定义 C385MCA 产品目标。",
                }
            ],
        },
        "scope_checks": [
            {
                "source_id": "jira-expected",
                "source": "PC-37681 Jira 测试预期",
                "source_location": "Jira描述，原话‘打开恒温座舱模式二’",
                "source_type": "jira",
                "role": "context_only",
                "project_model": "C385MCA",
                "trigger": "打开恒温座舱模式二",
                "target_behavior": "测试预期模式2开启低功耗模式",
                "match": "exact",
                "reason": "Jira 预期是待核对主张，不能独立定义产品目标。",
            },
            {
                "source_id": "c385mca-inheritance",
                "source": "C385MCA 需求清单",
                "source_location": "恒温座舱功能行，项目继承说明列",
                "source_type": "formal_config",
                "role": "context_only",
                "project_model": "C385MCA",
                "trigger": "恒温座舱功能设置",
                "target_behavior": "该功能借用 C385-EVE 生效定义",
                "match": "exact",
                "reason": "同项目资料明确记录继承关系，但不单独定义模式语义。",
            },
            {
                "source_id": "c385-definition",
                "source": "C385&C673 智能情景模式功能定义 V4.3",
                "source_location": "恒温座舱章节，模式1/模式2定义条款",
                "source_type": "special_prd",
                "role": "formal_target",
                "project_model": "C385/C673",
                "trigger": "选择正常模式或低功耗模式",
                "target_behavior": "模式1进入正常模式，模式2进入低功耗模式",
                "match": "partial",
                "inheritance_chain_id": "c385mca-c385-eve",
                "reason": "定义本身不是 C385MCA，但由同项目继承资料连接。",
            },
            {
                "source_id": "vos-actual",
                "source": "VOS 原始调试日志",
                "source_location": "原话‘打开恒温座舱模式二’对应NLU路由日志段",
                "source_type": "implementation_log",
                "role": "implementation_actual",
                "project_model": "C385MCA",
                "trigger": "打开恒温座舱模式二",
                "target_behavior": "当前命中通用 constant_temperature_cabin_on",
                "match": "exact",
                "reason": "日志覆盖 Jira 原话和当前意图。",
            },
            {
                "source_id": "j90a-definition",
                "source": "J90A 恒温座舱功能定义 V1.4",
                "source_location": "恒温座舱章节，模式1/模式2定义条款",
                "source_type": "special_prd",
                "role": "context_only",
                "project_model": "J90A",
                "trigger": "恒温座舱模式1/2",
                "target_behavior": "模式1为正常、模式2为低功耗",
                "match": "mismatch",
                "reason": "异车型资料只能补充术语，不能定义 C385MCA。",
            },
            {
                "source_id": "c385mca-ue-gap",
                "source": "C385MCA 模式入口 UE/MasterGo",
                "source_location": "未取得可读页面/图层；已记录为UE资料缺口",
                "source_type": "ue",
                "role": "context_only",
                "project_model": "C385MCA",
                "trigger": "语音直接开启子模式",
                "target_behavior": "模式入口交互与页面表现",
                "match": "gap",
                "material": False,
                "reason": "本结论只判断 NLU 子模式路由，入口 UE 不改变该责任边界。",
            },
            {
                "source_id": "alchemy-current",
                "source": "Alchemy在线对话",
                "source_location": "原话‘打开恒温座舱模式二’，meta_id=1127",
                "source_type": "alchemy_current",
                "role": "implementation_actual",
                "project_model": "C385MCA",
                "trigger": "打开恒温座舱模式二",
                "target_behavior": "当前返回通用恒温座舱开启功能",
                "match": "exact",
                "reason": "当前在线结果证明语音路由实际。",
            },
            {
                "source_id": "alchemy-standard",
                "source": "Alchemy标准功能点",
                "source_location": "功能点‘恒温座舱开启’，meta_id=1127",
                "source_type": "alchemy_standard",
                "role": "context_only",
                "project_model": "标准功能",
                "trigger": "恒温座舱开启",
                "target_behavior": "标准功能未区分低功耗子模式",
                "match": "exact",
                "reason": "用于核对标准语义边界。",
            },
            {
                "source_id": "alchemy-project",
                "source": "Alchemy C385MCA项目功能点",
                "source_location": "项目功能‘恒温座舱’，继承meta_id=1127",
                "source_type": "alchemy_project",
                "role": "context_only",
                "project_model": "C385MCA",
                "trigger": "恒温座舱模式2",
                "target_behavior": "项目模式2应进入低功耗分支",
                "match": "exact",
                "reason": "用于核对项目执行策略。",
            },
        ],
        "evidence_profiles": ["voice"],
        "evidence_profile_assessment": {
            "general": {
                "applicable": False,
                "reason": "语音画像已包含通用正式定义检索。",
            },
            "voice": {
                "applicable": True,
                "reason": "Jira原话经过NLU和Alchemy项目功能点执行。",
            },
            "map_navigation": {"applicable": False, "reason": "不涉及地图导航。"},
            "visible_interaction": {
                "applicable": False,
                "reason": "本结论仅判断NLU子模式路由，不判断页面控件交互。",
            },
        },
        "required_evidence_checks": [
            {
                "check_id": "formal_definition_search",
                "status": "read",
                "source_ids": ["c385-definition"],
                "searched_at": "2026-08-06",
                "search_location": "Google Drive/C385与C673/智能情景模式",
                "queries": queries(
                    ("jira_key", "PC-37681"),
                    ("problem_concept", "恒温座舱模式2低功耗"),
                    ("module_artifact", "C385MCA 恒温座舱 PRD"),
                ),
            },
            {
                "check_id": "alchemy_current",
                "status": "read",
                "source_ids": ["alchemy-current"],
                "searched_at": "2026-08-06",
                "search_location": "Alchemy在线对话/C385MCA",
                "queries": queries(("exact_trigger", "打开恒温座舱模式二")),
            },
            {
                "check_id": "alchemy_standard",
                "status": "read",
                "source_ids": ["alchemy-standard"],
                "searched_at": "2026-08-06",
                "search_location": "Alchemy标准功能点",
                "queries": queries(("meta_or_function", "meta_id=1127")),
            },
            {
                "check_id": "alchemy_project",
                "status": "read",
                "source_ids": ["alchemy-project"],
                "searched_at": "2026-08-06",
                "search_location": "Alchemy深蓝项目功能点",
                "queries": queries(
                    ("meta_or_function", "恒温座舱 meta_id=1127"),
                    ("project_scope", "C385MCA"),
                ),
            },
        ],
        "inheritance_chains": [
            {
                "id": "c385mca-c385-eve",
                "project_model": "C385MCA",
                "function": "恒温座舱",
                "project_source_id": "c385mca-inheritance",
                "definition_source_id": "c385-definition",
                "verified": True,
                "reason": "C385MCA 需求清单明确借用 C385-EVE 生效版本。",
            }
        ],
        "expected_behavior": {
            "trigger": "用户说“打开恒温座舱模式二”",
            "target_state": "恒温座舱低功耗模式开启",
            "intent_function_signal": "下发低功耗子模式对应项目功能点",
            "ui_tts_vehicle_behavior": "按低功耗模式定义执行并返回对应结果",
            "boundary": "C385MCA 当前生效继承版本",
            "source_ids": ["c385-definition"],
        },
        "conflict_resolution": (
            "Jira 测试预期不作为定义；J90A 异车型资料排除。"
            "C385MCA 继承链连接 C385 生效定义后确定目标。"
        ),
        "voice_evidence": {
            "applicable": True,
            "availability": "complete",
            "original_utterance": "打开恒温座舱模式二",
            "alchemy_tested": True,
            "alchemy_result": "当前返回通用恒温座舱开启功能",
            "meta_id": "1127",
            "standard_function": {
                "status": "verified",
                "name": "恒温座舱开启",
                "assessment": "meta_id 已打开并核对，当前未区分低功耗子模式。",
            },
            "project_function": {
                "status": "verified",
                "name": "C385MCA 恒温座舱项目功能点",
                "assessment": "已核对项目继承点，模式2应进入低功耗分支。",
            },
        },
        "decision": {
            "status": "可转语音",
            "owner": "语音 NLU 责任方",
            "implementation_source_ids": ["vos-actual"],
            "text": (
                "结论：模式2当前未进入低功耗子模式，属于语音 NLU 映射缺陷。\n"
                "依据：C385MCA 继承链、C385 功能定义、Alchemy 与 VOS 日志。\n"
                "处理：补齐模式2到低功耗项目功能点的映射；语音 NLU 责任方处理。"
            ),
        },
    }


class BugEvidenceGateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.item = hur_case()

    def test_hur_case_passes(self) -> None:
        self.assertEqual(validate_manifest(self.item, "HUR-82492"), [])

    def test_unread_related_issue_fails(self) -> None:
        self.item["related_issues"]["items"][0]["read"] = False
        self.assertIn("关联票第 1 项未标记已读", validate_manifest(self.item))

    def test_missing_scope_fails(self) -> None:
        self.item["scope_checks"] = []
        self.assertIn("至少需要一条资料适用范围核验", validate_manifest(self.item))

    def test_missing_source_location_fails(self) -> None:
        del self.item["scope_checks"][0]["source_location"]
        self.assertIn("资料范围第 1 项缺少 source_location", validate_manifest(self.item))

    def test_key_mismatch_fails(self) -> None:
        self.assertIn(
            "Jira key 不一致：期望 ADS-1，实际 HUR-82492",
            validate_manifest(self.item, "ADS-1"),
        )

    def test_missing_customer_classification_fails(self) -> None:
        del self.item["customer_issue"]
        self.assertIn(
            "客户问题识别必须包含 identified 布尔值",
            validate_manifest(self.item),
        )

    def test_pc37681_old_jira_plus_mismatch_pattern_fails(self) -> None:
        item = pc37681_case()
        item["scope_checks"] = [
            scope
            for scope in item["scope_checks"]
            if scope["source_id"] in {"jira-expected", "vos-actual", "j90a-definition"}
        ]
        item["inheritance_chains"] = []
        item["expected_behavior"]["source_ids"] = [
            "jira-expected",
            "j90a-definition",
        ]
        item["voice_evidence"] = {
            "applicable": True,
            "availability": "unavailable",
            "alchemy_tested": False,
            "standard_function": {
                "status": "unavailable",
                "reason": "首轮未打开标准功能点。",
            },
            "project_function": {
                "status": "unavailable",
                "reason": "首轮未打开项目功能点。",
            },
            "unavailable_reason": "首轮仅使用 Jira 预期和 VOS 日志。",
            "next_action": "重新执行 Alchemy 原话并读取标准/项目功能点。",
        }
        errors = validate_manifest(item)
        self.assertTrue(
            any("缺少有效 formal_target" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any("语音证据不完整时禁止确定性定责" in error for error in errors),
            errors,
        )

    def test_pc37681_verified_inheritance_and_voice_chain_pass(self) -> None:
        self.assertEqual(validate_manifest(pc37681_case(), "PC-37681"), [])

    def test_unverified_inheritance_does_not_promote_partial_definition(self) -> None:
        item = pc37681_case()
        item["inheritance_chains"][0]["verified"] = False
        errors = validate_manifest(item)
        self.assertTrue(
            any("缺少有效 formal_target" in error for error in errors),
            errors,
        )

    def test_mismatch_formal_target_is_excluded(self) -> None:
        item = pc37681_case()
        definition = next(
            scope
            for scope in item["scope_checks"]
            if scope["source_id"] == "c385-definition"
        )
        definition["match"] = "mismatch"
        item["inheritance_chains"] = []
        errors = validate_manifest(item)
        self.assertTrue(
            any("缺少有效 formal_target" in error for error in errors),
            errors,
        )

    def test_material_gap_forces_downgrade(self) -> None:
        item = pc37681_case()
        gap = next(
            scope
            for scope in item["scope_checks"]
            if scope["source_id"] == "c385mca-ue-gap"
        )
        gap["material"] = True
        gap["next_action"] = "补齐模式入口 UE 图层后重新判断交互预期。"
        errors = validate_manifest(item)
        self.assertTrue(
            any("存在会改变判断的关键 gap" in error for error in errors),
            errors,
        )

    def test_material_gap_can_be_recorded_with_pending_status(self) -> None:
        item = pc37681_case()
        gap = next(
            scope
            for scope in item["scope_checks"]
            if scope["source_id"] == "c385mca-ue-gap"
        )
        gap["material"] = True
        gap["next_action"] = "补齐模式入口 UE 图层后重新判断交互预期。"
        item["decision"]["status"] = "待复核"
        item["decision"]["owner"] = "C385MCA 产品资料责任方"
        item["decision"]["text"] = (
            "结论：入口交互仍存在关键 UE 缺口，暂不作确定性判断。\n"
            "依据：已读功能定义与 UE 检索结果。\n"
            "处理：补齐模式入口 UE 图层后复核；C385MCA 产品资料责任方处理。"
        )
        self.assertEqual(validate_manifest(item), [])

    def test_voice_unavailable_can_only_pass_as_pending(self) -> None:
        item = pc37681_case()
        item["voice_evidence"] = {
            "applicable": True,
            "availability": "unavailable",
            "original_utterance": "打开恒温座舱模式二",
            "alchemy_tested": False,
            "standard_function": {
                "status": "unavailable",
                "reason": "Alchemy 页面当前不可访问。",
            },
            "project_function": {
                "status": "unavailable",
                "reason": "无法从标准功能继续读取项目功能点。",
            },
            "unavailable_reason": "Alchemy 当前不可访问，meta_id 未核验。",
            "next_action": "恢复访问后重跑原话并读取标准/项目功能点。",
        }
        deterministic_errors = validate_manifest(item)
        self.assertTrue(
            any("语音证据不完整时禁止确定性定责" in error for error in deterministic_errors),
            deterministic_errors,
        )
        item["decision"]["status"] = "待复核"
        item["decision"]["owner"] = "语音平台证据补齐责任方"
        item["decision"]["text"] = (
            "结论：Alchemy 当前证据不可用，暂不定责语音 NLU。\n"
            "依据：Jira 原话、VOS 日志及平台访问限制。\n"
            "处理：恢复后重跑原话并读取功能点；语音平台证据补齐责任方处理。"
        )
        self.assertEqual(validate_manifest(item), [])

    def test_ads47560_missing_customer_case_forces_pending(self) -> None:
        item = deepcopy(hur_case())
        item["jira_key"] = "ADS-47560"
        item["customer_issue"] = {
            "identified": True,
            "external_id": "CUSTOMER-20260729-0001",
            "test_case": {
                "checked": True,
                "status": "missing",
                "source": "Jira 未附完整客户测试用例",
            },
        }
        item["decision"]["status"] = "可关闭"
        item["decision"]["owner"] = "吴优产品负责人"
        item["decision"]["text"] = (
            "结论：当前实现符合正式定义。\n"
            "依据：生效正式定义。\n"
            "处理：向客户收集客户测试用例后复核；吴优产品负责人处理。"
        )
        errors = validate_manifest(item)
        self.assertIn(
            "客户测试用例缺失或不完整时禁止关闭或判为非 Bug",
            errors,
        )
        self.assertIn(
            "客户测试用例缺失或不完整时状态必须降为待确认",
            errors,
        )

        item["decision"]["status"] = "待确认"
        item["decision"]["text"] = (
            "结论：客户测试用例缺失，暂不关闭。\n"
            "依据：Jira 原票与当前资料。\n"
            "处理：向客户收集客户测试用例后复核；吴优产品负责人处理。"
        )
        self.assertEqual(validate_manifest(item), [])

    def test_context_only_cannot_replace_implementation_actual(self) -> None:
        item = hur_case()
        actual = next(
            scope
            for scope in item["scope_checks"]
            if scope["source_id"] == "jira-actual"
        )
        actual["role"] = "context_only"
        errors = validate_manifest(item)
        self.assertTrue(
            any("缺少 exact 的 implementation_actual" in error for error in errors),
            errors,
        )

    def test_pc38036_without_drive_definition_check_fails(self) -> None:
        item = pc37681_case()
        item["jira_key"] = "PC-38036"
        item["required_evidence_checks"] = [
            check
            for check in item["required_evidence_checks"]
            if check["check_id"] != "formal_definition_search"
        ]
        errors = validate_manifest(item)
        self.assertIn(
            "证据画像缺少必查资料：formal_definition_search",
            errors,
        )

    def test_pc37808_map_profile_requires_drive_prd_and_special_definition(self) -> None:
        item = pc37681_case()
        item["jira_key"] = "PC-37808"
        item["evidence_profiles"].append("map_navigation")
        item["evidence_profile_assessment"]["map_navigation"] = {
            "applicable": True,
            "reason": "带路线偏好的地图导航并经过POI二次交互。",
        }
        errors = validate_manifest(item)
        self.assertIn("证据画像缺少必查资料：main_prd_search", errors)
        self.assertIn(
            "证据画像缺少必查资料：special_definition_search",
            errors,
        )

    def test_visible_interaction_profile_requires_config_and_ue_search(self) -> None:
        item = pc37681_case()
        item["evidence_profiles"].append("visible_interaction")
        item["evidence_profile_assessment"]["visible_interaction"] = {
            "applicable": True,
            "reason": "问题涉及页面可见节点和控件状态。",
        }
        errors = validate_manifest(item)
        self.assertIn("证据画像缺少必查资料：formal_config_search", errors)
        self.assertIn(
            "证据画像缺少必查资料：interaction_or_ue_search",
            errors,
        )

    def test_alchemy_project_cannot_be_sole_product_formal_target(self) -> None:
        item = pc37681_case()
        definition = next(
            scope
            for scope in item["scope_checks"]
            if scope["source_id"] == "c385-definition"
        )
        definition["source_type"] = "alchemy_project"
        errors = validate_manifest(item)
        self.assertTrue(
            any("不允许的来源类型：alchemy_project" in error for error in errors),
            errors,
        )
        self.assertIn(
            "确定性结论不能只依赖Alchemy功能点；预期行为卡必须引用产品正式定义来源",
            errors,
        )

    def test_alchemy_current_cannot_be_formal_target(self) -> None:
        item = pc37681_case()
        current = next(
            scope
            for scope in item["scope_checks"]
            if scope["source_id"] == "alchemy-current"
        )
        current["role"] = "formal_target"
        errors = validate_manifest(item)
        self.assertTrue(
            any("alchemy_current 不得标为 formal_target" in error for error in errors),
            errors,
        )

    def test_missing_drive_sources_can_only_pass_as_pending_with_trace(self) -> None:
        item = pc37681_case()
        item["evidence_profiles"].append("map_navigation")
        item["evidence_profile_assessment"]["map_navigation"] = {
            "applicable": True,
            "reason": "问题涉及地图导航执行。",
        }
        for check_id in ("main_prd_search", "special_definition_search"):
            item["required_evidence_checks"].append(
                {
                    "check_id": check_id,
                    "status": "unavailable",
                    "source_ids": [],
                    "searched_at": "2026-08-06",
                    "search_location": "Google Drive/深蓝/地图",
                    "queries": queries(
                        ("jira_key", "PC-37681"),
                        ("problem_concept", "路线偏好 POI二次交互"),
                        ("module_artifact", "深蓝地图主PRD专项定义"),
                    ),
                    "candidate_audit": {
                        "completed": True,
                        "results_count": 0,
                        "candidates": [],
                    },
                    "reason": "当前未取得可读文档。",
                    "material": True,
                    "next_action": "取得主PRD和专项定义后复核。",
                }
            )
        deterministic_errors = validate_manifest(item)
        self.assertTrue(
            any("状态必须降为待复核" in error for error in deterministic_errors),
            deterministic_errors,
        )
        item["decision"]["status"] = "待复核"
        item["decision"]["owner"] = "地图产品资料责任方"
        item["decision"]["text"] = (
            "结论：地图正式资料当前不可读，暂不作确定性定责。\n"
            "依据：已记录Drive检索入口和资料限制。\n"
            "处理：取得主PRD和专项定义后复核；地图产品资料责任方处理。"
        )
        self.assertEqual(validate_manifest(item), [])

    def test_weak_string_queries_fail_schema_v3(self) -> None:
        item = pc37681_case()
        formal = next(
            check
            for check in item["required_evidence_checks"]
            if check["check_id"] == "formal_definition_search"
        )
        formal["queries"] = ["x"]
        errors = validate_manifest(item)
        self.assertTrue(
            any("query 第 1 项必须是对象" in error for error in errors),
            errors,
        )

    def test_formal_search_requires_semantic_query_kinds(self) -> None:
        item = pc37681_case()
        formal = next(
            check
            for check in item["required_evidence_checks"]
            if check["check_id"] == "formal_definition_search"
        )
        formal["queries"] = queries(("jira_key", "PC-37681"))
        errors = validate_manifest(item)
        self.assertTrue(
            any("缺少查询类型" in error for error in errors),
            errors,
        )

    def test_not_found_drive_search_requires_candidate_audit(self) -> None:
        item = pc37681_case()
        item["decision"]["status"] = "待复核"
        item["decision"]["owner"] = "资料责任方"
        item["decision"]["text"] = (
            "结论：正式资料仍需补齐，暂不定责。\n"
            "依据：当前检索未形成有效目标。\n"
            "处理：补齐正式资料后复核；资料责任方处理。"
        )
        formal = next(
            check
            for check in item["required_evidence_checks"]
            if check["check_id"] == "formal_definition_search"
        )
        formal.update(
            {
                "status": "not_found",
                "source_ids": [],
                "reason": "未定位正式定义。",
                "material": True,
                "next_action": "继续补查正式定义。",
            }
        )
        errors = validate_manifest(item)
        self.assertIn(
            "必查资料 formal_definition_search not_found 时缺少候选文件审计",
            errors,
        )

    def test_read_candidate_cannot_be_hidden_as_not_found(self) -> None:
        item = pc37681_case()
        item["decision"]["status"] = "待复核"
        item["decision"]["owner"] = "资料责任方"
        item["decision"]["text"] = (
            "结论：已读候选资料仍存在规则缺口。\n"
            "依据：已读正式资料候选。\n"
            "处理：补齐缺口后复核；资料责任方处理。"
        )
        formal = next(
            check
            for check in item["required_evidence_checks"]
            if check["check_id"] == "formal_definition_search"
        )
        formal.update(
            {
                "status": "not_found",
                "source_ids": [],
                "reason": "候选资料未定义完整目标。",
                "material": True,
                "next_action": "另记规则缺口。",
                "candidate_audit": {
                    "completed": True,
                    "results_count": 1,
                    "candidates": [
                        {
                            "title": "C385 恒温座舱功能定义",
                            "url": "https://drive.google.com/example",
                            "disposition": "read",
                            "source_ids": ["c385-definition"],
                        }
                    ],
                },
            }
        )
        errors = validate_manifest(item)
        self.assertTrue(
            any("存在已读候选，不能标记 not_found" in error for error in errors),
            errors,
        )

    def test_batch_log_requires_one_card_per_jira(self) -> None:
        text = """# 批量处理

- 涉及 Jira：PC-38036、PC-37808

## 决策核验卡

- 备注因果链：仅有一张卡。
- 客户问题识别：否。
- 关联票：已核验无直接关联票。
- 证据画像与必查资料：voice，已查资料。
- 资料适用范围：同项目 exact。
- 冲突处理：已处理。
- 唯一结论：待复核，由资料责任方处理。
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "batch.md"
            path.write_text(text, encoding="utf-8")
            errors = validate_log(path, "PC-38036")
        self.assertIn("批量日志缺少 PC-38036 独立决策核验卡", errors)


if __name__ == "__main__":
    unittest.main()
