# Historical Bug Scripts

本目录仅保存已执行任务的一次性构建脚本，供历史审计和问题复盘。

## 2026-08-12 运行闭环更正

- `rebuild_2026_08_12_run_closure.py`：一次性把首次每日新增批次重建为schema v4 manifest、逐Key日志和run bundle。
- `build_2026_08_12_recheck_patches.py`：一次性从写前A:J回读生成321–331行的recheck patch输入。
- `validate_2026_08_12_recheck.py`：一次性校验写后A:J、保护列、链接、公式、BOOLEAN、格式和重复Key，并收口final run bundle。
- 三个脚本只服务Run ID `20260812T105609+0800-daily-bug-recheck`，不得作为日常入口复用；日常入口为`agent/scripts/`中的通用门禁。

- 不用于当前 Bug 处理，不代表现行规则。
- 不得从本目录生成新的线上写表请求。
- 当前可执行、可复用且受架构校验约束的脚本只放在 `agent/scripts/`。
- 如需复用历史逻辑，必须重新实现为受测试和 manifest 门禁约束的通用能力。
