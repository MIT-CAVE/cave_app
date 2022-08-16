import json


def encode_like_js(obj):
    """
    Code to encode an object like js
    """
    if isinstance(obj, dict):
        return {key: encode_like_js(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [encode_like_js(i) for i in obj]
    # Note check for bool before int as bools are also ints in python
    elif isinstance(obj, bool):
        return obj
    elif isinstance(obj, (int, float)):
        if obj > 9007199254740992:
            raise Exception("Only numbers under 2^53 are supported")
        elif int(obj) == obj:
            return int(obj)
    return obj


def json_like_js(obj):
    return json.dumps(encode_like_js(obj), separators=(",", ":"))
