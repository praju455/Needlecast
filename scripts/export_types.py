"""Generate schema and operation types from the checked M00 OpenAPI subset."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def literal(value: object) -> str:
    return json.dumps(value, ensure_ascii=False)


def typescript(schema: dict) -> str:
    if not schema:
        return "unknown"
    if "$ref" in schema:
        return f'components["schemas"][{literal(schema["$ref"].rsplit("/", 1)[-1])}]'
    if "const" in schema:
        return literal(schema["const"])
    if "enum" in schema:
        return " | ".join(map(literal, schema["enum"]))
    if "anyOf" in schema:
        return " | ".join(map(typescript, schema["anyOf"]))
    match schema.get("type"):
        case "object":
            required = set(schema.get("required", []))
            if "properties" in schema:
                fields = (
                    f"{literal(k)}{'' if k in required else '?'}: {typescript(v)};"
                    for k, v in schema["properties"].items()
                )
                return "{ " + " ".join(fields) + " }"
            if "additionalProperties" in schema and isinstance(
                schema["additionalProperties"], dict
            ):
                return "Record<string, " + typescript(schema["additionalProperties"]) + ">"
            return "Record<string, unknown>"
        case "array":
            return f"Array<{typescript(schema['items'])}>"
        case "number" | "integer":
            return "number"
        case "boolean" | "string" | "null":
            return schema["type"]
        case _:
            raise ValueError(f"Unsupported OpenAPI schema: {schema}")


def export(source: Path, destination: Path) -> None:
    document = json.loads(source.read_text())
    lines = [
        "// Generated from backend/openapi.json by scripts/export_types.py.",
        "export interface components {",
        "  schemas: {",
    ]
    for key, value in document["components"]["schemas"].items():
        lines.append(f"    {literal(key)}: {typescript(value)};")
    lines.extend(["  };", "}", "", "export interface paths {"])
    for path, item in document["paths"].items():
        lines.append(f"  {literal(path)}: {{")
        for method, operation in item.items():
            lines.append(f"    {method}: {{")
            body = operation.get("requestBody", {}).get("content", {}).get("application/json")
            if body is not None:
                lines.append(
                    f'      requestBody: {{ content: {{ "application/json": {typescript(body["schema"])} }} }};'
                )
            lines.append("      responses: {")
            for code, response in operation["responses"].items():
                content = response.get("content", {}).get("application/json")
                if content is not None:
                    lines.append(
                        f'        {code}: {{ content: {{ "application/json": {typescript(content["schema"])} }} }};'
                    )
            lines.extend(["      };", "    };"])
        lines.append("  };")
    lines.extend(["}", ""])
    destination.write_text("\n".join(lines))


if __name__ == "__main__":
    export(ROOT / "backend/openapi.json", ROOT / "frontend/src/lib/types/api.d.ts")
