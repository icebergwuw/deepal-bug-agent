# Analyze Bug

面向 Codex 与 Gemini CLI 的 Jira Bug 分析工具包。当前版本将 skill、安装器与 MCP runtime 拆开管理，并内置 Jira、Debug、Rules、Alchemy Ops 四类能力。

## 架构说明

- 当前仓库只保留 `analyze-bug` 这一套有效实现，不再依赖 `shared/`、`src/servers/`、`src/commands/`、`src/rules/` 这类旧结构。
- 源码按 `core/ + runtime/ + mcp_server/` 三层组织：公共能力、运行入口、MCP 服务彻底分离。
- 根目录的 `install.sh` / `install.ps1` 是薄安装器，只负责保证 `uv` 可用并调用 `analyze-bug-admin install`。
- `alchemy-ops` 已内置到 runtime 中，只暴露只读接口，不再维护独立的外部分发链路。

## 功能

- 保持原有五阶段分析流程不变
- 支持运营配置优先、Rules 补充、Cloud 按需结合 `online-dialogue` 静态代码证据
- 支持 Bugfree 汇总票逐行回填
- 支持分析过程中调用 shell 做本地辅助处理
- 支持 Codex / Gemini CLI 双平台 skill 与 MCP 自动安装
- 支持 zip 分发与 macOS / Linux / Windows 脚本化安装

## 项目结构

```text
analyze-bug/
├── pyproject.toml                         # 项目元数据、依赖、uv 构建配置和 console entrypoint
├── uv.lock                                # uv 锁文件，保证安装与分发依赖一致
├── install.sh                             # macOS / Linux 安装脚本
├── install.ps1                            # Windows 安装脚本
├── package.sh                             # zip 打包入口
├── src/
│   ├── resources/                         # 与 src/analyze_bug 平级的静态资源目录
│   │   ├── config-bug-foundation.md       # 运营配置排障经验和判责知识
│   │   ├── rules.json                     # 内置规则数据
│   │   └── workflow.md                    # skill 共用的 canonical workflow
│   ├── analyze_bug/
│   │   ├── __init__.py                    # 包版本和最小元信息
│   │   ├── core/
│   │   │   ├── config.py                  # 统一配置读取、写入和旧配置迁移
│   │   │   ├── http.py                    # 通用 HTTP 请求、重试和错误处理
│   │   │   ├── logging_utils.py           # 独立日志文件初始化
│   │   │   ├── paths.py                   # 跨平台配置、安装、日志、skill 路径管理
│   │   │   ├── repo_locator.py            # 本地 online-dialogue 仓库探测
│   │   │   ├── responses.py               # 统一 MCP 返回格式和错误包裹
│   │   │   ├── skills.py                  # Codex / Gemini skill 渲染
│   │   ├── runtime/
│   │   │   ├── admin.py                   # analyze-bug-admin 管理 CLI
│   │   │   └── build.py                   # 分发包 staging 逻辑
│   │   └── mcp_server/
│   │       ├── jira/
│   │       │   ├── jira_service.py        # Jira 业务逻辑
│   │       │   └── jira_mcp.py            # Jira MCP 适配层
│   │       ├── debug/
│   │       │   ├── debug_service.py       # Debug 业务逻辑
│   │       │   └── debug_mcp.py           # Debug MCP 适配层
│   │       ├── rules/
│   │       │   ├── rules_service.py       # 规则读取逻辑
│   │       │   └── rules_mcp.py           # Rules MCP 适配层
│   │       └── ops/
│   │           ├── ops_service.py         # Alchemy Ops 业务逻辑与只读查询实现
│   │           └── ops_mcp.py             # Alchemy Ops MCP 适配层
└── tests/                                 # 回归测试目录
    ├── test_admin.py                      # 安装、卸载、MCP 注册、管理命令测试
    ├── test_config.py                     # 配置读取、写入、迁移测试
    ├── test_http.py                       # HTTP 重试与请求测试
    ├── test_logging.py                    # 独立日志写入测试
    ├── test_ops_server.py                 # ops service / mcp 分层与只读接口测试
    ├── test_paths.py                      # 跨平台路径解析测试
    ├── test_repo_locator.py               # online-dialogue 仓库探测测试
    ├── test_services.py                   # Jira / Debug / Rules 服务测试
    └── test_skills.py                     # skill 渲染与打包结构测试
```

## 安装

