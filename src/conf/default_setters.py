"""Server level default setters"""
def flower(params: dict, defaults: dict):
    params.setdefault('user', defaults.get('user'))
    params.setdefault('password', defaults.get('password'))
    params.setdefault('port', defaults.get('port'))

def docker(params: dict, defaults: dict):
    params.setdefault('port', defaults.get('port', 22)) # Standard SSH port
