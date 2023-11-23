import socket
import pickle

def add_numbers(a, b):
    return a + b

def subtract_numbers(a, b):
    return a - b

def handle_request(request):
    # Desencapsula a mensagem e chama a função correspondente
    method, args = pickle.loads(request)
    if method == "add":
        result = add_numbers(*args)
    elif method == "subtract":
        result = subtract_numbers(*args)
    else:
        result = "Método desconhecido"
    return result

# Configuração do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(1)

while True:
    # Aceita conexão
    client_socket, address = server_socket.accept()
    
    # Recebe a mensagem do cliente
    request = client_socket.recv(1024)
    
    # Processa a requisição e obtém o resultado
    result = handle_request(request)
    
    # Envia o resultado de volta para o cliente
    client_socket.send(pickle.dumps(result))
    
    # Fecha a conexão com o cliente
    client_socket.close()
