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
    try:
        request_message = json.dumps(request_message)
        client_socket.send(request_message.encode('utf-8'))
        # client_socket.settimeout(10)  # 设置 10 秒超时

        # 假设服务器使用换行符 `\n` 作为消息结束标识符
        response = ""
        while True:
            part = client_socket.recv(1024).decode('utf-8')
            response += part
            if "\n" in part:  # 检测到结束符
                break
        
        resp = json.loads(response.strip())
    except Exception as e:
        logging.error("An error occurred: Can not find basic configurations")
        logging.error(traceback.format_exc())
        raise e
    
    return resp

def send_mess(client_socket, message):
    try:
        message = json.dumps(message)
        client_socket.sendall(message.encode('utf-8'))
    except Exception as e:
        raise e

    return 0