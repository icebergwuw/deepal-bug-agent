from mcp.server.fastmcp import FastMCP

from analyze_bug.core.logging_utils import setup_logger
from analyze_bug.mcp_server.debug.debug_service import (
    fetch_debug_log_list as fetch_debug_log_list_impl,
    get_debug_log_detail as get_debug_log_detail_impl,
)

logger = setup_logger("debug-mcp", "debug_mcp.log")
mcp = FastMCP("DebugAnalyzer")


@mcp.tool()
def fetch_debug_log_list(
    log_type: str,
    vin: str,
    start_time: str,
    end_time: str,
    query: str | None = None,
) -> str:
    return fetch_debug_log_list_impl(log_type, vin, start_time, end_time, logger, query=query)


@mcp.tool()
def get_debug_log_detail(log_type: str, rid: str, ts: str) -> str:
    return get_debug_log_detail_impl(log_type, rid, ts, logger)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
