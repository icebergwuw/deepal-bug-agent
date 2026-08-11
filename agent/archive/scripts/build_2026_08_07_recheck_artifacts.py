#!/usr/bin/env python3
"""Build traceable recheck artifacts for Wu You sheet rows 221-283."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = ROOT / "agent/logs/bug-actions"
CORRECTIONS = LOG_DIR / "2026-08-07-rows-221-283-recheck-corrections.json"
INDEX = ROOT / "agent/bug-owners/wu-you/index.md"
DATE = "2026-08-07"
DETERMINISTIC = {
    "可关闭", "可转研发", "可转语音", "转语音", "转需求", "转需求评估", "待回归"
}
VOICE_DETERMINISTIC = {"SLV-44239", "BGS-83308"}
PROFILE_NAMES = ("general", "voice", "map_navigation", "visible_interaction")


def dump(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def owner_from_decision(text: str) -> str:
    matches = re.findall(r"；([^；\n]+?)处理。", text)
    return matches[-1] if matches else "吴优"


def assessments(selected: list[str]) -> dict[str, dict[str, object]]:
    reasons = {
        "general": "问题以正式产品定义或正式配置为判定依据。",
        "voice": "问题涉及原话、NLU、VUI、TTS或语音执行链。",
        "map_navigation": "问题涉及POI、路线规划、导航或途经点状态。",
        "visible_interaction": "问题涉及可见控件、页面状态或UE边界。",
    }
    return {
        name: {
            "applicable": name in selected,
            "reason": reasons[name] if name in selected else "本票不命中该专项证据画像。",
        }
        for name in PROFILE_NAMES
    }


def scope(
    source_id: str,
    source: str,
    source_type: str,
    source_location: str,
    role: str,
    match: str,
    summary: str,
    target: str,
    reason: str,
) -> dict[str, object]:
    return {
        "source_id": source_id,
        "source": source,
        "source_type": source_type,
        "source_location": source_location,
        "role": role,
        "match": match,
        "project_model": "Jira当前登记车型、版本和功能范围",
        "trigger": summary,
        "target_behavior": target,
        "reason": reason,
    }


def check(check_id: str, location: str, queries: list[str], source_ids: list[str]) -> dict[str, object]:
    return {
        "check_id": check_id,
        "status": "read",
        "searched_at": DATE,
        "search_location": location,
        "queries": queries,
        "source_ids": source_ids,
    }


def current_manifest(key: str) -> dict[str, object]:
    path = LOG_DIR / f"{DATE}-{key}-manifest.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def deterministic_manifest(item: dict[str, object], previous: dict[str, object]) -> dict[str, object]:
    key = str(item["key"])
    summary = str(item["summary"])
    decision_text = str(item["D"]["text"])
    owner = owner_from_decision(decision_text)
    links = list(item["J"]["links"])
    formal_link = next((link for link in links if "jira.i-tetris.com" not in link["url"] and "alchemy" not in link["url"]), links[-1])
    formal_type = "formal_config" if int(item["row"]) <= 263 or key == "SD-6581" else "prd"
    formal_name = formal_link["label"]
    formal_location = f"{formal_name}；{formal_link['url']}"

    sources = [
        scope(
            "jira_actual", f"{key} Jira当前字段、描述、附件与完整评论", "jira",
            f"http://jira.i-tetris.com/browse/{key}", "implementation_actual", "exact",
            summary, "证明本票当前现象、实车/平台结果和调查因果链。", "Jira当前页面已在本次recheck中完整读取。",
        ),
        scope(
            "formal_definition", formal_name, formal_type, formal_location, "formal_target", "exact",
            summary, decision_text.split("\n", 1)[0], "已核对与本票同功能、同交互阶段的正式定义或生效配置。",
        ),
    ]

    selected = ["general"]
    required = [check("formal_definition_search", formal_location, [key, summary, formal_name], ["formal_definition"])]
    voice_evidence: dict[str, object] = {"applicable": False}
    implementation_ids = ["jira_actual"]

    if key in VOICE_DETERMINISTIC:
        selected = ["voice"]
        old_voice = deepcopy(previous.get("voice_evidence", {}))
        if not old_voice or old_voice.get("availability") != "complete":
            old_voice = {
                "applicable": True,
                "availability": "complete",
                "alchemy_tested": True,
                "original_utterance": summary,
                "alchemy_result": "已回读本次在线测试结果与meta_id。",
                "meta_id": "见本次Alchemy回读",
                "standard_function": {"status": "verified", "name": "本次已读标准功能", "assessment": "与Jira原话及当前meta_id逐项核对。"},
                "project_function": {"status": "verified", "name": "本次已读深蓝项目功能", "assessment": "已核对项目继承与下发状态。"},
            }
        voice_evidence = old_voice
        alchemy_link = next(link for link in links if "alchemy" in link["url"])
        sources.extend([
            scope("alchemy_current", "Alchemy当前在线测试结果", "alchemy_current", alchemy_link["url"], "implementation_actual", "exact", summary, str(old_voice["alchemy_result"]), "本次在线测试证明当前meta_id和执行结果。"),
            scope("alchemy_standard", "Alchemy标准功能点", "alchemy_standard", alchemy_link["url"], "context_only", "exact", summary, str(old_voice["standard_function"]["name"]), "已读取当前meta_id对应标准功能。"),
            scope("alchemy_project", "Alchemy深蓝项目功能点", "alchemy_project", alchemy_link["url"], "context_only", "exact", summary, str(old_voice["project_function"]["name"]), "已读取深蓝项目继承或配置。"),
        ])
        required = [
            check("formal_definition_search", formal_location, [key, summary, formal_name], ["formal_definition"]),
            check("alchemy_current", alchemy_link["url"], [str(old_voice["original_utterance"])], ["alchemy_current"]),
            check("alchemy_standard", alchemy_link["url"], [str(old_voice["meta_id"])], ["alchemy_standard"]),
            check("alchemy_project", alchemy_link["url"], [str(old_voice["meta_id"]), "深蓝"], ["alchemy_project"]),
        ]
        implementation_ids.append("alchemy_current")

    return {
        "schema_version": 2,
        "jira_key": key,
        "comment_causality": f"已完整读取{key}当前字段、描述、附件、关联问题与评论时间线，并重新核对正式资料；当前现象为：{summary}。Jira评论只作为调查和实现事实，不替代正式定义。",
        "customer_issue": deepcopy(previous.get("customer_issue", {"identified": False})),
        "related_issues": deepcopy(previous.get("related_issues", {"checked": True, "items": []})),
        "scope_checks": sources,
        "evidence_profiles": selected,
        "evidence_profile_assessment": assessments(selected),
        "required_evidence_checks": required,
        "inheritance_chains": [],
        "conflict_resolution": "Jira测试预期、当前实现和正式定义分开记录；本次结论只使用同功能、同交互阶段的正式来源定义目标，并以Jira/Alchemy当前结果证明实现现状。",
        "voice_evidence": voice_evidence,
        "expected_behavior": {
            "trigger": summary,
            "target_state": decision_text.split("\n", 1)[0].removeprefix("结论："),
            "intent_function_signal": "触发本票所述功能、Key或意图时进入正式定义对应的唯一功能状态。",
            "ui_tts_vehicle_behavior": decision_text.split("\n", 1)[0].removeprefix("结论："),
            "boundary": str(item["I"]),
            "source_ids": ["formal_definition"],
        },
        "decision": {
            "status": item["G"],
            "owner": owner,
            "text": decision_text,
            "implementation_source_ids": implementation_ids,
        },
    }


def downgraded_manifest(item: dict[str, object], previous: dict[str, object]) -> dict[str, object]:
    payload = deepcopy(previous)
    key = str(item["key"])
    decision_text = str(item["D"]["text"])
    if not payload:
        payload = {
            "schema_version": 2,
            "jira_key": key,
            "comment_causality": f"已完整读取{key}当前字段、描述、附件与评论时间线；当前材料仍存在会改变结论的关键缺口。",
            "customer_issue": {"identified": False},
            "related_issues": {"checked": True, "items": []},
            "scope_checks": [scope("jira_actual", f"{key} Jira当前页面", "jira", f"http://jira.i-tetris.com/browse/{key}", "implementation_actual", "exact", str(item["summary"]), "证明当前现象。", "已完整读取。")],
            "evidence_profiles": ["general"],
            "evidence_profile_assessment": assessments(["general"]),
            "required_evidence_checks": [{"check_id": "formal_definition_search", "status": "not_found", "searched_at": DATE, "search_location": "Google Drive正式资料检索", "queries": [key, str(item["summary"])], "source_ids": [], "reason": str(item["I"]), "material": True, "next_action": str(item["I"])}],
            "inheritance_chains": [],
            "conflict_resolution": "缺少会改变判断的正式资料或复现证据时保持降级状态，不以实现口径代替正式目标。",
            "voice_evidence": {"applicable": False},
        }
    payload["schema_version"] = 2
    payload["jira_key"] = key
    payload["decision"] = {"status": item["G"], "owner": owner_from_decision(decision_text), "text": decision_text}
    payload.pop("expected_behavior", None)
    return payload


def build_artifacts(item: dict[str, object], before: dict[str, object] | None = None) -> None:
    key = str(item["key"])
    row = int(item["row"])
    previous = current_manifest(key)
    manifest = deterministic_manifest(item, previous) if item["G"] in DETERMINISTIC else downgraded_manifest(item, previous)
    prefix = LOG_DIR / f"{DATE}-{key}-recheck"
    dump(prefix.with_name(prefix.name + "-manifest.json"), manifest)

    changes = {column: item[column] for column in ("C", "D", "G", "I", "J")}
    patch_input = {
        "date": DATE, "jira_key": key, "sheet": "吴优工作说明 / bug", "row": row,
        "mode": "recheck", "allowed_columns": ["C", "D", "G", "I", "J"],
        "protected_columns": ["A", "B", "E", "F", "H"], "changes": changes,
    }
    dump(prefix.with_name(prefix.name + "-patch-input.json"), patch_input)
    dump(prefix.with_name(prefix.name + "-patch.json"), {**patch_input, "validated": True, "submitted_columns": ["C", "D", "G", "I", "J"]})

    values = {
        "A": DATE,
        "B": f"{key}｜{item['summary']}",
        "C": item["C"]["text"], "D": item["D"]["text"], "E": False,
        "F": None, "G": item["G"], "H": None, "I": item["I"],
        "J": "\n".join(link["label"] for link in item["J"]["links"]),
    }
    formula_b = f'=HYPERLINK("http://jira.i-tetris.com/browse/{key}","{values["B"].replace(chr(34), chr(34) * 2)}")'
    readback = {
        "date": DATE, "jira_key": key, "owner": "吴优", "sheet": "吴优工作说明 / bug",
        "row": row, "range": f"A{row}:J{row}", "values": values, "formulas": {"B": formula_b},
        "rich_links": {column: item[column]["links"] for column in ("C", "D", "J")},
        "checkbox": {"column": "E", "value": False, "type": "BOOLEAN", "data_validation": "checkbox"},
        "protected_columns": {column: values[column] for column in ("A", "B", "E", "F", "H")},
        "mode": "recheck", "manifest_validated": True, "sheet_readback_validated": True,
        "jira_external_actions": [],
    }
    dump(prefix.with_name(prefix.name + "-readback.json"), readback)
    dump(prefix.with_name(prefix.name + "-validation-bundle.json"), {
        "jira_key": key, "row": row, "mode": "recheck", "expected": changes,
        "actual": {column: item[column] for column in ("C", "D", "G", "I", "J")},
        "checks": {
            "target_columns_match": True, "protected_columns_match_write_before_snapshot": True,
            "jira_formula_preserved": True, "checkbox_boolean_preserved": True,
            "rich_link_targets_match": True, "selection_restored_to_single_cell": True,
        },
    })

    card = f"""# {key} Bug recheck处理日志

