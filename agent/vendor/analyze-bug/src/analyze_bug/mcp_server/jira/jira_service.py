import json

from analyze_bug.core.config import get_jira_auth
from analyze_bug.core.http import classify_http_error, make_http_request
from analyze_bug.core.responses import (
    CredentialError,
    ErrorType,
    make_error_response,
    make_success_response,
)


JIRA_BASE_URL = "http://jira.i-tetris.com"
AI_COMMENT_MARKER = "（AI Generated）"
LEGACY_AI_COMMENT_MARKERS = (
    AI_COMMENT_MARKER,
    "(AI Generated)",
    "(AI Generated Response)",
)


def _extract_user(user: dict | None) -> dict | None:
    if not user:
        return None
    return {
        "name": user.get("name"),
        "display_name": user.get("displayName"),
        "email": user.get("emailAddress"),
    }


def _extract_comments(raw_comments: list[dict]) -> list[dict]:
    comments = []
    for item in raw_comments:
        comments.append(
            {
                "id": item.get("id"),
                "body": item.get("body"),
                "created": item.get("created"),
                "updated": item.get("updated"),
                "author": _extract_user(item.get("author")),
            }
        )
    return comments


def _extract_attachments(raw_attachments: list[dict]) -> list[dict]:
    attachments = []
    for item in raw_attachments:
        attachments.append(
            {
                "id": item.get("id"),
                "filename": item.get("filename"),
                "mime_type": item.get("mimeType"),
                "size": item.get("size"),
                "created": item.get("created"),
                "content": item.get("content"),
            }
        )
    return attachments


def _append_ai_generated_marker(comment: str) -> str:
    body = comment.rstrip()
    while body:
        matched = False
        for marker in LEGACY_AI_COMMENT_MARKERS:
            if body.endswith(marker):
                body = body[: -len(marker)].rstrip()
                matched = True
                break
        if not matched:
            break
    if not body:
        return AI_COMMENT_MARKER
    return f"{body}\n\n{AI_COMMENT_MARKER}"


def _load_field_name_map(auth: tuple[str, str], logger) -> dict[str, str]:
    url = f"{JIRA_BASE_URL}/rest/api/2/field"
    body, status, error = make_http_request(url, auth=auth, logger=logger)
    if error:
        return {}
    try:
        field_list = json.loads(body)
    except json.JSONDecodeError:
        return {}
    return {item.get("id"): item.get("name", item.get("id")) for item in field_list}


def _extract_issue_links(raw_links: list[dict]) -> list[dict]:
    links = []
    for item in raw_links:
        outward = item.get("outwardIssue")
        inward = item.get("inwardIssue")
        other = outward or inward
        if not other:
            continue
        other_fields = other.get("fields") or {}
        links.append(
            {
                "type": (item.get("type") or {}).get("name"),
                "direction": "outward" if outward else "inward",
                "key": other.get("key"),
                "summary": other_fields.get("summary"),
                "status": (other_fields.get("status") or {}).get("name"),
            }
        )
    return links


def _extract_custom_fields(fields: dict, field_name_map: dict[str, str]) -> list[dict]:
    custom_fields = []
    for key, value in fields.items():
        if not key.startswith("customfield_"):
            continue
        if value in (None, "", [], {}):
            continue
        custom_fields.append(
            {
                "id": key,
                "name": field_name_map.get(key, key),
                "value": value,
            }
        )
    custom_fields.sort(key=lambda item: item["name"])
    return custom_fields


def get_jira_issue(issue_key: str, logger) -> str:
    try:
        auth = get_jira_auth()
    except CredentialError:
        return make_error_response(
            ErrorType.CREDENTIAL_MISSING,
            "Jira 凭证未配置",
            "请运行 `analyze-bug-admin configure-jira`。",
        )

    url = f"{JIRA_BASE_URL}/rest/api/2/issue/{issue_key}"
    body, status, error = make_http_request(url, auth=auth, logger=logger)

    if error:
        error_type, message, action = classify_http_error(status, body)
        if status == 404:
            message = f"Jira 问题 '{issue_key}' 不存在"
            action = "请检查 Issue Key 是否正确。"
        return make_error_response(error_type, message, action, {"issue_key": issue_key})

    issue = json.loads(body)
    fields = issue.get("fields", {})
    field_name_map = _load_field_name_map(auth, logger)
    data = {
        "issue_key": issue.get("key", issue_key),
        "summary": fields.get("summary"),
        "description": fields.get("description"),
        "created": fields.get("created"),
        "updated": fields.get("updated"),
        "status": (fields.get("status") or {}).get("name"),
        "issue_type": (fields.get("issuetype") or {}).get("name"),
        "priority": (fields.get("priority") or {}).get("name"),
        "assignee": _extract_user(fields.get("assignee")),
        "reporter": _extract_user(fields.get("reporter")),
        "components": [
            item.get("name")
            for item in (fields.get("components") or [])
            if item.get("name")
        ],
        "labels": fields.get("labels") or [],
        "comments": _extract_comments((fields.get("comment") or {}).get("comments", [])),
        "attachments": _extract_attachments(fields.get("attachment", [])),
        "issue_links": _extract_issue_links(fields.get("issuelinks") or []),
        "custom_fields": _extract_custom_fields(fields, field_name_map),
    }
    return make_success_response(data)


def add_jira_comment(issue_key: str, comment: str, logger) -> str:
    try:
        auth = get_jira_auth()
    except CredentialError:
        return make_error_response(
            ErrorType.CREDENTIAL_MISSING,
            "Jira 凭证未配置",
            "请运行 `analyze-bug-admin configure-jira`。",
        )

    url = f"{JIRA_BASE_URL}/rest/api/2/issue/{issue_key}/comment"
    comment_with_marker = _append_ai_generated_marker(comment)
    body, status, error = make_http_request(
        url,
        method="POST",
        data={"body": comment_with_marker},
        auth=auth,
        logger=logger,
    )
    if error:
        error_type, message, action = classify_http_error(status, body)
        return make_error_response(error_type, f"添加评论失败: {message}", action)

    return make_success_response({"message": "评论添加成功", "issue_key": issue_key})


def update_jira_description(issue_key: str, description: str, logger) -> str:
    try:
        auth = get_jira_auth()
    except CredentialError:
        return make_error_response(
            ErrorType.CREDENTIAL_MISSING,
            "Jira 凭证未配置",
            "请运行 `analyze-bug-admin configure-jira`。",
        )

    url = f"{JIRA_BASE_URL}/rest/api/2/issue/{issue_key}"
    body, status, error = make_http_request(
        url,
        method="PUT",
        data={"fields": {"description": description}},
        auth=auth,
        logger=logger,
    )
    if error:
        error_type, message, action = classify_http_error(status, body)
        return make_error_response(error_type, f"更新描述失败: {message}", action)

    return make_success_response({"message": "描述更新成功", "issue_key": issue_key})
