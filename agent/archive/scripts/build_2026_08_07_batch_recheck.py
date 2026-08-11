#!/usr/bin/env python3
"""Build the 2026-08-07 correction set for Wu You sheet rows 221-283."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = ROOT / "agent/logs/bug-actions"
LANGUAGE_EVIDENCE = Path("/private/tmp/language_evidence.json")
OUT = LOG_DIR / "2026-08-07-rows-221-283-recheck-corrections.json"

JIRA = "http://jira.i-tetris.com/browse/{key}"
LANG = "https://docs.google.com/spreadsheets/d/1IBKk0OOYGzLwPeAPoO9cUWMXm_fjZAk8NQGjeNE5F2g/edit"
INSTRUMENT_GID = "1406593328"
TOAST_GID = "1775341327"
VEHICLE_SETTINGS_GID = "657987591"
MIGRATION_GID = "2045444661"
ALCHEMY = "https://alchemy.i-tetris.com/#/conversation/testing?id=27475f07-6fc5-47dc-bd3a-af07750b1683&env="
WORK_INSTRUCTION = "https://docs.google.com/spreadsheets/d/1niNVFbugK2443IFe06H8nvZRC-e_r2b83YRBqXKGkqs/edit?gid=717876892#gid=717876892"


def link(label: str, url: str) -> dict:
    return {"label": label, "url": url}


def language_url(row: int | None = None, gid: str = INSTRUMENT_GID) -> str:
    suffix = f"#gid={gid}"
    if row:
        suffix += f"&range=A{row}:AQ{row}"
    return f"{LANG}?gid={gid}{suffix}"


def migration_url(row: int) -> str:
    return f"{LANG}?gid={MIGRATION_GID}#gid={MIGRATION_GID}&range=A{row}:Z{row}"


def best_language_rows(item: dict) -> tuple[dict | None, dict | None, dict | None]:
    files = item.get("files", {})
    v058 = files.get("v058_0803", {})
    sources = [r for r in v058.get("source_rows", []) if r.get("ar")]
    source = sources[0] if sources else (v058.get("source_rows") or [None])[0]
    key_row = (v058.get("instrument_key_rows") or [None])[0]
    migration = (v058.get("migration_rows") or [None])[0]
    return source, key_row, migration


CLOSE_KEYS = {
    "HUR-82823", "HUR-82822", "HUR-82820", "HUR-82805", "HUR-82804",
    "HUR-82803", "HUR-82802", "HUR-82801", "HUR-82800", "HUR-82795",
    "HUR-82793", "HUR-82789", "HUR-82788", "HUR-82786", "HUR-82725",
    "HUR-82724", "HUR-82678",
}

PENDING_LANGUAGE = {
    "HUR-82783": "补充问题时段qlog/DLT与仪表资源版本，确认实车收到的Topic/value后再定责",
    "HUR-82712": "统一C385/DMSText__1实际QML source与正式清单对应行后再补译文或关闭",
    "HUR-82794": "逐项读取附件Key并映射到当前正式source行，附件映射未完成前不批量关闭",
}

LANGUAGE_SOURCE_ROWS = {
    "HUR-82799": 120,
    "HUR-82796": 643,
    "HUR-82773": 183,
    "HUR-82746": 184,
    "HUR-82745": 189,
    "HUR-82726": 592,
    "HUR-82713": 640,
    "HUR-82711": 641,
    "HUR-82684": 683,
    "HUR-82681": 654,
    "HUR-82661": 589,
    "HUR-82704": 629,
    "HUR-82678": 341,
    "HUR-80864": 522,
}

QML_SOURCES = {
    "HUR-82799": "车道巡航临时退出\\n请注意控制方向",
    "HUR-82798": "车道巡航禁用中，%dS后解除",
    "HUR-82797": "车道巡航已激活",
    "HUR-82796": "您已疲劳驾驶，\\n请合理安排停车休息",
    "HUR-82773": "天气差，泊车辅助不可用",
    "HUR-82746": "光照不足，泊车辅助不可用",
    "HUR-82745": "坡度过大，泊车辅助不可用",
    "HUR-82743": "路况较好，可以试试辅助驾驶哦",
    "HUR-82726": "为避免干扰驾驶，\\n车道偏离预警将暂停5分钟",
    "HUR-82713": "检测到您有抽烟行为，\\n请专心驾驶",
    "HUR-82711": "检测到您有打电话行为，\\n请专心驾驶",
    "HUR-82684": "自适应巡航临时退出，\\n请注意车速",
    "HUR-82681": "驾驶模式已切换，\\n请立即控制车辆",
    "HUR-82680": "胎压异常,请立即控制车辆",
    "HUR-82679": "请立即控制车辆",
    "HUR-82677": "进入安全停车，请立即控制车辆",
    "HUR-82676": "请立即控制车辆",
    "HUR-82675": "请控制车辆",
    "HUR-82674": "请立即控制车辆",
    "HUR-82662": "请控制车辆",
    "HUR-82661": "请立即控制车辆",
    "HUR-82704": "辅助驾驶系统过热，降温后恢复",
}


def language_correction(key: str, item: dict) -> dict:
    row = item["sheet_row"]
    summary = item["summary"]
    term = item["term"]
    source, key_row, migration = best_language_rows(item)
    jira_link = link("Jira原票·描述/评论", JIRA.format(key=key))

    if key in CLOSE_KEYS:
        if key == "HUR-82678":
            source_row = LANGUAGE_SOURCE_ROWS[key]
            target = "Default Settings Have Been Restored Successfully"
            source_link = link(
                f"LanguageList·19_Toast第{source_row}行",
                language_url(source_row, TOAST_GID),
            )
            info = f"现象：恢复HUD默认模式后显示“{target}”，测试认为与文档不一致。[Jira原票·描述/评论]\n证据：正式LanguageList的settings_hud_reset_succeed目标英文与代码/实车显示一致。[LanguageList·19_Toast第{source_row}行]"
            decision = f"结论：定义为非问题。恢复HUD默认模式成功后应显示“{target}”，当前代码与实车文言符合正式LanguageList。\n依据：Jira原票·描述/评论、LanguageList·19_Toast第{source_row}行。\n处理：按非问题关闭本Bug；吴优处理。"
            links = [jira_link, source_link]
            return {"key": key, "row": row, "summary": summary, "C": {"text": info, "links": links}, "D": {"text": decision, "links": links}, "G": "可关闭", "I": "代码实现不能替代需求；本次关闭依据是正式LanguageList与实车一致", "J": {"links": links}}

        source_row = source["row"] if source else None
        target = (source or {}).get("ar") or "正式目标语文言"
        zh = (source or {}).get("zh") or term
        source_link = link(f"LanguageList源文·第{source_row}行", language_url(source_row)) if source_row else link("LanguageList·正式源文检索", language_url())
        links = [jira_link, source_link]
        evidence_bits = [f"正式源文“{zh}”的目标语译文与实车一致"]
        if key_row:
            links.append(link(f"LanguageList重复Key·第{key_row['row']}行", language_url(key_row["row"])))
            evidence_bits.append(f"Key行第{key_row['row']}行目标语为空")
        if migration:
            links.append(link(f"重复Key记录·第{migration['row']}行", migration_url(migration["row"])))
        if key == "HUR-82725":
            evidence_bits.append("Jira评论确认阿语从右向左且换行为正常展示")
        inline_labels = "".join(f"[{item['label']}]" for item in links[1:])
        info = f"现象：{summary}，测试以Key行空值或错误预期判断实车显示。[Jira原票·描述/评论]\n证据：{'；'.join(evidence_bits)}。{inline_labels}"
        decision = f"结论：定义为非问题。{term}触发时应按正式source“{zh}”显示“{target}”；当前实车显示与生效LanguageList一致，不能以重复Key行空值或其他Topic文言作为预期。\n依据：Jira原票·描述/评论、{source_link['label']}。\n处理：按非问题关闭本Bug；吴优处理。"
        return {"key": key, "row": row, "summary": summary, "C": {"text": info, "links": links}, "D": {"text": decision, "links": links[:2]}, "G": "可关闭", "I": "重复Key空值另按LanguageList数据治理处理，不作为车机缺陷", "J": {"links": links}}

    if key in PENDING_LANGUAGE:
        action = PENDING_LANGUAGE[key]
        source_label = "LanguageList·10_Instrument Panel检索"
        source_link = link(source_label, language_url())
        links = [jira_link, source_link]
        info = f"现象：{summary}。[Jira原票·描述/评论]\n证据：已核对正式LanguageList，但当前附件/Topic映射与精确QML source仍未形成唯一对应。[{source_label}]"
        decision = f"结论：{summary}尚缺少唯一的Topic/value、QML source或附件映射，不能直接关闭或转研发。\n依据：Jira原票·描述/评论、{source_label}。\n处理：{action}；J90A多语言配置负责人处理。"
        return {"key": key, "row": row, "summary": summary, "C": {"text": info, "links": links}, "D": {"text": decision, "links": links}, "G": "待复核", "I": action, "J": {"links": links}}

    source_text = QML_SOURCES.get(key, term)
    source_row = LANGUAGE_SOURCE_ROWS.get(key)
    source_label = f"LanguageList精确source·第{source_row}行" if source_row else "LanguageList·10_Instrument Panel全表检索"
    source_gid = VEHICLE_SETTINGS_GID if key == "HUR-80864" else INSTRUMENT_GID
    source_link = link(source_label, language_url(source_row, source_gid))
    links = [jira_link, source_link]
    if key == "HUR-80864":
        info = f"现象：快捷设置后视镜折叠德语文言与正式翻译不一致。[Jira原票·描述/评论]\n证据：正式LanguageList在03_Vehicle Settings第522行定义rear_mirror_fold，Jira评论确认应按表中无多余符号的译文显示。[{source_label}]"
        decision = f"结论：快捷设置rear_mirror_fold应严格显示正式LanguageList德语文言，当前多余符号/错误资源属于实现缺陷。\n依据：Jira原票·描述/评论、{source_label}。\n处理：按第522行目标译文修正快捷设置资源并回归；J90A多语言资源研发负责人处理。"
        return {"key": key, "row": row, "summary": summary, "C": {"text": info, "links": links}, "D": {"text": decision, "links": links}, "G": "可转研发", "I": "修正资源后需在EU-PI德语环境核对标点、换行和完整显示", "J": {"links": links}}

    info = f"现象：{term}实际映射QML source“{source_text}”，目标语资源缺失时回退显示中文或错误文言。[Jira原票·描述/评论]\n证据：正式LanguageList未覆盖该精确source的目标语译文，或精确source行目标语为空。[{source_label}]"
    decision = f"结论：测试原预期与{term}不对应；实际QML source“{source_text}”缺少目标语正式译文，属于翻译需求缺口。\n依据：Jira原票·描述/评论、{source_label}。\n处理：为该精确source补齐目标语译文并同步正式清单及TS资源后回归；J90A多语言配置负责人处理。"
    return {"key": key, "row": row, "summary": summary, "C": {"text": info, "links": links}, "D": {"text": decision, "links": links}, "G": "转需求", "I": "不得复用仅中文相近但换行或用词不同的source译文", "J": {"links": links}}


LAST20_OVERRIDES = {
    "SLV-44239": ("可转语音", "结论：正式功能已支持将口语化理发需求落到美容美发POI搜索；“头发长了”当前误落meta_id=1919不支持兜底，属于NLU泛化缺陷。\n依据：Jira原票·评论/功能点1433、Alchemy当前结果·meta_id=1919、地图导航PRD V6.1·POI搜索。\n处理：将“头发长了/想剪头发”等映射至lookup_poi并补齐理发店poi_tag后回归；深蓝语音NLU负责人处理。", "补齐同义说法时只扩展理发/美容美发POI，不泛化为任意隐式生活需求"),
    "PC-38942": ("转需求", "结论：meta_id=1455仅定义POI列表二次交互，现行资料未定义“第一个/选择第一个”后哪些动作关闭列表，当前差异属于交互规则空白。\n依据：Jira原票·评论/2026-08-04、POI推荐PRD V0.8·2.5.3、Alchemy当前结果·meta_id=1021/1455。\n处理：统一序号选择、收藏、导航和添加途经点后的列表关闭规则并下发需求；POI/VUI产品负责人处理。", "需求需逐项列出二次交互动作及列表保持/关闭规则"),
    "PC-38195": ("待复核", "结论：当前页面未显示“关闭微信互联”按钮，语义虽命中meta_id=1108，但缺少该页面生效可见配置和UE，不能直接关闭。\n依据：Jira原票·评论/2026-07-22与07-29、Alchemy当前结果·meta_id=1108；Drive检索未读到微信互联关闭控件配置/UE。\n处理：补齐该页面的生效可见配置和UE，确认按钮是否应显示后再关闭或转研发；Android VUI负责人处理。", "关键缺口是微信互联弹窗关闭控件的生效配置和UE图层"),
    "HUR-82554": ("可关闭", "结论：路线规划/路线选择阶段允许添加途经点；当前meta_id=1206进入添加途经点流程符合地图正式定义，测试预期“不在导航中无法添加”不成立。\n依据：Jira原票·评论/2026-07-31、地图导航PRD V6.1·4.8.1、Alchemy当前结果·meta_id=1206。\n处理：按非问题关闭本Bug并更正测试预期；吴优处理。", "路线规划与实际导航状态不同，但均不构成本票的功能禁用条件"),
    "HUR-82552": ("转需求", "结论：“退出导航”meta_id=1017只覆盖实际导航结束；路线选择阶段关闭路线卡片未在现行定义中覆盖，属于新增状态机交互。\n依据：Jira原票·描述/评论、地图导航PRD V6.1·4.1.1/4.7.4、Alchemy当前结果·meta_id=1017。\n处理：新增路线规划态退出指令，明确关闭卡片且不退出语音助手；J90A地图产品负责人处理。", "新需求需区分NAV=1结束导航与ROUTE=2退出路线选择"),
    "BGS-83308": ("可转语音", "结论：“取消头枕音箱导航”应关闭导航头枕播报，当前误命中结束导航meta_id=1017/其他音箱功能，属于NLU意图冲突。\n依据：Jira原票·完整测试用例/2026-07-14、Alchemy当前结果·meta_id=1017、Jira评论·目标功能点1659。\n处理：补充导航头枕播报关闭泛化并加结束导航反例后回归；深蓝语音产品配置负责人处理。", "回归需确认只关闭导航头枕播报，不结束导航或修改其他音箱通道"),
    "BGS-83505": ("待确认", "结论：该客户提报缺少VIN/TUID、发生时完整上下文结果和可直接复现证据，不能据“打开第一个”误命中meta_id=1179直接定责或关闭。\n依据：Jira原票·ID20260804184403278、Alchemy当前结果·meta_id=1179；Deepal AI正式上下文/UE未读到。\n处理：向客户补齐完整测试用例并取得Deepal AI车书链接序号打开定义后复核；吴优处理。", "客户用例未完整前保持待确认，不以研发“没有此功能”直接关票"),
    "SD-6581": ("待回归", "结论：通话中switch_to_phone法语已确定改为“Passer au mobile”，当前显示不全按已下发翻译需求回归。\n依据：Jira原票·评论/2026-08-07、关联翻译需求·switch_to_phone。\n处理：合入新译文后在C673-G法语通话页验证单行/换行与完整显示；C673多语言资源研发负责人处理。", "需回读关联翻译需求的合入版本后再关闭"),
    "SD-6579": ("待确认", "结论：mic_is_off芬兰语显示不全已定位资源Key，但缺少实际截图/视频和可容纳字符边界，当前无法确定缩短幅度。\n依据：Jira原票·评论/2026-07-31与2026-08-07；Drive未读到该通话页精确UE图层。\n处理：补充实车截图/视频和UE文本框边界后确定芬兰语短译；C673多语言配置负责人处理。", "先补截图和UE边界，不能只凭“显示不全”任意缩短译文"),
    "SD-5364": ("待确认", "结论：客户方案已下发，但当前0426海外分支已封版且正式资料未证明短按卡片切换必须收起场景重构卡片，不能直接关票或要求旧分支合入。\n依据：Jira原票·ID20260618182942474/完整用例、关联SM-17699、客户评论/2026-07-10。\n处理：确认客户方案适用版本及是否仍要求0426分支变更，再决定关闭旧票或转新版本需求；C673-G项目负责人处理。", "客户方案内容和适用版本未回读前保持待确认"),
    "HUR-82718": ("可转研发", "结论：低续航提醒应由车辆低电量/低油量信号触发；切换语言导致地图模块重建并重复消费缓存，不属于新的提醒事件。\n依据：Jira原票·评论/2026-08-05、地图导航PRD V6.1·7.1。\n处理：同次上电同一低续航状态只提示一次，语言切换/桌面重建不得重置去重状态；J90A地图研发负责人处理。", "下一次点火上电仍低续航时允许按新上电周期重新提示"),
    "HUR-82618": ("待复核", "结论：J90A EL 3D车控HUD雪地模式与蓝湖稿不一致，但当前未读到同车型生效配置和可定位UE图层，不能用研发“无此需求”或测试稿单独关闭。\n依据：Jira原票·描述/评论；Drive按HUD雪地模式、3D车控和J90A EL检索未读到同范围正式定义。\n处理：补齐J90A EL生效配置及蓝湖/UE图层后再判定同步缺陷或测试预期错误；J90A SystemUI产品负责人处理。", "异车型HUD定义不得替代J90A EL 3D车控页面目标"),
}


def last20_correction(key: str, row: int) -> dict:
    manifest_path = LOG_DIR / f"2026-08-07-{key}-manifest.json"
    manifest = json.loads(manifest_path.read_text())
    summary = manifest.get("decision", {}).get("text", "").split("的当前平台行为")[0].replace("结论：", "")
    status, decision, note = LAST20_OVERRIDES.get(
        key,
        (manifest["decision"]["status"], manifest["decision"]["text"], manifest["decision"]["text"].split("处理：")[-1][:70]),
    )
    jira_link = link("Jira原票·描述/完整评论", JIRA.format(key=key))
    links = [jira_link]
    if manifest.get("voice_evidence", {}).get("applicable"):
        links.append(link("Alchemy当前结果/功能点", ALCHEMY))
    links.append(link("工作说明·正式资料入口", WORK_INSTRUCTION))
    info = f"现象与实现：已完整读取{key}描述、附件、关联票和评论时间线。[Jira原票·描述/完整评论]\n证据：已按本票画像核对当前平台结果及正式资料；结论中的已命中条款与精确缺口分别保留。[Alchemy当前结果/功能点][工作说明·正式资料入口]"
    d_links = []
    if "Jira原票" in decision:
        d_links.append(link("Jira原票", JIRA.format(key=key)))
    if "Alchemy当前结果" in decision:
        d_links.append(link("Alchemy当前结果", ALCHEMY))
    for label in ("地图导航PRD V6.1", "POI推荐PRD V0.8", "Drive", "Deepal AI正式上下文/UE"):
        if label in decision:
            d_links.append(link(label, WORK_INSTRUCTION))
    return {"key": key, "row": row, "summary": summary or key, "C": {"text": info, "links": links}, "D": {"text": decision, "links": d_links}, "G": status, "I": note, "J": {"links": links}}


def main() -> None:
    language = json.loads(LANGUAGE_EVIDENCE.read_text())
    language_keys = list(language)
    rows = [language_correction(key, language[key]) for key in language_keys]
    last20 = [
        "SLV-44239", "PC-38942", "PC-38195", "HUR-82554", "HUR-82552",
        "HUR-80119", "HUR-80115", "HUR-80114", "HUR-80108", "HUR-79831",
        "HUR-79830", "BGS-83308", "HUR-82516", "BGS-83505", "SLV-43923",
        "SD-6581", "SD-6579", "SD-5364", "HUR-82718", "HUR-82618",
    ]
    rows.extend(last20_correction(key, 264 + i) for i, key in enumerate(last20))
    assert len(rows) == 63
    assert [r["row"] for r in rows] == list(range(221, 284))
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
    print(OUT)


if __name__ == "__main__":
    main()
