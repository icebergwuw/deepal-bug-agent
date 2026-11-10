# MasterGo Vibe MCP 接入方法

- 记录日期：2026-09-11
- 适用场景：读取、生成、修改和同步当前 MasterGo 画布；优先用于可编辑设计文件，不直接改写未知二进制 `.mg`。

## 前置条件

- MasterGo 客户端已打开目标文件。
- MasterGo 内的 MasterGo MCP 已处于连接状态。
- Node.js >= 18、npm >= 8。
- 默认本地服务地址为 `http://localhost:30678`；若端口被占用，按 MasterGo 实际端口修改。

## Codex 配置

在 `~/.codex/config.toml` 增加：

```toml
[mcp_servers.mastergo]
command = "npx"
args = ["-y", "@mastergo/vibe-mcp@latest", "--url=http://localhost:30678"]
startup_timeout_sec = 120
```

重载 Codex 的 MCP 配置后，检查 MasterGo MCP 工具是否出现。

## 验证流程

1. 在 MasterGo 画布中选中目标页面或图层。
2. 发送：`使用 MasterGo MCP，获取我当前选中图层的代码。`
3. 应能调用 `get_selection_code`，并在工作区生成或更新 `.mastergo/design/` 基准文件。
4. 需要视觉检查时发送：`使用 MasterGo MCP，获取当前选中页面的预览图。`，对应工具为 `get_selection_image`。
5. 修改前先读取目标图层代码；修改后重新读取并检查页面预览，避免误覆盖父容器或丢失子节点。

## 本次验证

- MasterGo 客户端已打开目标文件。
- 本机 30678 端口有服务响应。
- `@mastergo/vibe-mcp@latest` 可由 npm 拉取并启动。
- 已将 MCP 配置加入当前用户的 Codex 配置；尚未执行画布写入，避免未经明确选择目标图层而修改设计。

## 注意事项

- Vibe MCP 不需要个人 token。
- 操作画布期间不要切换页面。
- 修改已有图层时必须先选中目标图层，再读取代码。
- `.mg` 是 MasterGo 专有二进制容器；除非通过 MCP 或官方导出流程，不要直接修改其中的 `document`。

来源：MasterGo 官方 Vibe MCP 文档（2026-09-11 读取）。


## 2026-11-10 优先使用 MCP

- 吴优要求：MasterGo 任务必须优先使用 MasterGo MCP，并写入项目规则。
- 读取和修改画布时调用 `get_selection_node`、`get_screenshot`、`agent_update_node`、`agent_replace_node`、`agent_remove_node`、`submit_page_to_canvas`。
- 会话工具列表没有 MasterGo MCP 时，启动官方 `@mastergo/vibe-mcp`，`--url` 指向本机 MasterGo `httpPort`，再通过 MCP 客户端调用工具。
- 直接请求 `http://127.0.0.1:<port>/api/*`、打开浏览器登录页、用 Computer Use 点画布，都不算使用 MasterGo MCP。
- `agent_update_node` 传入完整子树会替换子节点。空内容或更新已不存在的帧会删掉图层。不要更新页面根节点，以免带走同页其他帧。
- 选项文字必须放进按钮或选项组件内部。作为矩形的兄弟节点时会被盖住。
- 新增控件沿用同页已有标题、选项组件、字体和说明，不另画红框标注条。
