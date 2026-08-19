#!/usr/bin/env python3
"""Build the SD-5269 Drive deep-recheck artifacts from the prior audited run."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
LOG_DIR = ROOT / "agent/logs/bug-actions"
OLD_PREFIX = "2026-08-19-SD-5269-comment-recheck"
NEW_PREFIX = "2026-08-19-SD-5269-drive-deep-recheck"
RUN_ID = "bug-20260819T-SD-5269-drive-deep-recheck"

JIRA_URL = "http://jira.i-tetris.com/browse/SD-5269"
VOICE_URL = "https://docs.google.com/spreadsheets/d/159bd_jBCou9dmXZNEH8y_cQQiMKmUj7rJoVHMl2d1SI/edit"
SYSTEM_URL = "https://drive.google.com/file/d/1HnHnqbq5CV5I0LqB9ShbP9hve7J_mPO3/view"

INFO = (
    "Jira：评论询问无主体指令‘把音量调到50%’究竟调哪个音量。"
    "Drive：最新正式语料清单逐字命中泰语，分类为系统设置/声音/无指定通道百分比调节；"
    "系统设置功能定义V5.1明确‘音量调大调小，根据当前的音源焦点进行调节’，并分别定义媒体、通话、导航、智能语音通道，未定义全局/默认音量。"
    "Alchemy：当前误落1146小憩模式时长，与音量目标不符。资料：Jira原票 / 最新正式语料清单 / 系统设置V5.1。"
)
DECISION = (
    "结论：无主体的百分比音量指令按当前音源焦点对应通道执行；当前焦点为媒体、通话、导航或智能语音时，将对应通道调到50%。"
    "不是全局同时调多个通道，也不是固定的‘默认音量’。当前BIGSUR误映射到1146小憩模式时长，属于泰语NLU映射缺陷。\n"
    "依据：最新正式语料清单将原话归为‘无指定通道百分比调节’；系统设置V5.1规定无主体音量调节按当前音源焦点，并逐项定义四类可调通道。\n"
    "处理：恢复到音量百分比调节意图，并按当前音源焦点落对应通道；清除1146错误竞争。语音NLU/泰语算法负责人处理。\n"
    "资料：Jira原票 / 最新正式语料清单 / 系统设置V5.1。"
)
NOTE = (
    "经办人：吴优；2026-08-19 Drive深查复核；已纠正‘全局/默认音量’过度解释；"
    "正式规则为按当前音源焦点对应通道调到50%；责任方：语音NLU/泰语算法负责人；未评论/转派/关闭Jira。"
)


def load(name: str) -> dict:
    return json.loads((LOG_DIR / name).read_text(encoding="utf-8"))


def dump(name: str, payload: dict) -> None:
    (LOG_DIR / name).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


manifest = copy.deepcopy(load(f"{OLD_PREFIX}-manifest.json"))
manifest["comment_causality"] = (
    "聂汉维评论询问无主体指令‘把音量调到50%’究竟调哪个音量；本次补读Drive最新正式语料清单和系统设置V5.1后，纠正此前‘全局/默认音量’的过度解释。"
)
manifest["scope_checks"][1].update(
    {
        "source_id": "drive-latest-voice-list",
        "source": "【正式版】长安系_海外各国语料清单汇总_V0.3.2.11",
        "source_location": "深蓝-删减版，表格行605/序号439；正文已读",
        "target_behavior": "原话归类为系统设置/声音/无指定通道百分比调节；C673-G、D587-G均支持。",
        "reason": "当前检索到的最新正式海外语音能力清单。",
    }
)
manifest["scope_checks"].insert(
    2,
    {
        "source_id": "drive-system-settings-v5.1",
        "source": "C673_功能定义_系统设置功能定义V5.1.pdf",
        "source_location": "3.3语音及4.7.8-4.7.11音量调节正文；正文已读",
        "source_type": "prd",
        "role": "formal_target",
        "project_model": "C673",
        "trigger": "无主体音量调节",
        "target_behavior": "音量调节按当前音源焦点；可调通道分别为媒体、通话、导航、智能语音。",
        "match": "exact",
        "reason": "定义无主体音量调节的通道选择规则；未定义全局/默认音量。",
    },
)
check = manifest["required_evidence_checks"][0]
check["source_ids"] = ["drive-latest-voice-list", "drive-system-settings-v5.1"]
check["searched_at"] = "2026-08-19"
check["search_location"] = "Google Drive实时检索；逐字原话、完整文档名和版本族均已追查并读取最新适用正文"
check["queries"] = [
    {"kind": "jira_key", "text": "SD-5269"},
    {"kind": "problem_concept", "text": "无指定通道 音量 当前音源焦点"},
    {"kind": "module_artifact", "text": "C673 系统设置 声音 语音"},
    {"kind": "exact_document_name", "text": "C673_功能定义_系统设置功能定义V5.1.pdf"},
    {"kind": "version_family", "text": "C673_功能定义_系统设置功能定义"},
    {"kind": "version_family", "text": "C673_功能定义_音频策略功能定义"},
    {"kind": "version_family", "text": "【正式版】长安系_海外各国语料清单汇总"},
]
check["search_receipt_ids"] = ["SD-5269-drive-deep-recheck-20260819"]
check["candidate_audit"] = {
    "completed": True,
    "results_count": 3,
    "candidates": [
        {
            "id": "159bd_jBCou9dmXZNEH8y_cQQiMKmUj7rJoVHMl2d1SI",
            "title": "【正式版】长安系_海外各国语料清单汇总_V0.3.2.11",
            "url": VOICE_URL,
            "disposition": "read",
            "source_ids": ["drive-latest-voice-list"],
            "references": [],
            "version_family": "【正式版】长安系_海外各国语料清单汇总",
        },
        {
            "id": "1HnHnqbq5CV5I0LqB9ShbP9hve7J_mPO3",
            "title": "C673_功能定义_系统设置功能定义V5.1.pdf",
            "url": SYSTEM_URL,
            "disposition": "read",
            "source_ids": ["drive-system-settings-v5.1"],
            "references": [],
            "version_family": "C673_功能定义_系统设置功能定义",
        },
        {
            "id": "1jOcQXhtLxBVX93-q81XIMJ11QtjKqgkx",
            "title": "C673_功能定义_音频策略功能定义V0.6.docx",
            "url": "https://docs.google.com/document/d/1jOcQXhtLxBVX93-q81XIMJ11QtjKqgkx/edit",
            "disposition": "read",
            "source_ids": ["drive-system-settings-v5.1"],
            "references": [],
            "reason": "已读音源/通道定义；未发现把无主体指令定义为全局/默认音量。",
            "version_family": "C673_功能定义_音频策略功能定义",
        },
    ],
}
check["search_completion"] = {
    "completed": True,
    "referenced_sources": [],
    "version_families": [
        {
            "family": "C673_功能定义_系统设置功能定义",
            "status": "enumerated",
            "receipt_ids": ["SD-5269-drive-deep-recheck-20260819"],
            "selected_candidate_id": "1HnHnqbq5CV5I0LqB9ShbP9hve7J_mPO3",
            "selection_reason": "已枚举V0.1至V5.1并读取最新可见适用版本V5.1。",
            "newer_version_checked": True,
        },
        {
            "family": "【正式版】长安系_海外各国语料清单汇总",
            "status": "enumerated",
            "receipt_ids": ["SD-5269-drive-deep-recheck-20260819"],
            "selected_candidate_id": "159bd_jBCou9dmXZNEH8y_cQQiMKmUj7rJoVHMl2d1SI",
            "selection_reason": "已比较0723、0803、0805及0807正式版，选择最新正式版。",
            "newer_version_checked": True,
        },
        {
            "family": "C673_功能定义_音频策略功能定义",
            "status": "enumerated",
            "receipt_ids": ["SD-5269-drive-deep-recheck-20260819"],
            "selected_candidate_id": "1jOcQXhtLxBVX93-q81XIMJ11QtjKqgkx",
            "selection_reason": "已枚举V0.1至V0.6并读取最新可见适用版本V0.6。",
            "newer_version_checked": True,
        },
    ],
}
manifest["expected_behavior"] = {
    "trigger": "ตั้งระดับเสียง 50 เปอร์เซ็นต์",
    "target_state": "按当前音源焦点对应的媒体、通话、导航或智能语音通道调到50%。",
    "intent_function_signal": "音量百分比调节；1146为错误的小憩模式时长竞争",
    "ui_tts_vehicle_behavior": "只调整当前音源焦点对应通道，不做全局多通道同时调整，也不使用固定默认通道。",
    "boundary": "C673-G3/G5，BIGSUR及对应海外语种",
    "source_ids": ["drive-latest-voice-list", "drive-system-settings-v5.1"],
    "comment_answer": "无主体时按当前音源焦点：媒体、通话、导航或智能语音当前谁持有焦点，就把对应通道调到50%。",
}
manifest["conflict_resolution"] = (
    "最新正式语料清单证明该原话属于无指定通道百分比调节；系统设置V5.1进一步规定无主体音量调节按当前音源焦点。"
    "因此纠正此前‘全局/默认音量’表述；当前误命中1146仍为泰语NLU映射缺陷。"
)
manifest["decision"] = {
    "status": "转语音",
    "owner": "语音NLU/泰语算法负责人",
    "implementation_source_ids": ["jira-actual", "alchemy-current"],
    "text": DECISION.rsplit("\n资料：", 1)[0],
}
manifest["run_context"].update(
    {
        "run_id": RUN_ID,
        "jira_timeline_read_at": "2026-08-19",
        "jira_comment_answered": True,
    }
)
manifest["search_receipts"].append(
    {
        "receipt_id": "SD-5269-drive-deep-recheck-20260819",
        "provider": "google_drive",
        "check_id": "formal_definition_search",
        "searched_at": "2026-08-19T16:00:00+08:00",
        "queries": check["queries"],
        "results": [
            {"id": "159bd_jBCou9dmXZNEH8y_cQQiMKmUj7rJoVHMl2d1SI", "title": "【正式版】长安系_海外各国语料清单汇总_V0.3.2.11", "url": VOICE_URL, "mime_type": "application/vnd.google-apps.spreadsheet"},
            {"id": "1HnHnqbq5CV5I0LqB9ShbP9hve7J_mPO3", "title": "C673_功能定义_系统设置功能定义V5.1.pdf", "url": SYSTEM_URL, "mime_type": "application/pdf"},
            {"id": "1jOcQXhtLxBVX93-q81XIMJ11QtjKqgkx", "title": "C673_功能定义_音频策略功能定义V0.6.docx", "url": "https://docs.google.com/document/d/1jOcQXhtLxBVX93-q81XIMJ11QtjKqgkx/edit", "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"},
        ],
    }
)
dump(f"{NEW_PREFIX}-manifest.json", manifest)

old_patch = load(f"{OLD_PREFIX}-patch-input.json")
patch_input = {
    "current_row": old_patch["current_row"],
    "changes": {
        "C": {"text": INFO, "links": [
            {"label": "Jira原票", "url": JIRA_URL},
            {"label": "最新正式语料清单", "url": VOICE_URL},
            {"label": "系统设置V5.1", "url": SYSTEM_URL},
        ]},
        "D": {"text": DECISION, "links": [
            {"label": "Jira原票", "url": JIRA_URL},
            {"label": "最新正式语料清单", "url": VOICE_URL},
            {"label": "系统设置V5.1", "url": SYSTEM_URL},
        ]},
        "G": "转语音",
        "I": NOTE,
        "J": {"links": [
            {"label": "Jira原票", "url": JIRA_URL},
            {"label": "最新正式语料清单", "url": VOICE_URL},
            {"label": "系统设置V5.1", "url": SYSTEM_URL},
        ]},
    },
}
dump(f"{NEW_PREFIX}-patch-input.json", patch_input)

log = f"""# SD-5269 Drive深查复核日志

