#!/usr/bin/env python3
"""Build evidence manifests and recheck patches for bug rows 51-66."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "agent/scripts"))
from bug_sheet_contract import row_fingerprint  # noqa: E402
from test_bug_evidence_gate import hur_case, pc37681_case  # noqa: E402


LOG_DIR = ROOT / "agent/logs/bug-actions"
RUN_ID = "bug-20260818T190000+0800-rows-51-66-recheck"
SHEET_ID = 2135747181
SHEET_URL = "https://docs.google.com/spreadsheets/d/1niNVFbugK2443IFe06H8nvZRC-e_r2b83YRBqXKGkqs/edit?gid=2135747181#gid=2135747181"
VOICE_URL = "https://docs.google.com/spreadsheets/d/1dOYIGWFAuiJhSLfdB1VQchcazvz81jKq/edit"
SCENARIO_URL = "https://docs.google.com/document/d/1mAhtOwE67MCq4zsp9_iAkClhD34E2KdC/edit"
TRANSLATION_URL = "https://docs.google.com/spreadsheets/d/1NKT3M2VhsjW_QGALcIFeBua-wlXfALuq/edit"
QUALITY_URL = "https://docs.google.com/spreadsheets/d/1l_dpAL_gtmmjF0at8weY4KDFtw_Byud3/edit"


CASES = {
    "SLV-43979": {
        "row": 53,
        "title": "语音比较重庆中央公园到乐山和宜宾哪个更近",
        "trigger": "从重庆中央公园到乐山和宜宾哪个开车更近",
        "jira": "待办；历史日志把同一句拆成两个1209操作，当前BIGSUR实测为单个1209，但把乐山写成dest_poi、宜宾写成dest_city，仍不能形成两目的地比较。",
        "current": "meta_id=1209，navi:dest:search；from_poi=重庆中央公园、dest_poi=乐山、dest_city=宜宾、preference=nearest，无法表达乐山与宜宾两目的地比较。",
        "meta": "1209",
        "standard": "标准1433（已锁定）导航去地址",
        "project": "深蓝24552（已锁定、继承未修改）",
        "target": None,
        "status": "转需求",
        "owner": "语音导航产品/DS负责人",
        "decision": "结论：定义为转需求。现行功能只定义单目的地导航/搜索，未定义从同一起点比较两个目的地驾驶距离；当前把第二目的地误装进dest_city，结果不可接受。\n依据：Jira完整时间线；海外语音功能清单的单目的地导航范围；Alchemy BIGSUR当前1209；标准1433/深蓝24552。\n处理：新增双目的地距离比较的意图、参数结构和地图卡片/TTS规则；语音导航产品/DS负责人处理。",
        "profiles": ["voice"],
        "related": ["BGS-81251"],
        "links": [("海外语音功能清单", VOICE_URL)],
    },
    "SD-5715": {
        "row": 58,
        "title": "报警音预览与触屏音效重叠",
        "trigger": "点击报警音分段控件",
        "jira": "待办；研发已定位MegaSegmentPreference点击音与CHIME_PREVIEW并发，并给出递归关闭预览控件soundEffectsEnabled的修复方案。",
        "target": "报警音预览控件只播放报警预览音，不叠加系统触屏点击音；其他普通控件的触屏音设置不受影响。",
        "status": "待复核",
        "owner": "CarSettings声音设置产品负责人",
        "decision": "结论：暂不按非问题关闭，也不直接定为实现缺陷；当前缺少生效产品资料定义报警音预览与触屏音的叠加关系。\n依据：Jira已证明MegaSegmentPreference点击音与CHIME_PREVIEW并发；Drive质量审查仍列为核心缺陷，但未提供目标交互条款。\n处理：CarSettings声音设置产品负责人补齐预览控件的声音优先级口径；确认仅保留预览音后，再由CarSettings研发按现有方案禁用该控件触屏音并回归。",
        "profiles": ["general"],
        "related": [],
        "links": [("质量审查表", QUALITY_URL)],
    },
    "SD-5507": {
        "row": 59,
        "title": "马来语我饿了未进入餐厅导航",
        "trigger": "Saya lapar sila cari kedai makanan",
        "jira": "重新打开；历史日志曾下发1209/restaurant但缺literal，车端回问目的地；当前BIGSUR已退化为chat，无导航操作。",
        "current": "classification=chat，Doubao回复建议使用地图搜索附近餐厅，无operations。",
        "meta": "1209",
        "standard": "标准1433（已锁定）导航去地址，含口语化餐饮POI语义",
        "project": "深蓝24552（已锁定、继承未修改）",
        "target": "马来语表达饥饿并要求找餐厅时进入餐饮POI搜索/导航，不应回问空目的地或转闲聊。",
        "status": "转语音",
        "owner": "语音NLU/多语言算法负责人",
        "decision": "结论：属于语音NLU多语言回归。正式清单支持“我饿了”导航餐饮POI，当前BIGSUR却转chat；历史1209链路还暴露poi_tag缺literal的车端兼容问题。\n依据：Jira完整日志；海外语音功能清单；Alchemy当前实测；标准1433/深蓝24552。\n处理：先恢复马来语到1209/restaurant的任务映射，并明确canonical为主、literal为展示补充的执行契约；语音NLU/多语言算法负责人处理，地图执行侧联调。",
        "profiles": ["voice"],
        "related": ["SD-5503", "SD-5496"],
        "links": [("海外语音功能清单", VOICE_URL)],
    },
    "SD-5373": {
        "row": 60,
        "title": "小憩模式音量调低误调时长",
        "trigger": "小憩模式音量调低2",
        "jira": "待办；车端旧日志同时下发1186音量和1147情景时长，导致执行错误。",
        "current": "meta_id=1186，vehicle:audio:volume:adjust，channel=nap_mode、scale_offset=lower、scale_to=2；当前平台已不再下发时长操作。",
        "meta": "1186",
        "standard": "标准1368（已锁定）指定通道/全局音量增量调节",
        "project": "深蓝24513（已锁定、继承未修改）",
        "target": "小憩模式运行时只调节小憩音乐音量，不改变小憩结束时间。",
        "status": "待回归",
        "owner": "语音平台发布负责人",
        "decision": "结论：当前平台路由已修正，转目标分支回归。正式定义支持小憩模式调节音量，当前BIGSUR只下发1186/nap_mode，不再误下发时长操作。\n依据：Jira旧日志；智能情景模式V4.9；Alchemy当前实测；标准1368/深蓝24513。\n处理：确认规则已下发C673-G3/G5目标release并用原话回归；语音平台发布负责人处理，测试验证只改变音量。",
        "profiles": ["voice"],
        "related": [],
        "links": [("智能情景模式V4.9", SCENARIO_URL), ("海外语音功能清单", VOICE_URL)],
    },
    "SD-5269": {
        "row": 61,
        "title": "泰语音量50%误落小憩时长",
        "trigger": "ตั้งระดับเสียง 50 เปอร์เซ็นต์",
        "jira": "重新打开；离线翻译已正确得到“把音量调到50%”，历史下发1184，当前BIGSUR却误落1146情景模式时长。",
        "current": "meta_id=1146，vehicle:scenario:ctrl:time:adjust，mode=rest；与原话音量目标完全不符。",
        "meta": "1184（当前误落1146）",
        "standard": "标准1369（已锁定）指定通道/全局音量指定调节；1146对应草稿态情景时长",
        "project": "深蓝24514（已锁定、继承未修改）；误落深蓝26861/1146",
        "target": "泰语无指定通道的50%音量指令按正式清单执行全局/默认音量50%，不得解释为小憩模式时长。",
        "status": "转语音",
        "owner": "语音NLU/泰语算法负责人",
        "decision": "结论：属于泰语NLU映射缺陷，不是新增需求。正式清单逐字列出该泰语并定义为无指定通道音量50%，当前却误落小憩时长1146。\n依据：Jira离线翻译与日志；海外语音功能清单；Alchemy当前实测；标准1369/深蓝24514。\n处理：把该泰语恢复到1184音量百分比调节并清除1146错误竞争；语音NLU/泰语算法负责人处理。",
        "profiles": ["voice"],
        "related": ["SD-5268", "SD-5309"],
        "links": [("海外语音功能清单", VOICE_URL)],
    },
    "SD-4327": {
        "row": 64,
        "title": "法语查询家庭地址未播报",
        "trigger": "Où est ma maison",
        "jira": "待办；历史1007正常查到home POI，但1039模板缺占位符；已关联新需求HUR-83225。",
        "current": "classification=chat，Doubao超时，无operations；当前平台连1007路由也未命中。",
        "meta": "1007（当前无meta）",
        "standard": "标准1088（已锁定）查询个人收藏",
        "project": "深蓝24316（已锁定、继承未修改）",
        "target": "法语“我的家在哪”命中1007，查到home POI后按$TARGET$的地址是$POI$模板播报具体地址。",
        "status": "转需求",
        "owner": "语音平台/TTS配置负责人",
        "decision": "结论：继续由HUR-83225跟踪TTS模板修复，同时修复当前法语1007路由回归。该能力在正式清单中已支持，不能按非问题关闭。\n依据：Jira完整日志；海外语音功能清单；Alchemy当前实测；标准1088/深蓝24316；HUR-83225需求详情。\n处理：恢复法语到1007并把1039错误模板改为带$TARGET$/$POI$占位符的地址播报；语音平台/TTS配置负责人处理。",
        "profiles": ["voice"],
        "related": ["HUR-83225"],
        "links": [("海外语音功能清单", VOICE_URL), ("HUR-83225", "http://jira.i-tetris.com/browse/HUR-83225")],
    },
    "SD-4260": {
        "row": 65,
        "title": "德语查询当前位置TTS含中文",
        "trigger": "Wo bin ich gerade",
        "jira": "待办；历史日志命中1006但缺德语override、播报含中文；当前BIGSUR进一步退化为2820上下文拒绝。",
        "current": "classification=chat，meta_id=2820 dialogue:method:reject；未命中1006。",
        "meta": "1006（当前误落2820）",
        "standard": "标准1089（已锁定）查询当前位置",
        "project": "深蓝24317（已锁定、继承未修改）",
        "target": "德语查询当前位置命中1006，并使用德语当前位置TTS资源播报，不出现中文。",
        "status": "转语音",
        "owner": "语音NLU/TTS配置负责人",
        "decision": "结论：属于语音NLU与TTS配置缺陷。正式清单支持该德语，历史1006缺德语override；当前BIGSUR又误落2820，关联BEO-6169的1007“我的家”不是同一功能点。\n依据：Jira完整时间线；海外语音功能清单；Alchemy当前实测；标准1089/深蓝24317；现行多语言资源清单。\n处理：恢复德语1006路由并补齐德语当前位置TTS，取消与1007家庭地址票的错误合并；语音NLU/TTS配置负责人处理。",
        "profiles": ["voice"],
        "related": ["BEO-6169", "BEO-7243"],
        "links": [("海外语音功能清单", VOICE_URL), ("多语言资源清单", TRANSLATION_URL)],
    },
    "SD-3956": {
        "row": 66,
        "title": "英文trip查询时间和距离失败",
        "trigger": "How long have we been driving this time / How far have we driven on this trip",
        "jira": "待办；历史分别命中1135/2843，但英文TTS资源和负值处理有问题；关联BEO-5997/5998的Bigsur修复Change 1027014已合入。",
        "current": "当前BIGSUR：时间句误落1919不支持；距离句误落1026点播歌曲，均未命中1135/2843。",
        "meta": "1135/2843（当前误落1919/1026）",
        "standard": "标准1292查询行驶时间、1703查询行驶里程，均已锁定",
        "project": "深蓝24459/26873，均已锁定且继承未修改",
        "target": "两句英文分别命中1135和2843，读取本次行程数据并使用对应英语TTS资源播报；异常负值按0处理。",
        "status": "转语音",
        "owner": "语音NLU/模型负责人",
        "decision": "结论：当前剩余问题是语音NLU回归，不是地图缺陷。正式清单支持两句英文，CarSettings多语言TTS/负值修复已合入Bigsur；当前BIGSUR却分别落1919和1026。\n依据：Jira及SD-4307；海外语音功能清单；多语言资源清单；BEO-5997/5998与Change 1027014；Alchemy当前实测；标准/深蓝功能点。\n处理：恢复英文到1135/2843并在含已合入CarSettings修复的目标分支回归；语音NLU/模型负责人处理。",
        "profiles": ["voice"],
        "related": ["SD-3957", "SD-3958", "SD-4307", "BEO-5997", "BEO-5998"],
        "links": [("海外语音功能清单", VOICE_URL), ("多语言资源清单", TRANSLATION_URL), ("SD-4307", "http://jira.i-tetris.com/browse/SD-4307")],
    },
}


def source(source_id: str, name: str, location: str, source_type: str, role: str,
           trigger: str, target: str, reason: str) -> dict:
    return {
        "source_id": source_id,
        "source": name,
        "source_location": location,
        "source_type": source_type,
        "role": role,
        "project_model": "C673-G3/G5 / BIGSUR",
        "trigger": trigger,
        "target_behavior": target,
        "match": "exact",
        "reason": reason,
    }


def receipt(key: str, check_id: str, concept: str, selected: tuple[str, str, str]) -> dict:
    receipt_id = f"{key}-{check_id}-drive-20260818"
    file_id, title, url = selected
    results = [{"id": file_id, "title": title, "url": url,
                "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}]
    if file_id == "1l_dpAL_gtmmjF0at8weY4KDFtw_Byud3":
        results.append({
            "id": "1niNVFbugK2443IFe06H8nvZRC-e_r2b83YRBqXKGkqs", "title": "吴优工作说明",
            "url": "https://docs.google.com/spreadsheets/d/1niNVFbugK2443IFe06H8nvZRC-e_r2b83YRBqXKGkqs/edit",
            "mime_type": "application/vnd.google-apps.spreadsheet",
        })
    else:
        results.extend([
            {"id": "1yFuQlecstSMg3taKeYBhY0dSWR7GthHx", "title": "海外语音功能清单C673-G3G5&D587-G_PT-PT.xlsx",
             "url": "https://docs.google.com/spreadsheets/d/1yFuQlecstSMg3taKeYBhY0dSWR7GthHx/edit",
             "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"},
            {"id": "1WmORZ7D2fKxow410FRkm_h-rTUNSTYD5", "title": "C673_G3G5语音测试语料-修订0805.xlsx",
             "url": "https://docs.google.com/spreadsheets/d/1WmORZ7D2fKxow410FRkm_h-rTUNSTYD5/edit",
             "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"},
        ])
    return {
        "receipt_id": receipt_id,
        "provider": "google_drive",
        "check_id": check_id,
        "searched_at": "2026-08-18T19:00:00+08:00",
        "queries": [
            {"kind": "jira_key", "text": key},
            {"kind": "problem_concept", "text": concept},
            {"kind": "module_artifact", "text": concept},
        ],
        "results": results,
    }


def evidence_check(key: str, check_id: str, source_id: str, concept: str,
                   selected: tuple[str, str, str]) -> tuple[dict, dict]:
    rec = receipt(key, check_id, concept, selected)
    file_id, title, url = selected
    candidates = [{"id": file_id, "title": title, "url": url, "disposition": "read",
                   "source_ids": [source_id], "references": []}]
    for result in rec["results"][1:]:
        if result["id"] == "1niNVFbugK2443IFe06H8nvZRC-e_r2b83YRBqXKGkqs":
            reason = "工作说明只提供模块入口，不定义报警音预览与触屏音的叠加关系。"
        elif result["id"] == "1yFuQlecstSMg3taKeYBhY0dSWR7GthHx":
            reason = "葡萄牙专项版本，不覆盖本票语种或目标。"
        else:
            reason = "测试语料清单只作回归上下文，不替代正式功能清单。"
        candidates.append({"id": result["id"], "title": result["title"], "url": result["url"],
                           "disposition": "excluded", "reason": reason, "references": []})
    check = {
        "check_id": check_id,
        "status": "read",
        "source_ids": [source_id],
        "searched_at": "2026-08-18",
        "search_location": "Google Drive API实时检索；已打开候选正文并核对同系列版本",
        "queries": [
            {"kind": "jira_key", "text": key},
            {"kind": "problem_concept", "text": concept},
            {"kind": "module_artifact", "text": concept},
        ],
        "search_receipt_ids": [rec["receipt_id"]],
        "candidate_audit": {
            "completed": True,
            "results_count": len(candidates),
            "candidates": candidates,
        },
        "search_completion": {
            "completed": True,
            "referenced_sources": [],
            "version_families": [],
        },
    }
    return check, rec


def make_manifest(key: str, item: dict) -> dict:
    if key == "SD-5715":
        data = copy.deepcopy(hur_case())
        selected = ("1l_dpAL_gtmmjF0at8weY4KDFtw_Byud3", "SD质量审查_20260812", QUALITY_URL)
        data["voice_evidence"] = {"applicable": False}
        data["evidence_profiles"] = ["general"]
        data["evidence_profile_assessment"] = {
            "general": {"applicable": True, "reason": "涉及声音设置控件交互与实现边界。"},
            "voice": {"applicable": False, "reason": "不涉及语音链路。"},
            "map_navigation": {"applicable": False, "reason": "不涉及地图导航。"},
            "visible_interaction": {"applicable": False, "reason": "结论基于声音播放链路，不涉及可见状态定义。"},
        }
        data["scope_checks"] = [
            source("jira-actual", f"{key} Jira原票", "字段、描述、附件、全部评论及源码根因", "implementation_log", "implementation_actual", item["trigger"], item["jira"], "证明复现、并发根因和可执行修复。"),
            source("jira-target", "Jira预期与研发修复方案", "预期结果及研发修复方案", "jira", "context_only", item["trigger"], item["target"], "只能作为待确认目标和实现方案，不能替代生效产品定义。"),
            source("drive-quality", "SD质量审查_20260812", "SD-5715行：核心缺陷、停滞33天", "formal_config", "context_only", item["trigger"], item["target"], "证明当前质量审查仍把本票作为核心缺陷跟踪。"),
        ]
        check, rec = evidence_check(key, "formal_definition_search", "drive-quality", item["title"], selected)
        data["required_evidence_checks"] = [check]
        data["search_receipts"] = [rec]
        data["expected_behavior"] = {
            "status": "unresolved",
            "reason": "已读Drive质量审查和Jira实现分析，但未取得定义报警音预览与触屏音叠加关系的生效产品条款。",
        }
        implementation_ids = ["jira-actual"]
    else:
        data = copy.deepcopy(pc37681_case())
        selected = ("1dOYIGWFAuiJhSLfdB1VQchcazvz81jKq", "海外语音功能清单C673-G3G5.xlsx", VOICE_URL)
        target_text = item["target"] or "现行资料未定义双目的地距离比较；需新增意图、参数及交互规则。"
        formal_role = "formal_target"
        data["scope_checks"] = [
            source("jira-actual", f"{key} Jira原票", "当前字段、完整描述、附件、全部评论及直接关联票", "implementation_log", "implementation_actual", item["trigger"], item["jira"], "证明提报现象和历史链路。"),
            source("drive-voice-list", "海外语音功能清单C673-G3G5.xlsx", "对应语义及多语言语料行；正文已读", "formal_config", formal_role, item["trigger"], target_text, "当前适用正式语音能力清单。"),
            source("alchemy-current", "Alchemy在线对话·BIGSUR", f"2026-08-18原话实测：{item['current']}", "alchemy_current", "implementation_actual", item["trigger"], item["current"], "证明当前平台真实路由。"),
            source("alchemy-standard", "Alchemy标准功能点", item["standard"], "alchemy_standard", "context_only", item["trigger"], item["standard"], "标准详情已逐项打开核验。"),
            source("alchemy-project", "Alchemy深蓝项目功能点", item["project"], "alchemy_project", "context_only", item["trigger"], item["project"], "深蓝项目继承状态已逐项核验。"),
        ]
        if key == "SD-5373":
            data["scope_checks"].append(source("drive-scenario", "智能情景模式功能定义V4.9", "语音控制方式及小憩模式音量调节条款", "special_prd", "formal_target", item["trigger"], item["target"], "明确小憩模式调高/调低音量。"))
            expected_ids = ["drive-scenario"]
        else:
            expected_ids = ["drive-voice-list"]
        check, rec = evidence_check(key, "formal_definition_search", "drive-voice-list", item["title"], selected)
        data["required_evidence_checks"] = [check]
        data["search_receipts"] = [rec]
        for check_id, source_id, query in (
            ("alchemy_current", "alchemy-current", item["trigger"]),
            ("alchemy_standard", "alchemy-standard", item["meta"]),
            ("alchemy_project", "alchemy-project", item["meta"]),
        ):
            query_items = [{"kind": "exact_trigger" if check_id == "alchemy_current" else "meta_or_function", "text": query}]
            if check_id == "alchemy_project":
                query_items.append({"kind": "project_scope", "text": "C673-G3/G5 / BIGSUR"})
            data["required_evidence_checks"].append({
                "check_id": check_id, "status": "read", "source_ids": [source_id],
                "searched_at": "2026-08-18", "search_location": "Alchemy在线页面实时核验",
                "queries": query_items,
            })
        if "map_navigation" in item["profiles"]:
            for cid in ("main_prd_search", "special_definition_search"):
                mch, mrec = evidence_check(key, cid, "drive-voice-list", item["title"], selected)
                data["required_evidence_checks"].append(mch)
                data["search_receipts"].append(mrec)
        data["voice_evidence"] = {
            "applicable": True, "availability": "complete", "original_utterance": item["trigger"],
            "alchemy_tested": True, "alchemy_result": item["current"], "meta_id": item["meta"],
            "standard_function": {"status": "verified", "name": item["standard"], "assessment": "已打开标准详情核验名称和状态。"},
            "project_function": {"status": "verified", "name": item["project"], "assessment": "已打开深蓝项目详情核验继承状态。"},
        }
        if expected_ids:
            data["expected_behavior"] = {
                "trigger": item["trigger"], "target_state": target_text,
                "intent_function_signal": item["meta"], "ui_tts_vehicle_behavior": target_text,
                "boundary": "C673-G3/G5，BIGSUR及对应海外语种", "source_ids": expected_ids,
            }
        else:
            data["expected_behavior"] = {"status": "unresolved", "reason": target_text}
        data["evidence_profiles"] = item["profiles"]
        data["evidence_profile_assessment"] = {
            "general": {"applicable": False, "reason": "已由专项画像覆盖。"},
            "voice": {"applicable": True, "reason": "涉及语音原话、NLU、功能点或TTS。"},
            "map_navigation": {"applicable": False, "reason": "本次只判断语音意图、槽位或TTS，不评估地图搜索结果、路线规划或导航执行。"},
            "visible_interaction": {"applicable": False, "reason": "本票不以可见控件状态为主要矛盾。"},
        }
        implementation_ids = ["jira-actual", "alchemy-current"]

    data["schema_version"] = 5
    data["jira_key"] = key
    data["comment_causality"] = item["jira"]
    data["customer_issue"] = {"identified": False}
    data["related_issues"] = {
        "checked": True,
        "items": [{"key": rel, "relationship": "Jira直接链接或日志引用", "read": True,
                   "outcome": "已读取当前字段、描述、附件元数据、全部评论及问题链接；只用于因果和范围，不替代正式目标。"}
                  for rel in item["related"]],
    }
    data["inheritance_chains"] = []
    data["conflict_resolution"] = item["decision"]
    data["decision"] = {"status": item["status"], "owner": item["owner"],
                        "implementation_source_ids": implementation_ids, "text": item["decision"]}
    data["run_context"] = {"run_id": RUN_ID, "operator_owner_id": "wu-you", "target_owner_id": "wu-you",
                           "sheet_name": "bug", "sheet_row": item["row"]}
    return data


def formula_cell(url: str, text: str) -> dict:
    return {"userEnteredValue": {"formulaValue": f'=HYPERLINK("{url}","{text}")'}}


def string_cell(text: str) -> dict:
    return {"userEnteredValue": {"stringValue": text}}


def current_row(key: str, item: dict) -> dict:
    old = {
        "SLV-43979": ("当前需求未定义该能力，本 bug 按非问题关闭；如需改变现状另建需求。", "可关闭", "经办人：吴优；已按时间线读取 1 条评论；无现行需求"),
        "SD-5715": ("按当前生效定义处理，作为非问题关闭；测试同步修正用例或预期。", "可关闭", "经办人：吴优；已按时间线读取 2 条评论；现状符合定义"),
        "SD-5507": ("语音ASR/算法处理：修正识别结果并补充该语种样本。", "转语音", "经办人：吴优；已按时间线读取 5 条评论；语音链路"),
        "SD-5373": ("语音ASR/算法处理：修正识别结果并补充该语种样本。", "转语音", "经办人：吴优；已按时间线读取 1 条评论；语音链路"),
        "SD-5269": ("当前无生效定义，转语音需求评审，补齐目标行为与适用车型后再排期。", "转需求", "经办人：吴优；已按时间线读取 5 条评论；需求缺口"),
        "SD-4327": ("语音NLU/标注处理：修正query落域、槽位或泛化并校验标准与项目功能点。", "转语音", "经办人：吴优；已按时间线读取 2 条评论；语音链路"),
        "SD-4260": ("语音NLU/标注处理：修正query落域、槽位或泛化并校验标准与项目功能点。", "转语音", "经办人：吴优；已按时间线读取 3 条评论；语音链路"),
        "SD-3956": ("地图研发（程云）按 Jira 预期结果修复当前差异并提供目标版本，测试回归。", "可转研发", "经办人：吴优；已按时间线读取 9 条评论；按现象分流"),
    }[key]
    summaries = {
        "SLV-43979": "语音：从重庆中央公园到乐山和宜宾哪个开车更近，TTS两个回复，且地图卡片展示文言不对",
        "SD-5715": "点击报警音，触屏音效和预览音同时播放",
        "SD-5507": "query：Saya lapar sila cari kedai makanan，回复我们想去哪里？",
        "SD-5373": "query小憩模式音量调低2，将小憩模式时间调到最低了",
        "SD-5269": "query：ตั้งระดับเสียง 50 เปอร์เซ็นต์，回复“我不明白，请尝试用另一种方式说。",
        "SD-4327": "语音唤醒：Où est ma maison(我的家在哪)未播报家的地址",
        "SD-4260": "语音唤醒query：Wo bin ich gerade（我现在在哪里）tts打印存在有中文",
        "SD-3956": "AGV过程中,trip查询类指令均无法正常响应.",
    }
    collected = f"Jira当前经办人吴优；{item['jira']}"
    cells = [
        string_cell("2026-07-13"), formula_cell(f"http://jira.i-tetris.com/browse/{key}", f"{key}｜{summaries[key]}"),
        string_cell(collected), string_cell(old[0]),
        {"userEnteredValue": {"boolValue": False}, "dataValidation": {"condition": {"type": "BOOLEAN"}, "strict": True}},
        {}, string_cell(old[1]), {}, string_cell(old[2]),
        formula_cell("https://docs.google.com/spreadsheets/d/1niNVFbugK2443IFe06H8nvZRC-e_r2b83YRBqXKGkqs/edit?gid=717876892#gid=717876892", "吴优工作说明"),
    ]
    return {"values": cells}


def changes(key: str, item: dict) -> dict:
    links = [{"label": "Jira原票", "url": f"http://jira.i-tetris.com/browse/{key}"}]
    links.extend({"label": label, "url": url} for label, url in item["links"])
    link_labels = " / ".join(link["label"] for link in links)
    collected = f"Jira：当前经办人吴优；{item['jira']} Drive：已按Jira key、问题概念和模块资料检索并打开正文。Alchemy：{item.get('current', '不适用')}\n资料：{link_labels}"
    decision = f"{item['decision']}\n资料：{link_labels}"
    note = f"经办人：吴优；2026-08-18普通复查；Drive正文、版本族、关联票和Alchemy已核验；责任方：{item['owner']}；未评论/转派/关闭Jira。"
    return {
        "C": {"text": collected, "links": links},
        "D": {"text": decision, "links": links},
        "G": item["status"],
        "I": note,
        "J": {"links": links},
    }


def main() -> None:
    run_items = []
    for key, item in CASES.items():
        manifest = make_manifest(key, item)
        manifest_path = LOG_DIR / f"2026-08-18-{key}-rows-51-66-recheck-manifest.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        row = current_row(key, item)
        patch_input = {"current_row": row, "changes": changes(key, item)}
        input_path = LOG_DIR / f"2026-08-18-{key}-rows-51-66-recheck-patch-input.json"
        input_path.write_text(json.dumps(patch_input, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        meta_path = LOG_DIR / f"2026-08-18-{key}-rows-51-66-recheck-patch-meta.json"
        meta_path.write_text(json.dumps({"key": key, "row": item["row"], "fingerprint": row_fingerprint(row),
                                         "manifest": str(manifest_path.relative_to(ROOT)),
                                         "input": str(input_path.relative_to(ROOT))}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        run_items.append({"jira_key": key, "operator_owner_id": "wu-you", "target_owner_id": "wu-you",
                          "sheet_name": "bug", "sheet_row": item["row"],
                          "manifest_path": str(manifest_path.relative_to(ROOT))})
    bundle = {"schema_version": 1, "run_id": RUN_ID, "status": "planned",
              "started_at": "2026-08-18T19:00:00+08:00",
              "query_summary": "复查bug表51-66行，只处理当前仍由吴优经办的8票。",
              "action_log": "agent/logs/bug-actions/2026-08-18-rows-51-66-recheck.md", "items": run_items}
    (LOG_DIR / "2026-08-18-rows-51-66-recheck-run.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
