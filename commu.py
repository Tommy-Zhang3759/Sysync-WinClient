import socket
import json

NET_BUFFER_SIZE = 1024
NET_TIMEOUT_LIM = 10

def create_client_socket(server_ip, server_port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        client_socket.connect((server_ip, server_port))
    except Exception as e:
        raise e

    return client_socket

def send_req(client_socket, request_message):
    try:
        request_message = json.dumps(request_message)
        client_socket.sendall(request_message.encode('utf-8'))
        # client_socket.settimeout(NET_TIMEOUT_LIM)
        response = client_socket.recv(NET_BUFFER_SIZE)  # 缓冲区大小为 1024 字节
        resp = json.loads(response.decode('utf-8'))
    except Exception as e:
        raise e

    return resp

def send_mess(client_socket, message):
    try:
        message = json.dumps(message)
        client_socket.sendall(message.encode('utf-8'))
    except Exception as e:
        raise e

    return 0