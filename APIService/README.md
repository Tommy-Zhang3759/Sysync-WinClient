# API Service Module

## Intro

This module (all files under this folder) is responsible for factoring UDP APIs of server-client communication. Each API is defined by a class, which inherits from the parent API template class: UDPAPIWorker.

## Usage

Send a json message to the running port of API Gateway. A specific function can be called by the argument *f_name*, followed by additional arguments allowed. 

## API List

### *run_command* 

- protocol: UDP
- args: *string* *command* shell language script would like to run; 


### *update_host_name* 

- protocol: UDP
- args: *string* *host_ip* target server that will response host name checking request; *int* *host_port* the target port on the target server;
- description: The client will send a request, which includes *f_name* equals to *host_name_req* to the target server on target port to get the host name identified by the MAC address.


### *host_name_offer*

- protocol: UDP
- args: *string* *host_name* the client will set local NetBIOS name as this value;
- description: By modifying regestory, changing NetBIOS name


### *net_ip_dhcp* 

- protocol: UDP
- args: *string* *interface_name* target local network interface name *bool* *dhcp_dns=True* set *False* to disable set DNS server included in DHCP potion;
- description: 

### *net_static_ip* 
- protocol: UDP
args: *string* *interface_name* target local network interface name; *string* *ip_address* IP address to set; *string* *subnet_mask* subnet mask to set; *string* *gateway* the IP address of net gateway; *string* *dns* the IP address of DNS server to set;
- description: This function is used to set address and other necessities manually.

### *net_dns_static* 
- protocol: UDP
- args: *string* *interface_name* The network interface to configure; *string* *dns*: The DNS server IP address.
*bool* *dhcp_dns=True* Determines if DNS should be assigned via DHCP; 
- description: Sets a static DNS server for the specified network interface, with optional DHCP-based DNS configuration.

### *set_server_info* 
- protocol: UDP
- args: *string* *server_ip* The IP address of the server to be set in the configuration file; *int* *server_port*: The port of the server to be set in the configuration file.
- description: Updates the server's IP address and port in the client configuration file (SETTINGS_FILE).