### macOS / Linux

```bash
chmod +x install.sh
./install.sh
```

### Windows

推荐直接执行单条命令：

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

这是最稳的方式，适合双击打开 PowerShell 后直接复制执行。

如果你已经在 PowerShell 里，也可以分两步执行，但必须一行一条命令，不要把两条命令粘到同一行：

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\install.ps1
```

若出现 `无法绑定参数 Scope`，通常不是权限问题，而是把两条命令粘成了一行，例如 `... -Scope ProcessSet-ExecutionPolicy ...`。重新开一个 PowerShell 窗口，按上面的格式逐行执行即可。

安装脚本会优先尝试 `pip` 国内镜像，并默认使用清华镜像 `https://pypi.tuna.tsinghua.edu.cn/simple`；若失败，再回退到官方 `uv` 安装器。
如需显式指定镜像，可设置：

- `UV_INSTALLER_URL`
- `UV_PIP_INDEX_URL`

若 `uv` 通过 `pip --user` 安装到 Python 用户脚本目录，安装脚本会自动探测该目录并继续主流程；Windows 下还会把该目录写入用户 `Path`，确保后续在任意终端位置都可以直接执行 `uv`。

Windows 常见问题：

1. `无法绑定参数 Scope`
   原因：把 `Set-ExecutionPolicy ...` 和 `.\install.ps1` 粘成了一行。
   处理：重新打开一个 PowerShell 窗口，按上面的两行命令分别执行；或者直接改用单条命令 `powershell -ExecutionPolicy Bypass -File .\install.ps1`。

2. `uv installation completed, but uv.exe was still not found.`
   原因：`pip --user` 常把 `uv.exe` 安装到 `%APPDATA%\Python\PythonXXX\Scripts`，而当前终端的 `Path` 还没加载这个目录。
   处理：新版安装脚本会自动探测这个目录并写入用户 `Path`。如果当前窗口还是找不到 `uv`，请关闭当前 PowerShell，重新打开后执行：

```powershell
uv --version
```

   若仍失败，可手动定位 `uv.exe`：

```powershell
(Get-ChildItem -Path "$env:APPDATA\Python" -Filter "uv.exe" -Recurse).DirectoryName | Select-Object -First 1
```

   然后把返回目录加入用户 `Path`，再重新打开 PowerShell：

```powershell
$uvDir = (Get-ChildItem -Path "$env:APPDATA\Python" -Filter "uv.exe" -Recurse | Select-Object -First 1).DirectoryName
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($uvDir -and $userPath -notlike "*$uvDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$uvDir", "User")
}
```

3. `Gemini MCP 注册失败` 或 `命令执行超时`
   原因：通常是 Gemini CLI 自身登录或网络问题，不是 runtime 安装失败。
   处理：先执行 `gemini` 完成登录，再执行 `analyze-bug-admin install --no-prompt` 或手动执行 `gemini mcp add ...` 重试。runtime、skill、配置文件通常已经安装完成。

安装脚本会：

1. 检测并安装 `uv`
2. 清理旧版 analyze-bug 安装内容
3. 复制 runtime 到用户目录
4. 执行 `uv sync --frozen`
5. 显式引导配置 Jira / Debug / 运营系统凭证（缺失项会逐项提示输入）
6. 安装 Codex / Gemini skill
7. 注册 Codex / Gemini MCP
8. 迁移旧版 Gemini-only 配置
9. 校验 Jira / Debug，若已配置 ops 也会校验运营系统连通性

## 如何使用

安装完成后，日常分析不要直接执行 `analyze-bug-admin`，而是进入 `Codex` 或 `Gemini CLI`，然后直接说要分析哪张 Jira 票。

### Codex

1. 进入 Codex。
2. 直接输入：

```text
分析 PC-35280
```

或：

```text
分析 ADS-37476
```

Codex 会自动调用已安装的 skill 和 MCP，开始拉取 Jira、Debug、Rules、Ops，并按当前流程输出分析结果。

### Gemini CLI

1. 进入 Gemini CLI。
2. 直接输入：

```text
分析 PC-35280
```

或任意 Jira issue key，例如：

```text
分析 SJ-45962
```

Gemini CLI 会自动触发已安装的 `analyze-bug` skill，并通过 MCP 开始分析。

### 适用输入方式

推荐直接使用这类自然语言：

```text
分析 XX-12345
```