- run_id：{RUN_ID}
- 日期：2026-08-19
- 负责人：吴优
- 线上清单：吴优工作说明 / bug / 第61行
- 更新模式：recheck，仅更新 C/D/G/I/J；A/B/E/F/H 保护
- Jira外部动作：未执行评论、转派、关闭或状态变更
- Drive深查：已检索泰语原话、中文概念、完整文档名、Jira Key及版本族；读取最新正式语料清单、系统设置V5.1、音频策略V0.6
- 评论答案：无主体时按当前音源焦点对应通道调到50%；不是全局/默认音量
- 结论：转语音；当前1146小憩时长为错误竞争，责任方为语音NLU/泰语算法负责人

## SD-5269 决策核验卡

- 备注因果链：评论询问无主体时具体调哪个音量；Drive系统设置V5.1明确按当前音源焦点。
- 客户问题识别：否
- 关联票：SD-5268、SD-5309 已读取
- 证据画像与必查资料：voice；Jira完整时间线、Drive最新正式语料清单、系统设置V5.1、音频策略V0.6、Alchemy当前/标准/项目功能点
- 资料适用范围：正式语料清单定义能力覆盖；系统设置V5.1定义通道选择规则；Alchemy证明当前错误实现
- 冲突处理：纠正此前‘全局/默认音量’过度解释，以当前音源焦点作为执行对象
- 唯一结论：状态=转语音；责任方=语音NLU/泰语算法负责人；按当前音源焦点落对应通道并清除1146竞争
- 表格位置：bug!A61:J61，SD-5269 行61。
"""
(LOG_DIR / f"{NEW_PREFIX}.md").write_text(log, encoding="utf-8")

run = {
    "schema_version": 1,
    "run_id": RUN_ID,
    "started_at": "2026-08-19T16:00:00+08:00",
    "status": "planned",
    "query_summary": "补查Drive完整定义并纠正SD-5269第61行无主体音量对象。",
    "action_log": f"agent/logs/bug-actions/{NEW_PREFIX}.md",
    "items": [
        {
            "jira_key": "SD-5269",
            "operator_owner_id": "wu-you",
            "target_owner_id": "wu-you",
            "sheet_name": "bug",
            "sheet_row": 61,
            "manifest_path": f"agent/logs/bug-actions/{NEW_PREFIX}-manifest.json",
        }
    ],
}
dump(f"{NEW_PREFIX}-run.json", run)

contract = subprocess.run(
    [
        sys.executable,
        str(ROOT / "agent/scripts/bug_sheet_contract.py"),
        "patch",
        "--sheet-id", "2135747181",
        "--row-number", "61",
        "--key", "SD-5269",
        "--owner-id", "wu-you",
        "--mode", "recheck",
        "--preview-fingerprint", "23d79634390f487422c215c8b898a5aea8a6a52601823ea5f02e4d57d68ff5de",
        "--manifest", str(LOG_DIR / f"{NEW_PREFIX}-manifest.json"),
        "--run-bundle", str(LOG_DIR / f"{NEW_PREFIX}-run.json"),
    ],
    input=json.dumps(patch_input, ensure_ascii=False),
    text=True,
    capture_output=True,
    check=True,
    cwd=ROOT,
)
dump(f"{NEW_PREFIX}-requests.json", json.loads(contract.stdout))
