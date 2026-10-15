from analyze_bug.core.paths import get_resource_file


SKILL_DESCRIPTION = (
    "当用户提供 Jira issue key，需要自动分析语音交互 Bug、检索 Debug 日志、"
    "并生成中文分析结论时使用。"
)


def load_canonical_workflow() -> str:
    workflow_path = get_resource_file("workflow.md")
    return workflow_path.read_text(encoding="utf-8").strip()


def render_skill(platform: str) -> str:
    if platform not in {"codex", "gemini"}:
        raise ValueError(f"Unsupported skill platform: {platform}")

    platform_note = {
        "codex": "该技能面向 Codex，依赖已注册的 MCP 服务和本地 shell 工具。",
        "gemini": "该技能面向 Gemini CLI，依赖已注册的 MCP 服务和本地 shell 工具。",
    }[platform]

    workflow = load_canonical_workflow()
    return "\n".join(
        [
            "---",
            "name: analyze-bug",
            f"description: {SKILL_DESCRIPTION}",
            "---",
            "",
            "# Analyze Bug",
            "",
            platform_note,
            "",
            workflow,
            "",
        ]
    )
