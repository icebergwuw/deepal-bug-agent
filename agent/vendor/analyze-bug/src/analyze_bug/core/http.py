import base64
import json
import socket
import time
from urllib import error, request

from analyze_bug.core.responses import ErrorType


def check_cookie_expired(response_body: str, status_code: int | None = None) -> bool:
    if status_code in (401, 403):
        return True

    indicators = [
        "unauthorized",
        "login required",
        "session expired",
        "token expired",
        "请登录",
        "登录已过期",
        "认证失败",
    ]
    response_lower = response_body.lower()
    return any(indicator in response_lower for indicator in indicators)


def classify_http_error(status_code: int, error_body: str = "") -> tuple[str, str, str]:
    if status_code == 401:
        return (
            ErrorType.UNAUTHORIZED,
            "认证失败，用户名或密码错误",
            "请运行 `analyze-bug-admin configure-jira` 重新配置 Jira 凭证。",
        )
    if status_code == 403:
        return (
            ErrorType.FORBIDDEN,
            "权限不足，无法访问该资源",
            "请确认账号是否有权限访问该 Jira 问题。",
        )
    if status_code == 404:
        return (
            ErrorType.NOT_FOUND,
            "资源不存在",
            "请检查 Jira Issue Key 是否正确。",
        )
    if status_code >= 500:
        return (
            ErrorType.NETWORK_ERROR,
            f"服务器错误 (HTTP {status_code})",
            "服务器暂时不可用，请稍后重试。",
        )
    return (
        ErrorType.UNKNOWN,
        f"HTTP 错误 {status_code}",
        error_body or "请检查网络连接或稍后重试。",
    )


def make_http_request(
    url: str,
    method: str = "GET",
    data: dict | bytes | None = None,
    headers: dict | None = None,
    auth: tuple[str, str] | None = None,
    cookie: str | None = None,
    timeout: int = 15,
    logger=None,
    max_retries: int = 2,
    retry_delay: float = 1.0,
) -> tuple[str, int | None, str | None]:
    request_headers = dict(headers or {})
    payload = data
    if isinstance(data, dict):
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        request_headers["Content-Type"] = "application/json"

    if auth:
        auth_str = base64.b64encode(f"{auth[0]}:{auth[1]}".encode("utf-8")).decode("utf-8")
        request_headers["Authorization"] = f"Basic {auth_str}"

    if cookie:
        request_headers["Cookie"] = cookie

    last_error = None
    for attempt in range(max_retries + 1):
        req = request.Request(
            url,
            data=payload,
            headers=request_headers,
            method=method,
        )
        if logger:
            logger.debug("HTTP %s %s (attempt %s)", method, url, attempt + 1)

        try:
            # 内网 Jira 不走系统代理。macOS 上 urllib 会拾取本机代理，导致 i-tetris.com 被断开。
            opener = request.build_opener(request.ProxyHandler({}))
            with opener.open(req, timeout=timeout) as response:
                body = response.read().decode("utf-8")
                return body, response.getcode(), None
        except error.HTTPError as exc:
            error_body = ""
            try:
                error_body = exc.read().decode("utf-8")
            except Exception:
                error_body = ""
            message = f"HTTP Error {exc.code}: {exc.reason}"
            if error_body:
                message = f"{message}\n{error_body}"
            if logger:
                logger.error(message)
            return error_body, exc.code, message
        except (error.URLError, socket.timeout, TimeoutError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            if logger:
                logger.warning("Request attempt %s failed: %s", attempt + 1, last_error)
        except Exception as exc:
            last_error = f"Request Error: {exc}"
            if logger:
                logger.warning("Request attempt %s failed: %s", attempt + 1, last_error)

        if attempt < max_retries:
            time.sleep(retry_delay)

    final_error = f"{last_error} (已重试 {max_retries} 次)" if last_error else "Request failed"
    if logger:
        logger.error(final_error)
    return "", None, final_error
