from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Any, Literal

import httpx
from dotenv import load_dotenv
from pydantic import Field, StringConstraints

from analyze_bug.core.paths import get_config_file, iter_legacy_config_files

load_dotenv()

logger = logging.getLogger("analyze_bug.ops-mcp")

DEFAULT_BASE_URL = "https://alchemy.i-tetris.com/api/v1/ops"
PROJECT_ROOT = Path(__file__).resolve().parents[4]

SortOrder = Literal["asc", "desc"]
InheritState = Literal["COMMON", "INHERIT", "INHERIT_UPDATE", "PROJECT_CREATE"]
FunctionState = Literal["DRAFT", "LOCKED", "ISSUED"]
DialogueTestType = Literal["online", "offline"]

NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
PositiveInt = Annotated[int, Field(gt=0)]
PageSize = Annotated[int, Field(gt=0, le=200)]
NonNegativeInt = Annotated[int, Field(ge=0)]
FunctionStateInput = FunctionState | list[FunctionState] | None
StringOrNumber = NonEmptyStr | PositiveInt

DIALOGUE_ENV_CONFIG: dict[str, dict[str, Any]] = {
    "stg": {
        "host": "https://ds-stg.i-tetris.com:443",
        "appId": 100246271,
    },
    "ca-prod": {
        "host": "https://ds.changan.x-tetris.com:443",
        "appId": 100246271,
    },
    "df-prod": {
        "host": "https://tsp-dongfeng.i-tetris.com:443",
        "appId": 102312379,
    },
    "jmc-prod": {
        "host": "https://ds-jmc.x-tetris.com:443",
        "appId": 101568913,
    },
}

DEFAULT_DIALOGUE_LOCATION: dict[str, Any] = {
    "address": "",
    "city_name": "东莞市",
    "latitude": 23.076159166666667,
    "longitude": 113.9518675,
    "name": "",
}

DEFAULT_DIALOGUE_BASE: dict[str, Any] = {
    "vehicle_id": "029f779022352ab17f26a2691eb2e926",
    "vehicle_model": "BIGSUR",
    "sdk_version": "20250306",
    "language": "CHINESE",
    "region": "CHINA_MAINLAND",
    "context_type": "INIT",
    "source": "FT_TEST",
    "wakeup_free": "false",
    "awaken": "true",
    "awaken_zone": "FRONT_LEFT",
    "voice_zone": "FRONT_LEFT",
    "ui_nodes": [],
    "last_req_id": "",
    "last_query": "",
    "last_tts": "",
    "last_query_type": "",
    "interrupted_req_id": "",
    "dialog_timestamp": 0,
    "tts_stop_timestamp": "0",
}

DEFAULT_ONLINE_VEHICLE_CONFIG: dict[str, Any] = {
    "is_right_rudder": False,
    "mic_number": 4,
    "voice_id": 0,
    "asr_nonstop": True,
    "continuous_dialog": True,
    "navi_app": "GAODE",
    "chat_llm_model": "doubao",
}

DEFAULT_OFFLINE_VEHICLE_CONFIG: dict[str, Any] = {
    "is_right_rudder": False,
    "mic_number": 4,
    "voice_id": 0,
    "asr_nonstop": True,
    "continuous_dialog": True,
    "navi_app": "GAODE",
}


@dataclass(frozen=True)
class Settings:
    base_url: str
    cookie: str

    @classmethod
    def from_env(cls) -> "Settings":
        import os

        raw_base_url = (
            os.environ.get("ALCHEMY_BASE_URL")
            or _load_persisted_setting("ALCHEMY_BASE_URL")
            or DEFAULT_BASE_URL
        ).rstrip("/")
        raw_cookie = (
            os.environ.get("ALCHEMY_COOKIE")
            or _load_persisted_setting("ALCHEMY_COOKIE")
            or ""
        ).strip()
        return cls(base_url=raw_base_url, cookie=raw_cookie)


@dataclass(frozen=True)
class DownloadedFile:
    buffer: bytes
    filename: str | None
    content_type: str | None


@dataclass(frozen=True)
class AppRuntime:
    service: AlchemyService | None


class AlchemyApiError(RuntimeError):
    def __init__(self, message: str, status: int | None = None, body: Any | None = None) -> None:
        super().__init__(message)
        self.status = status
        self.body = body


