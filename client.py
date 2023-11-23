import socket
import pickle

def rpc_stub(method, *args):
    # Encapsula os parâmetros em uma mensagem de RPC
    request = pickle.dumps((method, args))

    # Configuração do cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))

    # Envia a mensagem para o servidor
    client_socket.send(request)

    # Recebe o resultado do servidor
    result = client_socket.recv(1024)

    # Fecha a conexão com o servidor
    client_socket.close()

    # Retorna o resultado
    return pickle.loads(result)

# Exemplo de uso
add_result = rpc_stub("add", 3, 5)
print("Resultado da adição:", add_result)

subtract_result = rpc_stub("subtract", 8, 3)
print("Resultado da subtração:", subtract_result)