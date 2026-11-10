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


## 2026-11-10 Vibe MCP 与 Magic MCP

- 来源：[MasterGo Vibe MCP 帮助](https://mastergo.com/help/ai-features/vibe-mcp.html)，2026-11-10 读取。
- 画布读写只用 Vibe MCP：`@mastergo/vibe-mcp`。2026-11-10 实际调用的是 `@mastergo/vibe-mcp@1.0.32`，`--url=http://127.0.0.1:30678`。
- Magic MCP（`@mastergo/magic-mcp` v0.2.4）是 2026-07-17 验证过的旧读取通道。它不能代替 Vibe 修改当前画布。不要再启动 Magic MCP 做图层修改。
- Vibe 不需要个人 token，能读取、生成、局部修改、替换、删除、同步和截图，并直接作用到当前打开的画布。Magic 做不到这次这种局部改图层。

### 操作约束

- 操作期间不要切换 MasterGo 文件或页面。焦点跳走会返回 `TargetNodePageMismatch`。要同时看别的稿，用浏览器另开，不切客户端当前页。
- 改之前先 `get_selection_node`。改文案、颜色、尺寸和布局用 `agent_update_node`。换图标或图片用 `agent_replace_node`。
- 只改父容器自身时，传带 `data-node-id` 的空根节点，系统保留子节点。要改子结构必须传完整子树。禁止空内容更新页面根节点。
- 删除样式必须写 `property: initial`，不能靠省略属性。
- 不要把已有绝对定位的父容器改成 `display: flex` 或纵向自动布局。控件会失去坐标并堆到左上角。
- `agent_update_node` 返回 `accepted` 后，画布仍在后台处理。不要立刻再读或再截图。返回「任务队列过长」时等待后重试，不要连发。
- `agent_sync_design` 只在用户明确要求同步到画布时使用，目标应是页面根节点。不要把 `.vue`、`.tsx` 当同步文件。
- 删除变量用 `agent_remove_variable`，不要用 `agent_update_variables` 删除。
- `30678` 被占用时，以 MasterGo status 的 `httpPort` 为准改 `--url`。查看 status 只用于确认文件和端口，不算已经用 MCP 改了画布。
