import json


def _parse_js(text):
    array_text = text.split("=", 1)[1].strip().rstrip(";").strip()
    return json.loads(array_text)
