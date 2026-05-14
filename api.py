import socket
import toons

try:
    from .constant import IP, PORT
except (ImportError, ModuleNotFoundError):
    from constant import IP, PORT

def _blocker_conect(data: dict):
    s = socket.socket()
    s.connect((IP, PORT))
    s.send(toons.dumps(data).encode())
    ret = toons.loads(s.recv(1024).decode())
    s.close()
    if  ret["type"] == "error":
        raise ValueError(ret["data"])
    elif data["is_return"]:
        return toons.loads(ret["data"])


def get_list_activ() -> list:
    return _blocker_conect({
    "type": "get_activs", # команда
    "args": [], # аргументы
    "kargs": {}, # аргументы по ключам
    "is_return": True # возвращаемый аргуменет
})


def add_list_activ(arg: str) -> None:
    return _blocker_conect({
    "type": "add_activs", # команда
    "args": [arg], # аргументы
    "kargs": {}, # аргументы по ключам
    "is_return": False # возвращаемый аргуменет
})

def del_list_index(index: int) -> str:
    return _blocker_conect({
    "type": "del_activs", # команда
    "args": [index], # аргументы
    "kargs": {}, # аргументы по ключам
    "is_return": False # возвращаемый аргуменет
})

def del_list_activ(data) -> str:
    return _blocker_conect({
    "type": "del_activs", # команда
    "args": [get_list_activ().index(data)], # аргументы
    "kargs": {}, # аргументы по ключам
    "is_return": False # возвращаемый аргуменет
})
