import re

def valid_date_param(date: str) -> bool:
    date_pattern = "^\d{4}-\d{2}-\d{2}$"
    if re.match(date_pattern, date):
        return True
    else:
        return False

def swap_spaces_for_plus(params: str) -> str:
    params.replace(' ', '+')
    if params[len(params) - 1] == '+':
        params = params[:-1]
    return params