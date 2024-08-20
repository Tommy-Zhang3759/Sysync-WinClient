import socket
import pandas as pd
import json

df = pd.read_csv("mac_ip_host_name.csv")

def create_server_socket(server_ip, server_port):
    # 创建一个 TCP/IP 套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 绑定套接字到指定的 IP 地址和端口
    server_socket.bind((server_ip, server_port))
    
    # 开始监听传入的连接
    server_socket.listen(50)  # 允许的最大连接数为 50
    print(f'Server listening on {server_ip}:{server_port}')
    
    return server_socket

def handle_client_connection(client_socket, client_address):
    print(f'Connection from {client_address} has been established!')
    
    # 接收客户端的请求消息
    request = client_socket.recv(1024).decode('utf-8')

    req_dict = json.loads(request)

    print(f'Received from client: {req_dict}')
    
    cli_info = df.loc[df['mac'] == req_dict["mac"]]
    cli_info_dict = cli_info.iloc[0].to_dict()
    # 发送响应消息回客户端
    response_message = cli_info.to_json(orient="records")
    response_message = json.dumps(cli_info_dict)
    client_socket.sendall(response_message.encode('utf-8'))
    
    # 关闭与客户端的连接
    client_socket.close()

def main():
    server_ip = '0.0.0.0'  # 服务器的 IP 地址
    server_port = 65432       # 服务器的端口
    
    server_socket = create_server_socket(server_ip, server_port)
    
    try:
        while True:
            # 接受一个新的连接
            client_socket, client_address = server_socket.accept()
            
            # 处理客户端的连接
            handle_client_connection(client_socket, client_address)
    finally:
        # 关闭服务器套接字
        server_socket.close()

if __name__ == '__main__':
    main()
