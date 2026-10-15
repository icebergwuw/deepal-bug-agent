import json

from analyze_bug.core.paths import get_resource_file
from analyze_bug.core.responses import ErrorType, make_error_response, make_success_response


def _load_rules() -> dict:
    rules_path = get_resource_file("rules.json")
    return json.loads(rules_path.read_text(encoding="utf-8"))


def get_analysis_rules(logger) -> str:
    logger.info("Loading full analysis rules")
    try:
        return make_success_response(_load_rules())
    except FileNotFoundError:
        return make_error_response(
            ErrorType.NOT_FOUND,
            "规则文件不存在",
            "请重新安装 analyze-bug 运行时。",
        )
    except json.JSONDecodeError:
        return make_error_response(
            ErrorType.UNKNOWN,
            "规则文件格式错误",
            "请检查 rules.json 内容。",
        )
    except Exception as exc:
        return make_error_response(
            ErrorType.UNKNOWN,
            f"加载规则失败: {exc}",
            "请检查规则文件。",
        )


def get_module_rules(module: str, logger) -> str:
    valid_modules = ["acoustics", "asr", "nlu", "cloud", "vehicle", "tts"]
    module_key = module.lower()
    if module_key not in valid_modules:
        return make_error_response(
            ErrorType.NOT_FOUND,
            f"未知模块: {module}",
            f"有效模块: {', '.join(valid_modules)}",
        )

    try:
        rules = _load_rules()
        module_rules = rules.get(module_key)
        if not module_rules:
            return make_error_response(
                ErrorType.NOT_FOUND,
                f"模块 {module} 的规则未定义",
                "请检查 rules.json。",
            )
        return make_success_response({"module": module_key, "rules": module_rules})
    except Exception as exc:
        logger.error("Failed to load module rules: %s", exc)
        return make_error_response(
            ErrorType.UNKNOWN,
            f"加载模块规则失败: {exc}",
            "请检查规则文件。",
        )


def get_fault_priority(logger) -> str:
    try:
        rules = _load_rules()
        return make_success_response(
            {
                "priority": rules.get("fault_priority", []),
                "description": "按此顺序依次检查，一旦发现问题立即停止并归责",
            }
        )
    except Exception as exc:
        logger.error("Failed to load fault priority: %s", exc)
        return make_error_response(
            ErrorType.UNKNOWN,
            f"加载优先级失败: {exc}",
            "请检查规则文件。",
        )


def get_rules_version(logger) -> str:
    try:
        rules = _load_rules()
        return make_success_response(
            {
                "version": rules.get("version", "unknown"),
                "last_updated": rules.get("last_updated", "unknown"),
            }
        )
    except Exception as exc:
        logger.error("Failed to load rules version: %s", exc)
        return make_error_response(
            ErrorType.UNKNOWN,
            f"加载版本信息失败: {exc}",
            "请检查规则文件。",
        )
