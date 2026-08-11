#!/usr/bin/env python3
"""Prepare and validate a local operator before any Bug-sheet write.

The tracked repository contains team rules and owner routing.  This script keeps
machine-specific identity and access receipts in an ignored local JSON file.  It
never accepts or stores passwords, browser cookies, API keys, or access tokens.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "agent/bug-owners/registry.yaml"
PROFILE_PATH = ROOT / "agent/config/local-profile.json"
SKILL_SOURCE = ROOT / "agent/skills/deepal-product-bug-handler/SKILL.md"
PLATFORMS = ("jira", "google_drive", "alchemy", "mastergo")


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"null", "~"}:
        return None
    if value in {"true", "false"}:
        return value == "true"
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return json.loads(value)
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value


def load_owners(path: Path = REGISTRY_PATH) -> dict[str, dict[str, Any]]:
    """Read top-level owner scalar fields without requiring a YAML package."""

    owners: dict[str, dict[str, Any]] = {}
    current: dict[str, Any] | None = None
    in_owners = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if raw_line == "owners:":
            in_owners = True
            continue
        if not in_owners:
            continue
        start = re.match(r'^  - id:\s*(.+?)\s*$', raw_line)
        if start:
            owner_id = str(parse_scalar(start.group(1)))
            current = {"id": owner_id}
            owners[owner_id] = current
            continue
        field = re.match(r'^    ([a-zA-Z0-9_]+):\s*(.*?)\s*$', raw_line)
        if current is not None and field:
            current[field.group(1)] = parse_scalar(field.group(2))
    return owners


def codex_home() -> Path:
    configured = os.environ.get("CODEX_HOME")
    return Path(configured).expanduser() if configured else Path.home() / ".codex"


def installed_skill_path() -> Path:
    return codex_home() / "skills/deepal-product-bug-handler/SKILL.md"


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def format_time(value: datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def load_profile(path: Path = PROFILE_PATH) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("local-profile.json 必须是 JSON 对象")
    return payload


def save_profile(payload: dict[str, Any], path: Path = PROFILE_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.chmod(temporary, 0o600)
    temporary.replace(path)
    os.chmod(path, 0o600)


def owner_is_writable(owner: dict[str, Any] | None) -> bool:
    return bool(
        owner
        and owner.get("status") == "active"
        and owner.get("write_mode") == "read_write"
    )


def initialize_profile(
    owner_id: str,
    allowed_owner_ids: list[str],
    *,
    replace: bool,
    owners: dict[str, dict[str, Any]],
    path: Path = PROFILE_PATH,
) -> dict[str, Any]:
    current = load_profile(path)
    if current and not replace:
        raise ValueError("本机身份已存在；如需更换，明确使用 --replace-profile")
    if not owner_is_writable(owners.get(owner_id)):
        raise ValueError(f"负责人 {owner_id} 不是 active + read_write")
    allowed = list(dict.fromkeys([owner_id, *allowed_owner_ids]))
    invalid = [item for item in allowed if not owner_is_writable(owners.get(item))]
    if invalid:
        raise ValueError("不可写负责人：" + "、".join(invalid))
    now = format_time(utc_now())
    payload = {
        "schema_version": 1,
        "operator_owner_id": owner_id,
        "allowed_write_owner_ids": allowed,
        "identity_confirmed_at": now,
        "online_access": {},
    }
    save_profile(payload, path)
    return payload


def update_allowed_owners(
    profile: dict[str, Any],
    additions: list[str],
    owners: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    invalid = [item for item in additions if not owner_is_writable(owners.get(item))]
    if invalid:
        raise ValueError("不可写负责人：" + "、".join(invalid))
    profile["allowed_write_owner_ids"] = list(
        dict.fromkeys([*profile.get("allowed_write_owner_ids", []), *additions])
    )
    return profile


def record_access(profile: dict[str, Any], platforms: list[str]) -> dict[str, Any]:
    access = profile.setdefault("online_access", {})
    now = format_time(utc_now())
    for platform in platforms:
        access[platform] = {
            "verified_at": now,
            "method": "live_read_verified_by_agent",
        }
    return profile


def skill_status(source: Path = SKILL_SOURCE, target: Path | None = None) -> dict[str, Any]:
    target = target or installed_skill_path()
    installed = target.is_file()
    matches = installed and target.read_text(encoding="utf-8") == source.read_text(
        encoding="utf-8"
    )
    return {
        "installed": installed,
        "matches_template": matches,
        "target": str(target),
    }


def local_secret_file_status(path: Path | None = None) -> dict[str, Any]:
    path = path or ROOT / ".env"
    if not path.exists():
        return {"exists": False, "private_permissions": True, "path": str(path)}
    mode = path.stat().st_mode & 0o777
    return {
        "exists": True,
        "private_permissions": mode & 0o077 == 0,
        "mode": oct(mode),
        "path": str(path),
    }


def assess(
    profile: dict[str, Any] | None,
    owners: dict[str, dict[str, Any]],
    *,
    required_owner_id: str | None,
    required_platforms: list[str],
    max_access_age_hours: float,
    skill: dict[str, Any],
    secret_file: dict[str, Any] | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    now = now or utc_now()
    blockers: list[str] = []
    warnings: list[str] = []
    guidance: list[str] = []

    operator_id = profile.get("operator_owner_id") if profile else None
    identity_ready = bool(profile and owner_is_writable(owners.get(str(operator_id))))
    if not identity_ready:
        blockers.append("本机尚未绑定 active + read_write 负责人身份")
        guidance.append(
            "先运行 --list-owners，再运行 --init-owner <owner-id>；不要根据电脑用户名猜身份"
        )

    allowed = set(profile.get("allowed_write_owner_ids", [])) if profile else set()
    owner_scope_ready = not required_owner_id or required_owner_id in allowed
    if required_owner_id and not owner_scope_ready:
        blockers.append(f"本机未授权写负责人范围：{required_owner_id}")
        guidance.append(f"由当前操作者明确运行 --allow-owner {required_owner_id}")

    if not skill.get("matches_template"):
        blockers.append("已安装 Bug Skill 缺失或与 Git 模板不一致")
        guidance.append("运行 python3 agent/scripts/sync_bug_skill.py --install")

    secret_file = secret_file or local_secret_file_status()
    if secret_file.get("exists") and not secret_file.get("private_permissions"):
        blockers.append("本机 .env 权限过宽，可能向其他本地用户暴露凭据")
        guidance.append("运行 chmod 600 .env；不要把 .env 加入Git")

    access_results: dict[str, dict[str, Any]] = {}
    access = profile.get("online_access", {}) if profile else {}
    max_age = timedelta(hours=max_access_age_hours)
    for platform in PLATFORMS:
        receipt = access.get(platform, {}) if isinstance(access, dict) else {}
        verified_at = parse_time(receipt.get("verified_at")) if isinstance(receipt, dict) else None
        fresh = bool(verified_at and now - verified_at <= max_age)
        access_results[platform] = {
            "fresh": fresh,
            "verified_at": receipt.get("verified_at") if isinstance(receipt, dict) else None,
            "required": platform in required_platforms,
        }
        if platform in required_platforms and not fresh:
            blockers.append(f"{platform} 尚未完成本次有效期内的真实读取验证")
            guidance.append(
                f"在已登录环境真实读取 {platform} 后运行 --mark-access {platform}；不得只凭页面可打开标记"
            )
        elif not fresh:
            warnings.append(f"{platform} 未验证；涉及该平台的 Bug 将按证据门禁降级")

    return {
        "ok": not blockers,
        "mode": "read_write" if not blockers else "read_only",
        "profile_path": str(PROFILE_PATH),
        "operator_owner_id": operator_id,
        "allowed_write_owner_ids": sorted(allowed),
        "identity_ready": identity_ready,
        "owner_scope_ready": owner_scope_ready,
        "skill": skill,
        "local_secret_file": secret_file,
        "online_access": access_results,
        "blockers": blockers,
        "warnings": warnings,
        "guidance": list(dict.fromkeys(guidance)),
        "security": "本文件不保存密码、Cookie、Token或平台访问口令",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list-owners", action="store_true")
    parser.add_argument("--init-owner")
    parser.add_argument("--replace-profile", action="store_true")
    parser.add_argument("--allow-owner", action="append", default=[])
    parser.add_argument("--allow-all-active", action="store_true")
    parser.add_argument("--mark-access", action="append", choices=PLATFORMS, default=[])
    parser.add_argument("--require-owner")
    parser.add_argument("--require-platform", action="append", choices=PLATFORMS, default=[])
    parser.add_argument("--max-access-age-hours", type=float, default=24.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    owners = load_owners()
    if args.list_owners:
        available = [
            {
                "id": owner_id,
                "name": owner.get("name"),
                "status": owner.get("status"),
                "write_mode": owner.get("write_mode"),
            }
            for owner_id, owner in owners.items()
        ]
        print(json.dumps({"owners": available}, ensure_ascii=False, indent=2))
        return 0

    try:
        additions = list(args.allow_owner)
        if args.allow_all_active:
            additions.extend(
                owner_id for owner_id, owner in owners.items() if owner_is_writable(owner)
            )
        if args.init_owner:
            profile = initialize_profile(
                args.init_owner,
                additions,
                replace=args.replace_profile,
                owners=owners,
            )
        else:
            profile = load_profile()
            if (additions or args.mark_access) and profile is None:
                raise ValueError("先使用 --init-owner 绑定本机身份")
            if additions:
                profile = update_allowed_owners(profile, additions, owners)  # type: ignore[arg-type]
            if args.mark_access:
                profile = record_access(profile, args.mark_access)  # type: ignore[arg-type]
            if additions or args.mark_access:
                save_profile(profile)  # type: ignore[arg-type]
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False, indent=2))
        return 2

    result = assess(
        profile,
        owners,
        required_owner_id=args.require_owner,
        required_platforms=args.require_platform,
        max_access_age_hours=args.max_access_age_hours,
        skill=skill_status(),
        secret_file=local_secret_file_status(),
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
