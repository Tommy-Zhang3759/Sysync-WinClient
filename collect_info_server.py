import socket
import pandas as pd

def start_server(host='0.0.0.0', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started, listening on {host}:{port}")

    df = pd.DataFrame(columns=["mac", "ip", "host name"])

    i = 1

    while i <= 44:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        data = client_socket.recv(1024).decode('utf-8')
        print(f"Received data: {data}")

        mac, ip, host_name = data.split()

        new_row = pd.DataFrame([[mac, ip, host_name]], columns=["mac", "ip", "host name"])

        df = pd.concat([df, new_row], ignore_index=True)

        client_socket.close()

        i += 1

    df.to_excel('output.xlsx', index=False)

if __name__ == "__main__":
    start_server()
