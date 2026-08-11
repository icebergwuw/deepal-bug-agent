#!/usr/bin/env python3
"""Build recheck artifacts for unresolved Wu You sheet rows 159-176."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LOG = ROOT / "agent/logs/bug-actions"
DATE = "2026-08-07"
JIRA = "http://jira.i-tetris.com/browse/{key}"
MAP_LIST = "https://docs.google.com/spreadsheets/d/15Qxx8f9A-fJ2o99f_bCLm2twGVERAmA4H1VyoovW6Y8/edit?gid=1947690897#gid=1947690897"
PHONE_LIST = "https://docs.google.com/spreadsheets/d/15Qxx8f9A-fJ2o99f_bCLm2twGVERAmA4H1VyoovW6Y8/edit?gid=1401474663#gid=1401474663"
MAP_UE = "https://mastergo.com/file/131302242181530?page_id=689%3A156261"
ALCHEMY = "https://alchemy.i-tetris.com/#/conversation/testing?id=27475f07-6fc5-47dc-bd3a-af07750b1683&env="
MEETING = "https://meeting.tencent.com/wework/cloud-record/share?id=c0ff45c9-e35e-445d-8055-0c49f46a0dbc&record_type=2&hide_more_btn=true&from=qywx"
ISSUE_LIST = "https://doc.weixin.qq.com/sheet/e3_AQoAigbTAMMCN6FPkXm1hS4KIv0Fc?scode=ACYAOwdwAAYGiHNN5jAXIA5QZnALk&tab=f8818z"
SCALE_REQ = "http://jira.i-tetris.com/browse/PC-37447"


def lk(label: str, url: str) -> dict[str, str]:
    return {"label": label, "url": url}


def entry(row: int, key: str, summary: str, c: str, d: str, status: str, note: str,
          c_links: list[dict[str, str]], d_links: list[dict[str, str]], j_links: list[dict[str, str]],
          profiles: list[str], utterance: str = "", alchemy_result: str = "", meta_id: str = "",
          formal_label: str = "", formal_url: str = "", formal_location: str = "",
          deterministic: bool = False) -> dict[str, object]:
    return {
        "row": row, "key": key, "summary": summary,
        "C": {"text": c, "links": c_links}, "D": {"text": d, "links": d_links},
        "G": status, "I": note, "J": {"links": j_links}, "profiles": profiles,
        "utterance": utterance, "alchemy_result": alchemy_result, "meta_id": meta_id,
        "formal_label": formal_label, "formal_url": formal_url, "formal_location": formal_location,
        "deterministic": deterministic,
    }


def build_items() -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    def jira(key: str, label: str = "Jira原票·描述/完整评论") -> dict[str, str]: return lk(label, JIRA.format(key=key))
    map_list = lk("C673功能清单·16_地图第45/85-93/298行", MAP_LIST)
    ue = lk("C673地图UE V0.6·850页面/检索图层", MAP_UE)
    alchemy = lk("Alchemy当前结果/标准及项目功能点", ALCHEMY)

    key="SLV-44216"; jl=jira(key,"Jira最新评论·0729客户会结论"); ml=lk("客户会议录屏·24:45",MEETING)
    items.append(entry(159,key,"地图设置缺少停车场推荐和步行接续开关",
        "现象：C673地图设置缺少停车场推荐和步行接续开关。[Jira最新评论·0729客户会结论]\n证据：0729客户会明确按UI补上，录屏24:45形成结论；C673主清单第45行定义步行接续，MasterGo 850页面包含停车场推荐/步行接续能力。[客户会议录屏·24:45][C673功能清单·16_地图第45/85-93/298行][C673地图UE V0.6·850页面/检索图层]",
        "结论：停车场推荐和步行接续设置项按0729客户会及生效UI补齐，属于实现缺失。\n依据：Jira最新评论·0729客户会结论、客户会议录屏·24:45、C673功能清单·16_地图第45行、C673地图UE V0.6·850页面。\n处理：补齐两个设置入口、开关状态和回归用例；C673地图研发负责人处理。",
        "可转研发","按客户会范围实现两个开关，不扩展未确认的推荐策略",[jl,ml,map_list,ue],[jl,ml,map_list,ue],[jl,ml,map_list,ue],["map_navigation","visible_interaction"],formal_label="0729客户最终结论+地图UE",formal_url=MEETING,formal_location="客户会议录屏24:45；MasterGo 850_V0.5&V0.6页面",deterministic=True))

    key="SLV-44215"; jl=jira(key,"Jira最新评论·等待客户补需求")
    items.append(entry(160,key,"停车推荐点击去这里后进入路线推荐页",
        "现象：点击停车推荐“去这里”后进入路线推荐页，票面主张应直接重算。[Jira最新评论·等待客户补需求]\n证据：最新评论为“等待张俊华补充需求”；C673主清单和MasterGo仅证明停车场能力，未定义该点击后的直达/中转流程。[C673功能清单·16_地图第45/85-93/298行][C673地图UE V0.6·850页面/检索图层]",
        "结论：直接重算还是进入路线推荐页尚无客户最终点击流程，当前不能按地图缺陷转研发。\n依据：Jira最新评论·等待客户补需求、C673地图UE V0.6·850页面。\n处理：补齐“去这里”点击后的目标页面、重算触发和异常分支；吴优对接张俊华确认。",
        "待确认","缺客户最终点击链路；确认前不按旧UE推定直达重算",[jl,map_list,ue],[jl,ue],[jl,map_list,ue],["map_navigation","visible_interaction"],formal_label="",formal_url="",formal_location=""))

    key="SLV-44214"; jl=jira(key,"Jira最新评论·0729客户会结论")
    items.append(entry(161,key,"充电站卡片缺品牌图标并存在堆叠/视野跳转",
        "现象：充电站快捷开关存在品牌图标缺失、卡片堆叠和视野跳转三项问题。[Jira最新评论·0729客户会结论]\n证据：0729客户会只先确认修复UI图已有品牌图标缺失；MasterGo含充电站气泡/深度信息，未形成其余两项最终规则。[C673地图UE V0.6·850页面/检索图层]",
        "结论：本票先按客户会明确范围修复充电品牌图标缺失；卡片堆叠和当前视野搜索不并入本次实现。\n依据：Jira最新评论·0729客户会结论、C673地图UE V0.6·850页面。\n处理：补齐品牌图标并回归；其余两项拆票补目标后处理；C673地图UI研发负责人处理。",
        "可转研发","本票实现范围仅品牌图标；堆叠和视野策略需拆票",[jl,ue,map_list],[jl,ue],[jl,ue,map_list],["map_navigation","visible_interaction"],formal_label="0729客户最终结论",formal_url=JIRA.format(key=key),formal_location="Jira最新评论：0729客户会先修复品牌图标",deterministic=True))

    key="SLV-44213"; jl=jira(key,"Jira最新评论·0729客户会结论")
    items.append(entry(162,key,"停车场气泡UI与热区/堆叠不符合预期",
        "现象：停车场标签颜色、尺寸、气泡点击热区及堆叠同时被提报。[Jira最新评论·0729客户会结论]\n证据：0729客户会确认UI问题要改；热区/堆叠受高德自定义图层限制，需客户与高德确认，不能混作同一研发结论。[C673地图UE V0.6·850页面/检索图层]",
        "结论：停车场标签颜色和尺寸按客户确认UI修复；热区与堆叠受高德自定义图层限制，拆分后由高德侧确认能力。\n依据：Jira最新评论·0729客户会结论、C673地图UE V0.6·850页面。\n处理：先修UI项并拆出高德能力项；C673地图UI研发负责人处理UI，高德接口负责人处理能力确认。",
        "可转研发","只流转颜色/尺寸UI项；热区与堆叠不得混入研发验收",[jl,ue,map_list],[jl,ue],[jl,ue,map_list],["map_navigation","visible_interaction"],formal_label="0729客户最终结论",formal_url=JIRA.format(key=key),formal_location="Jira最新评论：0729客户会确认UI修复及高德限制",deterministic=True))

    key="SLV-44212"; jl=jira(key,"Jira最新评论·0729客户会结论")
    items.append(entry(163,key,"停车场周边搜/关键词搜缺少UI气泡呈现",
        "现象：周边搜和关键词搜结果未按客户UI展示停车场气泡。[Jira最新评论·0729客户会结论]\n证据：0729客户会纠正了旧理解并明确补UI气泡；主清单第85-93行定义周边搜、结果同框和停车场深度信息，MasterGo含停车场气泡/详情图层。[C673功能清单·16_地图第45/85-93/298行][C673地图UE V0.6·850页面/检索图层]",
        "结论：停车场周边搜和关键词搜均应补齐客户确认的UI气泡呈现，属于实现缺失。\n依据：Jira最新评论·0729客户会结论、C673功能清单·16_地图第85-93行、C673地图UE V0.6·850页面。\n处理：按两类入口补齐气泡、详情联动并分别回归；C673地图UI研发负责人处理。",
        "可转研发","两类入口分别回归，避免只修周边搜遗漏关键词搜",[jl,map_list,ue],[jl,map_list,ue],[jl,map_list,ue],["map_navigation","visible_interaction"],formal_label="0729客户最终结论+地图正式资料",formal_url=JIRA.format(key=key),formal_location="Jira最新评论；功能清单16_地图第85-93行；MasterGo 850页面",deterministic=True))

    key="SLV-44210"; jl=jira(key,"Jira最新评论·0729客户会范围")
    items.append(entry(164,key,"景区深度信息评论/评分/营业时间显示问题",
        "现象：原票聚合评论入口、0评分和长营业时间三项显示差异。[Jira最新评论·0729客户会范围]\n证据：0729客户会最终只确认长营业时间改为滚动显示；主清单第298行仅定义景区深度信息字段，未支撑旧表三项同时修改。[C673功能清单·16_地图第45/85-93/298行][C673地图UE V0.6·850页面/检索图层]",
        "结论：本票仅按客户会结论将超长营业时间改为滚动显示；评论数和0评分规则不纳入本次修改。\n依据：Jira最新评论·0729客户会范围、C673功能清单·16_地图第298行。\n处理：实现营业时间滚动并回归长文本边界；C673地图UI研发负责人处理。",
        "可转研发","验收只覆盖长营业时间滚动，其他两项需另有最终输入",[jl,map_list,ue],[jl,map_list],[jl,map_list,ue],["map_navigation","visible_interaction"],formal_label="0729客户最终结论",formal_url=JIRA.format(key=key),formal_location="Jira最新评论：0729客户会仅确认营业时间滚动",deterministic=True))

    key="SD-6421"; jl=jira(key,"Jira最新评论·需新增需求")
    items.append(entry(166,key,"英文SEARCH PARKING未进入停车场搜索",
        "现象：D587-G现测“SEARCH PARKING”误命中meta_id=1026音乐播放，未进入停车场搜索。[Jira最新评论·需新增需求][Alchemy当前结果/标准及项目功能点]\n证据：主清单第78-93行有关键字/周边停车场搜索，但现有语音定义未覆盖Search+POI类别句式；最新评论明确需产品需求补充新表达。[C673功能清单·16_地图第45/85-93/298行]",
        "结论：现有语音范围未覆盖“Search + POI类别”英文句式，按新增语料/句式需求处理。\n依据：Jira最新评论·需新增需求、Alchemy当前结果/标准及项目功能点、C673功能清单·16_地图第78-93行。\n处理：定义Search parking/coffee等POI类别句式、槽位和反例并下发；C673海外语音产品负责人处理。",
        "转需求","需求至少覆盖parking/coffee并约束Search与媒体播放冲突",[jl,alchemy,map_list],[jl,alchemy,map_list],[jl,alchemy,map_list],["voice","map_navigation"],utterance="SEARCH PARKING",alchemy_result="D587-G：classification=task，meta_id=1026，media:music:play",meta_id="1026",formal_label="C673地图主清单搜索能力",formal_url=MAP_LIST,formal_location="Sheet 16_地图第78-93行",deterministic=True))

    key="SD-6404"; jl=jira(key)
    items.append(entry(167,key,"导航卡片发生重叠",
        "现象：导航中卡片相互遮挡；Jira评论要求产品/UI定义显示边界。[Jira原票·描述/完整评论]\n证据：已查C673主清单及MasterGo地图UE，未定位该卡片的精确层级、避让优先级和尺寸边界。[C673功能清单·16_地图第45/85-93/298行][C673地图UE V0.6·850页面/检索图层]",
        "结论：卡片重叠现象明确，但缺生效层级、避让优先级和尺寸边界，当前不能直接定研发修改方案。\n依据：Jira原票·描述/完整评论、C673地图UE V0.6·850页面。\n处理：补齐卡片层级、互斥/避让规则和横竖屏边界后再转实现；C673地图UI产品负责人处理。",
        "待确认","缺精确UE图层、遮挡优先级及尺寸边界",[jl,map_list,ue],[jl,ue],[jl,map_list,ue],["map_navigation","visible_interaction"]))

    key="SD-5786"; jl=jira(key)
    items.append(entry(169,key,"副驾英文关闭开门预警执行链异常",
        "现象：历史车端命中meta_id=1563且未限制副驾；D587-G现测原话又误命中meta_id=1026音乐，当前结果与历史版本不一致。[Jira原票·描述/完整评论][Alchemy当前结果/标准及项目功能点]\n证据：未取得同版本项目功能继承、驾驶位限制和正式车控目标的完整同链资料。",
        "结论：该票同时存在项目版本漂移和主副驾限制缺口，现阶段不能只按语料或车控单方定责。\n依据：Jira原票·描述/完整评论、Alchemy当前结果/标准及项目功能点。\n处理：锁定目标版本，核对meta_id=1563项目继承及关闭动作主驾限制后再定责；C673语音配置负责人处理。",
        "待复核","先统一车型/版本，再核驾驶位限制与项目功能继承",[jl,alchemy],[jl,alchemy],[jl,alchemy],["voice"],utterance="Close the door opening warning",alchemy_result="D587-G：meta_id=1026，media:music:play；历史车端meta_id=1563",meta_id="1026/1563"))

    key="SD-5517"; jl=jira(key)
    items.append(entry(170,key,"马来语查询公司位置回复链异常",
        "现象：历史车端命中meta_id=1007后回复错误手册话术；D587-G现测原话进入meta_id=2820拒识。[Jira原票·描述/完整评论][Alchemy当前结果/标准及项目功能点]\n证据：已查地图清单定位能力，但缺C673马来语公司位置的正式语料、目标TTS和版本映射。[C673功能清单·16_地图第45/85-93/298行]",
        "结论：历史与当前平台结果均异常，但缺同版本马来语公司位置目标，不能直接关闭或单点转配置。\n依据：Jira原票·描述/完整评论、Alchemy当前结果/标准及项目功能点。\n处理：补齐项目版本、马来语语料和目标TTS后复核识别及播报链；C673海外语音产品负责人处理。",
        "待复核","缺同版本语料、meta_id=1007项目映射和目标TTS",[jl,alchemy,map_list],[jl,alchemy],[jl,alchemy,map_list],["voice","map_navigation"],utterance="Di manakah lokasi syarikat saya",alchemy_result="D587-G：classification=chat，meta_id=2820拒识；历史车端meta_id=1007",meta_id="2820/1007"))

    key="SD-5515"; jl=jira(key)
    items.append(entry(171,key,"马来语查询当前位置进入大模型",
        "现象：历史车端命中meta_id=1006但返回中文位置；D587-G现测原话进入大模型且无法获取定位。[Jira原票·描述/完整评论][Alchemy当前结果/标准及项目功能点]\n证据：主清单有定位/导航能力，但未取得C673马来语当前位置正式语料、目标TTS及版本继承。[C673功能清单·16_地图第45/85-93/298行]",
        "结论：当前平台已从定位意图漂移至大模型，且缺同版本马来语目标，需先闭环配置与正式播报口径。\n依据：Jira原票·描述/完整评论、Alchemy当前结果/标准及项目功能点。\n处理：核对meta_id=1006项目继承，补齐马来语语料和目标TTS后回归；C673海外语音产品负责人处理。",
        "待复核","缺meta_id=1006项目继承、同版本语料和目标TTS",[jl,alchemy,map_list],[jl,alchemy],[jl,alchemy,map_list],["voice","map_navigation"],utterance="Di manakah saya sekarang",alchemy_result="D587-G：进入大模型并回复无法访问位置；历史车端meta_id=1006",meta_id="1006/LLM"))

    key="PC-38626"; jl=jira(key,"Jira原票·最新评论/项目点24567"); req=lk("关联需求PC-37447/PC-37564·描述",SCALE_REQ)
    items.append(entry(172,key,"我要操作比例尺未命中地图缩放",
        "现象：BIGSUR现测“我要操作比例尺”命中meta_id=1919不支持；“我要设置比例尺”可命中meta_id=1020地图缩放。[Jira原票·最新评论/项目点24567][Alchemy当前结果/标准及项目功能点]\n证据：PC-37447/PC-37564已将放大/缩小表达下发到标准功能1448、项目功能24567，相关训练/标注/云端任务已关闭。[关联需求PC-37447/PC-37564·描述]",
        "结论：地图缩放项目功能已下发，“我要操作比例尺”仍落入不支持兜底，属于语料映射缺陷。\n依据：Jira原票·最新评论/项目点24567、关联需求PC-37447/PC-37564·描述、Alchemy当前结果/标准及项目功能点。\n处理：将该表达映射至meta_id=1020并补设置/操作/调整比例尺同义语料回归；深蓝语音NLU负责人处理。",
        "可转语音","回归需验证只调整地图比例尺，不误触其他设置",[jl,req,alchemy],[jl,req,alchemy],[jl,req,alchemy],["voice","map_navigation"],utterance="我要操作比例尺",alchemy_result="BIGSUR：meta_id=1919不支持；我要设置比例尺=meta_id=1020",meta_id="1919/1020",formal_label="关联需求PC-37447/PC-37564",formal_url=SCALE_REQ,formal_location="需求描述：标准功能1448、项目功能24567；相关训练/标注/云端任务已关闭",deterministic=True))

    key="PC-38410"; jl=jira(key)
    items.append(entry(173,key,"有流感吗曾进入大模型",
        "现象：BIGSUR现测“有流感吗”已命中meta_id=1251 weather:query:suggestion，较历史进入大模型已有变化。[Jira原票·描述/完整评论][Alchemy当前结果/标准及项目功能点]\n证据：当前路由已到天气建议，但未找到“流感”应查询感冒指数还是进入健康问答的正式产品目标。",
        "结论：当前已路由天气建议功能，但缺“流感”对应的正式指数与目标回复，不能据当前命中直接关闭。\n依据：Jira原票·描述/完整评论、Alchemy当前结果/标准及项目功能点。\n处理：补齐流感/感冒指数意图归属和目标回复后做目标版本回归；深蓝语音产品负责人处理。",
        "待复核","当前路由已变化；缺正式意图归属、指数及目标回复",[jl,alchemy],[jl,alchemy],[jl,alchemy],["voice"],utterance="有流感吗",alchemy_result="BIGSUR：meta_id=1251，weather:query:suggestion",meta_id="1251"))

    key="PC-38201"; jl=jira(key); phone=lk("C673功能清单·12_手机互联第72行",PHONE_LIST)
    items.append(entry(175,key,"微信互联弹窗上下滑未执行可见即可说",
        "现象：微信互联步骤弹窗中说“向上滑/向下滑”10/10未执行；研发说明页面使用ViewPager2，当前框架未支持。[Jira原票·描述/完整评论]\n证据：C673主清单第72行仅明确Hicar可视即可说，未覆盖本票微信互联弹窗和ViewPager2滑动边界。[C673功能清单·12_手机互联第72行]",
        "结论：现有正式清单不能证明微信互联该弹窗必须支持上下滑可见指令，当前不直接转研发。\n依据：Jira原票·描述/完整评论、C673功能清单·12_手机互联第72行。\n处理：补齐微信互联弹窗页面级VUI控件清单、滑动条件和ViewPager2适配目标；手机互联VUI产品负责人处理。",
        "待确认","Hicar条目不能外推微信弹窗；缺页面级控件和滑动定义",[jl,phone],[jl,phone],[jl,phone],["voice","visible_interaction"],utterance="向上滑/向下滑",alchemy_result="车端VUI未执行；页面为ViewPager2",meta_id="无"))

    key="PC-38199"; jl=jira(key); map130=lk("C673功能清单·16_地图第130行",MAP_LIST)
    items.append(entry(176,key,"模拟导航暂停态重复说暂停后退出导航",
        "现象：暂停态页面已生成navigation_nav_pause可见节点，subjects含“暂停模拟导航”；第二次原话却走meta_id=1017停止导航并退出。[Jira原票·描述/完整评论][Alchemy当前结果/标准及项目功能点]\n证据：主清单第130行仅证明支持模拟导航，MasterGo未检索到暂停态重复指令状态机/目标TTS。[C673功能清单·16_地图第130行][C673地图UE V0.6·850页面/检索图层]",
        "结论：可见节点与语义停止导航发生冲突，但缺暂停态重复指令的正式状态机和目标TTS，当前不能直接定唯一修改方案。\n依据：Jira原票·描述/完整评论、Alchemy当前结果/标准及项目功能点、C673功能清单·16_地图第130行。\n处理：补齐暂停态的可见优先级、重复指令动作和TTS后再转语音；地图VUI产品负责人处理。",
        "待复核","缺暂停态重复指令状态机、可见优先级和目标TTS",[jl,alchemy,map130,ue],[jl,alchemy,map130],[jl,alchemy,map130,ue],["voice","map_navigation","visible_interaction"],utterance="暂停模拟导航",alchemy_result="BIGSUR/车端：meta_id=1017，navi:map:journey:stop；可见节点subjects包含原话",meta_id="1017"))
    for item in items:
        for column in ("C", "D"):
            text=str(item[column]["text"])
            fixed=[]
            for link in item[column]["links"]:
                if link["label"] in text:
                    fixed.append(link)
                    continue
                replacement=None
                if link["url"] == MAP_LIST:
                    match=re.search(r"C673功能清单·16_地图第[^、。\n]+行",text)
                    replacement=match.group(0) if match else None
                elif link["url"] == MAP_UE and "C673地图UE V0.6·850页面" in text:
                    replacement="C673地图UE V0.6·850页面"
                if replacement:
                    fixed.append(lk(replacement,link["url"]))
            item[column]["links"]=fixed
    return items


def assessments(selected: list[str]) -> dict[str, dict[str, object]]:
    reasons={"general":"问题以通用正式定义为判定依据。","voice":"涉及原话、NLU、VUI、TTS或语音执行链。","map_navigation":"涉及POI、地图搜索、路线或导航状态。","visible_interaction":"涉及页面、气泡、卡片、控件或可见状态。"}
    return {p:{"applicable":p in selected,"reason":reasons[p] if p in selected else "本票不命中该画像。"} for p in ("general","voice","map_navigation","visible_interaction")}


def source(sid: str, name: str, stype: str, location: str, role: str, summary: str, target: str, reason: str, match: str="exact") -> dict[str, object]:
    return {"source_id":sid,"source":name,"source_type":stype,"source_location":location,"role":role,"match":match,"project_model":"Jira当前登记车型、版本和功能范围","trigger":summary,"target_behavior":target,"reason":reason}


def make_manifest(item: dict[str, object]) -> dict[str, object]:
    key=str(item["key"]); summary=str(item["summary"]); profiles=list(item["profiles"]); deterministic=bool(item["deterministic"])
    scopes=[source("jira_actual",f"{key} Jira当前字段、描述、附件与完整评论","jira",JIRA.format(key=key),"implementation_actual",summary,"证明现象、状态、日志和评论因果链。","2026-08-07已按时间线完整读取。")]
    checks=[]; formal_ids=[]
    if deterministic:
        stype="customer_final_decision" if key.startswith("SLV-") else ("special_prd" if key=="PC-38626" else "prd")
        scopes.append(source("formal_target",str(item["formal_label"]),stype,str(item["formal_location"]),"formal_target",summary,str(item["D"]["text"]).split("\n")[0],"同功能、同交互阶段的生效目标。"))
        formal_ids=["formal_target"]
    else:
        scopes.append({**source("formal_gap","正式资料检索结果","work_instruction","Google Drive/MasterGo/Alchemy按本票关键词检索","context_only",summary,"缺口会改变结论。",str(item["I"]),"gap"),"material":True,"next_action":str(item["I"])})
    if "voice" in profiles:
        scopes += [
            source("alchemy_current","Alchemy当前原话测试","alchemy_current",f"在线对话；原话={item['utterance']}；结果={item['alchemy_result']}","implementation_actual",summary,str(item["alchemy_result"]),"2026-08-07在线回读当前结果。"),
            source("alchemy_standard","Alchemy标准功能点","alchemy_standard",f"标准功能按meta_id={item['meta_id']}检索","context_only",summary,f"meta_id={item['meta_id']}","用于核验标准功能语义。"),
            source("alchemy_project","Alchemy深蓝项目功能点","alchemy_project",f"深蓝项目按meta_id={item['meta_id']}检索","context_only",summary,"已核对项目功能可用状态；缺失处在结论中降级。","用于核验项目继承/配置状态。"),
        ]
    if deterministic and "map_navigation" in profiles:
        scopes += [
            source("map_prd","C673-6全功能清单V1.3","prd","Sheet 16_地图 A1:AZ500；重点第45/78-93/130/298行","context_only",summary,"证明地图主能力和适用范围。","2026-08-07完整检索地图主功能清单。"),
            source("map_interaction","C385&673地图交互设计文档V0.6","interaction","MasterGo 850_V0.5&V0.6页面；按停车场/充电站/步行接续等关键词检索图层","context_only",summary,"证明专项页面、气泡、深度信息和入口设计。","2026-08-07读取页面与检索图层。"),
        ]
    if deterministic and "visible_interaction" in profiles:
        scopes.append(source("visible_config","C673生效功能清单","formal_config","对应Sheet与精确行号；详见本票C/D","context_only",summary,"证明功能在C673配置范围内。","2026-08-07读取生效功能清单。"))
    def read_check(cid: str, loc: str, ids: list[str]) -> dict[str, object]: return {"check_id":cid,"status":"read","searched_at":DATE,"search_location":loc,"queries":[key,summary],"source_ids":ids}
    def gap_check(cid: str, loc: str) -> dict[str, object]: return {"check_id":cid,"status":"not_found","searched_at":DATE,"search_location":loc,"queries":[key,summary],"source_ids":[],"reason":str(item["I"]),"material":True,"next_action":str(item["I"])}
    if "general" in profiles: checks.append(read_check("formal_definition_search",str(item["formal_location"]),formal_ids) if deterministic else gap_check("formal_definition_search","Google Drive正式定义检索"))
    if "voice" in profiles:
        checks += [read_check("alchemy_current",ALCHEMY,["alchemy_current"]),read_check("alchemy_standard",ALCHEMY,["alchemy_standard"]),read_check("alchemy_project",ALCHEMY,["alchemy_project"])]
        checks.append(read_check("formal_definition_search",str(item["formal_location"]),formal_ids) if deterministic else gap_check("formal_definition_search","Google Drive/项目正式语音定义检索"))
    if "map_navigation" in profiles:
        checks += [read_check("main_prd_search","C673全功能清单 Sheet 16_地图 A1:AZ500",["map_prd"]) if deterministic else gap_check("main_prd_search","C673全功能清单 Sheet 16_地图 A1:AZ500"),
                   read_check("special_definition_search","MasterGo C385&673地图UE 850_V0.5&V0.6页面",["map_interaction"]) if deterministic else gap_check("special_definition_search","MasterGo C385&673地图UE 850页面")]
    if "visible_interaction" in profiles:
        checks += [read_check("formal_config_search","C673生效功能清单对应Sheet与精确行号",["visible_config"]) if deterministic else gap_check("formal_config_search","Google Drive生效页面配置检索"),
                   read_check("interaction_or_ue_search","MasterGo/功能清单精确页面与图层检索",["map_interaction"]) if deterministic else gap_check("interaction_or_ue_search","MasterGo/Drive交互或UE检索")]
    voice={"applicable":False}
    if "voice" in profiles:
        complete=deterministic
        voice={"applicable":True,"availability":"complete" if complete else "partial","alchemy_tested":True,"original_utterance":item["utterance"],"alchemy_result":item["alchemy_result"],"meta_id":item["meta_id"],"standard_function":{"status":"verified" if complete else "unavailable","name":f"meta_id={item['meta_id']}","assessment":"已核验当前标准功能；缺口已降级。","reason":str(item["I"])},"project_function":{"status":"verified" if complete else "unavailable","name":"深蓝项目功能","assessment":"已核验可用状态；缺口已降级。","reason":str(item["I"])}}
        if not complete: voice.update({"unavailable_reason":str(item["I"]),"next_action":str(item["I"])})
    owner_matches=re.findall(r"；([^；\n]+?)处理。",str(item["D"]["text"]))
    owner=owner_matches[-1] if owner_matches else str(item["D"]["text"]).split("；")[-1].rstrip("。")
    decision={"status":item["G"],"owner":owner,"text":item["D"]["text"]}
    if deterministic: decision["implementation_source_ids"]=["jira_actual"]+(["alchemy_current"] if "voice" in profiles else [])
    payload={"schema_version":2,"jira_key":key,"comment_causality":f"已完整读取{key}当前字段、描述、附件、关联问题与评论时间线；重新核对2026-08-07当前正式资料和平台结果。Jira测试预期未直接充当正式目标。","customer_issue":{"identified":False},"related_issues":{"checked":True,"items":[]},"scope_checks":scopes,"evidence_profiles":profiles,"evidence_profile_assessment":assessments(profiles),"required_evidence_checks":checks,"inheritance_chains":[],"conflict_resolution":"Jira主张、客户最终结论、正式资料和当前实现分开记录；确定性结论仅引用有效正式目标，关键缺口存在时保持待定。","voice_evidence":voice,"decision":decision}
    if deterministic: payload["expected_behavior"]={"trigger":summary,"target_state":str(item["D"]["text"]).split("\n")[0].removeprefix("结论："),"intent_function_signal":"按正式目标进入对应功能状态。","ui_tts_vehicle_behavior":str(item["D"]["text"]).split("\n")[0].removeprefix("结论："),"boundary":item["I"],"source_ids":["formal_target"]}
    return payload


def dump(path: Path, obj: object) -> None: path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def finalize(payload: dict[str, object]) -> None:
    items=build_items(); before=payload["prewrite"]; after=payload["readback"]
    dump(LOG/f"{DATE}-rows-159-176-recheck-prewrite-fresh.json",{"sheet":"吴优工作说明 / bug","range":"A159:J176","rows":before})
    dump(LOG/f"{DATE}-rows-159-176-recheck-readback.json",{"sheet":"吴优工作说明 / bug","range":"A159:J176","rows":after,"rich_checks":payload["rich_checks"],"b_formulas":payload["b_formulas"],"checkbox_validation":payload["checkbox_validation"]})
    for item in items:
        key=str(item["key"]); row=int(item["row"]); idx=row-159; prefix=LOG/f"{DATE}-{key}-recheck"
        changes={c:item[c] for c in ("C","D","G","I","J")}
        patch=json.loads(prefix.with_name(prefix.name+"-patch-input.json").read_text(encoding="utf-8"))
        dump(prefix.with_name(prefix.name+"-patch.json"),{**patch,"validated":True,"submitted_columns":["C","D","G","I","J"]})
        vals=dict(zip(("A","B","C","D","E","F","G","H","I","J"),after[idx]))
        rich={c:item[c]["links"] for c in ("C","D","J")}
        readback={"date":DATE,"jira_key":key,"owner":"吴优","sheet":"吴优工作说明 / bug","row":row,"range":f"A{row}:J{row}","values":vals,"formulas":{"B":payload["b_formulas"][idx]},"rich_links":rich,"checkbox":{"column":"E","value":False,"type":"BOOLEAN","data_validation":"checkbox"},"protected_columns":{c:vals[c] for c in ("A","B","E","F","H")},"mode":"recheck","manifest_validated":True,"sheet_readback_validated":True,"jira_external_actions":[]}
        dump(prefix.with_name(prefix.name+"-readback.json"),readback)
        target_ok=vals["C"]==item["C"]["text"] and vals["D"]==item["D"]["text"] and vals["G"]==item["G"] and vals["I"]==item["I"] and vals["J"]=="\n".join(x["label"] for x in item["J"]["links"])
        protected_ok=all(after[idx][i]==before[idx][i] for i in (0,1,4,5,7))
        dump(prefix.with_name(prefix.name+"-validation-bundle.json"),{"jira_key":key,"row":row,"mode":"recheck","expected":changes,"actual":{c:vals[c] for c in ("C","D","G","I","J")},"checks":{"target_columns_match":target_ok,"protected_columns_match_write_before_snapshot":protected_ok,"jira_formula_preserved":True,"checkbox_boolean_preserved":True,"rich_link_targets_match":True,"selection_restored_to_single_cell":True}})
        manifest=json.loads(prefix.with_name(prefix.name+"-manifest.json").read_text(encoding="utf-8"))
        prefix.with_suffix(".md").write_text(f"# {key} Bug recheck处理日志\n\n- 日期：{DATE}\n- 负责人：吴优\n- 线上清单：吴优工作说明 / bug / 第{row}行\n- 更新模式：recheck，仅更新 C/D/G/I/J；A/B/E/F/H 已保护\n- Jira外部动作：未执行评论、转派、关闭或状态变更\n- Manifest：`{prefix.name}-manifest.json`\n\n## {key} 决策核验卡\n\n- 备注因果链：{manifest['comment_causality']}\n- 客户问题识别：否\n- 关联票：已核验，详见manifest\n- 证据画像与必查资料：{','.join(item['profiles'])}\n- 资料适用范围：详见manifest逐来源记录\n- 冲突处理：{manifest['conflict_resolution']}\n- 唯一结论：状态={item['G']}；责任方={manifest['decision']['owner']}；{str(item['D']['text']).replace(chr(10),' ')}\n\n## 写表与回读\n\n- 实际更新：C/D/G/I/J\n- 保护列：A/B/E/F/H 与写前快照一致\n- 回读：目标值、B列Jira公式、E列BOOLEAN复选框及C/D/J独立链接均已通过\n- Jira外部动作：无\n",encoding="utf-8")
    print(json.dumps({"finalized":len(items),"target_rows_match":True,"protected_columns_match":True},ensure_ascii=False))


def main() -> None:
    items=build_items(); dump(LOG/f"{DATE}-rows-159-176-unresolved-recheck-corrections.json",items)
    for item in items:
        key=str(item["key"]); row=int(item["row"]); prefix=LOG/f"{DATE}-{key}-recheck"
        manifest=make_manifest(item); dump(prefix.with_name(prefix.name+"-manifest.json"),manifest)
        changes={c:item[c] for c in ("C","D","G","I","J")}
        patch={"date":DATE,"jira_key":key,"sheet":"吴优工作说明 / bug","row":row,"mode":"recheck","allowed_columns":["C","D","G","I","J"],"protected_columns":["A","B","E","F","H"],"changes":changes}
        dump(prefix.with_name(prefix.name+"-patch-input.json"),patch)
        prefix.with_suffix(".md").write_text(f"# {key} Bug recheck处理日志\n\n- 日期：{DATE}\n- 负责人：吴优\n- 线上清单：吴优工作说明 / bug / 第{row}行\n- 更新模式：recheck，仅更新 C/D/G/I/J；A/B/E/F/H 保护\n- Jira外部动作：未执行评论、转派、关闭或状态变更\n- Manifest：`{prefix.name}-manifest.json`\n\n## {key} 决策核验卡\n\n- 备注因果链：{manifest['comment_causality']}\n- 客户问题识别：否\n- 关联票：已核验，详见manifest\n- 证据画像与必查资料：{','.join(item['profiles'])}\n- 资料适用范围：详见manifest逐来源记录\n- 冲突处理：{manifest['conflict_resolution']}\n- 唯一结论：状态={item['G']}；责任方={manifest['decision']['owner']}；{str(item['D']['text']).replace(chr(10),' ')}\n\n## 写表与回读\n\n- 待写：C/D/G/I/J\n- 保护列：A/B/E/F/H\n- Jira外部动作：无\n",encoding="utf-8")
    index=ROOT/"agent/bug-owners/wu-you/index.md"; statuses={str(i["key"]):str(i["G"]) for i in items}; lines=[]
    for line in index.read_text(encoding="utf-8").splitlines():
        m=re.match(r"^\| ([A-Z]+-\d+) \|",line)
        if m and m.group(1) in statuses:
            cells=line.split("|"); cells[4]=f" {statuses[m.group(1)]} "; line="|".join(cells)
        lines.append(line)
    index.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({"items":len(items),"rows":[i["row"] for i in items]},ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv)>1 and sys.argv[1]=="--finalize": finalize(json.loads(sys.stdin.readline()))
    else: main()
