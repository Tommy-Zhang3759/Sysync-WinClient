import winreg
import os
import platform
import uuid
import json
import logging

from commu import *

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

def set_hostname(new_hostname):
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters', 0, winreg.KEY_ALL_ACCESS)
        
        winreg.SetValueEx(key, 'Hostname', 0, winreg.REG_SZ, new_hostname)
        winreg.SetValueEx(key, 'NV Hostname', 0, winreg.REG_SZ, new_hostname)
        
        winreg.CloseKey(key)
        
        # os.system(f'wmic computersystem where name="%computername%" call rename name="{new_hostname}"')
        
        print(f'Host name has been changes as: {new_hostname}')
    except Exception as e:
        print(f'Error: {e}')


def req_host_name(client_socket):
    mac, _, _ = get_device_info()
    try:
        req = json.dumps({"mac": mac})
        response = send_req(client_socket, req)
        print(f'Response from server: {response}')
        rep_dict = json.loads(response)
        print(rep_dict["host_name"])
        set_hostname(rep_dict["host_name"])
    except Exception as e:
        raise e
    
    return 0

def auto_req(socket):
    try: 
        stat = req_host_name(socket)
        mac, cip, cname = get_device_info() 
        resp = {
            "status": stat,
            "mac": mac,
            "ip": cip,
            "host_name": cname
            }
    except OSError as e:
        resp = {
            "status": -1,
            "error": "Can not open the regedit to modify host name"
            }
        logging.error("An error occurred: Can not open the regedit to modify host name")
        logging.error(traceback.format_exc())