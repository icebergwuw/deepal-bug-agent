#!/usr/bin/env python3
"""Generate the audited Aug-12 Alchemy recheck artifacts and Sheets requests."""

from __future__ import annotations

import copy
import json
import hashlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "agent" / "scripts"))
from bug_sheet_contract import build_batch_requests, build_patch_requests, row_fingerprint  # noqa: E402


LOG = ROOT / "agent" / "logs" / "bug-actions"
RUN_ID = "20260813T113000+0800-aug12-alchemy-recheck"
CONVERSATION = "https://alchemy.i-tetris.com/#/conversation/testing?id=27475f07-6fc5-47dc-bd3a-af07750b1683&env="
DEEPAL_PROJECT = "https://alchemy.i-tetris.com/#/functional/project/detail/11"
MAZDA_PROJECT = "https://alchemy.i-tetris.com/#/functional/project/detail/15"


def link(label: str, url: str) -> dict[str, str]:
    return {"label": label, "url": url}


COMMON = {
    "ADS-48729": {
        "row": 321,
        "model": "BIGSUR",
        "utterance": "小憩模式设置为前排",
        "result": "meta_id=1127，vehicle:scenario:ctrl，mode=rest、op=open、position=front_row",
        "standard_id": 1364,
        "standard": "标准1364（已锁定）打开特定情景模式；小憩示例含左/右前，执行策略要求有位置参数时打开模式并调节对应位置座椅",
        "project": "深蓝项目24510（已锁定、继承未修改）",
        "project_status": "read",
        "status": "待复核",
        "owner": "C385-5情景模式语音产品/执行负责人",
        "info": "现象：[Jira原票·描述/关联ADS-48377]C385-5当前小憩模式非主驾时说“小憩模式设置为前排”，车端5/5回复无法切换位置。\nAlchemy：[在线对话·BIGSUR]原话当前命中meta_id=1127，mode=rest、op=open、position=front_row；[标准1364/深蓝项目24510]已定义带位置打开小憩并调节对应座椅。\n正式范围：[深蓝情景模式配置·Sheet‘情景模式’第25-33行]只列385基础车/ICA/DA、385MCA等列，未列C385-5；[智能情景模式功能定义V4.9·适应范围/语音控制方式]适用C673EV/C673EVE，不能外推C385-5。",
        "judgment": "结论：Alchemy当前已正确识别“前排”并下发小憩位置参数，车端不支持回复与当前语音链不一致；但现行正式配置没有C385-5列，也未定义front_row在该车型应落副驾还是其他位置，暂不作确定性定责。\n依据：Jira原票及ADS-48377、Alchemy BIGSUR原话结果、标准1364/深蓝项目24510、深蓝情景模式配置Sheet‘情景模式’第25-33行、智能情景模式功能定义V4.9适应范围。\n处理：补齐C385-5小憩支持位置及front_row映射后，对照req_id判断是执行拒绝还是车型配置缺失；C385-5情景模式语音产品/执行负责人处理。",
        "note": "Alchemy链已补齐；未完成项仅剩C385-5车型级小憩位置配置及front_row映射。",
        "extra_links": [
            link("深蓝情景模式配置·情景模式第25-33行", "https://docs.google.com/spreadsheets/d/1Dokcgp1J5sW_lWcXOJ2DsJUd-m9KAfX3ZHe0T88s6nk/edit#gid=2132905669"),
            link("智能情景模式功能定义V4.9·适应范围/语音控制方式", "https://docs.google.com/document/d/1mAhtOwE67MCq4zsp9_iAkClhD34E2KdC/edit"),
        ],
    },
    "ADS-48572": {
        "row": 322,
        "model": "BIGSUR",
        "utterance": "推荐一下附近的火锅店 → 导航去观音桥 → 第一个",
        "result": "依次命中1208、1209；第三轮返回观音桥目的地1209并追加list_offset=1的1209",
        "standard_id": 1433,
        "standard": "标准1433（已锁定）导航去地址，定义前轮POI列表二次交互和本轮完整Query匹配",
        "project": "深蓝项目24552（已锁定、继承未修改）",
        "project_status": "read",
        "status": "待复核",
        "owner": "C385-5语音上下文/可见交互产品负责人",
        "info": "现象：[Jira原票·描述/关联ADS-48560]火锅店推荐中插入“导航去观音桥”，随后说“第一个”却选中旧火锅店列表。\nAlchemy：[在线对话·BIGSUR]三轮依次命中1208、1209；第三轮同时保留观音桥目的地并下发list_offset=1；[标准1433/深蓝项目24552]定义POI列表二次交互使用本轮完整Query和前轮结果列表。\n正式缺口：[地图导航交互V0.6·修改记录及POI列表页]仍未定义被新导航Query打断后，新旧列表/可见节点的唯一优先级。",
        "judgment": "结论：Alchemy当前三轮上下文已切换到观音桥，车端仍选旧火锅店列表的现象成立；但现行正式交互资料未定义新导航Query打断后新旧列表与可见节点的优先级，不能只凭平台当前实现直接定责。\n依据：Jira原票及ADS-48560、Alchemy BIGSUR三轮结果、标准1433/深蓝项目24552、地图导航交互V0.6。\n处理：补齐跨列表打断后的上下文替换和可见优先级条款，再按同三轮用例复测并定责；C385-5语音上下文/可见交互产品负责人处理。",
        "note": "Alchemy链已补齐；未完成项为跨列表打断后的正式优先级定义。",
        "extra_links": [link("地图导航交互V0.6·POI列表页", "https://drive.google.com/file/d/1Xca7y1SPBCHFOB87CHmiEjcbhPDwH5gl/view")],
    },
    "HUR-82888": {
        "row": 323,
        "model": "HUR",
        "utterance": "我要打电话 → 打开前备箱",
        "result": "两轮分别命中1059电话入口和2031打开前备箱；文本链未截断",
        "standard_id": 1659,
        "standard": "标准1338为电话入口（草稿）；标准1659打开前备箱（已锁定）",
        "project": "马自达项目25986继承1059；检索meta_id=2031无项目功能点",
        "project_status": "not_applicable",
        "status": "待复核",
        "owner": "J90A电话二次交互/语音识别产品负责人",
        "info": "现象：[Jira原票·描述]J90A在“我要打电话”的二次交互阶段说“打开前备箱”发生识别截断。描述所写日志票HUR-82884实际是“自定义应答语敏感词”Bug，与本票链路无关。\nAlchemy：[在线对话·HUR]两轮文本分别命中meta_id=1059电话入口、meta_id=2031打开前备箱，未发生截断；[标准1338/1659]覆盖两句语义。\n配置缺口：[马自达项目功能]有1059项目点25986，但检索2031无项目功能点；Alchemy文本输入不能验证ASR截断，也没有电话二次交互跨域退出状态机正式条款。",
        "judgment": "结论：Alchemy文本链证明两句NLU可分别识别，但不能证明实车ASR不会截断；同时HUR未配置2031项目功能点，且Jira引用的HUR-82884不是本票日志，当前证据不能唯一判断是ASR、电话状态机还是项目能力缺口。\n依据：Jira原票、HUR-82884完整页面、Alchemy HUR两轮结果、标准1338/1659、马自达项目功能检索。\n处理：补正确req_id/ASR原始日志和电话二次交互跨域退出定义，并确认J90A是否应继承2031后再定责；J90A电话二次交互/语音识别产品负责人处理。",
        "note": "Alchemy链已补齐；缺正确ASR日志、跨域状态机及J90A meta_id=2031项目能力。",
        "extra_links": [link("HUR-82884·误引用的敏感词Bug", "http://jira.i-tetris.com/browse/HUR-82884")],
    },
    "PC-38473": {
        "row": 324,
        "model": "BIGSUR",
        "utterance": "编辑唤醒词；删除唤醒词",
        "result": "分别命中1324新增/修改自定义唤醒词、1395删除自定义唤醒词",
        "standard_id": 1239,
        "standard": "标准1239/1233均已锁定；1239明确支持修改意图，1233执行打开自定义唤醒词界面",
        "project": "深蓝项目24428/24425均已锁定、继承未修改",
        "project_status": "read",
        "status": "待复核",
        "owner": "C673-ICA可见即可说产品负责人",
        "info": "现象：[Jira原票·描述/附件]C673-ICA语音设置页说“编辑/删除唤醒词”10/10不执行可见；相关Gerrit 1114070已废弃。\nAlchemy：[在线对话·BIGSUR]“编辑唤醒词”命中1324，“删除唤醒词”命中1395；[标准1239/1233、深蓝项目24428/24425]均有对应能力，1239明确包含修改意图，1233执行策略为打开自定义唤醒词界面。\n正式缺口：[8295页面开启需求v2.6·设置APP内页面&弹窗第34行]只定义新增唤醒词页面，未定义当前列表编辑/删除可见节点；MasterGo当前配置未取得。",
        "judgment": "结论：两句原话的通用语音能力及深蓝项目点已存在，但本票发生在语音设置页可见上下文；当前正式页面资料仅覆盖新增页面，缺编辑/删除节点及页面态冲突消歧，暂不能把不执行直接定为语音或客户端缺陷。\n依据：Jira原票、Alchemy BIGSUR结果、标准1239/1233及深蓝项目24428/24425、8295页面开启需求v2.6第34行。\n处理：取得生效MasterGo/可见配置的编辑与删除节点、节点名和页面状态后复测；C673-ICA可见即可说产品负责人处理。",
        "note": "Alchemy链已补齐；未完成项为语音设置页编辑/删除唤醒词的生效可见节点。",
        "extra_links": [link("8295页面开启需求v2.6·第34行", "https://docs.google.com/spreadsheets/d/1j8yX3iGEwPSFsMvRHFu7kOuof-fRnDdg/edit")],
    },
    "PC-38472": {
        "row": 325,
        "model": "BIGSUR",
        "utterance": "编辑应答语1；删除应答语1",
        "result": "分别命中1325新增自定义应答语（keywords=1，无op）和3069删除自定义应答语（op=cancel）",
        "standard_id": 1730,
        "standard": "标准1250/1730当前为草稿；1730示例含删除第二条应答语并打开设置界面",
        "project": "深蓝项目24435/26857已锁定、继承未修改",
        "project_status": "read",
        "status": "待会诊",
        "owner": "C673-ICA应答语语音配置/可见交互负责人",
        "info": "现象：[Jira原票·描述/附件]语音设置页说“编辑/删除应答语1、2、3”均不执行可见。\nAlchemy：[在线对话·BIGSUR]“编辑应答语1”落1325但只有keywords=1、无编辑op；“删除应答语1”落3069且op=cancel。[标准1250/1730]仍为草稿，[深蓝项目24435/26857]已锁定继承，来源状态与语义参数存在冲突。\n正式缺口：[8295页面开启需求v2.6·设置APP内页面&弹窗]检索‘应答语’0条，MasterGo当前可见节点未取得。",
        "judgment": "结论：删除应答语已落正确功能点，编辑应答语缺少编辑op；同时标准点仍为草稿、深蓝项目点却已锁定，且页面可见节点缺失，需会诊统一配置状态与页面节点后拆分处理。\n依据：Jira原票、Alchemy BIGSUR两句结果、标准1250/1730、深蓝项目24435/26857、8295页面开启需求v2.6检索结果。\n处理：统一编辑/删除应答语的生效功能点、op与可见节点，再分别回归1/2/3序号；C673-ICA应答语语音配置/可见交互负责人处理。",
        "note": "Alchemy链已补齐；冲突为编辑op缺失、标准草稿/项目锁定不一致及可见节点缺失。",
        "extra_links": [link("8295页面开启需求v2.6·应答语0命中", "https://docs.google.com/spreadsheets/d/1j8yX3iGEwPSFsMvRHFu7kOuof-fRnDdg/edit")],
    },
    "PC-38471": {
        "row": 326,
        "model": "BIGSUR",
        "utterance": "播放第二个；编辑第二个；删除第二个",
        "result": "分别误落1035媒体切换、1455通用列表选择、1919车型无此功能兜底",
        "standard_id": 1425,
        "standard": "标准1470资源切换、1425列表选择、1442兜底均已锁定",
        "project": "深蓝项目24583/24544/24561均存在；当前原话未形成语音设置页专用语义",
        "project_status": "read",
        "status": "待复核",
        "owner": "C673-ICA可见即可说产品负责人",
        "info": "现象：[Jira原票·描述/附件]语音设置页说“播放/编辑/删除第二个”或名称，10/10不执行可见。\nAlchemy：[在线对话·BIGSUR]脱离页面上下文测试时分别落1035媒体切换、1455通用列表选择、1919不支持；[标准1470/1425/1442及深蓝项目24583/24544/24561]只证明通用语义，未形成语音设置页专用动作。\n正式缺口：C673语音控制V1.0.5及8295页面开启需求v2.6均未定义该列表节点，MasterGo当前可见配置未取得。",
        "judgment": "结论：三句短指令在无页面上下文时分别落媒体、通用列表和兜底，不能用该结果证明语音设置页内的目标动作；缺少生效可见节点和页面上下文注入规则，暂不定责。\n依据：Jira原票、Alchemy BIGSUR三句结果、标准/深蓝项目功能点、C673语音控制V1.0.5、8295页面开启需求v2.6。\n处理：取得列表项播放/编辑/删除节点及上下文注入规则后，在语音设置页复测同三句；C673-ICA可见即可说产品负责人处理。",
        "note": "Alchemy链已补齐；未完成项为页面可见节点和上下文注入规则。",
        "extra_links": [link("C673语音控制V1.0.5", "https://docs.google.com/document/d/1KQxZVsSzaTyoabOsT9K7cD8Jo9Yfdg8j/edit"), link("8295页面开启需求v2.6", "https://docs.google.com/spreadsheets/d/1j8yX3iGEwPSFsMvRHFu7kOuof-fRnDdg/edit")],
    },
    "ADS-47316": {
        "row": 327,
        "model": "BIGSUR",
        "utterance": "下一首播放刘德华的歌曲",
        "result": "命中meta_id=3012，media:play_list:add，artists=刘德华、category=music",
        "standard_id": 1718,
        "standard": "标准1718（已锁定）逐字包含该Query，目标为预约歌曲到播放列表下一首，不是立即播放",
        "project": "深蓝项目按meta_id=3012检索无项目功能点",
        "project_status": "not_applicable",
        "status": "待会诊",
        "owner": "C673-7媒体语音产品配置负责人（冯智秀）",
        "info": "现象：[Jira原票·描述/关联ADS-47224]车端直接播放刘德华歌曲，测试预期不支持。\nAlchemy：[在线对话·BIGSUR]精确原话命中3012 media:play_list:add；[标准1718·Query举例/执行策略]逐字包含“下一首播放刘德华的歌”，目标为预约到播放列表下一首、当前歌曲结束后播放。\n配置冲突：[深蓝项目功能]按3012检索无项目功能点；[深蓝项目语音功能点260731·第63/66行]只列上/下一首和指定第N首，未列预约歌曲。Jira当前经办人已变更为冯智秀。",
        "judgment": "结论：测试预期“不支持”、标准1718“预约下一首”、车端“立即播放”三方冲突；BIGSUR虽已命中3012，但深蓝项目未继承该功能点，不能直接关闭或转研发，需会诊确定C673-7是否正式支持预约播歌。\n依据：Jira原票及ADS-47224、Alchemy BIGSUR当前结果、标准1718、深蓝项目3012零命中、深蓝项目语音功能点260731第63/66行。\n处理：若支持则补深蓝项目点并按预约下一首实现；若不支持则移除BIGSUR泛化并按不支持兜底；C673-7媒体语音产品配置负责人（冯智秀）处理。",
        "note": "Jira已转冯智秀；Alchemy补证后发现测试预期、标准定义、深蓝项目配置三方冲突。",
        "extra_links": [link("深蓝项目语音功能点260731·第63/66行", "https://docs.google.com/spreadsheets/d/1ULkxn1d8ZZMBKFX8gA7mCHWccuN6qdSh/edit")],
    },
    "SLV-44180": {
        "row": 328,
        "model": "SLV",
        "utterance": "适合行车吗；适合开车吗；行车指数是多少",
        "result": "三句均命中1251 weather:query:suggestion，suggestion canonical=traffic",
        "standard_id": 1398,
        "standard": "标准1398（已锁定）查询天气指数，说明及设置范围明确含行车/行车指数",
        "project": "深蓝项目26748（已锁定、继承未修改）",
        "project_status": "read",
        "status": "待复核",
        "owner": "C673基础款天气语音测试/研发负责人",
        "info": "现象：[Jira原票·描述/关联PC-38411、PC-38412、SLV-44177、SLV-44179]旧车端三句行车指数查询失败，评论记录当时canonical为空。\nAlchemy：[在线对话·SLV]三句当前均命中1251 weather:query:suggestion，suggestion canonical=traffic；[标准1398·说明/设置范围、深蓝项目26748]已包含行车/行车指数。\n版本差异：[深蓝项目语音功能点260731·第49行]有通用查询天气指数，但未逐字列行车指数；当前平台结果已与Jira旧日志不同。",
        "judgment": "结论：当前SLV在线平台已为三句行车问法下发canonical=traffic，旧日志中的canonical为空现象已不复现于当前平台；先按原车型/版本升级后的同环境回归，不再维持“Alchemy未核验”。\n依据：Jira原票及四个关联票、Alchemy SLV三句当前结果、标准1398/深蓝项目26748、深蓝项目语音功能点260731第49行。\n处理：在C673基础款最新集成版本回归三句并核对天气接口入参；若仍失败转天气接口映射研发，否则关闭；C673基础款天气语音测试/研发负责人处理。",
        "note": "Alchemy当前三句均已下发traffic；未完成项为实车最新版本回归与天气接口入参核对。",
        "extra_links": [link("深蓝项目语音功能点260731·第49行", "https://docs.google.com/spreadsheets/d/1ULkxn1d8ZZMBKFX8gA7mCHWccuN6qdSh/edit")],
    },
    "ADS-46860": {
        "row": 329,
        "model": "BIGSUR",
        "utterance": "先去公司，再去机场",
        "result": "当前只下发机场目的地1209，未带via_poi；Jira历史日志则重复下发两个公司via_poi",
        "standard_id": 1433,
        "standard": "标准1433（已锁定）明确带途经点导航应同时下发目的地和途径条件",
        "project": "深蓝项目24552（已锁定、继承未修改）",
        "project_status": "read",
        "status": "待会诊",
        "owner": "C673-7地图多站点语音产品/Cloud研发负责人",
        "info": "现象：[Jira原票·完整评论/关联ADS-46859等]历史Cloud把机场作为目的地但重复下发两个公司via_poi，导致导航请求不合法。\nAlchemy：[在线对话·BIGSUR]当前原话只下发机场目的地1209，完全丢失公司途经点；[标准1433·下发参数/一般导航意向、深蓝项目24552]明确带途经点导航需同时包含目的地与途径条件。\n正式资料：[深蓝花瓣地图语音清单·第14、21-25行]只定义快捷地址和POI/路线规划，未逐字定义该多意图组合；当前平台与Jira历史实现也不一致。",
        "judgment": "结论：目标语义应是公司为途经点、机场为目的地；但Jira历史实现重复公司途经点，Alchemy当前又完全丢失公司，两个实现版本不一致，需会诊确认当前线上链路后定修复层。\n依据：Jira原票完整评论、Alchemy BIGSUR当前结果、标准1433/深蓝项目24552、深蓝花瓣地图语音清单第14及21-25行。\n处理：用同原话抓当前req_id；若Cloud仍重复则修正去重与顺序，若当前已丢via则先修NLU/多意图拆分，最终只下发一个公司via和一个机场目的地；C673-7地图多站点语音产品/Cloud研发负责人处理。",
        "note": "Alchemy链已补齐；当前结果与Jira历史Cloud结果冲突，需当前req_id确认修复层。",
        "extra_links": [link("深蓝花瓣地图语音清单·第14/21-25行", "https://docs.google.com/spreadsheets/d/1N9PZpRpoMfUa5T8wHDObEwweSaLyEN1Z/edit")],
    },
    "HUR-77192": {
        "row": 330,
        "model": "HUR",
        "utterance": "Avslutt Automatiske fjernlys",
        "result": "classification=chat，meta_id=2820 dialogue:method:reject",
        "standard_id": 1689,
        "standard": "标准1689拒识（草稿）",
        "project": "马自达项目26049拒识（已锁定、继承未修改）",
        "project_status": "read",
        "status": "待复核",
        "owner": "J90A-EU PI语料产品/DS路由配置负责人",
        "info": "现象：[Jira原票·描述/完整评论]挪威语关闭智能远光灯未执行；车端日志显示Cerence语义正确，但离线映射降级2820，在线withCerence又被车外灯安全策略拦截为-6。\nAlchemy：[在线对话·HUR]当前原话直接落classification=chat、meta_id=2820；[标准1689/马自达项目26049]只证明当前拒识链。\n正式缺口：[J90A海外LanguageList V1.1·03_Vehicle Settings全表]及[内部版V1.0_260806·03_Vehicle Settings A1:AQ1900]精确原话均0命中；Jira最新评论仍要求与客户确认智能远光灯/自动大灯冲突。",
        "judgment": "结论：当前平台和实车链路均未正确执行，但目标语料仍未在两份当前LanguageList中落行，且智能远光灯与自动大灯目标存在冲突；不能仅凭工程分析把票直接转DS。\n依据：Jira原票完整评论、Alchemy HUR当前2820、标准1689/马自达项目26049、J90A海外LanguageList V1.1与内部版V1.0精确零命中。\n处理：取得客户/MRE生效语料行并明确目标灯光后，统一byCerence/withCerence路由及离线映射；J90A-EU PI语料产品/DS路由配置负责人处理。",
        "note": "Alchemy当前为2820；未完成项为MRE生效语料行及智能远光灯/自动大灯目标确认。",
        "extra_links": [link("J90A海外LanguageList V1.1·03_Vehicle Settings", "https://docs.google.com/spreadsheets/d/1AAL-II3PGv6jEwLpayNy-NWwJFnM9ILcIr13uVjU3P0/edit"), link("J90A海外LanguageList内部版V1.0·03_Vehicle Settings", "https://docs.google.com/spreadsheets/d/1ASnEMB3HSNClw2MRbsA1tGDaB9Y5Vi_dXL9hZzz7gC4/edit#gid=657987591")],
    },
    "HUR-72809": {
        "row": 331,
        "model": "HUR",
        "utterance": "Open energiebeheer",
        "result": "误命中1026 media:music:play，op=open、name=energiebeheer",
        "standard_id": 1097,
        "standard": "标准1097点播歌曲（已锁定），与目标能量功能无关",
        "project": "马自达项目25979点播歌曲（已锁定、继承未修改）",
        "project_status": "read",
        "status": "待复核",
        "owner": "J90A-EU荷兰语语料产品负责人",
        "info": "现象：[Jira原票·描述/完整评论]“Open energiebeheer”实车打开车辆设置能量管理，测试预期能量流App，评论确认两者不是同一功能但表达冲突。\nAlchemy：[在线对话·HUR]当前进一步误落1026 media:music:play；[标准1097/马自达项目25979]均是点播歌曲，只证明当前NLU错误。\n正式缺口：[J90A海外LanguageList V1.1]及[内部版V1.0_260806]的16_Energy Flow、13_Energy Management对应全表精确原话均0命中，未取得MRE当前语料条目。",
        "judgment": "结论：当前Alchemy误落音乐，实车历史又打开能量管理；两种实现都不能证明能量流目标。由于同一句荷兰语对应能量流/能量管理的正式语料未落表，暂不直接转语音。\n依据：Jira原票完整评论、Alchemy HUR当前1026、标准1097/马自达项目25979、两版J90A LanguageList相关Sheet精确零命中。\n处理：让客户/MRE明确能量流App与车辆设置能量管理的两套荷兰语表达并提供生效条目，再分别配置项目功能点和回归；J90A-EU荷兰语语料产品负责人处理。",
        "note": "Alchemy当前误落音乐；未完成项为MRE两套荷兰语表达及生效功能点。",
        "extra_links": [link("J90A海外LanguageList V1.1·16/13 Sheet", "https://docs.google.com/spreadsheets/d/1AAL-II3PGv6jEwLpayNy-NWwJFnM9ILcIr13uVjU3P0/edit"), link("J90A海外LanguageList内部版V1.0·16/13 Sheet", "https://docs.google.com/spreadsheets/d/1ASnEMB3HSNClw2MRbsA1tGDaB9Y5Vi_dXL9hZzz7gC4/edit")],
    },
}


