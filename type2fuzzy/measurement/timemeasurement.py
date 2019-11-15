import os
import logging
import datetime
import time

class TimeMeasurement(object):

	def __init__(self, report_folder, iterations=10):
		'''
		Decorator arguments are passed in constructor

		Arguments:
		----------
		report_folder -- string, location of the reporting folder
		iterations -- int, number of times function is repeated in order to calculate average
		'''
		self.report_folder = report_folder
		self.iterations = iterations

	def setup_logger(self, name, log_file, level=logging.DEBUG):
		'''
		Set up a new logger - so that multiple loggers can co-exist

		Arguments:
		----------
		name -- string, name of logger
		log_file -- string, location of log file

		Returns:
		--------
		logger -- newly created logger
		'''
		handler = logging.FileHandler(log_file)

		logger = logging.getLogger(name)
		logger.setLevel(level)
		logger.addHandler(handler)

		return logger

	def dispose_logger(self, logger):
		'''
		Disposes of logger

		Arguments:
		----------
		logger -- logger to be disposed of
		'''
		handlers_copy = logger.handlers.copy()
		for handler in handlers_copy:
			logger.removeHandler(handler)
			handler.flush()
			handler.close()


	def __call__(self, func):
		'''
		Is called to execute function.

		Arguments: (there can be only one)
		----------------------------------
		func -- function to be executed
		'''
		def wrapped_func(param, *args):
			'''
			Execution of the function
			'''
			dirname = self.report_folder

			#store the duration taken for each function to calculate average
			durations = []
			# create a logger for each iteration fo the function
			item_logger = self.setup_logger('item_logger', f'{dirname}\\item.log')

			# loop iteration times
			for i in range(self.iterations):
				#start timer, execute function, stop timer
				start = time.perf_counter()
				returns = func(param, *args)
				end = time.perf_counter()
				#calculate the duration and add it to the durations list
				duration = end - start
				durations.append(duration)
				#add item to list and echo
				item_logger.debug((f'\t{i},\t{args}\t{returns},\t{duration}').replace(']', '').replace('[', ''))

			#create a logger to add average duration and log
			summary_logger = self.setup_logger('summary_logger', f'{dirname}\\.summary.log')
			summary_logger.debug((f'\t{args},\t{sum(durations)/len(durations)}').replace(']', '').replace('[', ''))

			#get rid of loggers
			self.dispose_logger(item_logger)
			self.dispose_logger(summary_logger)

		return wrapped_func
