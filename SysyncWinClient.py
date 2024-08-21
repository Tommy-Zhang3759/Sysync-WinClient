import win32serviceutil
import win32service
import win32event
import servicemanager
import os
import sys
import logging
import traceback

import threading

import json

from commu import *

SETTINGS_FILE = r"C:\Users\tommyzhang\Documents\Projects\Sysync\WinClient\setting.json"

class SysyncWinClient(win32serviceutil.ServiceFramework):
	_svc_name_ = "SysyncWinClient"
	_svc_display_name_ = "Sysync"
	_svc_description_ = "Sysync Windows client background resident service"

	_server_ip_ = ""
	_server_broad_cast_port_ = -1
	_server_resident_port_ = -1
	_resident_socket_ = None

	_local_broad_cast_port_ = -1
	_debug_mode_ = False

	_setting_keys_ = ["server_ip", "broad_cast_port"]

	def __init__(self, args):
		if args == "debug":
			self._debug_mode_ = True
		
		if self._debug_mode_ != True:
			win32serviceutil.ServiceFramework.__init__(self, args)
		self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
		self.is_running = True

		logging.basicConfig(
            filename=r"C:\Users\tommyzhang\Documents\Projects\Sysync\WinClient\log.txt",
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
		


	def ReadSettings(self, path):
		try:
			f = open(path, 'r')
			settings = json.load(f)
		except Exception as e:
			logging.error("An error occurred: Can not find setting config file")
			logging.error(traceback.format_exc())
			self.SvcStop()
			raise e
		try:
			self._server_ip_ = settings['sesrver_ip']
			self._server_broad_cast_port_ = settings["server_broad_cast_port"]
			self._server_resident_port_ = settings["server_resident_port"]
			self._local_broad_cast_port_ = settings["local_broad_cast_port"]
		except Exception as e:
			logging.error("An error occurred: Can not find basic configurations")
			logging.error(traceback.format_exc())
			self.SvcStop()
			raise e 
		logging.info("Read settings succussfully")
		return True

	def ConnectServer(self):
		import modify_host_name
		try:
			mac, cip, cname = modify_host_name.get_device_info() 
		except Exception as e:
			self.SvcStop()

		req = {
			"f_name": "init_connect",
			"mac": mac,
			"ip": cip,
			"host_name": cname
		}

		send_req(self._resident_socket_, req)
		return
	
	def DisonnectServer(self):
		import modify_host_name
		try:
			mac, cip, cname = modify_host_name.get_device_info() 
		except Exception as e:
			self.SvcStop()

		req = {
			"f_name": "disconnect",
			"mac": mac,
			"ip": cip,
			"host_name": cname
		}

		send_req(self._resident_socket_, req)
		return
		
	def NetInit(self):
		try:
			self._resident_socket_ = create_client_socket()
			self._resident_socket_.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
			self._resident_socket_.connect((self._server_ip_, self._server_resident_port_))

			logging.info("Connected to %s" %(self._server_resident_port_))
			logging.info(traceback.format_exc())
		except Exception as e:
			logging.error("An error occurred: Can not creat resident socket")
			logging.error(traceback.format_exc())
		return 
	
	def SvcStop(self):
		if self._debug_mode_ != True:
			self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
		win32event.SetEvent(self.hWaitStop)
		self.is_running = False
		try:
			self._resident_socket_.close()
		except:
			pass
		return

	def SvcDoRun(self):
		servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
							  servicemanager.PYS_SERVICE_STARTED,
							  (self._svc_name_, ''))
		logging.info("Starting")
		if self.ReadSettings(SETTINGS_FILE):
			self.NetInit()

		self.ConnectServer()
		self.main()

	def EventHandler(self, mess):
		import collect_info
		import modify_host_name
		import modify_net
		import modify_reg
		try:
			match mess['f_name']:
					case "reg":
						pass
					case "setting":
						pass
					case "net":
						pass
					case "host_name":
						modify_host_name.req_host_name(self._resident_socket_)
					case "collect_input":
						pass
					case _:
						resp = {
							"status": -1, 
			  				"error": "Unexpected function name"
							}
						logging.error("An error occurred: Unexpected function name")
						logging.error(traceback.format_exc())
		except KeyError as e:
			resp = {
				"status": -1,
				"error": "Can not find key: f_name"
				}
			logging.error("An error occurred: Can not find key: f_name")
			logging.error(traceback.format_exc())
			send_mess(self._resident_socket_, resp)
		except Exception as e:
			resp = {
				"status": -1,
				"unexpected error": str(e)
				}
			logging.error("Unexpected error: %s", str(e))
			logging.error(traceback.format_exc())
			send_mess(self._resident_socket_, resp)

	def EventListener(self):
		self._resident_socket_.settimeout = None
		while self.is_running:
			mess = self._resident_socket_.recv(NET_BUFFER_SIZE)
			mess = json.loads(mess.decode("utf-8"))
			t = threading.Thread(target=self.EventHandler, kwargs=mess)
			t.start()
		return

	def main(self):
		eventListener = threading.Thread(target=self.EventListener)
		eventListener.start()
		while self.is_running:
			try:
				pass

			except Exception as e:
				logging.error("An error occurred: %s", str(e))
				logging.error(traceback.format_exc())
		eventListener.join()


if __name__ == '__main__':
    # 当作为服务运行时
    if len(sys.argv) != 1:
        win32serviceutil.HandleCommandLine(SysyncWinClient)
    else:
        # 以本地方式调试
        service = SysyncWinClient('debug')
        service.SvcDoRun()  # 直接调用服务的运行逻辑

# 你可以在这里直接调用测试代码，比如：
# service = SysyncWinClient('debug')
# service.SvcDoRun()