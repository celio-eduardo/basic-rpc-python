import socket
import pickle
import time

# Função para calcular o tempo decorrido desde o início da contagem
def elapsed_time(start_time):
    return time.time() - start_time

def rpc_stub(method, *args, timeout=5):
    # Gera um ID de transação único
    transaction_id = hash((method, args))

    # Encapsula os parâmetros e o ID da transação em uma mensagem de RPC
    request = pickle.dumps((method, args, transaction_id))

    # Configuração do cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))  # Usando o endereço localhost

    # Define um tempo limite para receber a resposta do servidor
    client_socket.settimeout(timeout)

    start_time = time.time()  # Marca o início do tempo

    while True:
        try:
            # Envia a mensagem para o servidor
            client_socket.send(request)

            # Recebe o resultado do servidor
            result = client_socket.recv(1024)

            # Desempacota o resultado e o ID da transação
            result, received_transaction_id = pickle.loads(result)

            # Verifica se recebeu uma confirmação válida para a transação
            if received_transaction_id == transaction_id:
                break  # Saímos do loop se a transação for confirmada
        except socket.timeout:
            # Caso ocorra um timeout, retransmitir a solicitação
            print("Timeout! Retransmitindo a solicitação...")
            if elapsed_time(start_time) > timeout:
                print("Tempo limite atingido. Abortando.")
                return "Tempo limite excedido"

    # Fecha a conexão com o servidor
    client_socket.close()

    # Retorna o resultado
    return result

# Exemplo de uso
add_result = rpc_stub("add", 3, 5)
print("Resultado da adição:", add_result)

subtract_result = rpc_stub("subtract", 8, 3)
print("Resultado da subtração:", subtract_result)
