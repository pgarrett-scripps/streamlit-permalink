from datetime import date, time

_EMPTY = "_STREAMLIT_PERMALINK_EMPTY"

def to_url_value(result):
    if isinstance(result, str):
        return result
    if isinstance(result, (bool, float, int)):
        return str(result)
    if isinstance(result, (list, tuple)):
        if len(result) == 0:
            return [_EMPTY]
        return list(map(to_url_value, result))
    if isinstance(result, date):
        return result.isoformat()
    if isinstance(result, time):
        return result.strftime('%H:%M')
    raise TypeError(f'unsupported type: {type(result)}') 