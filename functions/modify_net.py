import os
import win32api
import APIService
import logging


def set_static_ip(interface_name: str, ip_address: str, subnet_mask: str, gateway: str, dns: str):
    # 使用 netsh 命令设置IP地址、子网掩码和网关
    for_ip = f'netsh interface ip set address name="{interface_name}" static {ip_address} {subnet_mask} {gateway} 1'
    for_dns = f'netsh interface ip set address name="{interface_name}" {dns}'
    try:
        os.system(for_ip)
        # win32api.MessageBox(0, f"IP地址已设置为 {ip_address}", "设置成功", 0x00001000)
        os.system(for_dns)
    except Exception as e:
        win32api.MessageBox(0, f"设置IP地址失败: {str(e)}", "错误", 0x00001000)
    return


# 示例：设置名为"Ethernet"的网卡的IP地址

def set_dhcp(interface_name: str, dhcp_dns: bool = True):
    if dhcp_dns:
        for_dns = f'netsh interface ip set address name={interface_name} source=dhcp'
    try:
        os.system(for_dns)
    except Exception as e:
        win32api.MessageBox(0, f"设置DHCP失败: {str(e)}", "错误", 0x00001000)


def set_dns(interface_name: str = "", dns: str = "", hdcp_dns: bool = False):
    # 使用 netsh 命令设置IP地址、子网掩码和网关
    if hdcp_dns == True:
        for_dns = f'netsh interface ip set dns name={interface_name} source=dhcp'
    else:
        for_dns = f'netsh interface ip set address name={interface_name} {dns} register=primary'
    try:
        os.system(for_dns)
    except Exception as e:
        win32api.MessageBox(0, f"设置IP地址失败: {str(e)}", "错误", 0x00001000)
    return
