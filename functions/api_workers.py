from APIService.APIGateway import UDPAPIWorker
import json
import logging
import traceback




class run_cmd(UDPAPIWorker):
    def __init__(self):
        super().__init__()
        self.name = "run_command"
    
    def run(self):
        from run_command import run_command
        try:
            response = self.read_message()
            self.gateway.send_data(json.dumps({
                "f_name": "command_return",
                "return": run_command(response["command"])
            }))
        except Exception as e:
            logging.error(f"Error handling API {self.name}: {e}")
            logging.debug("An error occurred: %s", str(e))
            logging.debug(traceback.format_exc())
            return -1
        return 0




class update_host_name(UDPAPIWorker):
    def __init__(self):
        super().__init__()
        self.name = "update_host_name"
    
    def run(self):
        from modify_host_name import get_device_info
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
            logging.error(f"Error handling API {self.name}: {e}")
            logging.debug("An error occurred: %s", str(e))
            logging.debug(traceback.format_exc())
            return -1
        
        return 0
    
class host_name_offer(UDPAPIWorker):
    def __init__(self):
        super().__init__()
        self.name = "host_name_offer"
    
    def run(self):
        from modify_host_name import set_host_name
        try:
            response = self.read_message()
            set_host_name(response["host_name"])
        except Exception as e:
            logging.error(f"Error handling API {self.name}: {e}")
            logging.debug("An error occurred: %s", str(e))
            logging.debug(traceback.format_exc())
            return -1
        return 0



class net_ip_dhcp(UDPAPIWorker):
    def __init__(self):
        super().__init__()
        self.name = "net_ip_dhcp"
    
    def run(self):
        from modify_net import set_dhcp
        try:
            response = self.read_message()
            if "dhcp_dns" in response:
                set_dhcp(response["interface_name"], dhcp_dns=response["dhcp_dns"])
            else:
                set_dhcp(response["interface_name"])

        except Exception as e:
            logging.error(f"Error handling API {self.name}: {e}")
            logging.debug("An error occurred: %s", str(e))
            logging.debug(traceback.format_exc())
            return -1
        return 0
    
class net_ip_static(UDPAPIWorker):
    def __init__(self):
        super().__init__()
        self.name = "net_static_ip"
    
    def run(self):
        from modify_net import set_static_ip
        try:
            mess = self.read_message()
            set_static_ip(
                mess["interface_name"], 
                mess["ip_address"], 
                mess["subnet_mask"],
                mess["gateway"],
                mess["dns"]
            )
        except Exception as e:
            logging.error(f"Error handling API {self.name}: {e}")
            logging.debug("An error occurred: %s", str(e))
            logging.debug(traceback.format_exc())
            return -1
        return 0
    
class net_dns_static(UDPAPIWorker):
    def __init__(self):
        super().__init__()
        self.name = "net_dns_static"
    
    def run(self):
        from modify_net import set_dns
        try:
            mess = self.read_message()
            if "hdcp_dns" in mess:
                set_dns(
                    mess["interface_name"],
                    mess["dns"],
                    mess["dhcp_dns"]
                )
            else:
                set_dns(
                    mess["interface_name"],
                    mess["dns"]
                )
            
        except Exception as e:
            logging.error(f"Error handling API {self.name}: {e}")
            logging.debug("An error occurred: %s", str(e))
            logging.debug(traceback.format_exc())
            return -1
        return 0
    