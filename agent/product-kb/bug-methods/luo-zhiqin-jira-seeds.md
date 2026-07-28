# Luo Zhiqin Jira Seeds

第一阶段只以 `罗稚钦工作说明.xlsx` 中出现的 Jira key 作为历史 bug 方法学习种子，不做 Jira 全量搜索。

## 已抽取种子

```text
ADS-41356
ADS-41755
ADS-42560
ADS-42892
ADS-43148
ADS-43208
ADS-43266
ADS-43267
ADS-43268
ADS-43386
ADS-43438
ADS-43561
ADS-43611
ADS-43785
ADS-43844
ADS-44160
ADS-44488
ADS-44656
BEO-4532
BEO-6045
BEO-7467
BEO-7468
BEO-7754
HUR-80222
HUR-80262
HUR-80319
HUR-80341
HUR-80342
HUR-80343
HUR-81049
HUR-81050
PC-36286
PC-36843
PC-37128
SD-3528
SD-4665
SLV-43932
```

## 后续拉取策略

1. 用 JQL `key in (...)` 批量读取这些 key。
2. 字段至少包含：summary、status、components、labels、assignee、description、comment、attachment、resolution。
3. 按 `categories.md` 分类。
4. 只把可复用判断规则和典型案例写入知识库，不逐字复制 Jira 长评论。
