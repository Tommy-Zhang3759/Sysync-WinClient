import logging
import traceback

import json

import APIService.APIGateway
import APIService.api_workers
import APIService.api_workers

SETTINGS_FILE = "./setting.json"

DEBUG_MODE = True

class SysyncWinClient():

	_server_ip_: str = "255.255.255.255"
	_server_port_: int = -1
	_local_ip_: str = "0.0.0.0"
	_local_port_: int = 6003
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


		self.read_settings(SETTINGS_FILE, init=True)

		



	def read_settings(self, path: str, key: str = None, init: bool = False):
		try:
			with open(path, 'r') as f:
				settings = json.load(f)
		except Exception as e:
			logging.error("Can not open setting file")
			raise e
		
		if init:
			i = 0
			try:
				self._server_ip_ = settings['server_ip'] if settings['server_ip'] else self._server_ip_; i += 1
				self._server_port_ = settings["server_port"] if settings["server_port"] else self._server_port_; i += 1
				self._local_ip_ = settings["local_ip"] if settings["local_ip"] else self._local_ip_; i += 1
				self._local_port_ = settings["local_port"] if settings["local_port"] else self._local_port_; i += 1
				logging.info("Read settings: Success")
			except KeyError:
				logging.error(f"Can not find setting key: {self._setting_keys_[i]}")
			except Exception as e:
				logging.error("Unexpected Error while reading settings")
				logging.debug(traceback.format_exc())
			finally:
				if self._server_ip_ == None or self._server_port_ == None:
					logging.info("Unsetted server information")
			return True
		else:
			try:
				if key == None:
					raise KeyError
				else:
					return settings[key]
			except Exception as e:
				raise e
	
	def edit_settings(self, path: str, key: str, value):
		try:
			with open(path, 'r') as f:
				settings = json.load(f)
		except Exception as e:
			logging.error("Can not open setting file")
			raise e
		settings[key] = value

		try:
			with open(path, 'w') as f:
				json.dump(settings, f, indent=4)
		except Exception as e:
			logging.error("Failed to write to setting file")
			raise e


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
		gateway_thread.add_worker(APIService.api_workers.HostNameOffer())
		gateway_thread.add_worker(APIService.api_workers.UpdateHostName())
		gateway_thread.add_worker(APIService.api_workers.NetIPDHCP())
		gateway_thread.add_worker(APIService.api_workers.RunCmd())
		gateway_thread.add_worker(APIService.api_workers.NetIPStatic())
		gateway_thread.add_worker(APIService.api_workers.NetDNSStatic())
		gateway_thread.add_worker(APIService.api_workers.SetServerInfo(self.edit_settings))


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