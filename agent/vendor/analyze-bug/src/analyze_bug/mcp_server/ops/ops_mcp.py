import json
from contextlib import asynccontextmanager
from typing import Literal

from mcp.server.fastmcp import Context, FastMCP

from analyze_bug.core.logging_utils import setup_logger
from analyze_bug.mcp_server.ops.ops_service import (
    AlchemyClient,
    AlchemyService,
    AppRuntime,
    FunctionStateInput,
    InheritState,
    NonEmptyStr,
    PageSize,
    PositiveInt,
    Settings,
    SortOrder,
    logger as service_logger,
)


logger = setup_logger("ops-mcp", "ops_mcp.log")
service_logger.handlers = logger.handlers
service_logger.setLevel(logger.level)
service_logger.propagate = False


def text_result(data) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


@asynccontextmanager
async def app_lifespan(_: FastMCP):
    settings = Settings.from_env()
    if not settings.cookie:
        logger.warning("ALCHEMY_COOKIE is not configured; ops tools will return credential errors.")
        yield AppRuntime(service=None)
        return
    async with AlchemyClient(settings.base_url, settings.cookie) as client:
        yield AppRuntime(service=AlchemyService(client))


mcp = FastMCP("alchemy-ops-mcp", lifespan=app_lifespan)


def get_service(ctx: Context) -> AlchemyService:
    runtime = ctx.request_context.lifespan_context
    if not isinstance(runtime, AppRuntime):
        raise RuntimeError("Alchemy service is not initialized.")
    if runtime.service is None:
        raise RuntimeError("Missing ALCHEMY_COOKIE. Run `analyze-bug-admin configure-ops` first.")
    return runtime.service


@mcp.tool()
async def list_intents(*, ctx: Context) -> str:
    """获取标注规范 intent 列表，对应后端 /specification/intent_list。"""
    return text_result(await get_service(ctx).list_intents())


@mcp.tool()
async def list_slots(*, ctx: Context) -> str:
    """获取标注规范 slot 列表，对应后端 /specification/slot_list。"""
    return text_result(await get_service(ctx).list_slots())


@mcp.tool()
async def list_slot_properties(
    dictType: Literal[1, 2] | None = None,
    dictTerm: NonEmptyStr | None = None,
    language: NonEmptyStr | None = None,
    dictName: NonEmptyStr | None = None,
    slotDictProp: NonEmptyStr | None = None,
    orderByUpdateTime: SortOrder | None = None,
    orderBySlotDictName: SortOrder | None = None,
    orderBySlotDictProp: SortOrder | None = None,
    pageNum: PositiveInt = 1,
    pageSize: PageSize = 20,
    *,
    ctx: Context,
) -> str:
    """查看 slot property 列表，支持页面上的常用筛选与排序。"""
    return text_result(
        await get_service(ctx).list_slot_properties(
            dictType=dictType,
            dictTerm=dictTerm,
            language=language,
            dictName=dictName,
            slotDictProp=slotDictProp,
            orderByUpdateTime=orderByUpdateTime,
            orderBySlotDictName=orderBySlotDictName,
            orderBySlotDictProp=orderBySlotDictProp,
            pageNum=pageNum,
            pageSize=pageSize,
        )
    )


@mcp.tool()
async def list_standard_functions(
    id: PositiveInt | None = None,
    name: NonEmptyStr | None = None,
    functionTypeId: PositiveInt | None = None,
    reviewState: int | None = None,
    functionState: FunctionStateInput = None,
    offlinePriority: bool | None = None,
    orderByCreateTime: SortOrder | None = None,
    orderByName: SortOrder | None = None,
    metaId: PositiveInt | None = None,
    intentId: NonEmptyStr | None = None,
    pageNum: PositiveInt = 1,
    pageSize: PageSize = 20,
    carType: NonEmptyStr | None = None,
    *,
    ctx: Context,
) -> str:
    """查看标准功能列表。等同于不传 projectId 的功能查询，用来避免把标准功能和项目功能混淆。"""
    return text_result(
        await get_service(ctx).list_standard_functions(
            id=id,
            name=name,
            functionTypeId=functionTypeId,
            reviewState=reviewState,
            functionState=functionState,
            offlinePriority=offlinePriority,
            orderByCreateTime=orderByCreateTime,
            orderByName=orderByName,
            metaId=metaId,
            intentId=intentId,
            pageNum=pageNum,
            pageSize=pageSize,
            carType=carType,
        )
    )


