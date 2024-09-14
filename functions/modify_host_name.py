import winreg
import platform
import uuid

import logging
import traceback

import socket


def get_device_info():
    """
    get device information
    :return: mac address, ip address and device name
    """
    try:
        device_name = platform.node()
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                        for elements in range(0, 8 * 6, 8)][::-1])
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

    except:
        logging.error("An error occurred: Can not read platform information")
        raise SystemError

    return mac, ip_address, device_name


def set_host_name(new_hostname):
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters', 0,
                             winreg.KEY_ALL_ACCESS)

        winreg.SetValueEx(key, 'Hostname', 0, winreg.REG_SZ, new_hostname)
        winreg.SetValueEx(key, 'NV Hostname', 0, winreg.REG_SZ, new_hostname)

        winreg.CloseKey(key)

        # os.system(f'wmic computersystem where name="%computername%" call rename name="{new_hostname}"')

        logging.info(f'Host name has been changes as: {new_hostname}')
    except Exception as e:
        logging.error(f"Error setting host name: {e}")
        logging.debug(traceback.format_exc())
