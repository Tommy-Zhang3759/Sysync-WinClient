import socket
import uuid
import platform


def get_device_info():
    """
    get device information
    :return: mac address, ip address and device name
    """
    # 获取设备名
    device_name = platform.node()

    # 获取网卡的 MAC 地址
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                    for elements in range(0, 8 * 6, 8)][::-1])

    # 获取 IP 地址
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
    except socket.error as e:
        ip_address = "Unknown"

    return mac, ip_address, device_name


def send_device_info(server_host, server_port):
    mac, ip, host_name = get_device_info()
    data = f"{mac} {ip} {host_name}"

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))
    client_socket.sendall(data.encode('utf-8'))

    client_socket.close()


if __name__ == "__main__":
    server_host = '192.168.60.9'  # 替换为服务器的IP地址
    server_port = 12345  # 替换为服务器使用的端口号
    send_device_info(server_host, server_port)