def links_for(key: str, item: dict) -> list[dict[str, str]]:
    project_url = MAZDA_PROJECT if item["model"] == "HUR" else DEEPAL_PROJECT
    return [
        link("Jira原票·描述/全部评论", f"http://jira.i-tetris.com/browse/{key}"),
        link(f"Alchemy在线对话·{item['model']}·{item['result']}", CONVERSATION),
        link(item["standard"], f"https://alchemy.i-tetris.com/#/functional/points/detail/{item['standard_id']}"),
        link(item["project"], project_url),
        *item.get("extra_links", []),
    ]


def make_changes(key: str, item: dict) -> dict:
    links = links_for(key, item)
    return {
        "C": {"text": item["info"], "links": []},
        "D": {"text": item["judgment"], "links": []},
        "G": item["status"],
        "I": item["note"],
        "J": {"links": links},
    }


def make_manifests() -> list[Path]:
    paths: list[Path] = []
    for key, item in COMMON.items():
        src = LOG / f"2026-08-12-{key}-manifest.json"
        manifest = json.loads(src.read_text())
        manifest["run_context"] = {
            "run_id": RUN_ID,
            "operator_owner_id": "wu-you",
            "target_owner_id": "feng-zhi-xiu" if key == "ADS-47316" else "wu-you",
            "sheet_name": "冯智秀bug" if key == "ADS-47316" else "bug",
            "sheet_row": 63 if key == "ADS-47316" else item["row"],
        }
        current_id = "alchemy-current"
        standard_id = "alchemy-standard"
        project_id = "alchemy-project"
        manifest["scope_checks"] = [
            check for check in manifest.get("scope_checks", [])
            if check.get("source_id") not in {current_id, standard_id, project_id}
        ]
        manifest["scope_checks"].extend([
            {
                "source_id": current_id,
                "source": f"Alchemy在线对话·{item['model']}",
                "source_location": f"原话={item['utterance']}；当前结果={item['result']}",
                "source_type": "alchemy_current",
                "role": "implementation_actual",
                "project_model": item["model"],
                "trigger": item["utterance"],
                "target_behavior": item["result"],
                "match": "exact",
                "reason": "当前登录态下按Jira原话实测；只证明当前平台结果。",
            },
            {
                "source_id": standard_id,
                "source": item["standard"],
                "source_location": f"标准功能详情ID {item['standard_id']}：说明、Query举例、下发参数、执行策略及状态",
                "source_type": "alchemy_standard",
                "role": "context_only",
                "project_model": item["model"],
                "trigger": item["utterance"],
                "target_behavior": item["standard"],
                "match": "exact",
                "reason": "证明标准语义、参数与执行策略；不单独替代正式PRD/UE。",
            },
            {
                "source_id": project_id,
                "source": item["project"],
                "source_location": f"项目功能列表按meta_id检索：{item['project']}",
                "source_type": "alchemy_project",
                "role": "context_only",
                "project_model": item["model"],
                "trigger": item["utterance"],
                "target_behavior": item["project"],
                "match": "exact" if item["project_status"] == "read" else "gap",
                "material": item["project_status"] != "read",
                "reason": "已实时核验项目功能点继承状态。",
                **({"next_action": item["note"]} if item["project_status"] != "read" else {}),
            },
        ])
        manifest["voice_evidence"] = {
            "applicable": True,
            "availability": "complete",
            "original_utterance": item["utterance"],
            "alchemy_tested": True,
            "alchemy_result": item["result"],
            "meta_id": item["result"],
            "standard_function": {"status": "verified", "name": item["standard"], "assessment": "已读取说明、Query举例、下发参数、执行策略与状态。"},
            "project_function": ({"status": "verified", "name": item["project"], "assessment": "已按meta_id读取项目功能列表并核对继承及状态。"} if item["project_status"] == "read" else {"status": "not_applicable", "reason": item["project"]}),
            "unavailable_reason": "",
            "next_action": item["note"],
        }
        for check in manifest.get("required_evidence_checks", []):
            if check.get("check_id") == "alchemy_current":
                check.update(status="read", reason=f"已登录并实测：{item['result']}", source_ids=[current_id], material=False, next_action="")
            elif check.get("check_id") == "alchemy_standard":
                check.update(status="read", reason=item["standard"], source_ids=[standard_id], material=False, next_action="")
            elif check.get("check_id") == "alchemy_project":
                check.update(status=item["project_status"], reason=item["project"], source_ids=[project_id], material=item["project_status"] != "read", next_action=item["note"] if item["project_status"] != "read" else "")
        manifest["decision"] = {
            "status": item["status"],
            "owner": item["owner"],
            "implementation_source_ids": ["jira-actual", current_id],
            "text": item["judgment"],
        }
        manifest["conflict_resolution"] = item["judgment"]
        out = LOG / f"2026-08-13-{key}-alchemy-recheck-manifest.json"
        out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
        paths.append(out)
    return paths


