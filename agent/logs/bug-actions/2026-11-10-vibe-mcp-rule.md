# 2026-11-10 Vibe MCP 规则沉淀

- 操作者：吴优
- 请求：把 https://mastergo.com/help/ai-features/vibe-mcp.html 沉淀进项目规则，并确认之前用的是 Vibe MCP 还是 Magic MCP。
- 读取证据：上述帮助页 2026-11-10 正文；`agent/product-kb/rules/mastergo-vibe-mcp.md`；本机 MCP 客户端 `@mastergo/vibe-mcp@1.0.32`。
- 判断：画布修改已经在用 Vibe MCP，不是 Magic MCP。Vibe 是当前画布通道，Magic 只保留为 2026-07-17 的历史读取记录。
- 写入摘要：规则改为画布只走 Vibe。补上不切页、空根节点只用于改父容器自身、不把绝对定位父容器改成自动布局、accepted 后等待队列。
- 未写 Jira，未改画布。
