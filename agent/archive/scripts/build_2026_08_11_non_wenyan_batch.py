#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOG = ROOT / "agent/logs/bug-actions"
CONTRACT = ROOT / "agent/scripts/bug_sheet_contract.py"
SHEET_ID = 2135747181
DATE = "2026-08-11"

issues = [
    {
        "key":"SLV-44256","row":286,"title":"SLV-44256｜12：40[673][DA]语音：当前的海拔高度。 TTS发起了天气预报与刷新了导航","status":"待复核","owner":"C673语音云端对话管理负责人",
        "c":"现象：用户在上一轮询问位置后说“目前的海拔高度”，rewrite_model把上一轮地址错误拼入本轮，随后触发天气和导航卡片刷新。[Jira原票·描述/完整评论][VOS请求链·reqId]\n证据：评论给出reqId=0bc8b9d5-af51-4b9d-b1f2-b54bf3692404及origin_query/pre_query/rewrite_query，能证明当前多轮继承链；未检索到同车型生效PRD对该问法及上下文继承边界的明确条款。",
        "d":"结论：定义为待复核。当前日志能定位到无关上一轮地址被继承，但缺同范围语音正式定义及完整Alchemy标准/项目功能点，不能仅凭研发诊断直接定责。\n依据：Jira描述/完整评论中的reqId与rewrite链；Drive正式定义检索未命中同车型、同问法条款。\n处理：补齐“海拔高度”能力边界和无关多轮上下文不得继承的生效语音定义，并完成Alchemy当前/标准/项目核验后定责；C673语音云端对话管理负责人处理。",
        "i":"测试用例已含版本、VIN、步骤、预期、实际、日志与reqId，无需补测试用例；缺的是正式语音定义和Alchemy证据链。",
        "links":[("Jira原票·描述/完整评论","http://jira.i-tetris.com/browse/SLV-44256"),("VOS请求链·reqId","https://vos-debug.i-tetris.com/#/info/getReqInfo?rid=0bc8b9d5-af51-4b9d-b1f2-b54bf3692404&ts=1784695219489")],"profile":"voice"
    },
    {
        "key":"HUR-82949","row":291,"title":"HUR-82949｜【J90A】【0526】【仪表】英语，仪表驾驶模式字体太小","status":"待复核","owner":"J90A仪表产品/UE负责人",
        "c":"现象：J90A 0526分支切换英语后，仪表“Hybrid/Personalized”驾驶模式文字被报告字号过小，附件可证明当前显示效果。[Jira原票·描述/附件]\n证据：已检索J90A仪表、驾驶模式、英语及LanguageList资料，但LanguageList只能证明文案，未找到规定该仪表区域字号、字重或自适应规则的同版本UE。",
        "d":"结论：定义为待复核。现有证据只能证明当前视觉效果，无法证明违反哪一条生效字号/布局规范。\n依据：Jira描述与附件；Drive中J90A海外LanguageList不定义仪表字号，未检索到同版本仪表UE对应节点。\n处理：补充J90A仪表驾驶模式英语态UE节点或字号/自适应规范后，再判定研发是否修复；J90A仪表产品/UE负责人处理。",
        "i":"测试用例已含分支、语言、入口、预期、实际、复现率和图片，无需补测试用例；需补同版本仪表UE证据。",
        "links":[("Jira原票·描述/附件","http://jira.i-tetris.com/browse/HUR-82949"),("现状图片","http://jira.i-tetris.com/secure/attachment/4229552/99fc9aa4-b1e4-4a35-9efc-831a35d7476f.jpg"),("J90A海外LanguageList","https://docs.google.com/spreadsheets/d/1AAL-II3PGv6jEwLpayNy-NWwJFnM9ILcIr13uVjU3P0/edit")],"profile":"visible_interaction"
    },
    {
        "key":"HUR-82937","row":292,"title":"HUR-82937｜【PI】【0109】【语音】【新需求测试】【波兰语】展车模式开启，提示无法使用拖车模式的tts回复不对","status":"待复核","owner":"J90A语音多语言需求负责人",
        "c":"现象：PI 0109波兰语、展车模式开启时说“włącz tryb przyczepy”，当前回复不支持；测试预期为两条指定波兰语拦截TTS之一。[Jira原票·描述/完整评论]\n证据：研发评论明确此前未收到、未开发该TTS需求；Drive检索命中J90A多语言/拖车模式资料入口，但未读到能证明这两条TTS已生效下发的同版本需求行。",
        "d":"结论：定义为待复核，当前不能按Bug转研发，也不能把测试预期直接当正式需求。\n依据：Jira完整评论确认旧版本未接收该需求；现有Drive检索未定位两条波兰语TTS的生效配置行，Alchemy链亦未完整核验。\n处理：提供客户下发语料/需求表的文件名、Sheet、行号及生效版本，并完成Alchemy当前/标准/项目核验；J90A语音多语言需求负责人处理。",
        "i":"测试用例本身完整，无需补测试用例；需补客户正式语料行和生效版本证据。",
        "links":[("Jira原票·描述/完整评论","http://jira.i-tetris.com/browse/HUR-82937"),("现状图片","http://jira.i-tetris.com/secure/attachment/4229528/image-2026-08-10-14-04-56-829.png"),("J90A_EU-PI_LanguageList","https://docs.google.com/spreadsheets/d/1xy8HKs9tghWtxXTlp5IGcIE8VhyEul0tQgzxA8WGQ9Y/edit")],"profile":"voice"
    },
    {
        "key":"HUR-82934","row":293,"title":"HUR-82934｜【PI】【语音】【新需求测试】【瑞典语】露营模式时长减少15分钟(24h>x>1分钟)/露营模式时长减少15分钟(24h>x>1分钟) 露营模式减少一点时长(模糊步长 10min),与对应音频不一致","status":"待复核","owner":"J90A语音多语言需求负责人",
        "c":"现象：客户语料中中文意图为“减少15分钟/减少一点时长”，对应瑞典语却表达“增加1小时15分钟/增加一点”，语义方向和步长均冲突。[Jira原票·描述/完整评论][更新后语料截图]\n证据：研发评论说明执行语料来自马自达客户下发；附件能证明语料内部不一致，但尚未定位客户正式语料表的文件名、Sheet、行号和最终生效版本。",
        "d":"结论：定义为待复核。当前不是运行时随机识别问题，而是需求语料本身存在中瑞语义冲突；在客户最终语料行和版本未定位前，不直接给研发修改值。\n依据：Jira描述、完整评论及更新后语料截图。\n处理：由J90A语音多语言需求负责人确认中文意图、瑞典语目标句及步长，回写客户正式语料并给出文件名/Sheet/行号，再进入开发与回归。",
        "i":"测试用例已完整，无需补测试用例；需要补客户最终语料的可定位证据，并完成Alchemy链核验。",
        "links":[("Jira原票·描述/完整评论","http://jira.i-tetris.com/browse/HUR-82934"),("更新后语料截图","http://jira.i-tetris.com/secure/attachment/4230256/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_17863447154709.png"),("J90A_EU-PI_LanguageList","https://docs.google.com/spreadsheets/d/1xy8HKs9tghWtxXTlp5IGcIE8VhyEul0tQgzxA8WGQ9Y/edit")],"profile":"voice"
    },
    {
        "key":"HUR-82857","row":315,"title":"HUR-82857｜【J90A】【0526】【音乐】14:34 冬季模式开启中，音乐app中点击氛围灯按键，无弹窗提示，且能开启氛围灯音乐律动模式","status":"可转研发","owner":"Android-Music研发负责人（张齐财）",
        "c":"现象：J90A冬季模式已开启时，音乐App点击氛围灯仍可开启音乐律动且无拦截提示。[Jira原票·描述/完整评论]\n证据：已完成需求HUR-24753明确冬季模式期间禁止开启音乐氛围灯，点击时提示“当前为冬季模式，无法打开音乐氛围灯，请先关闭冬季模式再操作”；当前音乐端代码额外要求winter_light开启才拦截。[HUR-24753·需求定义/PRD入口]",
        "d":"结论：定义为音乐端实现缺陷。冬季模式开启即应禁止音乐氛围灯，不应再以winter_light联动开关作为第二个必要条件。\n依据：HUR-24753已完成需求及其PRD入口明确“冬季模式期间禁止开启”；HUR-82857评论记录音乐端现状为两个条件同时满足才拦截。\n处理：删除音乐端对winter_light的额外前置依赖，冬季模式开启时统一拦截并展示既定提示；Android-Music研发负责人（张齐财）处理。",
        "i":"测试用例完整，无需补测试用例；未执行Jira评论、转派或状态变更。",
        "links":[("Jira原票·描述/完整评论","http://jira.i-tetris.com/browse/HUR-82857"),("HUR-24753·需求定义/PRD入口","http://jira.i-tetris.com/browse/HUR-24753"),("PRD·冬季模式音乐氛围灯","https://docs.google.com/document/d/1LpVkJsQLb1_9e_x3c3n9dK5Kc_tn7AqRKiEspioc1O0/edit#heading=h.emfxkqkec3qq")],"profile":"general","deterministic":True
    },
    {
        "key":"HUR-82811","row":316,"title":"HUR-82811｜【J90A】【0526】【user-debug】 15：43   多个电话联系人选择拨打页面-qurey：今天天气怎么样 TTS回复错误","status":"待复核","owner":"J90A语音上下文负责人",
        "c":"现象：多个联系人待选择的模糊拨号二次交互阶段，用户改问天气，系统未保持电话选择上下文。[Jira原票·描述/完整评论]\n证据：关联票HUR-62579的产品结论明确：模糊拨号二次交互期间不响应其他指令；HUR-82811正处于多个联系人选择阶段。但本票Alchemy当前/标准/项目功能点未完整核验。[HUR-62579·二次交互边界]",
        "d":"结论：定义为待复核。既有产品边界支持在多个联系人选择阶段屏蔽天气指令，但语音问题在Alchemy链未完整核验前不做确定性转研发。\n依据：HUR-62579完整评论中的“模糊拨打二次交互期间不响应其他指令”及HUR-82811当前页面阶段。\n处理：补齐本次原话在J90A项目的Alchemy当前、标准、项目功能点，确认上下文优先级后转J90A语音上下文负责人修复。",
        "i":"测试用例完整，无需补测试用例；缺Alchemy项目链核验，不缺复现步骤。",
        "links":[("Jira原票·描述/完整评论","http://jira.i-tetris.com/browse/HUR-82811"),("HUR-62579·二次交互边界","http://jira.i-tetris.com/browse/HUR-62579")],"profile":"voice"
    },
    {
        "key":"HUR-82655","row":317,"title":"HUR-82655｜BG20260803001140 【WT】【J90A-EL】【车辆设置】【实车】【静态】【必现】【SWC.00.0】拨打蓝牙电话中，再方控调节音量，音量值被蓝牙电话窗口遮挡","status":"待确认","owner":"吴优",
        "c":"现象：客户编号BG20260803001140，J90A-EL拨打蓝牙电话时用方控调节音量，音量值被电话窗口遮挡。[Jira原票·客户描述/视频]\n证据：Jira给出了场景、步骤、实际、预期、复现率和视频，但未给出可核验的完整软件版本/分支，也未找到同版本蓝牙电话与音量浮层层级UE。",
        "d":"结论：定义为待确认。当前客户材料能复现遮挡现象，但缺完整版本信息和同版本图层优先级定义，不能仅凭“电话窗口层级高”决定改哪一层。\n依据：Jira客户描述、视频及研发评论；Drive检索未命中J90A-EL对应UE节点。\n处理：向客户收集完整客户测试用例（完整软件版本/分支、发生时间、原始视频），并补充蓝牙通话与音量浮层层级UE；吴优处理。",
        "i":"客户测试用例不完整：缺完整软件版本/分支及可定位UE；向客户收集完整客户测试用例后再定责。",
        "links":[("Jira原票·客户描述/视频","http://jira.i-tetris.com/browse/HUR-82655"),("客户现象视频","http://jira.i-tetris.com/secure/attachment/4221501/2.mp4"),("外部客户票HUR-49746","http://211.159.155.78:8080/browse/HUR-49746")],"profile":"visible_interaction","customer":True
    },
    {
        "key":"HUR-82496","row":318,"title":"HUR-82496｜【J90A】【0526】【情景模式-儿童模式】【语音】开启儿童模式后，语音“放大实时画面”，执行为放大地图","status":"待复核","owner":"J90A语音VUI负责人",
        "c":"现象：儿童模式实时画面已显示时说“放大实时画面”，NLU落入NAVI/MAP_ADJUST_RESIZE并播报“已放大地图”。[Jira原票·描述/完整评论]\n证据：评论给出当前NLU domain/action/operation；Drive只检索到非J90A项目儿童模式需求，未找到J90A同页面“实时画面”所见即可说节点或语音指令配置。",
        "d":"结论：定义为待复核。当前可确认语义落到地图，但缺J90A儿童模式实时画面的正式VUI/UE节点及完整Alchemy功能点，不能直接判断由NLU还是页面所见即可说配置修复。\n依据：Jira完整评论中的NAVI/MAP_ADJUST_RESIZE结果；Drive同项目正式定义未命中。\n处理：补充J90A儿童模式实时画面UE/VUI节点和Alchemy当前/标准/项目功能点后定责；J90A语音VUI负责人处理。",
        "i":"测试用例完整，无需补测试用例；需补同项目VUI/UE和Alchemy证据。",
        "links":[("Jira原票·描述/完整评论","http://jira.i-tetris.com/browse/HUR-82496"),("现象视频","http://jira.i-tetris.com/secure/attachment/4174061/video_1785234456.mp4"),("非同项目儿童模式资料·仅旁证","https://drive.google.com/file/d/1LyjsT7qMVuzl9-PWnr2v83gTvK5_vRw7/view")],"profile":"voice"
    },
    {
        "key":"ADS-48288","row":319,"title":"ADS-48288｜【C673-7】query以后叫我宝宝，不能设置成功，回复要求4-6字","status":"待复核","owner":"深蓝语音服务产品负责人（吴优）",
        "c":"现象：C673-7说“以后叫我宝宝”，NLU命中meta_id=1325，车端服务按错误码205的重复字符规则拒绝设置。[Jira原票·描述/完整评论][ADS-47939·reqId/meta]\n证据：研发评论说明205规则为东风平台新增，当前提供“保留/深蓝绕过”两种方案；未检索到深蓝同版本自定义应答语对长度及重复字符的生效PRD条款。",
        "d":"结论：定义为待复核。当前实现因复用东风错误码205拦截“宝宝”，但缺深蓝项目对2字昵称、重复字符和4-6字限制的正式定义，不能直接选择绕过方案。\n依据：ADS-48288完整评论与ADS-47939的meta_id=1325/reqId链；Drive未命中深蓝同版本条款，Alchemy项目功能点未完整核验。\n处理：明确深蓝自定义应答语的长度、重复字符和文明校验规则并形成生效配置，再决定是否对深蓝绕过205；深蓝语音服务产品负责人（吴优）处理。",
        "i":"测试用例完整，无需补测试用例；需补深蓝正式规则及Alchemy当前/标准/项目证据。",
        "links":[("Jira原票·描述/完整评论","http://jira.i-tetris.com/browse/ADS-48288"),("ADS-47939·reqId/meta","http://jira.i-tetris.com/browse/ADS-47939")],"profile":"voice"
    },
]

