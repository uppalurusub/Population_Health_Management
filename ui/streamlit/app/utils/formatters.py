import json

def humanize_key(key):
    return str(key).replace("_", " ").strip().title()

def format_metric_value(value):
    if value is None:
        return "N/A"
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, float):
        return f"{value:,.2f}"
    if isinstance(value, int):
        return f"{value:,}"
    return str(value)

def pretty_json(data):
    return json.dumps(data, indent=2, default=str)
