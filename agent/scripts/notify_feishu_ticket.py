#!/usr/bin/env python3
"""Notify the recorded Feishu group after a change-sheet ticket is created."""

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_text(args: argparse.Namespace) -> str:
    lines = [
        f"已新建需求票 {args.key}",
        args.summary,
        f"http://jira.i-tetris.com/browse/{args.key}",
        f"经办人：{args.assignee}",
        f"来源：{args.source}",
    ]
    dependencies = [item.strip() for item in args.dependency if item and item.strip()]
    if dependencies:
        lines.append("")
        lines.append("依赖：")
        lines.extend(f"- {item}" for item in dependencies)
    return "\n".join(lines)


def post(url: str, payload: dict, token=None) -> dict:
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")[:300]
        return {"code": error.code, "msg": body}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--assignee", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--dependency", action="append", default=[])
    args = parser.parse_args()

    root = repo_root()
    config = load_json(root / "agent/config/feishu-notify.json")
    secret_path = root / config["secret_file"]
    if not secret_path.is_file():
        print(json.dumps({"ok": False, "error": "missing_local_secret"}, ensure_ascii=False))
        return 2
    secret = load_json(secret_path).get("app_secret")
    if not secret or secret.startswith("put-the-local"):
        print(json.dumps({"ok": False, "error": "missing_local_secret"}, ensure_ascii=False))
        return 2

    auth = post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        {"app_id": config["app_id"], "app_secret": secret},
    )
    if auth.get("code") != 0 or not auth.get("tenant_access_token"):
        print(json.dumps({"ok": False, "step": "auth", "code": auth.get("code"), "msg": auth.get("msg")}, ensure_ascii=False))
        return 1

    sent = post(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=" + config["receive_id_type"],
        {
            "receive_id": config["receive_id"],
            "msg_type": "text",
            "content": json.dumps({"text": build_text(args)}, ensure_ascii=False),
        },
        auth["tenant_access_token"],
    )
    data = sent.get("data") or {}
    ok = sent.get("code") == 0 and bool(data.get("message_id"))
    print(json.dumps({
        "ok": ok,
        "code": sent.get("code"),
        "msg": sent.get("msg"),
        "message_id": data.get("message_id"),
        "chat_id": config["receive_id"],
    }, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
