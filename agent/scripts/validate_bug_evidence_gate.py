#!/usr/bin/env python3
"""Validate a Bug decision gate manifest or a completed action log.

The business rules remain in ``agent/evidence-contract.md``. This script
enforces the machine-checkable evidence-sufficiency subset before a Bug
decision is written to a sheet.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


EVIDENCE_REQUIREMENTS_PATH = (
    Path(__file__).resolve().parents[1] / "config" / "evidence-requirements.json"
)
EVIDENCE_REQUIREMENTS = json.loads(
    EVIDENCE_REQUIREMENTS_PATH.read_text(encoding="utf-8")
)
MANIFEST_SCHEMA_VERSION = EVIDENCE_REQUIREMENTS["manifest_schema_version"]
SOURCE_TYPES = set(EVIDENCE_REQUIREMENTS["source_types"])
FORMAL_TARGET_ALLOWED_SOURCE_TYPES = set(
    EVIDENCE_REQUIREMENTS["formal_target_allowed_source_types"]
)
PRODUCT_FORMAL_SOURCE_TYPES = set(
    EVIDENCE_REQUIREMENTS["product_formal_source_types"]
)
EVIDENCE_CHECKS = EVIDENCE_REQUIREMENTS["checks"]
EVIDENCE_PROFILES = EVIDENCE_REQUIREMENTS["profiles"]
CHECK_STATUSES = set(EVIDENCE_REQUIREMENTS["check_statuses"])
QUERY_KINDS = set(EVIDENCE_REQUIREMENTS["query_kinds"])
ALLOWED_SEARCH_ORIGINS = {"chrome", "connector", "in_app_browser"}
CANDIDATE_DISPOSITIONS = set(
    EVIDENCE_REQUIREMENTS["candidate_dispositions"]
)
REFERENCE_STATUSES = {"searched", "read", "unavailable", "not_applicable"}
VERSION_FAMILY_STATUSES = {"enumerated", "unavailable", "not_applicable"}
VERSION_PATTERN = re.compile(r"(?i)(?:^|[^a-z0-9])v\d+(?:\.\d+)+")

SCOPE_MATCHES = {"exact", "partial", "mismatch", "gap"}
SOURCE_ROLES = {"formal_target", "implementation_actual", "context_only"}
CARD_LABELS = (
    "备注因果链",
    "客户问题识别",
    "关联票",
    "证据画像与必查资料",
    "资料适用范围",
    "冲突处理",
    "唯一结论",
)

CUSTOMER_CASE_STATUSES = {"complete", "incomplete", "missing"}
CLOSURE_STATUSES = {"可关闭", "非 Bug", "非Bug", "设计如此", "Invalid", "invalid"}
DETERMINISTIC_STATUSES = CLOSURE_STATUSES | {
    "可转研发",
    "可转语音",
    "转语音",
    "转需求",
    "转需求评估",
    "待回归",
}
DOWNGRADE_STATUSES = {"待复核", "待确认", "待会诊"}
SUPPORTED_STATUSES = DETERMINISTIC_STATUSES | DOWNGRADE_STATUSES
VOICE_AVAILABILITY = {"complete", "partial", "unavailable"}
VOICE_FUNCTION_STATUSES = {"verified", "unavailable", "not_applicable"}
EXPECTED_BEHAVIOR_FIELDS = (
    "trigger",
    "target_state",
    "intent_function_signal",
    "ui_tts_vehicle_behavior",
    "boundary",
)


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_voice_function(
    value: Any,
    label: str,
    *,
    allow_not_applicable: bool,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return [f"语音证据缺少 {label}"]

    status = value.get("status")
    if status not in VOICE_FUNCTION_STATUSES:
        errors.append(
            f"{label} status 必须为 verified、unavailable"
            + (" 或 not_applicable" if allow_not_applicable else "")
        )
        return errors
    if status == "not_applicable" and not allow_not_applicable:
        errors.append(f"{label} 不允许标记 not_applicable")
    elif status == "verified":
        if not nonempty(value.get("name")):
            errors.append(f"{label} 已核验时缺少 name")
        if not nonempty(value.get("assessment")):
            errors.append(f"{label} 已核验时缺少 assessment")
    elif not nonempty(value.get("reason")):
        errors.append(f"{label} {status} 时缺少 reason")
    return errors


def validate_manifest(payload: Any, expected_key: str | None = None) -> list[str]:
    """Return human-readable gate errors for one structured Bug decision."""

    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["核验输入必须是 JSON 对象"]

    if payload.get("schema_version") != MANIFEST_SCHEMA_VERSION:
        errors.append(
            f"manifest schema_version 必须为 {MANIFEST_SCHEMA_VERSION}"
        )

    jira_key = payload.get("jira_key")
    if not nonempty(jira_key):
        errors.append("缺少 jira_key")
    elif expected_key and jira_key != expected_key:
        errors.append(f"Jira key 不一致：期望 {expected_key}，实际 {jira_key}")

    run_context = payload.get("run_context")
    if not isinstance(run_context, dict):
        errors.append("缺少 run_context")
        run_context = {}
    for field in ("run_id", "operator_owner_id", "target_owner_id", "sheet_name"):
        if not nonempty(run_context.get(field)):
            errors.append(f"run_context 缺少 {field}")
    if not isinstance(run_context.get("sheet_row"), int) or run_context.get("sheet_row", 0) < 1:
        errors.append("run_context.sheet_row 必须是正整数")

    receipt_by_id: dict[str, dict[str, Any]] = {}
    search_receipts = payload.get("search_receipts")
    if not isinstance(search_receipts, list):
        errors.append("search_receipts 必须是数组")
        search_receipts = []
    for index, receipt in enumerate(search_receipts, start=1):
        if not isinstance(receipt, dict):
            errors.append(f"检索回执第 {index} 项不是对象")
            continue
        receipt_id = receipt.get("receipt_id")
        if not nonempty(receipt_id):
            errors.append(f"检索回执第 {index} 项缺少 receipt_id")
        elif receipt_id in receipt_by_id:
            errors.append(f"检索回执 receipt_id 重复：{receipt_id}")
        else:
            receipt_by_id[receipt_id] = receipt
        if receipt.get("provider") != "google_drive":
            errors.append(f"检索回执 {receipt_id or index} provider 必须为 google_drive")
        origin = receipt.get("origin")
        if origin not in ALLOWED_SEARCH_ORIGINS:
            errors.append(
                f"检索回执 {receipt_id or index} origin 必须记录实际入口："
                f"{'、'.join(sorted(ALLOWED_SEARCH_ORIGINS))}；"
                "优先当前 Chrome 登录态，不再要求 origin=connector"
            )
        if not nonempty(receipt.get("check_id")):
            errors.append(f"检索回执 {receipt_id or index} 缺少 check_id")
        if not nonempty(receipt.get("searched_at")):
            errors.append(f"检索回执 {receipt_id or index} 缺少 searched_at")
        receipt_queries = receipt.get("queries")
        if not isinstance(receipt_queries, list) or not receipt_queries:
            errors.append(f"检索回执 {receipt_id or index} queries 必须是非空数组")
            receipt_queries = []
        for query_index, query in enumerate(receipt_queries, start=1):
            if not isinstance(query, dict):
                errors.append(f"检索回执 {receipt_id or index} query 第 {query_index} 项不是对象")
                continue
            if query.get("kind") not in QUERY_KINDS:
                errors.append(f"检索回执 {receipt_id or index} query 第 {query_index} 项 kind 未登记")
            if not nonempty(query.get("text")):
                errors.append(f"检索回执 {receipt_id or index} query 第 {query_index} 项缺少 text")
        receipt_results = receipt.get("results")
        if not isinstance(receipt_results, list):
            errors.append(f"检索回执 {receipt_id or index} results 必须是数组")
            continue
        seen_result_ids: set[str] = set()
        for result_index, result in enumerate(receipt_results, start=1):
            if not isinstance(result, dict):
                errors.append(f"检索回执 {receipt_id or index} 结果第 {result_index} 项不是对象")
                continue
            for field in ("id", "title", "url", "mime_type"):
                if not nonempty(result.get(field)):
                    errors.append(f"检索回执 {receipt_id or index} 结果第 {result_index} 项缺少 {field}")
            result_id = result.get("id")
            if nonempty(result_id):
                if result_id in seen_result_ids:
                    errors.append(f"检索回执 {receipt_id or index} 结果 id 重复：{result_id}")
                seen_result_ids.add(result_id)

    if not nonempty(payload.get("comment_causality")):
        errors.append("缺少备注因果链")

    customer_case_missing = False
    customer_issue = payload.get("customer_issue")
    if not isinstance(customer_issue, dict) or not isinstance(
        customer_issue.get("identified"), bool
    ):
        errors.append("客户问题识别必须包含 identified 布尔值")
    elif customer_issue["identified"]:
        if not nonempty(customer_issue.get("external_id")):
            errors.append("客户提报 Bug 缺少客户问题编号")
        test_case = customer_issue.get("test_case")
        if not isinstance(test_case, dict) or test_case.get("checked") is not True:
            errors.append("客户提报 Bug 必须检查客户测试用例")
        else:
            case_status = test_case.get("status")
            if case_status not in CUSTOMER_CASE_STATUSES:
                errors.append(
                    "客户测试用例 status 必须为 complete、incomplete 或 missing"
                )
            if not nonempty(test_case.get("source")):
                errors.append("客户测试用例缺少 source 或缺失说明")
            customer_case_missing = case_status in {"incomplete", "missing"}

    related = payload.get("related_issues")
    if not isinstance(related, dict) or related.get("checked") is not True:
        errors.append("关联票必须显式标记 checked=true")
    else:
        items = related.get("items", [])
        if not isinstance(items, list):
            errors.append("关联票 items 必须是数组")
        for index, item in enumerate(items, start=1):
            if not isinstance(item, dict):
                errors.append(f"关联票第 {index} 项不是对象")
                continue
            for field in ("key", "relationship", "outcome"):
                if not nonempty(item.get(field)):
                    errors.append(f"关联票第 {index} 项缺少 {field}")
            if item.get("read") is not True:
                errors.append(f"关联票第 {index} 项未标记已读")

    source_by_id: dict[str, dict[str, Any]] = {}
    material_gap_ids: list[str] = []
    scopes = payload.get("scope_checks")
    if not isinstance(scopes, list) or not scopes:
        errors.append("至少需要一条资料适用范围核验")
    else:
        for index, scope in enumerate(scopes, start=1):
            if not isinstance(scope, dict):
                errors.append(f"资料范围第 {index} 项不是对象")
                continue
            source_id = scope.get("source_id")
            if not nonempty(source_id):
                errors.append(f"资料范围第 {index} 项缺少 source_id")
            elif source_id in source_by_id:
                errors.append(f"资料范围 source_id 重复：{source_id}")
            else:
                source_by_id[source_id] = scope
            for field in (
                "source",
                "source_location",
                "project_model",
                "trigger",
                "target_behavior",
                "reason",
            ):
                if not nonempty(scope.get(field)):
                    errors.append(f"资料范围第 {index} 项缺少 {field}")
            if scope.get("role") not in SOURCE_ROLES:
                errors.append(
                    f"资料范围第 {index} 项 role 必须为 "
                    "formal_target、implementation_actual 或 context_only"
                )
            source_type = scope.get("source_type")
            if source_type not in SOURCE_TYPES:
                errors.append(
                    f"资料范围第 {index} 项 source_type 必须为已登记类型"
                )
            elif (
                scope.get("role") == "formal_target"
                and source_type not in FORMAL_TARGET_ALLOWED_SOURCE_TYPES
            ):
                errors.append(
                    f"资料范围第 {index} 项 {source_type} 不得标为 formal_target"
                )
            if scope.get("match") not in SCOPE_MATCHES:
                errors.append(
                    f"资料范围第 {index} 项 match 必须为 {', '.join(sorted(SCOPE_MATCHES))}"
                )
            elif scope.get("match") == "gap":
                if not isinstance(scope.get("material"), bool):
                    errors.append(f"资料范围第 {index} 项 gap 必须声明 material 布尔值")
                elif scope["material"]:
                    if nonempty(source_id):
                        material_gap_ids.append(source_id)
                    if not nonempty(scope.get("next_action")):
                        errors.append(
                            f"资料范围第 {index} 项关键 gap 缺少 next_action"
                        )

    selected_profiles: set[str] = set()
    profiles = payload.get("evidence_profiles")
    if not isinstance(profiles, list) or not profiles:
        errors.append("evidence_profiles 必须是非空数组")
        profiles = []
    else:
        for profile in profiles:
            if not nonempty(profile):
                errors.append("evidence_profiles 只能包含非空字符串")
            elif profile not in EVIDENCE_PROFILES:
                errors.append(f"未知证据画像：{profile}")
            elif profile in selected_profiles:
                errors.append(f"证据画像重复：{profile}")
            else:
                selected_profiles.add(profile)

    profile_assessment = payload.get("evidence_profile_assessment")
    if not isinstance(profile_assessment, dict):
        errors.append("缺少 evidence_profile_assessment")
        profile_assessment = {}
    for profile in EVIDENCE_PROFILES:
        assessment = profile_assessment.get(profile)
        if not isinstance(assessment, dict):
            errors.append(f"证据画像 {profile} 缺少适用性判断")
            continue
        applicable = assessment.get("applicable")
        if not isinstance(applicable, bool):
            errors.append(f"证据画像 {profile} applicable 必须是布尔值")
        elif applicable != (profile in selected_profiles):
            errors.append(
                f"证据画像 {profile} 适用性与 evidence_profiles 不一致"
            )
        if not nonempty(assessment.get("reason")):
            errors.append(f"证据画像 {profile} 缺少选择或排除理由")

    required_check_ids = {
        check_id
        for profile in selected_profiles
        for check_id in EVIDENCE_PROFILES[profile]["required_checks"]
    }
    check_by_id: dict[str, dict[str, Any]] = {}
    required_checks = payload.get("required_evidence_checks")
    if not isinstance(required_checks, list):
        errors.append("required_evidence_checks 必须是数组")
        required_checks = []
    for index, check in enumerate(required_checks, start=1):
        if not isinstance(check, dict):
            errors.append(f"必查资料第 {index} 项不是对象")
            continue
        check_id = check.get("check_id")
        if not nonempty(check_id):
            errors.append(f"必查资料第 {index} 项缺少 check_id")
            continue
        if check_id not in EVIDENCE_CHECKS:
            errors.append(f"未知必查资料：{check_id}")
            continue
        if check_id in check_by_id:
            errors.append(f"必查资料 check_id 重复：{check_id}")
            continue
        check_by_id[check_id] = check

        rule = EVIDENCE_CHECKS[check_id]
        status = check.get("status")
        if status not in CHECK_STATUSES:
            errors.append(
                f"必查资料 {check_id} status 必须为 "
                + "、".join(sorted(CHECK_STATUSES))
            )
            continue
        if status == "not_applicable" and not rule["allow_not_applicable"]:
            errors.append(f"必查资料 {check_id} 不允许标记 not_applicable")
        if not nonempty(check.get("searched_at")) or not re.fullmatch(
            r"\d{4}-\d{2}-\d{2}", str(check.get("searched_at", ""))
        ):
            errors.append(f"必查资料 {check_id} 缺少 YYYY-MM-DD searched_at")
        if not nonempty(check.get("search_location")):
            errors.append(f"必查资料 {check_id} 缺少 search_location")
        queries = check.get("queries")
        query_kinds: set[str] = set()
        if not isinstance(queries, list) or not queries:
            errors.append(f"必查资料 {check_id} queries 必须是非空对象数组")
            queries = []
        for query_index, query in enumerate(queries, start=1):
            if not isinstance(query, dict):
                errors.append(
                    f"必查资料 {check_id} query 第 {query_index} 项必须是对象"
                )
                continue
            kind = query.get("kind")
            if kind not in QUERY_KINDS:
                errors.append(
                    f"必查资料 {check_id} query 第 {query_index} 项 kind 未登记"
                )
            else:
                query_kinds.add(kind)
            if not nonempty(query.get("text")):
                errors.append(
                    f"必查资料 {check_id} query 第 {query_index} 项缺少 text"
                )
        missing_query_kinds = set(rule.get("required_query_kinds", [])) - query_kinds
        if missing_query_kinds:
            errors.append(
                f"必查资料 {check_id} 缺少查询类型："
                + "、".join(sorted(missing_query_kinds))
            )

        source_ids = check.get("source_ids")
        if not isinstance(source_ids, list):
            errors.append(f"必查资料 {check_id} source_ids 必须是数组")
            source_ids = []
        if status == "read" and not source_ids:
            errors.append(f"必查资料 {check_id} 已读时必须引用 source_ids")
        allowed_types = set(rule["allowed_source_types"])
        for source_id in source_ids:
            source = source_by_id.get(source_id)
            if source is None:
                errors.append(
                    f"必查资料 {check_id} source_id 未命中资料范围：{source_id}"
                )
            elif source.get("source_type") not in allowed_types:
                errors.append(
                    f"必查资料 {check_id} 引用了不允许的来源类型："
                    f"{source.get('source_type')}"
                )

        if rule.get("requires_candidate_audit_for_not_found") and status in {"read", "not_found"}:
            receipt_ids = check.get("search_receipt_ids")
            if not isinstance(receipt_ids, list) or not receipt_ids:
                errors.append(f"必查资料 {check_id} 缺少 search_receipt_ids")
                receipt_ids = []
            receipt_results: dict[str, dict[str, Any]] = {}
            bound_receipt_query_pairs: set[tuple[Any, Any]] = set()
            check_query_pairs = {
                (item.get("kind"), item.get("text"))
                for item in queries
                if isinstance(item, dict)
            }
            for receipt_id in receipt_ids:
                receipt = receipt_by_id.get(receipt_id)
                if receipt is None:
                    errors.append(f"必查资料 {check_id} 检索回执不存在：{receipt_id}")
                    continue
                if receipt.get("check_id") != check_id:
                    errors.append(f"必查资料 {check_id} 检索回执 check_id 不匹配：{receipt_id}")
                receipt_query_pairs = {
                    (item.get("kind"), item.get("text"))
                    for item in receipt.get("queries", [])
                    if isinstance(item, dict)
                }
                bound_receipt_query_pairs.update(receipt_query_pairs)
                for result in receipt.get("results", []):
                    if isinstance(result, dict) and nonempty(result.get("id")):
                        receipt_results[result["id"]] = result
            if not check_query_pairs.issubset(bound_receipt_query_pairs):
                errors.append(f"必查资料 {check_id} 绑定检索回执未覆盖声明 queries")

            audit = check.get("candidate_audit")
            audited_candidates: dict[str, dict[str, Any]] = {}
            discovered_references: set[tuple[str, str]] = set()
            discovered_version_families: set[str] = set()
            if not isinstance(audit, dict):
                errors.append(f"必查资料 {check_id} 缺少候选文件审计")
            else:
                if audit.get("completed") is not True:
                    errors.append(f"必查资料 {check_id} 候选文件审计未完成")
                results_count = audit.get("results_count")
                if not isinstance(results_count, int) or results_count < 0:
                    errors.append(
                        f"必查资料 {check_id} candidate_audit.results_count 必须是非负整数"
                    )
                    results_count = 0
                candidates = audit.get("candidates")
                if not isinstance(candidates, list):
                    errors.append(
                        f"必查资料 {check_id} candidate_audit.candidates 必须是数组"
                    )
                    candidates = []
                if results_count != len(receipt_results):
                    errors.append(
                        f"必查资料 {check_id} 候选数量与检索回执不一致："
                        f"audit={results_count} receipts={len(receipt_results)}"
                    )
                candidate_ids: set[str] = set()
                for candidate_index, candidate in enumerate(candidates, start=1):
                    if not isinstance(candidate, dict):
                        errors.append(
                            f"必查资料 {check_id} 候选第 {candidate_index} 项不是对象"
                        )
                        continue
                    for field in ("id", "title", "url"):
                        if not nonempty(candidate.get(field)):
                            errors.append(
                                f"必查资料 {check_id} 候选第 {candidate_index} 项缺少 {field}"
                            )
                    candidate_id = candidate.get("id")
                    if nonempty(candidate_id):
                        if candidate_id in candidate_ids:
                            errors.append(f"必查资料 {check_id} 候选 id 重复：{candidate_id}")
                        candidate_ids.add(candidate_id)
                        audited_candidates[candidate_id] = candidate
                        if candidate_id not in receipt_results:
                            errors.append(f"必查资料 {check_id} 候选未命中检索回执：{candidate_id}")
                    disposition = candidate.get("disposition")
                    references = candidate.get("references")
                    if not isinstance(references, list):
                        errors.append(
                            f"必查资料 {check_id} 候选第 {candidate_index} 项 references 必须是数组"
                        )
                        references = []
                    for reference_index, reference in enumerate(references, start=1):
                        if not isinstance(reference, dict) or not nonempty(
                            reference.get("reference_text")
                        ):
                            errors.append(
                                f"必查资料 {check_id} 候选第 {candidate_index} 项引用第 "
                                f"{reference_index} 项缺少 reference_text"
                            )
                        elif nonempty(candidate_id):
                            discovered_references.add(
                                (candidate_id, reference["reference_text"].strip())
                            )
                    title = candidate.get("title")
                    version_family = candidate.get("version_family")
                    if nonempty(title) and VERSION_PATTERN.search(title):
                        if not nonempty(version_family):
                            errors.append(
                                f"必查资料 {check_id} 版本化候选第 {candidate_index} 项缺少 version_family"
                            )
                        else:
                            discovered_version_families.add(version_family.strip())
                    if disposition not in CANDIDATE_DISPOSITIONS:
                        errors.append(
                            f"必查资料 {check_id} 候选第 {candidate_index} 项 disposition 未登记"
                        )
                    elif disposition == "read":
                        candidate_sources = candidate.get("source_ids")
                        if not isinstance(candidate_sources, list) or not candidate_sources:
                            errors.append(
                                f"必查资料 {check_id} 已读候选第 {candidate_index} 项缺少 source_ids"
                            )
                        else:
                            for source_id in candidate_sources:
                                if source_id not in source_by_id:
                                    errors.append(
                                        f"必查资料 {check_id} 候选 source_id 未命中资料范围：{source_id}"
                                    )
                        if status == "not_found":
                            errors.append(
                                f"必查资料 {check_id} 存在已读候选，不能标记 not_found；"
                                "应改为 read 并另记规则缺口"
                            )
                    elif not nonempty(candidate.get("reason")):
                        errors.append(
                            f"必查资料 {check_id} 候选第 {candidate_index} 项 "
                            f"{disposition} 时缺少 reason"
                        )
                missing_candidates = set(receipt_results) - candidate_ids
                if missing_candidates:
                    errors.append(
                        f"必查资料 {check_id} 检索回执结果未逐项审计："
                        + "、".join(sorted(missing_candidates))
                    )

            completion = check.get("search_completion")
            if not isinstance(completion, dict):
                errors.append(f"必查资料 {check_id} 缺少检索闭环")
            else:
                if completion.get("completed") is not True:
                    errors.append(f"必查资料 {check_id} 检索闭环未完成")
                referenced_sources = completion.get("referenced_sources")
                if not isinstance(referenced_sources, list):
                    errors.append(
                        f"必查资料 {check_id} search_completion.referenced_sources 必须是数组"
                    )
                    referenced_sources = []
                completed_references: set[tuple[str, str]] = set()
                for reference_index, reference in enumerate(referenced_sources, start=1):
                    if not isinstance(reference, dict):
                        errors.append(f"必查资料 {check_id} 引用闭环第 {reference_index} 项不是对象")
                        continue
                    source_candidate_id = reference.get("source_candidate_id")
                    reference_text = reference.get("reference_text")
                    if not nonempty(source_candidate_id) or not nonempty(reference_text):
                        errors.append(
                            f"必查资料 {check_id} 引用闭环第 {reference_index} 项缺少来源候选或文档名"
                        )
                        continue
                    pair = (source_candidate_id, reference_text.strip())
                    completed_references.add(pair)
                    if pair not in discovered_references:
                        errors.append(f"必查资料 {check_id} 引用闭环未命中候选声明：{reference_text}")
                    reference_status = reference.get("status")
                    if reference_status not in REFERENCE_STATUSES:
                        errors.append(f"必查资料 {check_id} 引用文档状态未完成：{reference_text}")
                    reference_receipt_ids = reference.get("receipt_ids")
                    if reference_status in {"searched", "read"}:
                        if not isinstance(reference_receipt_ids, list) or not reference_receipt_ids:
                            errors.append(f"必查资料 {check_id} 引用文档缺少精确检索回执：{reference_text}")
                            reference_receipt_ids = []
                        exact_query_found = False
                        reference_result_ids: set[str] = set()
                        for reference_receipt_id in reference_receipt_ids:
                            if reference_receipt_id not in receipt_ids:
                                errors.append(
                                    f"必查资料 {check_id} 引用文档回执未绑定必查动作：{reference_receipt_id}"
                                )
                            reference_receipt = receipt_by_id.get(reference_receipt_id)
                            if reference_receipt is None or reference_receipt.get("check_id") != check_id:
                                continue
                            exact_query_found = exact_query_found or any(
                                item.get("kind") == "exact_document_name"
                                and item.get("text") == reference_text
                                for item in reference_receipt.get("queries", [])
                                if isinstance(item, dict)
                            )
                            reference_result_ids.update(
                                result.get("id")
                                for result in reference_receipt.get("results", [])
                                if isinstance(result, dict) and nonempty(result.get("id"))
                            )
                        if not exact_query_found:
                            errors.append(f"必查资料 {check_id} 引用文档未按完整名称检索：{reference_text}")
                        if reference_status == "read" and not any(
                            audited_candidates.get(result_id, {}).get("disposition") == "read"
                            for result_id in reference_result_ids
                        ):
                            errors.append(f"必查资料 {check_id} 引用文档标记 read 但无已读命中：{reference_text}")
                    elif not nonempty(reference.get("reason")):
                        errors.append(f"必查资料 {check_id} 引用文档 {reference_status} 时缺少 reason：{reference_text}")
                for source_candidate_id, reference_text in sorted(
                    discovered_references - completed_references
                ):
                    errors.append(
                        f"必查资料 {check_id} 候选 {source_candidate_id} 的引用文档未追查：{reference_text}"
                    )

                version_families = completion.get("version_families")
                if not isinstance(version_families, list):
                    errors.append(
                        f"必查资料 {check_id} search_completion.version_families 必须是数组"
                    )
                    version_families = []
                completed_families: set[str] = set()
                for family_index, family in enumerate(version_families, start=1):
                    if not isinstance(family, dict) or not nonempty(family.get("family")):
                        errors.append(f"必查资料 {check_id} 版本族第 {family_index} 项缺少 family")
                        continue
                    family_name = family["family"].strip()
                    completed_families.add(family_name)
                    if family_name not in discovered_version_families:
                        errors.append(f"必查资料 {check_id} 版本族未命中候选声明：{family_name}")
                    family_status = family.get("status")
                    if family_status not in VERSION_FAMILY_STATUSES:
                        errors.append(f"必查资料 {check_id} 版本族状态未完成：{family_name}")
                        continue
                    if family_status == "enumerated":
                        family_receipt_ids = family.get("receipt_ids")
                        if not isinstance(family_receipt_ids, list) or not family_receipt_ids:
                            errors.append(f"必查资料 {check_id} 版本族缺少枚举回执：{family_name}")
                            family_receipt_ids = []
                        family_result_ids: set[str] = set()
                        family_query_found = False
                        for family_receipt_id in family_receipt_ids:
                            if family_receipt_id not in receipt_ids:
                                errors.append(
                                    f"必查资料 {check_id} 版本族回执未绑定必查动作：{family_receipt_id}"
                                )
                            family_receipt = receipt_by_id.get(family_receipt_id)
                            if family_receipt is None or family_receipt.get("check_id") != check_id:
                                continue
                            family_query_found = family_query_found or any(
                                item.get("kind") == "version_family"
                                and item.get("text") == family_name
                                for item in family_receipt.get("queries", [])
                                if isinstance(item, dict)
                            )
                            family_result_ids.update(
                                result.get("id")
                                for result in family_receipt.get("results", [])
                                if isinstance(result, dict) and nonempty(result.get("id"))
                            )
                        if not family_query_found:
                            errors.append(f"必查资料 {check_id} 版本族未按系列名检索：{family_name}")
                        selected_candidate_id = family.get("selected_candidate_id")
                        selected = audited_candidates.get(selected_candidate_id)
                        if selected_candidate_id not in family_result_ids:
                            errors.append(f"必查资料 {check_id} 版本族选中文档未命中枚举回执：{family_name}")
                        if selected is None or selected.get("disposition") != "read":
                            errors.append(f"必查资料 {check_id} 版本族选中文档未审计为 read：{family_name}")
                        elif selected.get("version_family") != family_name:
                            errors.append(f"必查资料 {check_id} 版本族选中文档不属于该系列：{family_name}")
                        if not nonempty(family.get("selection_reason")):
                            errors.append(f"必查资料 {check_id} 版本族缺少版本选择理由：{family_name}")
                        if family.get("newer_version_checked") is not True:
                            errors.append(f"必查资料 {check_id} 版本族未确认无更新版本：{family_name}")
                    elif not nonempty(family.get("reason")):
                        errors.append(f"必查资料 {check_id} 版本族 {family_status} 时缺少 reason：{family_name}")
                for family_name in sorted(discovered_version_families - completed_families):
                    errors.append(f"必查资料 {check_id} 版本化候选未完成同系列枚举：{family_name}")

        if status in {"not_found", "unavailable", "not_applicable"}:
            if not nonempty(check.get("reason")):
                errors.append(f"必查资料 {check_id} {status} 时缺少 reason")
        if status in {"not_found", "unavailable"}:
            if not isinstance(check.get("material"), bool):
                errors.append(
                    f"必查资料 {check_id} {status} 时必须声明 material 布尔值"
                )
            material = check.get("material") is True
            if rule["missing_is_material"] and not material:
                errors.append(f"必查资料 {check_id} 缺失时必须标记 material=true")
                material = True
            if material:
                material_gap_ids.append(f"required:{check_id}")
                if not nonempty(check.get("next_action")):
                    errors.append(f"必查资料 {check_id} 关键缺口缺少 next_action")

    for check_id in sorted(required_check_ids - set(check_by_id)):
        errors.append(f"证据画像缺少必查资料：{check_id}")

    inheritance_by_id: dict[str, dict[str, Any]] = {}
    verified_inheritance_ids: set[str] = set()
    inheritance_chains = payload.get("inheritance_chains", [])
    if not isinstance(inheritance_chains, list):
        errors.append("inheritance_chains 必须是数组")
        inheritance_chains = []
    for index, chain in enumerate(inheritance_chains, start=1):
        if not isinstance(chain, dict):
            errors.append(f"继承链第 {index} 项不是对象")
            continue
        chain_id = chain.get("id")
        if not nonempty(chain_id):
            errors.append(f"继承链第 {index} 项缺少 id")
        elif chain_id in inheritance_by_id:
            errors.append(f"继承链 id 重复：{chain_id}")
        else:
            inheritance_by_id[chain_id] = chain
        for field in (
            "project_model",
            "function",
            "project_source_id",
            "definition_source_id",
            "reason",
        ):
            if not nonempty(chain.get(field)):
                errors.append(f"继承链第 {index} 项缺少 {field}")
        if not isinstance(chain.get("verified"), bool):
            errors.append(f"继承链第 {index} 项 verified 必须是布尔值")

        project_source = source_by_id.get(chain.get("project_source_id"))
        definition_source = source_by_id.get(chain.get("definition_source_id"))
        structurally_valid = True
        if project_source is None:
            errors.append(f"继承链第 {index} 项 project_source_id 未命中资料范围")
            structurally_valid = False
        elif not (
            project_source.get("role") == "context_only"
            and project_source.get("match") == "exact"
        ):
            errors.append(
                f"继承链第 {index} 项项目继承来源必须为 context_only + exact"
            )
            structurally_valid = False
        if definition_source is None:
            errors.append(f"继承链第 {index} 项 definition_source_id 未命中资料范围")
            structurally_valid = False
        elif not (
            definition_source.get("role") == "formal_target"
            and definition_source.get("match") == "partial"
        ):
            errors.append(
                f"继承链第 {index} 项被继承定义必须为 formal_target + partial"
            )
            structurally_valid = False
        if (
            structurally_valid
            and chain.get("verified") is True
            and nonempty(chain_id)
        ):
            verified_inheritance_ids.add(chain_id)

    valid_formal_ids: set[str] = set()
    valid_actual_ids: set[str] = set()
    for source_id, scope in source_by_id.items():
        role = scope.get("role")
        match = scope.get("match")
        if role == "formal_target":
            if (
                scope.get("source_type") in FORMAL_TARGET_ALLOWED_SOURCE_TYPES
                and match == "exact"
            ):
                valid_formal_ids.add(source_id)
            elif (
                scope.get("source_type") in FORMAL_TARGET_ALLOWED_SOURCE_TYPES
                and match == "partial"
            ):
                chain_id = scope.get("inheritance_chain_id")
                chain = inheritance_by_id.get(chain_id)
                if (
                    chain_id in verified_inheritance_ids
                    and chain
                    and chain.get("definition_source_id") == source_id
                ):
                    valid_formal_ids.add(source_id)
        elif role == "implementation_actual" and match == "exact":
            valid_actual_ids.add(source_id)

    if not nonempty(payload.get("conflict_resolution")):
        errors.append("缺少冲突处理")

    voice = payload.get("voice_evidence")
    voice_applicable = False
    voice_availability: str | None = None
    if not isinstance(voice, dict) or not isinstance(voice.get("applicable"), bool):
        errors.append("语音证据必须包含 applicable 布尔值")
    else:
        voice_applicable = voice["applicable"]
        if voice_applicable and "voice" not in selected_profiles:
            errors.append("语音问题必须选择 voice 证据画像")
        if "voice" in selected_profiles and not voice_applicable:
            errors.append("voice 证据画像必须声明 voice_evidence.applicable=true")
        if voice_applicable:
            voice_availability = voice.get("availability")
            if voice_availability not in VOICE_AVAILABILITY:
                errors.append(
                    "语音证据 availability 必须为 complete、partial 或 unavailable"
                )
            if not isinstance(voice.get("alchemy_tested"), bool):
                errors.append("语音证据 alchemy_tested 必须是布尔值")
            errors.extend(
                _validate_voice_function(
                    voice.get("standard_function"),
                    "standard_function",
                    allow_not_applicable=False,
                )
            )
            errors.extend(
                _validate_voice_function(
                    voice.get("project_function"),
                    "project_function",
                    allow_not_applicable=True,
                )
            )
            if voice_availability == "complete":
                if not nonempty(voice.get("original_utterance")):
                    errors.append("完整语音证据缺少 Jira 用户原话")
                if voice.get("alchemy_tested") is not True:
                    errors.append("完整语音证据必须完成 Alchemy 在线对话测试")
                if not nonempty(voice.get("alchemy_result")):
                    errors.append("完整语音证据缺少 Alchemy 当前结果")
                if not nonempty(voice.get("meta_id")):
                    errors.append("完整语音证据缺少 meta_id")
                if (
                    isinstance(voice.get("standard_function"), dict)
                    and voice["standard_function"].get("status") != "verified"
                ):
                    errors.append("完整语音证据必须读取标准功能点")
                if (
                    isinstance(voice.get("project_function"), dict)
                    and voice["project_function"].get("status")
                    not in {"verified", "not_applicable"}
                ):
                    errors.append(
                        "完整语音证据必须读取项目功能点，或核验后标记 not_applicable"
                    )
            elif voice_availability in {"partial", "unavailable"}:
                if not nonempty(voice.get("unavailable_reason")):
                    errors.append("语音证据不完整时缺少 unavailable_reason")
                if not nonempty(voice.get("next_action")):
                    errors.append("语音证据不完整时缺少 next_action")

    decision = payload.get("decision")
    if not isinstance(decision, dict):
        errors.append("缺少唯一结论")
    else:
        status = decision.get("status")
        if not nonempty(status):
            errors.append("唯一结论缺少 status")
        elif status not in SUPPORTED_STATUSES:
            errors.append(
                "唯一结论 status 必须为受支持的确定性状态或 "
                "待复核、待确认、待会诊"
            )
        if not nonempty(decision.get("owner")):
            errors.append("唯一结论缺少 owner")
        text = decision.get("text")
        if not nonempty(text):
            errors.append("唯一结论缺少 decision text")
        else:
            for label in ("结论：", "依据：", "处理："):
                if label not in text:
                    errors.append(f"decision text 缺少 {label}")
            if customer_case_missing:
                if status in CLOSURE_STATUSES:
                    errors.append("客户测试用例缺失或不完整时禁止关闭或判为非 Bug")
                if status != "待确认":
                    errors.append("客户测试用例缺失或不完整时状态必须降为待确认")
                if "客户测试用例" not in text:
                    errors.append("客户测试用例缺失时 decision text 必须写明收集动作")

        if status in {"可转语音", "转语音"} and not voice_applicable:
            errors.append("语音流转状态必须声明 voice_evidence.applicable=true")

        if status in DETERMINISTIC_STATUSES:
            expected_behavior = payload.get("expected_behavior")
            if not isinstance(expected_behavior, dict):
                errors.append("确定性结论缺少预期行为卡")
                target_refs: list[Any] = []
            else:
                for field in EXPECTED_BEHAVIOR_FIELDS:
                    if not nonempty(expected_behavior.get(field)):
                        errors.append(f"预期行为卡缺少 {field}")
                target_refs = expected_behavior.get("source_ids")
                if not isinstance(target_refs, list) or not target_refs:
                    errors.append("预期行为卡必须引用至少一条 formal_target")
                    target_refs = []
            if not valid_formal_ids:
                errors.append(
                    "确定性结论缺少有效 formal_target："
                    "仅 exact 或经核验继承链连接的 partial 定义可用"
                )
            for source_id in target_refs:
                if source_id not in valid_formal_ids:
                    errors.append(
                        f"预期行为卡引用的来源不是有效 formal_target：{source_id}"
                    )
            if any(
                EVIDENCE_PROFILES[profile].get("requires_product_formal_target")
                for profile in selected_profiles
            ) and not any(
                source_by_id.get(source_id, {}).get("source_type")
                in PRODUCT_FORMAL_SOURCE_TYPES
                for source_id in target_refs
            ):
                errors.append(
                    "确定性结论不能只依赖Alchemy功能点；"
                    "预期行为卡必须引用产品正式定义来源"
                )

            actual_refs = decision.get("implementation_source_ids")
            if not isinstance(actual_refs, list) or not actual_refs:
                errors.append("确定性结论必须引用 implementation_actual")
                actual_refs = []
            if not valid_actual_ids:
                errors.append(
                    "确定性结论缺少 exact 的 implementation_actual"
                )
            for source_id in actual_refs:
                if source_id not in valid_actual_ids:
                    errors.append(
                        f"唯一结论引用的来源不是有效 implementation_actual：{source_id}"
                    )

            if material_gap_ids:
                errors.append(
                    "存在会改变判断的关键 gap，状态必须降为待复核、待确认或待会诊："
                    + ", ".join(material_gap_ids)
                )
            if voice_applicable and voice_availability != "complete":
                errors.append(
                    "语音证据不完整时禁止确定性定责，状态必须降为"
                    "待复核、待确认或待会诊"
                )

    return errors


def validate_log(log_path: Path, expected_key: str | None = None) -> list[str]:
    """Return errors when an action log lacks the readable seven-field card."""

    if not log_path.is_file():
        return [f"日志不存在：{log_path}"]

    text = log_path.read_text(encoding="utf-8")
    errors: list[str] = []
    card_text = text
    if expected_key:
        keyed_heading = re.search(
            rf"^## .*\b{re.escape(expected_key)}\b.*决策核验卡\s*$",
            text,
            re.MULTILINE,
        )
        if keyed_heading:
            next_heading = re.search(
                r"^## ", text[keyed_heading.end() :], re.MULTILINE
            )
            end = (
                keyed_heading.end() + next_heading.start()
                if next_heading
                else len(text)
            )
            card_text = text[keyed_heading.start() : end]
        else:
            involved = re.search(r"^- 涉及 Jira：(.+)$", text, re.MULTILINE)
            involved_keys = (
                set(re.findall(r"\b[A-Z][A-Z0-9]+-\d+\b", involved.group(1)))
                if involved
                else set()
            )
            if len(involved_keys) > 1:
                errors.append(f"批量日志缺少 {expected_key} 独立决策核验卡")
            generic = re.search(r"^## 决策核验卡\s*$", text, re.MULTILINE)
            if generic:
                next_heading = re.search(
                    r"^## ", text[generic.end() :], re.MULTILINE
                )
                end = generic.end() + next_heading.start() if next_heading else len(text)
                card_text = text[generic.start() : end]
            else:
                errors.append("日志缺少决策核验卡标题")
    elif "决策核验卡" not in text:
        errors.append("日志缺少决策核验卡标题")
    for label in CARD_LABELS:
        if not re.search(rf"^- {re.escape(label)}：.+$", card_text, re.MULTILINE):
            errors.append(f"日志决策核验卡缺少 {label}")
    if expected_key and not re.search(rf"\b{re.escape(expected_key)}\b", text):
        errors.append(f"日志未包含目标 Jira key：{expected_key}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--key", help="需要与 manifest 或日志匹配的 Jira key")
    parser.add_argument("--log", help="只校验指定操作日志的决策核验卡")
    args = parser.parse_args()

    if args.log:
        errors = validate_log(Path(args.log), args.key)
    else:
        try:
            payload = json.load(sys.stdin)
        except json.JSONDecodeError as error:
            errors = [f"无法解析核验 JSON：{error.msg}"]
        else:
            errors = validate_manifest(payload, args.key)

    print(json.dumps({"ok": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
