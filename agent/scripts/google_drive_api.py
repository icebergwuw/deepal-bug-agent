"""Local Google Drive API access. Tokens stay outside the repository."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

CONFIG_DIR = Path.home() / ".config" / "deepal-bug-agent" / "google"
TOKEN_PATH = CONFIG_DIR / "google_token.json"
SECRET_PATH = CONFIG_DIR / "client_secret.json"


def probe() -> dict[str, Any]:
    """Refresh the local token and read Drive about. Never return credentials."""

    if not TOKEN_PATH.is_file() or not SECRET_PATH.is_file():
        return {"ok": False, "entry": None, "error": "missing_token"}
    try:
        secret = json.loads(SECRET_PATH.read_text(encoding="utf-8"))["installed"]
        token = json.loads(TOKEN_PATH.read_text(encoding="utf-8"))
        access_token = _access_token(secret, token)
        request = urllib.request.Request(
            "https://www.googleapis.com/drive/v3/about?fields=user(emailAddress)",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode())
        email = str(payload.get("user", {}).get("emailAddress") or "")
        domain = email.split("@")[-1] if "@" in email else ""
        if not domain:
            return {"ok": False, "entry": None, "error": "about_missing_user"}
        return {"ok": True, "entry": "google_api", "error": None, "account_domain": domain}
    except (OSError, KeyError, json.JSONDecodeError, urllib.error.URLError):
        return {"ok": False, "entry": None, "error": "probe_failed"}


def _access_token(secret: dict[str, Any], token: dict[str, Any]) -> str:
    refresh_token = token.get("refresh_token")
    if not isinstance(refresh_token, str) or not refresh_token:
        raise KeyError("refresh_token")
    body = urllib.parse.urlencode(
        {
            "client_id": secret["client_id"],
            "client_secret": secret["client_secret"],
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }
    ).encode()
    request = urllib.request.Request(secret["token_uri"], data=body, method="POST")
    with urllib.request.urlopen(request, timeout=20) as response:
        refreshed = json.loads(response.read().decode())
    access_token = refreshed.get("access_token")
    if not isinstance(access_token, str) or not access_token:
        raise KeyError("access_token")
    token["access_token"] = access_token
    if "expires_in" in refreshed:
        token["expires_in"] = refreshed["expires_in"]
    TOKEN_PATH.write_text(json.dumps(token, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.chmod(TOKEN_PATH, 0o600)
    return access_token
