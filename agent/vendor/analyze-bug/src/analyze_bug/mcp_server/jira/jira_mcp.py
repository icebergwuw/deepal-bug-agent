from mcp.server.fastmcp import FastMCP

from analyze_bug.core.logging_utils import setup_logger
from analyze_bug.mcp_server.jira.jira_service import (
    add_jira_comment as add_jira_comment_impl,
    get_jira_issue as get_jira_issue_impl,
    update_jira_description as update_jira_description_impl,
)

logger = setup_logger("jira-mcp", "jira_mcp.log")
mcp = FastMCP("JiraAnalyzer")


@mcp.tool()
def get_jira_issue(issue_key: str) -> str:
    return get_jira_issue_impl(issue_key, logger)


@mcp.tool()
def add_jira_comment(issue_key: str, comment: str) -> str:
    return add_jira_comment_impl(issue_key, comment, logger)


@mcp.tool()
def update_jira_description(issue_key: str, description: str) -> str:
    return update_jira_description_impl(issue_key, description, logger)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
