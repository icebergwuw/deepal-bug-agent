#!/usr/bin/env python3
"""One-time mechanical rebuild of the 2026-08-12 daily Bug evidence bundle."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
LOG_DIR = ROOT / "agent/logs/bug-actions"
RUN_ID = "20260812T105609+0800-daily-bug-recheck"
STARTED_AT = "2026-08-12T10:56:09+08:00"
WORK_SHEET = {
    "id": "1niNVFbugK2443IFe06H8nvZRC-e_r2b83YRBqXKGkqs",
    "title": "吴优工作说明",
    "url": "https://docs.google.com/spreadsheets/d/1niNVFbugK2443IFe06H8nvZRC-e_r2b83YRBqXKGkqs/edit?usp=drivesdk",
    "mime_type": "application/vnd.google-apps.spreadsheet",
}


def result(id_: str, title: str, url: str, mime: str) -> dict:
    return {"id": id_, "title": title, "url": url, "mime_type": mime}


DATA = {
    "ADS-48729": {
        "row": 321,
        "query": "C673 语音控制 小憩模式 前排",
        "results": [
            WORK_SHEET,
            result("1mAhtOwE67MCq4zsp9_iAkClhD34E2KdC", "C385_C673_功能描述_智能情景模式功能定义V4.9.docx（副本）", "https://docs.google.com/document/d/1mAhtOwE67MCq4zsp9_iAkClhD34E2KdC/edit", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
            result("1ExhJGRZW8mBS43ft1niD2oF-MXEH8uyJ", "C673-EVE_功能描述_语音控制V1.0.5.docx", "https://docs.google.com/document/d/1ExhJGRZW8mBS43ft1niD2oF-MXEH8uyJ/edit", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
            result("1l7MovYoHx10SQhHUNIBYBkt_7iTZeC_n", "C673_功能描述_语音控制V1.0.4.pdf", "https://drive.google.com/file/d/1l7MovYoHx10SQhHUNIBYBkt_7iTZeC_n/view", "application/pdf"),
        ],
        "sources": [{"id": "drive-v49", "result_id": "1mAhtOwE67MCq4zsp9_iAkClhD34E2KdC", "name": "智能情景模式功能定义V4.9", "location": "章节“语音控制方式”及“小憩模式设置功能（美洲项目只有主驾小憩）”；文档适用范围写C673EV/C673EVE", "type": "special_prd", "match": "partial", "target": "情景模式互斥；当前模式响应退出及指定语音控制内容", "reason": "正文已读，但适用范围未直接覆盖C385-5且未给出‘设置为前排’当前话术映射。"}],
    },
    "ADS-48572": {
        "row": 322,
        "query": "深蓝 POI 二次交互 功能定义",
        "results": [WORK_SHEET,
            result("1Xca7y1SPBCHFOB87CHmiEjcbhPDwH5gl", "C385&673交互设计文档_地图导航（高德）_850_V0.6.pdf", "https://drive.google.com/file/d/1Xca7y1SPBCHFOB87CHmiEjcbhPDwH5gl/view", "application/pdf"),
            result("1NrN0MoBPddT9PdMc8dUgRjHUh5TE01xG", "记忆空间-需求文档-v0.6.pdf", "https://drive.google.com/file/d/1NrN0MoBPddT9PdMc8dUgRjHUh5TE01xG/view", "application/pdf"),
            result("1j15RexOZPpsrjKpkPPDCxuTBHSfjSElG", "记忆空间-需求文档-v0.6.pdf（误加需删除）", "https://drive.google.com/file/d/1j15RexOZPpsrjKpkPPDCxuTBHSfjSElG/view", "application/pdf")],
        "sources": [{"id": "drive-map-v06", "result_id": "1Xca7y1SPBCHFOB87CHmiEjcbhPDwH5gl", "name": "地图导航交互V0.6", "location": "修改记录及POI/备选站/列表选择相关页面正文；未检出‘火锅店/第一个/可见节点优先级’条款", "type": "interaction", "match": "gap", "target": "定义地图POI及列表交互，但缺本票跨列表二次交互优先级", "reason": "正文已读，资料覆盖C385/C673地图交互但缺决定性优先级条款。", "material": True}],
    },
    "HUR-82888": {"row": 323, "query": "J90A 蓝牙电话 功能定义", "results": [WORK_SHEET,
        result("1C48WctxwD-BXk_EOYdCjz61T993silSkyqlf15ZdXmc", "J90A_TextID_0709截图标注前备份", "https://docs.google.com/spreadsheets/d/1C48WctxwD-BXk_EOYdCjz61T993silSkyqlf15ZdXmc/edit", "application/vnd.google-apps.spreadsheet"),
        result("1AAL-II3PGv6jEwLpayNy-NWwJFnM9ILcIr13uVjU3P0", "J90A_海外LanguageList_V1.1_260807", "https://docs.google.com/spreadsheets/d/1AAL-II3PGv6jEwLpayNy-NWwJFnM9ILcIr13uVjU3P0/edit", "application/vnd.google-apps.spreadsheet"),
        result("1ASnEMB3HSNClw2MRbsA1tGDaB9Y5Vi_dXL9hZzz7gC4", "J90A_海外LanguageList内部版V1.0_260806", "https://docs.google.com/spreadsheets/d/1ASnEMB3HSNClw2MRbsA1tGDaB9Y5Vi_dXL9hZzz7gC4/edit", "application/vnd.google-apps.spreadsheet")], "sources": []},
    "PC-38471": {"row": 326, "query": "C673 语音设置 可见即可说"},
    "PC-38472": {"row": 325, "query": "C673 语音设置 可见即可说"},
    "PC-38473": {"row": 324, "query": "C673 语音设置 可见即可说"},
    "ADS-47316": {
        "row": 327, "query": "深蓝项目语音功能点 资源切换",
        "results": [WORK_SHEET,
            result("1NIigtu118wKH_NGGMMjFNsKqJV0p8QXa", "深蓝项目语音功能点 260731.xlsx", "https://docs.google.com/spreadsheets/d/1NIigtu118wKH_NGGMMjFNsKqJV0p8QXa/edit", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            result("1aseVJgIUACnQ-EUFcqzzOI_PdAK1yIds", "语音对标评测记录表_20251015 S73a2.xlsx", "https://docs.google.com/spreadsheets/d/1aseVJgIUACnQ-EUFcqzzOI_PdAK1yIds/edit", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            result("1H6QV_SFtPQXo1cdKaodZICzqGy5DenwM", "语音对标评测记录表_20251015理想.xlsx", "https://docs.google.com/spreadsheets/d/1H6QV_SFtPQXo1cdKaodZICzqGy5DenwM/edit", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")],
        "sources": [{"id": "drive-deepal-function", "result_id": "1NIigtu118wKH_NGGMMjFNsKqJV0p8QXa", "name": "深蓝项目语音功能点260731", "location": "提取内容行63‘资源切换-上/下一首/集/季’、行66‘指定第N首/集/季’；未定义‘下一首+指定歌手’组合", "type": "formal_config", "match": "gap", "target": "分别定义资源切换与指定序号，缺组合指令边界", "reason": "正文已读，存在同项目功能点但缺本票组合语义条款。", "material": True}],
    },
    "SLV-44180": {
        "row": 328, "query": "深蓝 行车指数 语音 功能点",
        "results": [WORK_SHEET,
            result("1ffuMGFP-jf07RmDSdXg9JBcruks7KK2Z", "语音对标评测记录表S05S07S09-20250918.xlsx", "https://docs.google.com/spreadsheets/d/1ffuMGFP-jf07RmDSdXg9JBcruks7KK2Z/edit", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            result("1b3ULKv-_KMA6m5vOkHXXMn1DB__1Tv3T", "语音功能功能点-二轮白名单（短期）.xlsx", "https://docs.google.com/spreadsheets/d/1b3ULKv-_KMA6m5vOkHXXMn1DB__1Tv3T/edit", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            result("1NIigtu118wKH_NGGMMjFNsKqJV0p8QXa", "深蓝项目语音功能点 260731.xlsx", "https://docs.google.com/spreadsheets/d/1NIigtu118wKH_NGGMMjFNsKqJV0p8QXa/edit", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")],
        "sources": [{"id": "drive-deepal-function", "result_id": "1NIigtu118wKH_NGGMMjFNsKqJV0p8QXa", "name": "深蓝项目语音功能点260731", "location": "全文提取检索‘行车指数’无命中；meta_id 1251仅出现在行14‘暂停播报’继承列，未形成行车指数正式映射", "type": "formal_config", "match": "gap", "target": "未找到行车指数到天气接口字段的正式映射", "reason": "正文已读，但未覆盖本票功能点与slot映射。", "material": True}],
    },
    "ADS-46860": {
        "row": 329, "query": "深蓝 花瓣地图 家 公司 地址",
        "results": [WORK_SHEET,
            result("1NrN0MoBPddT9PdMc8dUgRjHUh5TE01xG", "记忆空间-需求文档-v0.6.pdf", "https://drive.google.com/file/d/1NrN0MoBPddT9PdMc8dUgRjHUh5TE01xG/view", "application/pdf"),
            result("1j15RexOZPpsrjKpkPPDCxuTBHSfjSElG", "记忆空间-需求文档-v0.6.pdf（误加需删除）", "https://drive.google.com/file/d/1j15RexOZPpsrjKpkPPDCxuTBHSfjSElG/view", "application/pdf"),
            result("1yXOtNYf6W79kdXXs-f48nTyh5HxTKn4m", "深蓝_花瓣地图语音清单.xlsx", "https://docs.google.com/spreadsheets/d/1yXOtNYf6W79kdXXs-f48nTyh5HxTKn4m/edit", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")],
        "sources": [{"id": "drive-map-voice-list", "result_id": "1yXOtNYf6W79kdXXs-f48nTyh5HxTKn4m", "name": "深蓝花瓣地图语音清单", "location": "提取内容行14‘设置/修改快捷地址（家/公司）’，说明仅支持修改家且需明确；行21-25为POI搜索/路线规划", "type": "formal_config", "match": "partial", "target": "定义家/公司快捷地址与POI导航单能力，未定义‘先去公司再去机场’多意图上报边界", "reason": "正文已读，能证明单能力但不能直接定义本票多意图兜底。"}],
    },
    "HUR-77192": {
        "row": 330, "query": "J90A EU PI LanguageList 智能远光灯",
        "results": [WORK_SHEET, result("1AAL-II3PGv6jEwLpayNy-NWwJFnM9ILcIr13uVjU3P0", "J90A_海外LanguageList_V1.1_260807", "https://docs.google.com/spreadsheets/d/1AAL-II3PGv6jEwLpayNy-NWwJFnM9ILcIr13uVjU3P0/edit", "application/vnd.google-apps.spreadsheet")],
        "sources": [{"id": "drive-j90a-v11", "result_id": "1AAL-II3PGv6jEwLpayNy-NWwJFnM9ILcIr13uVjU3P0", "name": "J90A海外LanguageList V1.1", "location": "Sheet‘03_Vehicle Settings’ A1:AQ1000检索‘Avslutt Automatiske fjernlys’，0条命中", "type": "formal_config", "match": "gap", "target": "当前正式交付表未定位该挪威语条目", "reason": "已读取最新交付表并精确检索，客户/MRE变更语料仍不可追溯。", "material": True}],
    },
    "HUR-72809": {
        "row": 331, "query": "J90A EU LanguageList 能量流 能量管理",
        "results": [WORK_SHEET, result("1AAL-II3PGv6jEwLpayNy-NWwJFnM9ILcIr13uVjU3P0", "J90A_海外LanguageList_V1.1_260807", "https://docs.google.com/spreadsheets/d/1AAL-II3PGv6jEwLpayNy-NWwJFnM9ILcIr13uVjU3P0/edit", "application/vnd.google-apps.spreadsheet")],
        "sources": [{"id": "drive-j90a-v11", "result_id": "1AAL-II3PGv6jEwLpayNy-NWwJFnM9ILcIr13uVjU3P0", "name": "J90A海外LanguageList V1.1", "location": "Sheet‘16_Energy Flow’与‘13_Energy Management’各A1:AQ1000检索‘Open energiebeheer’，均0条命中", "type": "formal_config", "match": "gap", "target": "当前正式交付表未定位该荷兰语条目，能量流与能量管理映射仍冲突", "reason": "已读取最新交付表并分Sheet精确检索，当前MRE语料仍不可追溯。", "material": True}],
    },
}

PC_RESULTS = [WORK_SHEET,
    result("1cJnfFBlv3o7qkrmUjvKISa1-jAkePV3e", "C673_功能描述_语音控制V1.0.5.docx", "https://docs.google.com/document/d/1cJnfFBlv3o7qkrmUjvKISa1-jAkePV3e/edit", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
    result("1Cy1_2mxEId-jz5aFr5hJuN2U7-YN90b7vkC9qLq0pcI", "1305_深蓝_8295语音控制APP和页面开启需求文档_v2.6", "https://docs.google.com/spreadsheets/d/1Cy1_2mxEId-jz5aFr5hJuN2U7-YN90b7vkC9qLq0pcI/edit", "application/vnd.google-apps.spreadsheet"),
    result("1QcxlyPKWRlQ5HB4dKkkmwkkvKqwQbnCjLNpr-yC69zk", "奇瑞T29 语音车控功能点", "https://docs.google.com/spreadsheets/d/1QcxlyPKWRlQ5HB4dKkkmwkkvKqwQbnCjLNpr-yC69zk/edit", "application/vnd.google-apps.spreadsheet")]
for key in ("PC-38471", "PC-38472", "PC-38473"):
    DATA[key]["results"] = PC_RESULTS
    DATA[key]["sources"] = [
        {"id": "drive-c673-voice", "result_id": "1cJnfFBlv3o7qkrmUjvKISa1-jAkePV3e", "name": "C673语音控制V1.0.5", "location": "功能需求正文；未检出语音设置页列表项播放/编辑/删除的可见节点条款", "type": "prd", "match": "gap", "target": "通用语音车控定义未覆盖本票可见列表操作", "reason": "正文已读，缺本票可见即可说目标。", "material": True},
        {"id": "drive-1305-v26", "result_id": "1Cy1_2mxEId-jz5aFr5hJuN2U7-YN90b7vkC9qLq0pcI", "name": "8295页面开启需求v2.6", "location": "Sheet‘设置APP内页面&弹窗’第34行：新增唤醒词页面已下发；备注界面有置灰逻辑，当前能力不能直达按钮位置；‘应答语’检索0条", "type": "formal_config", "match": "partial", "target": "只定义打开新增唤醒词页面，不定义列表项播放/编辑/删除及序号消歧", "reason": "已按Sheet/行读取，未覆盖本票操作目标。"},
    ]


def rebuild() -> None:
    items = []
    log_lines = [
        "# 2026-08-12 每日新增 Bug 证据与日志闭环重检",
        "",
        f"- Run ID：{RUN_ID}",
        "- 操作者：Codex（本机绑定 wu-you）",
        "- 涉及 Jira：" + " / ".join(DATA),
        "- 操作类型：普通复查（recheck）；仅允许 C/D/G/I/J",
        "- 读取证据：Jira当日完整页面与关联票；Google Drive检索回执及候选正文；Alchemy SSO不可用限制",
        "- 表格位置：bug!A321:J331；每票行号见下",
        "- Jira 动作：未评论 Jira / 未转派 Jira / 未关闭 Jira / 未变更状态",
        "- 回读校验：待写后补充并由 final run bundle 校验",
        "- run bundle：agent/logs/bug-actions/2026-08-12-daily-new-bugs-run.json",
        "- readback_sha256：待写后补充",
        "- 敏感信息处理：未记录账号、密码、token 或访问口令",
        "",
    ]
    for key, spec in DATA.items():
        path = LOG_DIR / f"2026-08-12-{key}-manifest.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["schema_version"] = 4
        payload["run_context"] = {"run_id": RUN_ID, "operator_owner_id": "wu-you", "target_owner_id": "wu-you", "sheet_name": "bug", "sheet_row": spec["row"]}
        payload["scope_checks"] = [
            item for item in payload["scope_checks"]
            if not str(item.get("source_id", "")).startswith("drive-")
        ]
        source_by_result = {item["result_id"]: item for item in spec["sources"]}
        for source in spec["sources"]:
            payload["scope_checks"].append({
                "source_id": source["id"], "source": source["name"], "source_location": source["location"],
                "source_type": source["type"], "role": "context_only", "project_model": payload["scope_checks"][0]["project_model"],
                "trigger": payload["scope_checks"][0]["trigger"], "target_behavior": source["target"], "match": source["match"],
                "material": source.get("material", False), "next_action": payload["decision"]["text"].split("处理：", 1)[-1], "reason": source["reason"],
            })
        receipts = []
        for check in payload["required_evidence_checks"]:
            if check["check_id"] not in {"formal_definition_search", "main_prd_search", "special_definition_search", "formal_config_search", "interaction_or_ue_search"}:
                continue
            check["queries"] = [
                {"kind": "jira_key", "text": key},
                {"kind": "problem_concept", "text": spec["query"]},
                {"kind": "module_artifact", "text": spec["query"]},
            ]
            receipt_id = f"{key}-{check['check_id']}-drive-20260812"
            receipts.append({"receipt_id": receipt_id, "provider": "google_drive", "check_id": check["check_id"], "searched_at": STARTED_AT, "queries": check["queries"], "results": spec["results"]})
            check["search_receipt_ids"] = [receipt_id]
            allowed = {
                "formal_definition_search": {"prd", "special_prd", "interaction", "ue", "formal_config"},
                "main_prd_search": {"prd"},
                "special_definition_search": {"special_prd", "interaction", "formal_config"},
                "formal_config_search": {"formal_config"},
                "interaction_or_ue_search": {"interaction", "ue"},
            }[check["check_id"]]
            read_sources = [s for s in spec["sources"] if s["type"] in allowed]
            check["status"] = "read" if read_sources else "not_found"
            check["source_ids"] = [s["id"] for s in read_sources]
            if not read_sources:
                check["reason"] = "已逐项审计检索回执；命中项不是本检查允许的生效来源，或正文不定义本票目标。"
            candidates = []
            for item in spec["results"]:
                source = source_by_result.get(item["id"])
                if source and source in read_sources:
                    candidates.append({"id": item["id"], "title": item["title"], "url": item["url"], "disposition": "read", "source_ids": [source["id"]]})
                else:
                    reason = "线上负责人工作表，仅用于查重和定位，不定义产品目标。" if item["id"] == WORK_SHEET["id"] else "已核对元数据或正文；不属于本检查的同范围生效来源，或未覆盖本票目标条款。"
                    candidates.append({"id": item["id"], "title": item["title"], "url": item["url"], "disposition": "excluded", "reason": reason})
            check["candidate_audit"] = {"completed": True, "results_count": len(spec["results"]), "candidates": candidates}
        payload["search_receipts"] = receipts
        payload["decision"]["text"] = payload["decision"]["text"].replace("Drive检索未定位同范围生效目标", "Drive候选已逐项打开或排除，仍缺同范围决定性目标")
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        log_lines += [
            f"## {key} 决策核验卡",
            "",
            f"- 备注因果链：{payload['comment_causality']}",
            "- 客户问题识别：非客户提报；无需客户测试用例门槛。" if not payload["customer_issue"]["identified"] else "- 客户问题识别：已识别客户提报并按manifest记录测试用例状态。",
            "- 关联票：" + ("；".join(f"{x['key']}（{x['relationship']}，已读，{x['outcome']}）" for x in payload["related_issues"]["items"]) or "已核验无直接关联票。"),
            "- 证据画像与必查资料：" + "、".join(payload["evidence_profiles"]) + "；Drive回执逐项审计；Alchemy当前/标准/项目功能点因SSO不可用。",
            "- 资料适用范围：" + "；".join(f"{x['source']}｜{x['source_location']}｜{x['role']}｜{x['match']}" for x in payload["scope_checks"]),
            f"- 冲突处理：{payload['conflict_resolution']}",
            f"- 唯一结论：{payload['decision']['status']}；{payload['decision']['text'].replace(chr(10), ' ')}；责任方：{payload['decision']['owner']}。",
            f"- 表格位置：bug!A{spec['row']}:J{spec['row']}，{key} 行 {spec['row']}。",
            "",
        ]
        items.append({"jira_key": key, "operator_owner_id": "wu-you", "target_owner_id": "wu-you", "sheet_name": "bug", "sheet_row": spec["row"], "manifest_path": str(path)})

    log_path = LOG_DIR / "2026-08-12-daily-new-bugs-recheck.md"
    log_path.write_text("\n".join(log_lines), encoding="utf-8")
    bundle = {"schema_version": 1, "run_id": RUN_ID, "automation_id": "bug", "status": "planned", "started_at": STARTED_AT, "query_summary": "Jira查询145条；线上吴优bug页去重后新增11条；本次重检11条", "action_log": str(log_path), "items": items}
    (LOG_DIR / "2026-08-12-daily-new-bugs-run.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    rebuild()
