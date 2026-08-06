from agent.schemas import ToolCall, ToolResult


class ToolExecutor:

    def __init__(self, registry):
        self.registry = registry

    def execute(
        self,
        tool_call: ToolCall
    ) -> ToolResult:

        tool_info = self.registry.get(tool_call.name)

        if tool_info is None:

            return ToolResult(
                tool_call_id=tool_call.id,
                tool_name=tool_call.name,
                output=f"Unknown tool '{tool_call.name}'."
            )

        tool = tool_info["tool"]
        tool_fn = tool_info["function"]

        try:
            args = self._validate_arguments(
                tool_call.arguments,
                tool
            )

            result = tool_fn(
                **args
            )

            return ToolResult(
                tool_call_id=tool_call.id,
                tool_name=tool_call.name,
                output=result
            )

        except Exception as e:

            return ToolResult(
                tool_call_id=tool_call.id,
                tool_name=tool_call.name,
                output=f"Tool execution failed: {e}"
            )

    def _validate_arguments(self, arguments, tool):
        if not isinstance(arguments, dict):
            raise ValueError("Tool arguments must be a JSON object.")
        if "_parse_error" in arguments:
            raise ValueError(arguments["_parse_error"])

        unknown_args = sorted(set(arguments) - set(tool.parameters))
        if unknown_args:
            raise ValueError(
                f"Unexpected argument(s): {', '.join(unknown_args)}."
            )

        missing_args = [
            name for name in tool.required
            if name not in arguments or arguments[name] in [None, ""]
        ]
        if missing_args:
            raise ValueError(
                f"Missing required argument(s): {', '.join(missing_args)}."
            )

        validated = {}
        for name, value in arguments.items():
            param = tool.parameters[name]
            coerced = self._coerce_value(name, value, param.type)

            if param.enum and coerced not in param.enum:
                if isinstance(coerced, str) and coerced.lower() in param.enum:
                    coerced = coerced.lower()
                else:
                    allowed = ", ".join(str(item) for item in param.enum)
                    raise ValueError(
                        f"Invalid value for '{name}'. Expected one of: {allowed}."
                    )

            validated[name] = coerced

        return validated

    def _coerce_value(self, name, value, expected_type):
        if expected_type == "number":
            if isinstance(value, bool):
                raise ValueError(f"Argument '{name}' must be a number.")
            try:
                return float(value)
            except (TypeError, ValueError):
                raise ValueError(f"Argument '{name}' must be a number.")

        if expected_type == "integer":
            if isinstance(value, bool):
                raise ValueError(f"Argument '{name}' must be an integer.")
            try:
                number = int(value)
            except (TypeError, ValueError):
                raise ValueError(f"Argument '{name}' must be an integer.")
            try:
                if float(value) != number:
                    raise ValueError
            except (TypeError, ValueError):
                raise ValueError(f"Argument '{name}' must be an integer.")
            return number

        if expected_type == "boolean":
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                normalized = value.strip().lower()
                if normalized in ["true", "yes", "1"]:
                    return True
                if normalized in ["false", "no", "0"]:
                    return False
            raise ValueError(f"Argument '{name}' must be a boolean.")

        if expected_type == "string":
            if value is None:
                raise ValueError(f"Argument '{name}' must be a string.")
            return str(value).strip()

        return value