class AlchemyClient:
    def __init__(
        self,
        api_base_url: str,
        cookie_header: str,
        *,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self.api_base_url = api_base_url.rstrip("/")
        self.cookie_header = cookie_header
        self._transport = transport
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "AlchemyClient":
        await self._ensure_client()
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return await self._request_json("GET", path, params=params)

    async def post_json(self, path: str, body: Any | None = None) -> Any:
        return await self._request_json("POST", path, json_body=body)

    async def post_form(
        self,
        path: str,
        *,
        data: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
    ) -> Any:
        return await self._request_json("POST", path, data=data, files=files)

    async def download_file(self, path: str, params: dict[str, Any] | None = None) -> DownloadedFile:
        client = await self._ensure_client()
        response = await client.request(
            "GET",
            self._build_url(path),
            params=build_query_params(params),
        )

        if response.status_code >= 400:
            raise AlchemyApiError(
                f"Alchemy API download failed with status {response.status_code}",
                response.status_code,
                response.text,
            )

        return DownloadedFile(
            buffer=response.content,
            filename=parse_filename_from_content_disposition(response.headers.get("content-disposition")),
            content_type=response.headers.get("content-type"),
        )

    async def _request_json(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: Any | None = None,
        data: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
    ) -> Any:
        client = await self._ensure_client()
        response = await client.request(
            method,
            self._build_url(path),
            params=build_query_params(params),
            json=json_body,
            data=data,
            files=files,
        )

        raw = response.text
        parsed = safe_json_parse(raw) if raw else None

        if response.status_code >= 400:
            raise AlchemyApiError(
                f"Alchemy API request failed with status {response.status_code}",
                response.status_code,
                parsed if parsed is not None else raw,
            )

        if parsed is None:
            raise AlchemyApiError("Alchemy API returned a non-JSON response", response.status_code, raw)

        if not isinstance(parsed, dict):
            return parsed

        if "result_code" not in parsed:
            return parsed

        if parsed.get("result_code") != 0:
            raise AlchemyApiError(
                parsed.get("message") or "Alchemy API returned a business error",
                response.status_code,
                parsed,
            )

        return parsed.get("data")

    async def _ensure_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                headers={
                    "Accept": "application/json, text/plain, */*",
                    "Cookie": self.cookie_header,
                    "Referer": "https://alchemy.i-tetris.com/",
                },
                follow_redirects=True,
                timeout=httpx.Timeout(60.0, connect=10.0),
                transport=self._transport,
                trust_env=False,
            )
        return self._client

    def _build_url(self, path: str) -> str:
        return f"{self.api_base_url}{path}"


