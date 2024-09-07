import socket
import json
import logging
import traceback

NET_BUFFER_SIZE = 1024
NET_TIMEOUT_LIM = 10

def create_client_socket():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except Exception as e:
        raise e

    return client_socket

def send_req(client_socket, request_message):
    send_mess(client_socket, request_message)
    return recv_mess(client_socket)

def recv_mess(client_socket):
    try:
        response = ""
        while True:
            part = client_socket.recv(1024).decode('utf-8')
            response += part
            if "\n" in part:  # 检测到结束符
                break
        
        # 去除结束符
        response = response.replace("\n", "")
        resp = json.loads(response.strip())
    except Exception as e:
        logging.error("An error occurred: " + e)
        logging.error(traceback.format_exc())
        raise e
    
    return resp

def send_mess(client_socket, message):
    try:
        message = json.dumps(message) + "\n"
        client_socket.sendall(message.encode('utf-8'))
    except Exception as e:
        logging.error("An error occurred: " + e)
        logging.error(traceback.format_exc())
        raise e