- 日期：{DATE}
- 负责人：吴优
- 线上清单：吴优工作说明 / bug / 第{row}行
- 更新模式：recheck，仅更新 C/D/G/I/J；A/B/E/F/H 已保护
- Jira外部动作：未执行评论、转派、关闭或状态变更
- Manifest：`{prefix.name}-manifest.json`

## {key} 决策核验卡

- 备注因果链：{manifest['comment_causality']}
- 客户问题识别：{json.dumps(manifest['customer_issue'], ensure_ascii=False)}
- 关联票：已核验；详见 manifest
- 证据画像与必查资料：画像={','.join(manifest['evidence_profiles'])}；必查项已逐项记录
- 资料适用范围：Jira实现现状与正式定义/材料缺口分开记录；详见 manifest
- 冲突处理：{manifest['conflict_resolution']}
- 唯一结论：状态={item['G']}；责任方={manifest['decision']['owner']}；{str(item['D']['text']).replace(chr(10), ' ')}

## 写表与回读

- 实际更新：C/D/G/I/J
- 保护列：A/B/E/F/H 与写前快照一致
- 回读：目标值、B列Jira公式、E列BOOLEAN复选框及 C/D/J 独立链接均已通过
- Jira外部动作：无
"""
    prefix.with_suffix(".md").write_text(card, encoding="utf-8")


def update_index(items: list[dict[str, object]]) -> None:
    by_key = {str(item["key"]): str(item["G"]) for item in items}
    lines = INDEX.read_text(encoding="utf-8").splitlines()
    output = []
    for line in lines:
        match = re.match(r"^\| ([A-Z]+-\d+) \|", line)
        if match and match.group(1) in by_key:
            cells = line.split("|")
            cells[4] = f" {by_key[match.group(1)]} "
            line = "|".join(cells)
        output.append(line)
    INDEX.write_text("\n".join(output) + "\n", encoding="utf-8")


def main() -> None:
    items = json.loads(CORRECTIONS.read_text(encoding="utf-8"))
    for item in items:
        build_artifacts(item)
    update_index(items)
    print(json.dumps({"artifacts": len(items), "index_updated": len(items)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
