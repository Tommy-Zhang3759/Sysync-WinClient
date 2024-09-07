import threading
import queue
import time
import json
import socket

LISTEN_PORT = 6003
SERVER_PORT = 6004


# 定义子线程类，每个子线程有一个对应的队列来接收数据
class UDPAPIWorker():
    def __init__(self):
        super().__init__()
        self.name: str = None
        self.message_queue = queue.Queue()  # 每个线程都有自己的队列
        self.running: bool = True
        self.gateway: UDPGatewayThread = None

    def run(self):
        print(f"Thread {self.name} started.")
        while self.running:
            try:
                # 从队列中获取任务，超时时间设置为 1 秒
                task = self.message_queue.get(timeout=1)
                if task is None:  # None 作为退出标志
                    break
                print(f"Thread {self.name} processing task: {task}")
                # 模拟任务处理时间
                time.sleep(2)
            except queue.Empty:
                continue

    def add_message(self, task):
        self.message_queue.put(task)

    def read_message(self, timeout: int = 10):
        return self.message_queue.get(timeout=timeout)

    def stop(self):
        self.running = False
        self.message_queue.put(None)  # 停止标志

# Gateway 线程：负责分发任务
class UDPGatewayThread(threading.Thread):
    def __init__(self, ip: str, port: int, buffer_size: int = 1024):
        super().__init__()
        self.api_workers: dict[str, UDPAPIWorker] = {}
        self.gateway_rec_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.buffer_size = buffer_size
        self.work_ip = ip
        self.work_port = port

    def add_worker(self, w: UDPAPIWorker):
        w.gateway = self
        self.api_workers[w.name] = w


    def run(self):
        try:
            self.gateway_rec_sock.bind((self.work_ip, self.work_port))
            print("Gateway is listenging on: "+self.work_ip, self.work_port)
        except Exception as e:
            print("Error binding socket:" + e)
            return
        
        while True:
            received_data: dict = self.receive_data()

            if received_data == "exit":
                print("Shutting down Gateway...")
                break

            f_name = received_data['f_name']
            if f_name in self.api_workers:
                # 将任务分配给对应的线程
                self.api_workers[f_name].add_message(received_data)
                self.api_workers[f_name].run() # not using thread.start(); no necessity, using system udp port buffer queue
            else:
                print(f"No worker thread for {f_name}")

    def receive_data(self):
        data, addr = self.gateway_rec_sock.recvfrom(self.buffer_size)
        print(f"Received message from {addr}: {data.decode()}")
        
        return json.loads(data.decode())
    
    def send_data(self, message: str, target_ip: str = SERVER_PORT, target_port: int = SERVER_PORT):
        try:
            self.gateway_rec_sock.sendto(message.encode(), (target_ip, target_port))
            print(f"Message '{message}' sent to {target_ip}:{target_port}")
        
        except Exception as e:
            print(f"Failed to send message: {e}")
            return -1

        return 0

