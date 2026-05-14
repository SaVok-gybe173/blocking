import socket
import threading
import toons

try:
    from .constant import IP, PORT
except (ImportError, ModuleNotFoundError):
    from constant import IP, PORT


{
    "type": "", # команда
    "args": [], # аргументы
    "kargs": {}, # аргументы по ключам
    "is_return": False # возвращаемый аргуменет
}


class Main:
    activs = ["dad"]
    user_activ = True


    def __init__(self, ip = IP, port = PORT):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        self.server.listen(30)
        self.comands = {"get_activs": lambda: toons.dumps(self.activs), "add_activs": lambda activ: self.activs.append(toons.loads(activ)), "del_activs": lambda index: self.activs.pop(index), "get_user_activ": lambda: self.user_activ}
        

    def start(self):
        while True:
            client_socket, client_addr = self.server.accept()
            thread = threading.Thread(target=self.client, args=(client_socket, client_addr), daemon=True)
            thread.start()

    def client(self, client_socket: socket.socket, client_addr: tuple[str, int]):
        try:
            data: dict = toons.loads(client_socket.recv(1024).decode())
            
            ret = self.comands[data["type"]](*data["args"], **data["kargs"])
            client_socket.send(toons.dumps({"data": ret, "type": "ok"}).encode())
        except Exception as e:
            client_socket.send(toons.dumps({"data": str(e), "type": "error"}).encode())
        client_socket.close()

if __name__ == "__main__":
    Main().start()

