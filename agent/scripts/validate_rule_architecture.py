#!/usr/bin/env python3
"""Validate the active Bug rule architecture without modifying the workspace."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path


REQUIRED_FILES = (
    "AGENTS.md",
    "README.md",
    "agent/onboarding.md",
    "agent/rules-version.md",
    "agent/evidence-contract.md",
    "agent/output-contract.md",
    "agent/workflows/bug.md",
    "agent/workflows/review.md",
    "agent/sheet-contract.md",
    "agent/context.md",
    "agent/bug-owners/registry.yaml",
    "agent/config/evidence-requirements.json",
    "agent/config/external-skills.json",
    "agent/config/sheet-update-modes.json",
    "agent/config/local-profile.example.json",
    "agent/skills/deepal-product-bug-handler/SKILL.md",
    "agent/scripts/bug_sheet_contract.py",
    "agent/scripts/bug_project_preflight.py",
    "agent/scripts/validate_bug_evidence_gate.py",
    "agent/scripts/validate_bug_run.py",
    "agent/scripts/sync_bug_skill.py",
    "agent/scripts/test_bug_evidence_gate.py",
    "agent/scripts/test_bug_run.py",
    "agent/scripts/test_bug_sheet_contract.py",
    "agent/scripts/test_bug_project_preflight.py",
)

AUTHORITY_REFERENCES = (
    "agent/evidence-contract.md",
    "agent/output-contract.md",
    "agent/workflows/bug.md",
    "agent/workflows/review.md",
    "agent/sheet-contract.md",
    "agent/config/evidence-requirements.json",
    "agent/config/sheet-update-modes.json",
    "agent/skills/deepal-product-bug-handler/SKILL.md",
    "agent/bug-owners/registry.yaml",
    "agent/rules-version.md",
    "agent/onboarding.md",
)

COMPATIBILITY_FILES = (
    "agent/workflow.md",
    "agent/meeting-feedback-workflow.md",
    "agent/sheet-template.md",
    "agent/sheet-style.md",
    "agent/bug-index.md",
    "agent/li-xin-bug-index.md",
)

DECISION_GATE_LABELS = (
    "备注因果链",
    "客户问题识别",
    "关联票",
    "证据画像与必查资料",
    "资料适用范围",
    "冲突处理",
    "唯一结论",
)

OPERATIONAL_SCRIPT_ALLOWLIST = {
    "bug_sheet_contract.py",
    "bug_project_preflight.py",
    "sync_bug_skill.py",
    "test_bug_evidence_gate.py",
    "test_bug_run.py",
    "test_bug_sheet_contract.py",
    "test_bug_project_preflight.py",
    "validate_bug_evidence_gate.py",
    "validate_bug_run.py",
    "validate_rule_architecture.py",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate(root: Path, skill: Path) -> list[str]:
    errors: list[str] = []

    if not (root / ".git").is_dir():
        errors.append("工作区尚未初始化 Git 仓库")

    gitignore_path = root / ".gitignore"
    if not gitignore_path.is_file():
        errors.append("缺少 .gitignore")
    else:
        gitignore = read(gitignore_path)
        for pattern in (
            ".env",
            ".mastergo/",
            ".DS_Store",
            "__pycache__/",
            "agent/config/local-profile.json",
        ):
            if pattern not in gitignore:
                errors.append(f".gitignore 缺少安全模式：{pattern}")

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"缺少权威文件：{relative}")

    scripts_path = root / "agent/scripts"
    operational_scripts = {
        path.name for path in scripts_path.glob("*.py") if path.is_file()
    }
    unexpected_scripts = operational_scripts - OPERATIONAL_SCRIPT_ALLOWLIST
    if unexpected_scripts:
        errors.append(
            "agent/scripts 含未登记或一次性脚本："
            + "、".join(sorted(unexpected_scripts))
        )

    version_path = root / "agent/rules-version.md"
    version_text = read(version_path) if version_path.exists() else ""
    match = re.search(r"^- 当前版本：`([^`]+)`$", version_text, re.MULTILINE)
    if not match:
        errors.append("rules-version.md 缺少唯一当前版本")

    agents_text = read(root / "AGENTS.md")
    for reference in AUTHORITY_REFERENCES:
        if reference not in agents_text:
            errors.append(f"AGENTS.md 未登记权威入口：{reference}")
    for token in (
        "agent/config/local-profile.json",
        "agent/onboarding.md",
        "agent/scripts/bug_project_preflight.py",
        "不得根据电脑用户名",
    ):
        if token not in agents_text:
            errors.append(f"AGENTS.md 缺少团队身份门禁：{token}")

    registry_text = read(root / "agent/bug-owners/registry.yaml")
    wu_you_block = re.search(
        r'  - id: "wu-you"(?P<body>.*?)(?=\n  - id:|\Z)',
        registry_text,
        re.DOTALL,
    )
    if not wu_you_block or not re.search(
        r"^    format_anchor_row:\s*107\s*$",
        wu_you_block.group("body") if wu_you_block else "",
        re.MULTILINE,
    ):
        errors.append("吴优 bug 页固定格式锚点必须登记为第 107 行")

    for relative in (
        "AGENTS.md",
        "agent/evidence-contract.md",
        "agent/output-contract.md",
        "agent/workflows/bug.md",
        "agent/sheet-contract.md",
    ):
        text = read(root / relative)
        if re.search(r"(?:当前规则版本|规则版本)：`v\d", text):
            errors.append(f"{relative} 重复维护了具体版本号")

    for relative in COMPATIBILITY_FILES:
        path = root / relative
        if not path.is_file():
            errors.append(f"缺少兼容入口：{relative}")
            continue
        text = read(path)
        if "只保留旧路径兼容" not in text:
            errors.append(f"兼容入口含义不明确：{relative}")

    canonical_skill_path = (
        root / "agent/skills/deepal-product-bug-handler/SKILL.md"
    )
    canonical_skill_text = (
        read(canonical_skill_path) if canonical_skill_path.is_file() else ""
    )
    if not skill.is_file():
        errors.append(f"缺少已安装 Skill：{skill}")
        skill_text = ""
    else:
        skill_text = read(skill)
    if skill_text != canonical_skill_text:
        errors.append("已安装 Skill 与 Git 内唯一模板不一致")
    for reference in (
        "agent/onboarding.md",
        "agent/evidence-contract.md",
        "agent/output-contract.md",
        "agent/sheet-contract.md",
        "agent/workflows/bug.md",
    ):
        if reference not in skill_text:
            errors.append(f"Skill 未加载权威入口：{reference}")
    if "/Users/you.wu" in canonical_skill_text:
        errors.append("Skill 模板仍包含吴优电脑绝对路径")
    for old_heading in (
        "## Execute The Bug Flow",
        "## Query External Evidence",
        "## Return Concise Results",
    ):
        if old_heading in skill_text:
            errors.append(f"Skill 仍复制业务规则：{old_heading}")

    sheet_script = read(root / "agent/scripts/bug_sheet_contract.py")
    if "def linked_formula" in sheet_script:
        errors.append("写表脚本仍包含旧多 HYPERLINK 生成器")
    if "link_list_cell(links)" not in sheet_script:
        errors.append("写表脚本未使用富文本链接列表")
    for token in (
        "def build_patch_requests",
        "def validate_patch_readback",
        "def validate_append_readback",
        "def validate_bound_manifests",
        "UPDATE_MODES_PATH",
        "--manifest",
        "--run-bundle",
        "--row-number",
        "--preview-fingerprint",
        '"fields": "userEnteredValue,textFormatRuns"',
        "validate_local_write_gate",
        "--owner-id",
        "resolve_format_source_row_index",
        "validate_append_format",
        "DEFAULT_FORMAT_ANCHOR_ROW = 107",
    ):
        if token not in sheet_script:
            errors.append(f"写表脚本缺少已有行安全更新能力：{token}")

    modes_path = root / "agent/config/sheet-update-modes.json"
    if modes_path.is_file():
        try:
            modes_payload = json.loads(read(modes_path))
            modes = modes_payload["modes"]
            expected_modes = {
                "recheck": {
                    "allowed_columns": ["C", "D", "G", "I", "J"],
                    "protected_columns": ["A", "B", "E", "F", "H"],
                },
                "review": {
                    "allowed_columns": ["G", "H", "I", "J"],
                    "protected_columns": ["A", "B", "C", "D", "E", "F"],
                },
            }
            for mode, expected in expected_modes.items():
                if mode not in modes:
                    errors.append(f"更新模式配置缺少：{mode}")
                    continue
                for field, value in expected.items():
                    if modes[mode].get(field) != value:
                        errors.append(f"更新模式配置错误：{mode}.{field}")
        except (KeyError, TypeError, json.JSONDecodeError):
            errors.append("sheet-update-modes.json 无法解析")

    external_skills_path = root / "agent/config/external-skills.json"
    if external_skills_path.is_file():
        try:
            external_skills = json.loads(read(external_skills_path))
            audit_skill = next(
                skill
                for skill in external_skills["skills"]
                if skill.get("name") == "audit-ue-voice-coverage"
            )
            if external_skills.get("schema_version") != 1:
                errors.append("external-skills.json schema_version 必须为 1")
            if audit_skill.get("visibility") != "private":
                errors.append("UE 语音覆盖 Skill 必须使用私有仓库")
            if not re.fullmatch(r"v\d+\.\d+\.\d+", audit_skill.get("version", "")):
                errors.append("UE 语音覆盖 Skill 缺少独立语义版本")
            if not re.fullmatch(r"[0-9a-f]{40}", audit_skill.get("commit", "")):
                errors.append("UE 语音覆盖 Skill 缺少精确提交锁定")
            if "audit-ue-voice-coverage" not in audit_skill.get("repository", ""):
                errors.append("UE 语音覆盖 Skill 仓库地址无效")
        except (KeyError, StopIteration, TypeError, json.JSONDecodeError):
            errors.append("external-skills.json 无法解析或缺少 UE 语音覆盖 Skill")

    onboarding = read(root / "agent/onboarding.md")
    for token in (
        "私有仓库",
        "--list-owners",
        "--init-owner",
        "sync_bug_skill.py --install",
        "--mark-access",
        "--require-owner",
        "--require-platform",
        "Token",
    ):
        if token not in onboarding:
            errors.append(f"首次运行引导缺少：{token}")

    preflight_script = read(root / "agent/scripts/bug_project_preflight.py")
    for token in (
        "local-profile.json",
        "allowed_write_owner_ids",
        "live_read_verified_by_agent",
        "mode",
        "read_only",
        "Path.home()",
        "local_secret_file_status",
    ):
        if token not in preflight_script:
            errors.append(f"本机预检脚本缺少：{token}")
    if re.search(r"gh[pousr]_[A-Za-z0-9_]+", preflight_script):
        errors.append("本机预检脚本疑似包含GitHub凭据")

    sync_skill_script = read(root / "agent/scripts/sync_bug_skill.py")
    if "/Users/you.wu" in sync_skill_script:
        errors.append("Skill同步脚本仍包含吴优电脑绝对路径")
    for token in ("CODEX_HOME", "Path.home()"):
        if token not in sync_skill_script:
            errors.append(f"Skill同步脚本缺少可移植路径：{token}")

    evidence_requirements_path = root / "agent/config/evidence-requirements.json"
    if evidence_requirements_path.is_file():
        try:
            requirements = json.loads(read(evidence_requirements_path))
            if requirements.get("schema_version") != 1:
                errors.append("证据配置 schema_version 必须为 1")
            if requirements.get("manifest_schema_version") != 5:
                errors.append("证据配置 manifest_schema_version 必须为 5")

            query_kinds = set(requirements["query_kinds"])
            candidate_dispositions = set(requirements["candidate_dispositions"])
            if not query_kinds:
                errors.append("证据配置 query_kinds 不能为空")
            if not {"exact_document_name", "version_family"} <= query_kinds:
                errors.append("证据配置缺少引用文档或版本族查询类型")
            if candidate_dispositions != {"read", "excluded", "unavailable"}:
                errors.append("证据配置 candidate_dispositions 不完整")

            source_types = set(requirements["source_types"])
            formal_types = set(requirements["formal_target_allowed_source_types"])
            product_formal_types = set(requirements["product_formal_source_types"])
            if not source_types:
                errors.append("证据配置 source_types 不能为空")
            if not formal_types <= source_types:
                errors.append("formal_target_allowed_source_types 含未登记来源类型")
            if not product_formal_types <= formal_types:
                errors.append("product_formal_source_types 必须是 formal target 类型子集")

            statuses = set(requirements["check_statuses"])
            required_statuses = {"read", "not_found", "unavailable", "not_applicable"}
            if statuses != required_statuses:
                errors.append("证据配置 check_statuses 不完整")

            checks = requirements["checks"]
            profiles = requirements["profiles"]
            if not checks or not profiles:
                errors.append("证据配置 checks 和 profiles 不能为空")
            for check_id, check in checks.items():
                allowed_types = set(check.get("allowed_source_types", []))
                if not allowed_types or not allowed_types <= source_types:
                    errors.append(f"证据必查动作来源类型错误：{check_id}")
                if not isinstance(check.get("missing_is_material"), bool):
                    errors.append(f"证据必查动作缺少 material 定义：{check_id}")
                required_query_kinds = set(check.get("required_query_kinds", []))
                if not required_query_kinds:
                    errors.append(f"证据必查动作缺少检索维度：{check_id}")
                elif not required_query_kinds <= query_kinds:
                    errors.append(f"证据必查动作引用未知检索维度：{check_id}")
                if not isinstance(
                    check.get("requires_candidate_audit_for_not_found"), bool
                ):
                    errors.append(f"证据必查动作缺少候选审计定义：{check_id}")
            for profile_id, profile in profiles.items():
                check_ids = profile.get("required_checks", [])
                if not check_ids:
                    errors.append(f"证据画像没有必查动作：{profile_id}")
                for check_id in check_ids:
                    if check_id not in checks:
                        errors.append(f"证据画像引用未知必查动作：{profile_id}.{check_id}")
        except (KeyError, TypeError, json.JSONDecodeError):
            errors.append("evidence-requirements.json 无法解析")

    bug_workflow = read(root / "agent/workflows/bug.md")
    review_workflow = read(root / "agent/workflows/review.md")
    sheet_contract = read(root / "agent/sheet-contract.md")
    if "sheet-update-modes.json` 的 `recheck`" not in bug_workflow:
        errors.append("Bug 流程未消费 recheck 更新模式")
    if "sheet-update-modes.json` 的 `review`" not in review_workflow:
        errors.append("复盘流程未消费 review 更新模式")
    for token in ("`普通二次复查 / recheck`", "`会议/复盘 / review`"):
        if token not in sheet_contract:
            errors.append(f"表格契约缺少已有行模式：{token}")

    dashboard_token = "Dashboard.jspa?selectPageId=17302"
    if dashboard_token not in read(root / "agent/context.md"):
        errors.append("context.md 缺少 Bug 清单 Dashboard 17302")
    if "Jira Dashboard 17302" not in read(root / "agent/workflows/bug.md"):
        errors.append("Bug 流程未定义 Bug 清单入口")

    evidence_contract = read(root / "agent/evidence-contract.md")
    for token in (
        "决策核验卡",
        "备注因果链",
        "客户问题识别",
        "客户提报 Bug 与测试用例门槛",
        "客户测试用例",
        "关联票",
        "资料适用范围",
        "冲突处理",
        "唯一结论",
        "evidence-requirements.json",
        "evidence_profiles",
        "required_evidence_checks",
        "source_type",
        "validate_bug_evidence_gate.py",
    ):
        if token not in evidence_contract:
            errors.append(f"证据契约缺少决策核验字段：{token}")

    for token in (
        "问题链接",
        "客户问题编号",
        "客户测试用例",
        "关联票",
        "evidence-requirements.json",
        "validate_bug_evidence_gate.py",
    ):
        if token not in bug_workflow:
            errors.append(f"Bug 流程缺少关联票决策关口：{token}")

    for token in ("evidence-requirements.json", "validate_bug_evidence_gate.py"):
        if token not in review_workflow:
            errors.append(f"复盘流程缺少统一证据门槛：{token}")

    gate_script = read(root / "agent/scripts/validate_bug_evidence_gate.py")
    for token in (
        "customer_issue",
        "evidence_profile_assessment",
        "evidence_profiles",
        "required_evidence_checks",
        "required_query_kinds",
        "candidate_audit",
        "search_receipts",
        "search_receipt_ids",
        "run_context",
        "source_type",
        "客户问题识别",
        "客户测试用例缺失或不完整时禁止关闭或判为非 Bug",
    ):
        if token not in gate_script:
            errors.append(f"决策校验脚本缺少客户问题门槛：{token}")

    log_readme = read(root / "agent/logs/bug-actions/README.md")
    for token in ("决策核验卡", *DECISION_GATE_LABELS):
        if token not in log_readme:
            errors.append(f"操作日志规范缺少决策核验字段：{token}")
    if "## PC-12345 决策核验卡" not in log_readme:
        errors.append("操作日志规范未要求批量任务按 Jira 分卡")
    for token in ("Run ID", "run bundle", "无新增", "readback_sha256"):
        if token not in log_readme:
            errors.append(f"操作日志规范缺少运行闭环字段：{token}")

    comment_signals = read(root / "agent/product-kb/rules/jira-comment-signals.md")
    if "agent/evidence-contract.md" not in comment_signals:
        errors.append("评论信号库未指向证据契约")
    for duplicated_heading in ("研发评论的证据权重", "双轴判断顺序"):
        if duplicated_heading in comment_signals:
            errors.append(f"评论信号库仍复制证据规则：{duplicated_heading}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parents[2]),
        help="Bug workspace root",
    )
    parser.add_argument(
        "--skill",
        default=str(
            (
                Path(os.environ["CODEX_HOME"]).expanduser()
                if os.environ.get("CODEX_HOME")
                else Path.home() / ".codex"
            )
            / "skills/deepal-product-bug-handler/SKILL.md"
        ),
        help="Skill entrypoint",
    )
    args = parser.parse_args()

    errors = validate(Path(args.root).resolve(), Path(args.skill).resolve())
    print(json.dumps({"ok": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
