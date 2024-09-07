import winreg
import os
import platform
import uuid
import json

import logging
import traceback

import socket

import APIService.APIGateway

def get_device_info():
    try:
        device_name = platform.node()
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                    for elements in range(0, 8*6, 8)][::-1])
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

    except:
        logging.error("An error occurred: Can not read platform information")
        raise SystemError

    
    return mac, ip_address, device_name

def set_host_name(new_hostname):
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters', 0, winreg.KEY_ALL_ACCESS)
        
        winreg.SetValueEx(key, 'Hostname', 0, winreg.REG_SZ, new_hostname)
        winreg.SetValueEx(key, 'NV Hostname', 0, winreg.REG_SZ, new_hostname)
        
        winreg.CloseKey(key)
        
        # os.system(f'wmic computersystem where name="%computername%" call rename name="{new_hostname}"')
        
        logging.info(f'Host name has been changes as: {new_hostname}')
    except Exception as e:
        logging.error(f"Error setting host name: {e}")
        logging.debug(traceback.format_exc())


class update_host_name(APIService.APIGateway.UDPAPIWorker):
    def __init__(self):
        super().__init__()
        self.name = "updateHostName"
    
    def run(self):
        mac, ip, current_host_name = get_device_info()
        mess = self.read_message()
        try:
            self.gateway.send_data(
                json.dumps({
                    "f_name": "hostNameReq",
                    "mac": mac,
                    "ip": ip,
                    "current_host_name": current_host_name
                }),
                target_ip=mess["host_ip"],
                target_port=mess["host_port"]
            )
        except Exception as e:
            raise e
        
        return 0
    
class host_name_offer(APIService.APIGateway.UDPAPIWorker):
    def __init__(self):
        super().__init__()
        self.name = "hostNameOffer"
    
    def run(self):
        try:
            response = self.read_message()
            print(f'Response from server: {response}')
            print(response["host_name"])
            set_host_name(response["host_name"])
        except Exception as e:
            logging.error
            logging.debug("An error occurred: %s", str(e))

            raise e
        
        return 0