class AlchemyService:
    def __init__(self, client: AlchemyClient, *, project_root: Path | None = None) -> None:
        self.client = client
        self.project_root = project_root or PROJECT_ROOT

    async def export_interface_protocol(
        self,
        *,
        functionTypeId: int | None,
        projectId: int | None,
        outputDir: str | None,
    ) -> dict[str, Any]:
        file = await self.client.download_file(
            "/fi/function_type/exportNluMappingExcel",
            {
                "functionTypeId": functionTypeId,
                "projectId": projectId,
            },
        )
        final_output_dir = resolve_output_dir(outputDir)
        final_output_dir.mkdir(parents=True, exist_ok=True)

        filename = safe_decode_filename(file.filename or build_protocol_export_name(functionTypeId, projectId))
        output_path = final_output_dir / filename
        output_path.write_bytes(file.buffer)
        logger.info("Saved protocol export to %s", output_path)

        return {
            "ok": True,
            "functionTypeId": functionTypeId,
            "projectId": projectId,
            "contentType": file.content_type,
            "savedTo": str(output_path),
            "fileName": filename,
            "size": len(file.buffer),
        }

    async def list_intents(self) -> dict[str, Any]:
        items = ensure_list(await self.client.get("/specification/intent_list"))
        return {
            "total": len(items),
            "items": [summarize_intent(ensure_record(item, "intent")) for item in items],
        }

    async def list_slots(self) -> dict[str, Any]:
        items = [item for item in ensure_list(await self.client.get("/specification/slot_list")) if isinstance(item, str)]
        return {
            "total": len(items),
            "items": items,
        }

    async def list_slot_properties(
        self,
        *,
        dictType: int | None,
        dictTerm: str | None,
        language: str | None,
        dictName: str | None,
        slotDictProp: str | None,
        orderByUpdateTime: str | None,
        orderBySlotDictName: str | None,
        orderBySlotDictProp: str | None,
        pageNum: int,
        pageSize: int,
    ) -> dict[str, Any]:
        data = ensure_record(
            await self.client.get(
                "/tts/slot/page",
                {
                    "dictType": dictType,
                    "dictTerm": dictTerm,
                    "language": language,
                    "dictName": dictName,
                    "slotDictProp": slotDictProp,
                    "orderByUpdateTime": orderByUpdateTime,
                    "orderBySlotDictName": orderBySlotDictName,
                    "orderBySlotDictProp": orderBySlotDictProp,
                    "pageNum": pageNum,
                    "pageSize": pageSize,
                },
            ),
            "slot property page",
        )

        items = ensure_list(data.get("data"))
        return {
            "total": data.get("total"),
            "pageNum": pageNum,
            "pageSize": pageSize,
            "items": [summarize_slot_property(ensure_record(item, "slot property")) for item in items],
        }

    async def list_dialogue_sessions(self, *, dialogueTestType: DialogueTestType) -> dict[str, Any]:
        sessions = await self.list_dialogue_sessions_raw(dialogueTestType)
        return {
            "dialogueTestType": dialogueTestType,
            "total": len(sessions),
            "items": [summarize_dialogue_session(item) for item in sessions],
        }

    async def get_dialogue_records(self, *, requestId: str, dialogueEnv: str | None) -> dict[str, Any]:
        records = await self.get_dialogue_records_raw(requestId, dialogueEnv)
        return {
            "requestId": requestId,
            "dialogueEnv": dialogueEnv,
            "total": len(records),
            "items": [summarize_dialogue_record(item) for item in records],
        }

    async def chat_dialogue(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self.execute_chat_dialogue(payload)

    async def continue_dialogue_session(self, payload: dict[str, Any]) -> dict[str, Any]:
        session_id = as_trimmed_string(payload.get("sessionId"))
        if not session_id:
            raise AlchemyApiError("sessionId is required.")
        context = await self.resolve_dialogue_session_context(
            session_id,
            payload.get("dialogueTestType"),
            payload.get("dialogueEnv"),
        )
        merged = merge_dialogue_input_with_session_defaults(payload, context["session"], context)
        return await self.execute_chat_dialogue(merged)

    async def delete_dialogue_session(self, *, requestId: str, dialogueEnv: str | None) -> dict[str, Any]:
        deleted_result = await self.client.get(
            f"/tts/dialogue/remove/{quote_path_value(requestId)}",
            {
                "dialogueEnv": dialogueEnv,
            },
        )
        return {
            "ok": deleted_result,
            "requestId": requestId,
            "dialogueEnv": dialogueEnv,
        }

    async def list_function_categories(
        self,
        *,
        projectId: int | None,
        functionId: int | None,
        name: str | None,
        functionTypeId: int | None,
        reviewState: int | None,
        functionState: FunctionStateInput,
        offlinePriority: bool | None,
        inheritState: str | None,
        metaId: int | None,
        intentId: str | None,
        carType: str | None,
    ) -> dict[str, Any]:
        data = ensure_record(
            await self.client.get(
                "/fi/function_type/tree_count",
                {
                    "projectId": projectId,
                    "functionId": functionId,
                    "name": name,
                    "functionTypeId": functionTypeId,
                    "reviewState": reviewState,
                    "functionState": normalize_function_state(functionState),
                    "offlinePriority": offlinePriority,
                    "inheritState": inheritState,
                    "metaId": metaId,
                    "intentId": intentId,
                    "carType": carType,
                },
            ),
            "function categories",
        )
        return {
            "totalCategories": data.get("total"),
            "categories": flatten_categories(ensure_list(data.get("list"))),
        }

    async def list_standard_functions(
        self,
        *,
        id: int | None,
        name: str | None,
        functionTypeId: int | None,
        reviewState: int | None,
        functionState: FunctionStateInput,
        offlinePriority: bool | None,
        orderByCreateTime: str | None,
        orderByName: str | None,
        metaId: int | None,
        intentId: str | None,
        pageNum: int,
        pageSize: int,
        carType: str | None,
    ) -> dict[str, Any]:
        data = await self._list_functions_page(
            {
                "id": id,
                "name": name,
                "functionTypeId": functionTypeId,
                "reviewState": reviewState,
                "functionState": normalize_function_state(functionState),
                "offlinePriority": offlinePriority,
                "orderByCreateTime": orderByCreateTime,
                "orderByName": orderByName,
                "metaId": metaId,
                "intentId": intentId,
                "pageNum": pageNum,
                "pageSize": pageSize,
                "carType": carType,
            }
        )
        items = [item for item in data["items"] if item.get("projectId") is None]
        return {
            "scope": "standard",
            "total": data["total"],
            "pageNum": pageNum,
            "pageSize": pageSize,
            "items": [summarize_function(item) for item in items],
        }

    async def list_functions(
        self,
        *,
        id: int | None,
        name: str | None,
        functionTypeId: int | None,
        reviewState: int | None,
        functionState: FunctionStateInput,
        offlinePriority: bool | None,
        orderByCreateTime: str | None,
        orderByName: str | None,
        projectId: int | None,
        inheritState: str | None,
        metaId: int | None,
        intentId: str | None,
        pageNum: int,
        pageSize: int,
        carType: str | None,
    ) -> dict[str, Any]:
        data = await self._list_functions_page(
            {
                "id": id,
                "name": name,
                "functionTypeId": functionTypeId,
                "reviewState": reviewState,
                "functionState": normalize_function_state(functionState),
                "offlinePriority": offlinePriority,
                "orderByCreateTime": orderByCreateTime,
                "orderByName": orderByName,
                "projectId": projectId,
                "inheritState": inheritState,
                "metaId": metaId,
                "intentId": intentId,
                "pageNum": pageNum,
                "pageSize": pageSize,
                "carType": carType,
            }
        )
        return {
            "total": data["total"],
            "pageNum": pageNum,
            "pageSize": pageSize,
            "items": [summarize_function(item) for item in data["items"]],
        }

    async def get_standard_function_detail(self, *, id: int) -> dict[str, Any]:
        data = await self.get_function_detail_raw(id)
        if data.get("projectId") is not None:
            raise AlchemyApiError(f"Function {id} is a project function, not a standard function.")
        return inject_protocol_fields(data)

    async def get_function_detail(self, *, id: int) -> dict[str, Any]:
        return inject_protocol_fields(await self.get_function_detail_raw(id))

    async def get_function_vehicle_config(self, *, functionId: int) -> dict[str, Any]:
        data = await self.client.get("/rd/getConfigJson", {"functionId": functionId})
        if isinstance(data, str):
            config_json = data
            parsed = try_parse_json_string(data)
        else:
            parsed = data
            config_json = json.dumps(data, ensure_ascii=False, indent=2)
        return {
            "functionId": functionId,
            "configJson": config_json,
            "config": parsed,
        }

    async def list_projects(
        self,
        *,
        projectName: str | None,
        orderByUpdateTime: str,
        pageNum: int,
        pageSize: int,
    ) -> dict[str, Any]:
        data = ensure_record(
            await self.client.get(
                "/project/list",
                {
                    "projectName": projectName,
                    "orderByUpdateTime": orderByUpdateTime,
                    "pageNum": pageNum,
                    "pageSize": pageSize,
                },
            ),
            "project page",
        )
        items = ensure_list(data.get("data"))
        return {
            "total": data.get("total"),
            "pageNum": pageNum,
            "pageSize": pageSize,
            "items": [summarize_project(ensure_record(item, "project")) for item in items],
        }

    async def get_project_detail(self, *, id: int) -> dict[str, Any]:
        return ensure_record(await self.client.get("/project/detail", {"id": id}), "project detail")

    async def list_project_functions(
        self,
        *,
        projectId: int,
        id: int | None,
        name: str | None,
        functionTypeId: int | None,
        reviewState: int | None,
        functionState: FunctionStateInput,
        offlinePriority: bool | None,
        orderByCreateTime: str | None,
        orderByName: str | None,
        inheritState: str | None,
        metaId: int | None,
        intentId: str | None,
        pageNum: int,
        pageSize: int,
        carType: str | None,
    ) -> dict[str, Any]:
        data = await self._list_functions_page(
            {
                "projectId": projectId,
                "id": id,
                "name": name,
                "functionTypeId": functionTypeId,
                "reviewState": reviewState,
                "functionState": normalize_function_state(functionState),
                "offlinePriority": offlinePriority,
                "orderByCreateTime": orderByCreateTime,
                "orderByName": orderByName,
                "inheritState": inheritState,
                "metaId": metaId,
                "intentId": intentId,
                "pageNum": pageNum,
                "pageSize": pageSize,
                "carType": carType,
            }
        )
        return {
            "total": data["total"],
            "pageNum": pageNum,
            "pageSize": pageSize,
            "items": [summarize_function(item) for item in data["items"]],
        }

    async def list_dialogue_sessions_raw(self, dialogue_test_type: DialogueTestType) -> list[dict[str, Any]]:
        data = await self.client.get("/tts/dialogue/categories", {"dialogueTestType": dialogue_test_type})
        return [ensure_record(item, "dialogue session") for item in ensure_list(data)]

    async def get_dialogue_records_raw(
        self,
        request_id: str,
        dialogue_env: str | None = None,
    ) -> list[dict[str, Any]]:
        data = await self.client.get(
            f"/tts/dialogue/records/{quote_path_value(request_id)}",
            {"dialogueEnv": dialogue_env},
        )
        return [ensure_record(item, "dialogue record") for item in ensure_list(data)]

    async def get_function_detail_raw(self, function_id: int) -> dict[str, Any]:
        return ensure_record(await self.client.get("/fi/function/detail", {"id": function_id}), "function detail")

    async def _list_functions_page(self, params: dict[str, Any]) -> dict[str, Any]:
        data = ensure_record(await self.client.get("/fi/function/list", params), "function page")
        items = [ensure_record(item, "function item") for item in ensure_list(data.get("data"))]
        return {
            "total": data.get("total"),
            "items": items,
        }

    async def execute_chat_dialogue(self, input_payload: dict[str, Any]) -> dict[str, Any]:
        dialogue_test_type = input_payload["dialogueTestType"]
        before_sessions = (
            []
            if input_payload.get("sessionId")
            else await self.list_dialogue_sessions_raw(dialogue_test_type)
        )
        before_keys = {build_dialogue_session_key(item) for item in before_sessions}
        payload = await self.build_dialogue_request_payload(input_payload)
        response = await self.client.post_json("/tts/dialogue/chat", payload)
        response_items = ensure_list(response)

        session: dict[str, Any] | None = None
        session_id = as_trimmed_string(payload.get("session_id"))

        after_sessions = await self.list_dialogue_sessions_raw(dialogue_test_type)
        if session_id:
            session = find_dialogue_session(after_sessions, session_id, as_trimmed_string(payload.get("dialogue_env")))
        else:
            session = pick_created_dialogue_session(
                after_sessions,
                before_keys,
                input_payload["query"],
                as_trimmed_string(payload.get("dialogue_env")),
            )
            session_id = as_trimmed_string(session.get("sessionId")) if session else None

        return {
            "ok": True,
            "dialogueTestType": payload.get("dialogue_test_type"),
            "dialogueEnv": as_trimmed_string(payload.get("dialogue_env")),
            "sessionId": session_id,
            "requestId": extract_request_id_from_dialogue_message(response_items),
            "query": input_payload["query"],
            "session": summarize_dialogue_session(session) if session else None,
            "response": response_items,
            "requestPayload": sanitize_dialogue_payload(payload),
        }

    async def resolve_dialogue_session_context(
        self,
        session_id: str,
        dialogue_test_type: DialogueTestType | None,
        dialogue_env: str | None,
    ) -> dict[str, Any]:
        requested_types: list[DialogueTestType] = [dialogue_test_type] if dialogue_test_type else ["online", "offline"]
        for session_type in requested_types:
            sessions = await self.list_dialogue_sessions_raw(session_type)
            session = find_dialogue_session(sessions, session_id, dialogue_env)
            if session:
                return {
                    "dialogueTestType": session_type,
                    "dialogueEnv": as_trimmed_string(session.get("dialogueEnv")) or dialogue_env or "",
                    "session": session,
                }
        raise AlchemyApiError(f"Unable to find dialogue session {session_id}.")

    async def resolve_car_type_id_by_vehicle_model(self, vehicle_model: str) -> int:
        items = ensure_list(await self.client.get("/fi/carType/getAll"))
        for item in items:
            record = ensure_record(item, "car type")
            if record.get("carTypeAlias") == vehicle_model or record.get("carType") == vehicle_model:
                resolved_id = record.get("id")
                if isinstance(resolved_id, int):
                    return resolved_id
        raise AlchemyApiError(f"Unable to resolve carTypeId for vehicleModel {vehicle_model}.")

    async def build_dialogue_request_payload(self, input_payload: dict[str, Any]) -> dict[str, Any]:
        dialogue_test_type = input_payload["dialogueTestType"]
        resolved_dialogue_env = resolve_dialogue_env(dialogue_test_type, input_payload.get("dialogueEnv"))
        resolved_vehicle_model = input_payload.get("vehicleModel") or DEFAULT_DIALOGUE_BASE["vehicle_model"]
        resolved_car_type_id = input_payload.get("carTypeId") or await self.resolve_car_type_id_by_vehicle_model(
            resolved_vehicle_model
        )
        env_config = DIALOGUE_ENV_CONFIG.get(resolved_dialogue_env) if resolved_dialogue_env else None
        vehicle_config = dict(
            DEFAULT_ONLINE_VEHICLE_CONFIG if dialogue_test_type == "online" else DEFAULT_OFFLINE_VEHICLE_CONFIG
        )

        maybe_assign(vehicle_config, "is_right_rudder", input_payload.get("isRightRudder"))
        maybe_assign(vehicle_config, "mic_number", input_payload.get("micNumber"))
        maybe_assign(vehicle_config, "voice_id", input_payload.get("voiceId"))
        maybe_assign(vehicle_config, "asr_nonstop", input_payload.get("asrNonstop"))
        maybe_assign(vehicle_config, "continuous_dialog", input_payload.get("continuousDialog"))
        maybe_assign(vehicle_config, "navi_app", input_payload.get("naviApp"))
        if dialogue_test_type == "online":
            maybe_assign(vehicle_config, "chat_llm_model", input_payload.get("chatLlmModel"))

        payload: dict[str, Any] = {
            "query": input_payload["query"],
            "source_id": input_payload["sourceId"],
            "session_id": input_payload.get("sessionId"),
            "car_type_id": resolved_car_type_id,
            "dialogue_test_type": dialogue_test_type,
            "dialogue_env": resolved_dialogue_env,
            "host": input_payload.get("host") or (env_config or DIALOGUE_ENV_CONFIG["stg"])["host"],
            "app_id": input_payload.get("appId") or (env_config or DIALOGUE_ENV_CONFIG["stg"])["appId"],
            "vehicle_id": input_payload.get("vehicleId") or DEFAULT_DIALOGUE_BASE["vehicle_id"],
            "vehicle_model": resolved_vehicle_model,
            "sdk_version": input_payload.get("sdkVersion") or DEFAULT_DIALOGUE_BASE["sdk_version"],
            "language": input_payload.get("language") or DEFAULT_DIALOGUE_BASE["language"],
            "region": input_payload.get("region") or DEFAULT_DIALOGUE_BASE["region"],
            "location": {
                **DEFAULT_DIALOGUE_LOCATION,
                "address": input_payload.get("address", DEFAULT_DIALOGUE_LOCATION["address"]),
                "city_name": input_payload.get("cityName") or DEFAULT_DIALOGUE_LOCATION["city_name"],
                "latitude": input_payload.get("latitude", DEFAULT_DIALOGUE_LOCATION["latitude"]),
                "longitude": input_payload.get("longitude", DEFAULT_DIALOGUE_LOCATION["longitude"]),
                "name": input_payload.get("locationName", DEFAULT_DIALOGUE_LOCATION["name"]),
            },
            "vehicle_config": vehicle_config,
            "context_type": input_payload.get("contextType") or DEFAULT_DIALOGUE_BASE["context_type"],
            "source": DEFAULT_DIALOGUE_BASE["source"],
            "wakeup_free": input_payload.get("wakeupFree") or DEFAULT_DIALOGUE_BASE["wakeup_free"],
            "awaken": input_payload.get("awaken") or DEFAULT_DIALOGUE_BASE["awaken"],
            "awaken_zone": input_payload.get("awakenZone") or DEFAULT_DIALOGUE_BASE["awaken_zone"],
            "voice_zone": input_payload.get("voiceZone") or DEFAULT_DIALOGUE_BASE["voice_zone"],
            "ui_nodes": input_payload.get("uiNodes") or DEFAULT_DIALOGUE_BASE["ui_nodes"],
            "last_req_id": input_payload.get("lastReqId") or DEFAULT_DIALOGUE_BASE["last_req_id"],
            "last_query": input_payload.get("lastQuery") or DEFAULT_DIALOGUE_BASE["last_query"],
            "last_tts": input_payload.get("lastTts") or DEFAULT_DIALOGUE_BASE["last_tts"],
            "last_query_type": input_payload.get("lastQueryType") or DEFAULT_DIALOGUE_BASE["last_query_type"],
            "interrupted_req_id": input_payload.get("interruptedReqId")
            or DEFAULT_DIALOGUE_BASE["interrupted_req_id"],
            "dialog_timestamp": input_payload.get("dialogTimestamp") or current_time_millis(),
            "tts_stop_timestamp": input_payload.get("ttsStopTimestamp") or DEFAULT_DIALOGUE_BASE["tts_stop_timestamp"],
        }

        if input_payload.get("continueSession", True) is not False and input_payload.get("sessionId"):
            await self.hydrate_dialogue_continuation(
                payload,
                input_payload["sessionId"],
                resolved_dialogue_env or None,
            )

        return payload

    async def hydrate_dialogue_continuation(
        self,
        payload: dict[str, Any],
        session_id: str,
        dialogue_env: str | None,
    ) -> None:
        records = await self.get_dialogue_records_raw(session_id, dialogue_env)
        latest = records[-1] if records else None
        if latest is None:
            return

        if not as_trimmed_string(payload.get("last_req_id")):
            payload["last_req_id"] = extract_request_id_from_dialogue_message(
                parse_dialogue_json_field(latest.get("message"))
            )
        if not as_trimmed_string(payload.get("last_query")):
            payload["last_query"] = as_trimmed_string(latest.get("query")) or ""
        if not payload.get("dialog_timestamp") or int(payload["dialog_timestamp"]) <= 0:
            payload["dialog_timestamp"] = current_time_millis()


def stringify_query_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def build_query_params(params: dict[str, Any] | None) -> dict[str, str]:
    if not params:
        return {}
    normalized: dict[str, str] = {}
    for key, value in params.items():
        if value is None or value == "":
            continue
        normalized[key] = stringify_query_value(value)
    return normalized


def normalize_function_state(value: FunctionStateInput) -> str | None:
    if isinstance(value, list):
        return ",".join(value)
    return value


def try_parse_json_string(value: str) -> Any | None:
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


def resolve_output_dir(output_dir: str | None) -> Path:
    if output_dir:
        path = Path(output_dir).expanduser()
        return (path if path.is_absolute() else Path.cwd() / path).resolve()
    return (Path.cwd() / "exports").resolve()


def compact_dict(data: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in data.items() if value is not None}


def maybe_assign(target: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        target[key] = value


def current_time_millis() -> int:
    import time

    return int(time.time() * 1000)


def quote_path_value(value: str) -> str:
    from urllib.parse import quote

    return quote(value, safe="")


def resolve_dialogue_env(dialogue_test_type: DialogueTestType, dialogue_env: str | None) -> str:
    if dialogue_test_type == "offline":
        return dialogue_env.strip() if isinstance(dialogue_env, str) else ""
    if dialogue_env and dialogue_env in DIALOGUE_ENV_CONFIG:
        return dialogue_env
    return "stg"


def merge_dialogue_input_with_session_defaults(
    input_payload: dict[str, Any],
    session: dict[str, Any],
    context: dict[str, Any],
) -> dict[str, Any]:
    defaults = extract_dialogue_session_defaults(session)
    return {
        **defaults,
        **input_payload,
        "sessionId": input_payload["sessionId"],
        "query": input_payload["query"],
        "dialogueTestType": context["dialogueTestType"],
        "dialogueEnv": input_payload.get("dialogueEnv") or context.get("dialogueEnv"),
        "continueSession": True,
    }


def extract_dialogue_session_defaults(session: dict[str, Any]) -> dict[str, Any]:
    params = parse_dialogue_json_field(session.get("params"))
    if not is_record(params):
        return compact_dict(
            {
                "vehicleModel": as_trimmed_string(session.get("carTypeAlias"))
                or as_trimmed_string(session.get("carType")),
                "carTypeId": as_number(session.get("carTypeId")),
            }
        )

    location = params.get("location") if is_record(params.get("location")) else {}
    vehicle_config = params.get("vehicle_config") if is_record(params.get("vehicle_config")) else {}
    return compact_dict(
        {
            "sourceId": as_number(params.get("source_id")),
            "carTypeId": as_number(params.get("car_type_id")) or as_number(session.get("carTypeId")),
            "vehicleId": as_trimmed_string(params.get("vehicle_id")),
            "vehicleModel": as_trimmed_string(params.get("vehicle_model"))
            or as_trimmed_string(session.get("carTypeAlias"))
            or as_trimmed_string(session.get("carType")),
            "host": as_trimmed_string(params.get("host")),
            "appId": as_string_or_number(params.get("app_id")),
            "sdkVersion": as_trimmed_string(params.get("sdk_version")),
            "language": as_trimmed_string(params.get("language")),
            "region": as_trimmed_string(params.get("region")),
            "address": location.get("address") if isinstance(location.get("address"), str) else None,
            "cityName": as_trimmed_string(location.get("city_name")),
            "latitude": as_number(location.get("latitude")),
            "longitude": as_number(location.get("longitude")),
            "locationName": location.get("name") if isinstance(location.get("name"), str) else None,
            "isRightRudder": as_boolean(vehicle_config.get("is_right_rudder")),
            "micNumber": as_number(vehicle_config.get("mic_number")),
            "voiceId": as_number(vehicle_config.get("voice_id")),
            "asrNonstop": as_boolean(vehicle_config.get("asr_nonstop")),
            "continuousDialog": as_boolean(vehicle_config.get("continuous_dialog")),
            "naviApp": as_trimmed_string(vehicle_config.get("navi_app")),
            "chatLlmModel": as_trimmed_string(vehicle_config.get("chat_llm_model")),
            "contextType": as_trimmed_string(params.get("context_type")),
            "wakeupFree": as_trimmed_string(params.get("wakeup_free")),
            "awaken": as_trimmed_string(params.get("awaken")),
            "awakenZone": as_trimmed_string(params.get("awaken_zone")),
            "voiceZone": as_trimmed_string(params.get("voice_zone")),
            "uiNodes": params.get("ui_nodes") if isinstance(params.get("ui_nodes"), list) else None,
            "ttsStopTimestamp": as_trimmed_string(params.get("tts_stop_timestamp")),
        }
    )


def build_dialogue_session_key(item: dict[str, Any]) -> str:
    return f"{as_trimmed_string(item.get('sessionId')) or ''}::{as_trimmed_string(item.get('dialogueEnv')) or ''}"


def find_dialogue_session(
    items: list[dict[str, Any]],
    session_id: str,
    dialogue_env: str | None,
) -> dict[str, Any] | None:
    for item in items:
        if as_trimmed_string(item.get("sessionId")) != session_id:
            continue
        if not dialogue_env or as_trimmed_string(item.get("dialogueEnv")) == dialogue_env:
            return item
    return None


def pick_created_dialogue_session(
    items: list[dict[str, Any]],
    before_keys: set[str],
    query: str,
    dialogue_env: str | None,
) -> dict[str, Any] | None:
    for item in items:
        if build_dialogue_session_key(item) in before_keys:
            continue
        if as_trimmed_string(item.get("query")) != query:
            continue
        if (as_trimmed_string(item.get("dialogueEnv")) or "") == (dialogue_env or ""):
            return item

    for item in items:
        if as_trimmed_string(item.get("query")) != query:
            continue
        if (as_trimmed_string(item.get("dialogueEnv")) or "") == (dialogue_env or ""):
            return item
    return None


def parse_dialogue_json_field(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    parsed = safe_json_parse(value)
    return parsed if parsed is not None else value


def extract_request_id_from_dialogue_message(message: Any) -> str | None:
    if not isinstance(message, list) or not message:
        return None
    first = message[0]
    if not isinstance(first, dict):
        return None
    return as_trimmed_string(first.get("request_id"))


def sanitize_dialogue_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        **payload,
        "session_id": as_trimmed_string(payload.get("session_id")),
        "dialogue_env": as_trimmed_string(payload.get("dialogue_env")),
        "last_req_id": as_trimmed_string(payload.get("last_req_id")),
        "last_query": as_trimmed_string(payload.get("last_query")),
    }


def flatten_categories(categories: list[Any], depth: int = 0) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for category in categories:
        if not isinstance(category, dict):
            continue
        result.append(
            {
                "id": category.get("id"),
                "name": category.get("name"),
                "completeName": category.get("completeName"),
                "parentId": category.get("parentId"),
                "includeFunctionCount": category.get("includeFunctionCount", category.get("functionCount", 0)),
                "depth": depth,
                "ownerEmail": category.get("ownerEmail"),
            }
        )
        result.extend(flatten_categories(ensure_list(category.get("children")), depth + 1))
    return result


def summarize_function(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": item.get("id"),
        "name": item.get("name"),
        "projectId": item.get("projectId"),
        "projectName": item.get("projectName"),
        "functionTypeId": item.get("functionTypeId"),
        "functionTypeName": item.get("functionTypeName"),
        "functionState": item.get("functionState"),
        "reviewState": item.get("reviewState"),
        "inheritState": item.get("inheritState"),
        "offlinePriority": item.get("offlinePriority"),
        "metaId": item.get("functionCommonDataId"),
        "fromFunctionId": item.get("fromFunctionId"),
        "createTime": item.get("createTime"),
        "updateTime": item.get("updateTime"),
    }


def summarize_project(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": item.get("id"),
        "projectName": item.get("projectName"),
        "principal": item.get("principal"),
        "description": item.get("description"),
        "vehicleModel": item.get("vehicleModel"),
        "includeFunctionCount": item.get("includeFunctionCount"),
        "inheritedModifiedCount": item.get("inheritedModifiedCount"),
        "platformNewCount": item.get("platformNewCount"),
        "draftStatusCount": item.get("draftStatusCount"),
        "createTime": item.get("createTime"),
        "updateTime": item.get("updateTime"),
    }


def summarize_intent(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": item.get("id"),
        "intent": item.get("intent"),
        "intentRemark": item.get("intentRemark"),
        "domain": item.get("domain"),
        "slotsId": item.get("slotsId"),
        "exampleCommandId": item.get("exampleCommandId"),
        "createTime": item.get("createTime"),
        "updateTime": item.get("updateTime"),
    }


def summarize_slot_property(item: dict[str, Any]) -> dict[str, Any]:
    dict_type = item.get("dictType")
    return {
        "id": item.get("id"),
        "dictType": dict_type,
        "dictTypeLabel": "标注规范Slot" if dict_type == 1 else "自定义Slot" if dict_type == 2 else None,
        "slotName": item.get("slotName"),
        "slotDictName": item.get("slotDictName"),
        "slotDictProp": item.get("slotDictProp"),
        "slotDictTerm": item.get("slotDictTerm"),
        "language": item.get("language"),
        "remark": item.get("remark"),
        "updateUser": item.get("updateUser"),
        "createUser": item.get("createUser"),
        "updateTime": item.get("updateTime", item.get("time")),
    }


def summarize_dialogue_session(item: dict[str, Any] | None) -> dict[str, Any] | None:
    if item is None:
        return None
    return {
        "id": item.get("id"),
        "sessionId": item.get("sessionId"),
        "query": item.get("query"),
        "carTypeId": item.get("carTypeId"),
        "carType": item.get("carType"),
        "carTypeAlias": item.get("carTypeAlias"),
        "appId": item.get("appId"),
        "dialogueEnv": item.get("dialogueEnv"),
        "createUser": item.get("createUser"),
        "updateUser": item.get("updateUser"),
        "createTime": item.get("createTime"),
        "updateTime": item.get("updateTime"),
        "params": parse_dialogue_json_field(item.get("params")),
    }


def summarize_dialogue_record(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": item.get("id"),
        "sessionId": item.get("sessionId"),
        "query": item.get("query"),
        "carTypeId": item.get("carTypeId"),
        "carType": item.get("carType"),
        "carTypeAlias": item.get("carTypeAlias"),
        "appId": item.get("appId"),
        "dialogueEnv": item.get("dialogueEnv"),
        "createUser": item.get("createUser"),
        "updateUser": item.get("updateUser"),
        "createTime": item.get("createTime"),
        "updateTime": item.get("updateTime"),
        "params": parse_dialogue_json_field(item.get("params")),
        "message": parse_dialogue_json_field(item.get("message")),
    }


def as_trimmed_string(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    trimmed = value.strip()
    return trimmed or None


def as_number(value: Any) -> int | float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return value
    if isinstance(value, str) and value.strip():
        try:
            parsed = float(value) if "." in value else int(value)
        except ValueError:
            return None
        return parsed
    return None


def as_boolean(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if value == "true":
        return True
    if value == "false":
        return False
    return None


def as_string_or_number(value: Any) -> str | int | None:
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    return as_trimmed_string(value)


def is_record(value: Any) -> bool:
    return isinstance(value, dict)


def parse_filename_from_content_disposition(content_disposition: str | None) -> str | None:
    if not content_disposition:
        return None
    utf8_match = re.search(r"filename\*=UTF-8''([^;]+)", content_disposition, re.IGNORECASE)
    if utf8_match and utf8_match.group(1):
        return safe_decode_filename(utf8_match.group(1))
    plain_match = re.search(r'filename="?([^"]+)"?', content_disposition, re.IGNORECASE)
    if plain_match and plain_match.group(1):
        return safe_decode_filename(plain_match.group(1))
    return None


def safe_decode_filename(value: str) -> str:
    from urllib.parse import unquote

    decoded = value
    for _ in range(2):
        try:
            next_value = unquote(decoded)
        except Exception:
            break
        if next_value == decoded:
            break
        decoded = next_value
    return decoded


def build_protocol_export_name(function_type_id: int | None, project_id: int | None) -> str:
    suffix_parts = []
    if function_type_id:
        suffix_parts.append(f"functionType-{function_type_id}")
    if project_id:
        suffix_parts.append(f"project-{project_id}")
    suffix = "-".join(suffix_parts) if suffix_parts else "interface-protocol"
    return f"{suffix}-export.xlsx"


def safe_json_parse(value: str) -> Any | None:
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


def _load_persisted_setting(key: str) -> str | None:
    for config_path in [get_config_file(), *iter_legacy_config_files()]:
        if not config_path.exists():
            continue
        for raw_line in config_path.read_text(encoding="utf-8-sig").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            field, value = line.split("=", 1)
            if field.strip() == key:
                return value.strip()
    return None


def inject_protocol_fields(data: dict[str, Any]) -> dict[str, Any]:
    return {
        **data,
        "protocolRequest": data.get("protocolRequest"),
        "protocolResponse": data.get("protocolResponse"),
        "nluMapping": data.get("nluMapping"),
        "nerMapping": data.get("nerMapping"),
    }


def ensure_record(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise AlchemyApiError(f"Expected {name} to be an object.")
    return value


def ensure_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []
