import win32serviceutil
import win32service
import win32event
import servicemanager
import os
import logging
import traceback

import threading

import json


from commu import *

SETTINGS_FILE = "setting.json"

class SysyncWinClient(win32serviceutil.ServiceFramework):
	_svc_name_ = "SysyncWinClient"
	_svc_display_name_ = "Sysync"
	_svc_description_ = "Sysync Windows client background resident service"

	_server_ip_ = ""
	_server_broad_cast_port_ = -1
	_server_resident_port_ = -1
	_resident_socket_ = None

	_local_broad_cast_port_ = -1


	_setting_keys_ = ["server_ip", "broad_cast_port"]

	def __init__(self, args):
		win32serviceutil.ServiceFramework.__init__(self, args)
		self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
		self.is_running = True
		self.ReadSettings(SETTINGS_FILE)
		self.NetInit()
		
	def ReadSettings(self, path):
		with open(path, 'r') as f:
			settings = json.load()
		try:
			self._server_ip_ = settings['sesrver_ip']
			self._server_broad_cast_port_ = settings["server_broad_cast_port"]
			self._server_resident_port_ = settings["server_resident_port"]
			self._local_broad_cast_port_ = settings["local_broad_cast_port"]
		except:
			raise NameError
		
	def NetInit(self):
		self._resident_socket_ = create_client_socket(self._server_ip_, self._server_resident_port_)
		return 
	
	def SvcStop(self):
		self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
		win32event.SetEvent(self.hWaitStop)
		self.is_running = False
		self._resident_socket_.close()

	def SvcDoRun(self):
		servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
							  servicemanager.PYS_SERVICE_STARTED,
							  (self._svc_name_, ''))
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
						try: 
							stat = modify_host_name.req_host_name(self._resident_socket_)
							mac, cip, cname = modify_host_name.get_device_info() 
							resp = {
								"status": stat,
								"mac": mac,
								"ip": cip,
								"cname": cname
								}
						except OSError as e:
							resp = {
								"status": -1,
								"error": "Can not open the regedit to modify host name"
								}
							logging.error("An error occurred: Can not open the regedit to modify host name")
							logging.error(traceback.format_exc())
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
		except Exception as e:
			resp = {
				"status": -1,
				"unexpected error": str(e)
				}
			logging.error("Unexpected error: %s", str(e))
			logging.error(traceback.format_exc())
		finally:
			send_mess(self._resident_socket_, resp)
			return

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
	win32serviceutil.HandleCommandLine(SysyncWinClient)