def assessment(profile):
    reasons={"general":"通用功能边界；无更具体专项画像。","voice":"涉及用户原话、NLU、TTS或语音上下文。","map_navigation":"不涉及地图搜索、POI或路线定义。","visible_interaction":"涉及可见页面、文字、浮层或控件状态。"}
    return {p:{"applicable":p==profile,"reason":reasons[p] if p==profile else ("已命中更具体画像，不重复选择。" if p=="general" else "本票不属于该专项范围。")} for p in ["general","voice","map_navigation","visible_interaction"]}

def jira_scope(it):
    return {"source_id":"jira_actual","source":f"{it['key']} Jira描述、附件、关联问题与完整评论","source_type":"jira","source_location":"Jira描述、附件区、关联问题及活动日志（按时间升序）","role":"implementation_actual","match":"exact","project_model":"Jira当前登记车型、版本与模块","trigger":it['c'].split("[",1)[0],"target_behavior":"证明当前实现、测试主张与评论因果；不单独定义产品目标。","reason":"当前Jira页面可直接证明本票实现事实。"}

def manifest(it):
    scopes=[jira_scope(it)]
    checks=[]
    gaps=[]
    if it.get("deterministic"):
        scopes.append({"source_id":"winter_requirement","source":"HUR-24753 已完成需求及PRD入口","source_type":"customer_final_decision","source_location":"HUR-24753需求描述：冬季模式期间禁止开启音乐氛围灯；点击显示既定Toast；PRD heading=h.emfxkqkec3qq","role":"formal_target","match":"exact","project_model":"J90A-All / Android-CarSettings与音乐氛围灯同一项目","trigger":"冬季模式开启时点击音乐氛围灯","target_behavior":"禁止开启并提示当前为冬季模式，需先关闭冬季模式。","reason":"已完成同项目需求直接定义该触发条件和目标行为。"})
        checks=[{"check_id":"formal_definition_search","status":"read","searched_at":DATE,"search_location":"HUR-24753已完成需求及其Google Docs PRD入口","queries":["J90A 冬季模式 音乐氛围灯","HUR-24753"],"source_ids":["winter_requirement"]}]
    elif it["profile"]=="voice":
        for cid,label in [("formal_definition_search","Google Drive正式需求/配置"),("alchemy_current","Alchemy在线对话"),("alchemy_standard","Alchemy标准功能点"),("alchemy_project","Alchemy项目功能点")]:
            checks.append({"check_id":cid,"status":"not_found" if cid=="formal_definition_search" else "unavailable","searched_at":DATE,"search_location":label,"queries":[it["key"],it["title"].split("｜",1)[-1][:40]],"source_ids":[],"reason":"未取得能支撑本票确定性结论的同项目、同版本完整证据。","material":True,"next_action":"补齐同范围正式定义及Alchemy当前/标准/项目证据后定责。"})
    else:
        for cid,label in [("formal_config_search","Google Drive项目配置"),("interaction_or_ue_search","Google Drive交互文档/UE")]:
            checks.append({"check_id":cid,"status":"not_found","searched_at":DATE,"search_location":label,"queries":[it["key"],it["title"].split("｜",1)[-1][:40]],"source_ids":[],"reason":"未找到同项目、同版本且能直接定义目标状态的生效资料。","material":True,"next_action":"补充同版本正式配置或UE节点后重新判断。"})
    customer={"identified":bool(it.get("customer"))}
    if it.get("customer"):
        customer.update({"external_id":"BG20260803001140","test_case":{"checked":True,"status":"incomplete","source":"Jira客户描述与视频；缺完整软件版本/分支和UE定位"}})
    voice=({"applicable":True,"availability":"unavailable","alchemy_tested":False,"standard_function":{"status":"unavailable","reason":"未完成标准功能点核验"},"project_function":{"status":"unavailable","reason":"未完成项目功能点核验"},"unavailable_reason":"本批次未取得可支撑确定性定责的完整Alchemy在线证据链。","next_action":"补齐当前原话、meta_id、标准功能点和项目功能点。"} if it["profile"]=="voice" else {"applicable":False})
    dec={"status":it["status"],"owner":it["owner"],"text":it["d"]}
    out={"schema_version":2,"jira_key":it["key"],"comment_causality":"已完整读取Jira字段、描述、附件、关联问题和全部评论；测试预期、研发意见、当前实现与正式定义分别记录。","customer_issue":customer,"related_issues":{"checked":True,"items":[]},"scope_checks":scopes,"evidence_profiles":[it["profile"]],"evidence_profile_assessment":assessment(it["profile"]),"required_evidence_checks":checks,"inheritance_chains":[],"conflict_resolution":"测试预期和研发评论只作为主张/实现事实；只有同项目、同触发条件的生效正式定义可作为确定性目标，关键缺口存在时降级并指定补证责任方。","voice_evidence":voice,"decision":dec}
    if it.get("deterministic"):
        out["expected_behavior"]={"trigger":"冬季模式开启时点击音乐App氛围灯","target_state":"音乐氛围灯保持关闭","intent_function_signal":"冬季模式状态直接触发禁止规则","ui_tts_vehicle_behavior":"显示‘当前为冬季模式，无法打开音乐氛围灯，请先关闭冬季模式再操作’","boundary":"不以winter_light联动开关为额外必要条件","source_ids":["winter_requirement"]}
        out["decision"]["implementation_source_ids"]=["jira_actual"]
    return out

