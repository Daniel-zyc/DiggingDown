from Constant import *
from Map import Map
from Drill import Drill
from datetime import datetime
import shutil


class Log:
	def __init__(self):
		self.logs = [0]
		self.logs_info = [0]
		for i in range(1, LOG_NUM_MAX + 1):
			folder = LOG_ROOT_URL + f'/{i}'
			if not os.path.exists(folder):
				self.logs.append(False)
				self.logs_info.append(LOG_EMPTY_INFO)
				continue
			self.logs.append(True)
			with open(folder + '/info', mode = 'r', encoding = 'utf-8') as f:
				self.logs_info.append(f.readline().strip())

	def log_del(self, idx: int):
		folder = LOG_ROOT_URL + f'/{idx}'
		if not os.path.exists(folder):
			return
		shutil.rmtree(folder)
		self.logs[idx] = False

	def log_read(self, idx: int, mp: Map, dr: Drill):
		folder = LOG_ROOT_URL + f'/{idx}'
		with open(folder + '/map', mode = 'r') as f:
			data = eval(f.readline())
			for k, v in data.items():
				setattr(mp, k, v)
		with open(folder + '/drill', mode = 'r') as f:
			data = eval(f.readline())
			for k, v in data.items():
				setattr(dr, k, v)

	def log_save(self, idx: int, mp: Map, dr: Drill):
		folder = LOG_ROOT_URL + f'/{idx}'
		if not os.path.exists(folder):
			os.mkdir(folder)
		current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		info = LOG_INFO_FORM.format(current_time)
		logging.debug(f'{str(info)}')
		with open(folder + '/info', mode = 'w', encoding = 'utf-8') as f:
			f.write(str(info))
		with open(folder + '/map', mode = 'w') as f:
			f.write(str(vars(mp)))
		with open(folder + '/drill', mode = 'w') as f:
			f.write(str(vars(dr)))
		self.logs[idx] = True
		self.logs_info[idx] = info
