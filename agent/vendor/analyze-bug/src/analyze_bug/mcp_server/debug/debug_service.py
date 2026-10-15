from analyze_bug.core.config import get_debug_cookie
from analyze_bug.core.http import check_cookie_expired, make_http_request
from analyze_bug.core.responses import (
    CredentialError,
    ErrorType,
    make_error_response,
    make_success_response,
)


DEBUG_BASE_URL = "https://vos-debug.i-tetris.com"


def handle_debug_response(body: str, status: int | None, error: str | None, operation: str, logger) -> str:
    if check_cookie_expired(body, status):
        logger.warning("Detected expired debug cookie")
        return make_error_response(
            ErrorType.COOKIE_EXPIRED,
            "Debug 系统 Cookie 已过期",
            "请运行 `analyze-bug-admin configure-debug` 更新 Cookie。",
        )

    if error:
        if "timeout" in error.lower():
            return make_error_response(
                ErrorType.TIMEOUT,
                f"{operation}超时",
                "Debug 系统响应缓慢，请稍后重试。",
            )
        return make_error_response(
            ErrorType.NETWORK_ERROR,
            f"{operation}失败: {error}",
            "请检查网络连接或稍后重试。",
        )

    return make_success_response(body)


def fetch_debug_log_list(
    log_type: str,
    vin: str,
    start_time: str,
    end_time: str,
    logger,
    query: str | None = None,
) -> str:
    try:
        cookie = get_debug_cookie()
    except CredentialError:
        return make_error_response(
            ErrorType.COOKIE_MISSING,
            "Debug 系统 Cookie 未配置",
            "请运行 `analyze-bug-admin configure-debug`。",
        )

    payload = {
        "vin": vin,
        "begin_date": start_time,
        "end_date": end_time,
        "page_index": 1,
        "page_size": 20,
    }
    if query:
        payload["query"] = query

    body, status, error = make_http_request(
        f"{DEBUG_BASE_URL}/api/{log_type}_log/list",
        method="POST",
        data=payload,
        cookie=cookie,
        logger=logger,
    )
    return handle_debug_response(body, status, error, "检索日志列表", logger)


def get_debug_log_detail(log_type: str, rid: str, ts: str, logger) -> str:
    try:
        cookie = get_debug_cookie()
    except CredentialError:
        return make_error_response(
            ErrorType.COOKIE_MISSING,
            "Debug 系统 Cookie 未配置",
            "请运行 `analyze-bug-admin configure-debug`。",
        )

    body, status, error = make_http_request(
        f"{DEBUG_BASE_URL}/api/{log_type}_log/detail?rid={rid}&ts={ts}",
        cookie=cookie,
        logger=logger,
    )
    return handle_debug_response(body, status, error, "获取日志详情", logger)