@mcp.tool()
async def list_functions(
    id: PositiveInt | None = None,
    name: NonEmptyStr | None = None,
    functionTypeId: PositiveInt | None = None,
    reviewState: int | None = None,
    functionState: FunctionStateInput = None,
    offlinePriority: bool | None = None,
    orderByCreateTime: SortOrder | None = None,
    orderByName: SortOrder | None = None,
    projectId: PositiveInt | None = None,
    inheritState: InheritState | None = None,
    metaId: PositiveInt | None = None,
    intentId: NonEmptyStr | None = None,
    pageNum: PositiveInt = 1,
    pageSize: PageSize = 20,
    carType: NonEmptyStr | None = None,
    *,
    ctx: Context,
) -> str:
    """查看功能列表，可按页面筛选项过滤标准功能或项目功能。"""
    return text_result(
        await get_service(ctx).list_functions(
            id=id,
            name=name,
            functionTypeId=functionTypeId,
            reviewState=reviewState,
            functionState=functionState,
            offlinePriority=offlinePriority,
            orderByCreateTime=orderByCreateTime,
            orderByName=orderByName,
            projectId=projectId,
            inheritState=inheritState,
            metaId=metaId,
            intentId=intentId,
            pageNum=pageNum,
            pageSize=pageSize,
            carType=carType,
        )
    )


@mcp.tool()
async def get_standard_function_detail(id: PositiveInt, *, ctx: Context) -> str:
    """查看标准功能详情，包含协议配置。如果该功能属于某个项目，会直接报错，避免和项目功能混淆。"""
    return text_result(await get_service(ctx).get_standard_function_detail(id=id))


@mcp.tool()
async def get_function_detail(id: PositiveInt, *, ctx: Context) -> str:
    """查看单个功能详情，包含说明、协议配置、筛选信息和归属项目。"""
    return text_result(await get_service(ctx).get_function_detail(id=id))


@mcp.tool()
async def get_function_vehicle_config(functionId: PositiveInt, *, ctx: Context) -> str:
    """获取功能点车端配置，对应后端 /rd/getConfigJson。"""
    return text_result(await get_service(ctx).get_function_vehicle_config(functionId=functionId))


@mcp.tool()
async def list_projects(
    projectName: NonEmptyStr | None = None,
    orderByUpdateTime: SortOrder = "desc",
    pageNum: PositiveInt = 1,
    pageSize: PageSize = 20,
    *,
    ctx: Context,
) -> str:
    """查看项目列表。"""
    return text_result(
        await get_service(ctx).list_projects(
            projectName=projectName,
            orderByUpdateTime=orderByUpdateTime,
            pageNum=pageNum,
            pageSize=pageSize,
        )
    )


@mcp.tool()
async def get_project_detail(id: PositiveInt, *, ctx: Context) -> str:
    """查看单个项目详情。"""
    return text_result(await get_service(ctx).get_project_detail(id=id))


@mcp.tool()
async def list_project_functions(
    projectId: PositiveInt,
    id: PositiveInt | None = None,
    name: NonEmptyStr | None = None,
    functionTypeId: PositiveInt | None = None,
    reviewState: int | None = None,
    functionState: FunctionStateInput = None,
    offlinePriority: bool | None = None,
    orderByCreateTime: SortOrder | None = None,
    orderByName: SortOrder | None = None,
    inheritState: InheritState | None = None,
    metaId: PositiveInt | None = None,
    intentId: NonEmptyStr | None = None,
    pageNum: PositiveInt = 1,
    pageSize: PageSize = 20,
    carType: NonEmptyStr | None = None,
    *,
    ctx: Context,
) -> str:
    """查看某个项目下的功能列表，本质上等同于带 projectId 的功能查询。"""
    return text_result(
        await get_service(ctx).list_project_functions(
            projectId=projectId,
            id=id,
            name=name,
            functionTypeId=functionTypeId,
            reviewState=reviewState,
            functionState=functionState,
            offlinePriority=offlinePriority,
            orderByCreateTime=orderByCreateTime,
            orderByName=orderByName,
            inheritState=inheritState,
            metaId=metaId,
            intentId=intentId,
            pageNum=pageNum,
            pageSize=pageSize,
            carType=carType,
        )
    )


def main() -> None:
    logger.info("Starting alchemy-ops-mcp with stdio transport")
    mcp.run()
