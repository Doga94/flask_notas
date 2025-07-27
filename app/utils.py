def validate_required_fields(data: dict, required_fields: list) -> list:
    missing = [field for field in required_fields if not data.get(field, "").strip()]
    return missing