也可以补充上下文，例如：

```text
分析 PC-35280，重点看是不是运营配置问题
```

## 插件管理命令

下面这些 `analyze-bug-admin` 命令是给插件安装、配置、排障使用的，不是日常分析 Jira 票的入口。

安装完成后可使用：

```bash
analyze-bug-admin doctor
analyze-bug-admin configure-jira
analyze-bug-admin configure-debug
analyze-bug-admin configure-ops
analyze-bug-admin test
analyze-bug-admin uninstall
```

如果 `~/.local/bin` 不在 PATH 中，也可以使用：

```bash
uv run --project ~/.local/share/analyze-bug/runtime analyze-bug-admin doctor
```

## MCP 运行方式

四个 MCP server 都通过 `uv run --project <install_root> <entrypoint>` 启动：

- `analyze-bug-jira-mcp`
- `analyze-bug-debug-mcp`
- `analyze-bug-rules-mcp`
- `analyze-bug-ops-mcp`

安装器会自动注册：

- `jira-analyzer`
- `debug-analyzer`
- `rules-analyzer`
- `alchemy-ops`

安装/打包入口放在 `src/analyze_bug/runtime/` 下；四个 MCP server 则统一放在 `src/analyze_bug/mcp_server/` 下。静态规则、workflow 和运营经验文档放在 `src/resources/`，与 `src/analyze_bug/` 平级。`alchemy-ops` 也随 runtime 一起分发，只保留只读工具，不再额外保留独立包。

## 配置

统一配置文件：

- macOS / Linux：`~/.config/analyze-bug/credentials.env`
- Windows：`%APPDATA%\analyze-bug\credentials.env`

支持的关键字段：

- `JIRA_USERNAME`
- `JIRA_PASSWORD`
- `DEBUG_COOKIE`
- `ALCHEMY_COOKIE`
- `ALCHEMY_BASE_URL`
- `ONLINE_DIALOGUE_ROOT`

日志目录：

- macOS / Linux：`~/.local/state/analyze-bug/logs/`
- Windows：`%LOCALAPPDATA%\analyze-bug\logs\`

## 分析行为

- 先用 Jira + Debug 还原问题链路
- 再优先用 `alchemy-ops` 排查 `intent/slot/nluMapping/slotParams/protocolRequest/slotProperty/canonical`
- 若 ops 内配置缺失，归为运营配置问题
- 若云端已给出稳定且语义正确的归一值 `canonical/property`，但下游执行侧不支持该值，优先归为 `Vehicle/车端适配问题`，不再要求云端回退公共归一值
- 若 ops 已完整但 `online-dialogue` 的 `dialogScenario` 缺失或错误回落到兜底，归为 Cloud 问题
- 只有运营配置问题或 Cloud 问题，才按需结合本地 `online-dialogue` 做静态代码定位
- 如果本地没有 `online-dialogue`，则只结合运营系统和日志输出结论
- 除 Bugfree 汇总票外，Jira 评论统一使用固定结构；若未能定位问题，则只写到 `【问题原因】`：

```text
【基础信息】
【诊断证据】
【问题原因】
【解决方案】责任方：xxx。balabala修复建议。
（AI Generated）
```

其中 `【问题原因】` 不能只写模块名，必须用一句话说明直接原因；如果已经能判断到根因，应在同一句里把根因带出来。

## Skill 与 MCP 安装位置

### Codex

- skill 目录：`~/.codex/skills/analyze-bug/`
- MCP 查看：`codex mcp list`

### Gemini CLI

- skill 目录：`~/.agents/skills/analyze-bug/`
- MCP 查看：`gemini mcp list`

安装器会清理旧的 `~/.gemini/skills/analyze-bug/` 和旧 Gemini command，避免重复 skill 冲突。

## 打包

```bash
./package.sh
```

打包只生成 zip：

```text
dist/analyze-bug-<version>.zip
```

zip 内包含：

- `uv` runtime 源码
- `src/analyze_bug/mcp_server/ops/ops_mcp.py` 只读 MCP 运行时
- 已渲染的 Codex / Gemini skill
- `install.sh`
- `install.ps1`
- README

## 验证

常用回归命令：

```bash
uv run --project . pytest
./package.sh
./install.sh --no-prompt
```

安装完成后可进一步确认：

```bash
analyze-bug-admin doctor
codex mcp list
gemini mcp list
```
