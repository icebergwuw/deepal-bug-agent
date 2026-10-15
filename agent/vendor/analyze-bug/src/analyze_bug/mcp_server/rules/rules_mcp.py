from mcp.server.fastmcp import FastMCP

from analyze_bug.core.logging_utils import setup_logger
from analyze_bug.mcp_server.rules.rules_service import (
    get_analysis_rules as get_analysis_rules_impl,
    get_fault_priority as get_fault_priority_impl,
    get_module_rules as get_module_rules_impl,
    get_rules_version as get_rules_version_impl,
)


logger = setup_logger("rules-mcp", "rules_mcp.log")
mcp = FastMCP("RulesAnalyzer")


@mcp.tool()
def get_analysis_rules() -> str:
    return get_analysis_rules_impl(logger)


@mcp.tool()
def get_module_rules(module: str) -> str:
    return get_module_rules_impl(module, logger)


@mcp.tool()
def get_fault_priority() -> str:
    return get_fault_priority_impl(logger)


@mcp.tool()
def get_rules_version() -> str:
    return get_rules_version_impl(logger)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
