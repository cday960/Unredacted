

def swap_spaces_for_plus(params: str) -> str:
    params.replace(' ', '+')
    if params[len(params) - 1] == '+':
        params = params[:-1]
    return params