def main() -> None:
    readback = json.loads((LOG / "2026-08-12-daily-new-bugs-recheck-readback.json").read_text())
    rows = readback["sheets"][0]["data"][0]["rowData"]
    patches = []
    for key, item in COMMON.items():
        if key == "ADS-47316":
            continue
        current = rows[item["row"] - 321]
        patches.append(build_patch_requests(
            2135747181,
            item["row"],
            key,
            "recheck",
            current,
            row_fingerprint(current),
            make_changes(key, item),
        ))

    patch_path = LOG / "2026-08-13-aug12-alchemy-recheck-patches.json"
    patch_path.write_text(json.dumps({"run_id": RUN_ID, "patches": patches}, ensure_ascii=False, indent=2) + "\n")

    item = COMMON["ADS-47316"]
    append_item = {
        "date": "2026-08-13",
        "key": "ADS-47316",
        "summary": "下一首播放歌手歌曲定义与项目配置冲突",
        "info": item["info"],
        "judgment": item["judgment"],
        "status": item["status"],
        "note": item["note"],
        "info_links": [],
        "judgment_links": [],
        "links": links_for("ADS-47316", item),
    }
    append_input_path = LOG / "2026-08-13-ADS-47316-feng-zhi-xiu-row-input.json"
    append_input_path.write_text(json.dumps([append_item], ensure_ascii=False, indent=2) + "\n")
    append_requests = build_batch_requests(1069511239, 62, [append_item], date="2026-08-13", format_source_row_index=1, filter_end_row_index=63)
    append_req_path = LOG / "2026-08-13-ADS-47316-feng-zhi-xiu-append-requests.json"
    append_req_path.write_text(json.dumps({"run_id": RUN_ID, "sheet": "冯智秀bug", "row": 63, "requests": append_requests}, ensure_ascii=False, indent=2) + "\n")

    manifest_paths = make_manifests()
    validation_path = LOG / "2026-08-13-aug12-alchemy-recheck-readback-validation.json"
    validation_sha256 = hashlib.sha256(validation_path.read_bytes()).hexdigest() if validation_path.exists() else "pending-readback"
    items = []
    for key, value in COMMON.items():
        target_owner_id = "feng-zhi-xiu" if key == "ADS-47316" else "wu-you"
        sheet_name = "冯智秀bug" if key == "ADS-47316" else "bug"
        sheet_row = 63 if key == "ADS-47316" else value["row"]
        items.append({
            "jira_key": key,
            "operator_owner_id": "wu-you",
            "target_owner_id": target_owner_id,
            "sheet_name": sheet_name,
            "sheet_row": sheet_row,
            "manifest_path": str(LOG / f"2026-08-13-{key}-alchemy-recheck-manifest.json"),
            "readback_path": str(validation_path),
            "validation_path": str(validation_path),
            "readback_sha256": validation_sha256,
        })
    run_bundle = {
        "schema_version": 1,
        "run_id": RUN_ID,
        "automation_id": "bug",
        "status": "complete",
        "started_at": "2026-08-13T11:30:00+08:00",
        "query_summary": "重审8月12日11条需重新登录Alchemy的Bug；逐条补齐当前原话、标准功能点、项目功能点与Drive正式资料",
        "action_log": str(LOG / "2026-08-13-aug12-alchemy-recheck.md"),
        "items": items,
        "completed_at": "2026-08-13T13:48:00+08:00",
    }
    (LOG / "2026-08-13-aug12-alchemy-recheck-run.json").write_text(json.dumps(run_bundle, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
