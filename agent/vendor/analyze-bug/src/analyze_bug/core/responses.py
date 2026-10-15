import json


class ErrorType:
    CREDENTIAL_MISSING = "CREDENTIAL_MISSING"
    COOKIE_EXPIRED = "COOKIE_EXPIRED"
    COOKIE_MISSING = "COOKIE_MISSING"
    NOT_FOUND = "NOT_FOUND"
    FORBIDDEN = "FORBIDDEN"
    UNAUTHORIZED = "UNAUTHORIZED"
    NETWORK_ERROR = "NETWORK_ERROR"
    TIMEOUT = "TIMEOUT"
    UNKNOWN = "UNKNOWN"


class CredentialError(Exception):
    """Raised when persisted credentials are missing or incomplete."""


def make_error_response(
    error_type: str,
    message: str,
    action: str | None = None,
    details: dict | None = None,
) -> str:
    payload = {
        "error": True,
        "error_type": error_type,
        "message": message,
    }
    if action:
        payload["action"] = action
    if details:
        payload["details"] = details
    return json.dumps(payload, ensure_ascii=False, indent=2)


def make_success_response(data) -> str:
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            pass
    return json.dumps({"error": False, "data": data}, ensure_ascii=False, indent=2)
