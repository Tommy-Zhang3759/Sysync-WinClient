import logging
import traceback

import json

import APIService.APIGateway
import functions.api_workers
import functions.modify_host_name

SETTINGS_FILE = "./setting.json"

DEBUG_MODE = True

class SysyncWinClient():

	_server_ip_: str = "127.0.0.1"
	_server_port_: int = -1
	_local_ip_: str = "0.0.0.0"
	_local_port_ = 6003
	_resident_socket_ = None

	_debug_mode_ = False
	is_running: bool = False

	_setting_keys_ = [
		"server_ip", 
		"server_port", 
		"local_ip",
		"local_port"
	]

	def __init__(self, log_level: str="INFO", **args):
		self._debug_mode_ = DEBUG_MODE

		if self._debug_mode_:
			logging.basicConfig(
				filename="./log.txt",
				level=logging.DEBUG,
				format='%(asctime)s - %(levelname)s - %(message)s'
			)
		else:
			if log_level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
				logging.basicConfig(
					filename="./log.txt",
					level=logging.getLevelName(log_level),
					format='%(asctime)s - %(levelname)s - %(message)s'
				)
			else:
				raise ValueError("Invalid logging sensitive")

		self.is_running = True


		self.ReadSettings(SETTINGS_FILE)

	def ReadSettings(self, path):
		try:
			with open(path, 'r') as f:
				settings = json.load(f)
		except Exception as e:
			logging.error("Can not open config file")
			self.SvcStop()
			raise e
		
		i = 0
		try:
			self._server_ip_ = settings['server_ip']; i += 1
			self._server_port_ = settings["server_port"]; i += 1
			self._local_ip_ = settings["local_ip"]; i += 1
			self._local_port_ = settings["local_port"]; i += 1
		except KeyError:
			logging.error(f"Can not find setting key: {self._setting_keys_[i]}")
			self.SvcStop()
		except Exception as e:
			logging.error("Unexpected Error")
			logging.debug(traceback.format_exc())
			self.SvcStop()
			raise e 
		logging.info("Read settings: Success")
		return True
	
	def SvcStop(self):
		self.is_running = False
		try:
			self._resident_socket_.close()
		except:
			pass
		return

	def SvcDoRun(self):
		logging.info("Starting")
		self.is_running = True

		self.main()

	def main(self):
		gateway_thread = APIService.APIGateway.UDPGatewayThread(self._local_ip_, self._local_port_)
		gateway_thread.add_worker(functions.api_workers.host_name_offer())
		gateway_thread.add_worker(functions.api_workers.update_host_name())
		gateway_thread.add_worker(functions.api_workers.net_ip_dhcp())
		gateway_thread.add_worker(functions.api_workers.RunCmd())
		gateway_thread.add_worker(functions.api_workers.net_ip_static())
		gateway_thread.add_worker(functions.api_workers.net_dns_static())


		gateway_thread.start()

		while self.is_running:
			try:
				pass

			except Exception as e:
				logging.error("An error occurred: %s", str(e))
				logging.debug(traceback.format_exc())
		# eventListener.join()

if __name__ == '__main__':

	if DEBUG_MODE:
		service = SysyncWinClient('DEBUG')
		service.SvcDoRun()
	else:
		service = SysyncWinClient()
		service.SvcDoRun()