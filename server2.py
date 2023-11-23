import socket
import pickle

def add_numbers(a, b):
    return a + b

def subtract_numbers(a, b):
    return a - b

def handle_request(request, transactions):
    method, args, transaction_id = pickle.loads(request)

    # Verifica se já recebeu uma solicitação com o mesmo ID de transação
    if transaction_id in transactions:
        return f"Transação duplicada: {transaction_id}"

    # Processa a requisição e obtém o resultado
    if method == "add":
        result = add_numbers(*args)
    elif method == "subtract":
        result = subtract_numbers(*args)
    else:
        result = "Método desconhecido"

    # Adiciona o ID da transação à lista de transações concluídas
    transactions.add(transaction_id)

    return pickle.dumps((result, transaction_id))

# Configuração do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))  # Usando o endereço localhost
server_socket.listen(1)

transactions = set()  # Armazena IDs de transações concluídas

while True:
    # Aceita conexão
    client_socket, address = server_socket.accept()
    
    # Recebe a mensagem do cliente
    request = client_socket.recv(1024)
    
    # Processa a requisição e obtém o resultado
    result = handle_request(request, transactions)
    
    # Envia o resultado de volta para o cliente
    client_socket.send(result)
    
    # Fecha a conexão com o cliente
    client_socket.close()