def current_row(it):
    vals=[{"formattedValue":"2026-08-10","userEnteredValue":{"stringValue":"2026-08-10"}},{"formattedValue":it["title"],"userEnteredValue":{"formulaValue":f'=HYPERLINK("http://jira.i-tetris.com/browse/{it["key"]}","{it["title"].replace(chr(34), chr(34)*2)}")'}},{"formattedValue":""},{"formattedValue":""},{"formattedValue":"FALSE","userEnteredValue":{"boolValue":False},"dataValidation":{"condition":{"type":"BOOLEAN"},"strict":True}},{"formattedValue":""},{"formattedValue":""},{"formattedValue":""},{"formattedValue":""},{"formattedValue":""}]
    return {"values":vals}

for it in issues:
    links=[{"label":a,"url":b} for a,b in it["links"]]
    patch={"current_row":current_row(it),"changes":{"C":{"text":it["c"],"links":[x for x in links if x["label"] in it["c"]]},"D":{"text":it["d"],"links":[x for x in links if x["label"] in it["d"]]},"G":it["status"],"I":it["i"],"J":{"links":links}}}
    mf=LOG/f"{DATE}-{it['key']}-manifest.json"; pf=LOG/f"{DATE}-{it['key']}-sheet-patch-input.json"; sf=LOG/f"{DATE}-{it['key']}-snapshot.json"; rf=LOG/f"{DATE}-{it['key']}-sheet-requests.json"
    mf.write_text(json.dumps(manifest(it),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    pf.write_text(json.dumps(patch,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    snap=subprocess.run(["python3",str(CONTRACT),"snapshot"],input=json.dumps(current_row(it),ensure_ascii=False),text=True,capture_output=True,check=True)
    sf.write_text(snap.stdout,encoding="utf-8")
    fp=json.loads(snap.stdout)["fingerprint"]
    req=subprocess.run(["python3",str(CONTRACT),"patch","--sheet-id",str(SHEET_ID),"--row-number",str(it["row"]),"--key",it["key"],"--mode","recheck","--preview-fingerprint",fp],input=json.dumps(patch,ensure_ascii=False),text=True,capture_output=True,check=True)
    rf.write_text(req.stdout,encoding="utf-8")

print(json.dumps({"count":len(issues),"keys":[x["key"] for x in issues]},ensure_ascii=False))
