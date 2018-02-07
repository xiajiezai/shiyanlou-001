# -*- coding: utf-8 -*-
import sys
import csv
import queue
import configparser
from multiprocessing import Process, Queue
from collections import namedtuple
from getopt import getopt, GetoptError
from datetime import datetime

IncomeTaxQuickLookupItem = namedtuple(
	'IncomeTaxQuickLookupItem',
	['TaxableBracket','TaxRate','Subtractor']
)

Threshold=3500
QUICK_LOOKUP=[
	IncomeTaxQuickLookupItem(80000,0.45,13505),
	IncomeTaxQuickLookupItem(55000,0.35,5505),
	IncomeTaxQuickLookupItem(35000,0.3,2755),
	IncomeTaxQuickLookupItem(9000,0.25,1005),
	IncomeTaxQuickLookupItem(4500,0.2,555),
	IncomeTaxQuickLookupItem(1500,0.1,105),
	IncomeTaxQuickLookupItem(0,0.03,0)
]

q_user = Queue()
q_result=Queue()

#input: c, output:config.cfg,etc.
class Args(object):
	def __init__(self):
		self.options=self._options()

	def _options(self):
	#methods in a class usually start with an underline
		try:
			opts, _=getopt(sys.argv[1:],'hC:c:d:o:',['help'])
		except GetoptError:
			print('Parameter Error')
			exit()
		options = dict(opts)
		if len(options) ==1 and ('-h' in options or '--help' in options):
			print('Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata')
			exit()
		return options

	def _value_after_option(self, option):
		value=self.options.get(option)
		if value is None and option != '-C':
			print ('Parameter Error')
			exit()
		return value

	@property
	def city(self):
		return self._value_after_option('-C')

	@property
	def config_path(self):
		return self._value_after_option('-c')
	#if we don't use property, when we use config_path, we have to write args.config_path(), with the bracket.

	@property
	def userdata_path(self):
		return self._value_after_option('-d')
	@property
	def export_path(self):
		return self._value_after_option('-o')

args=Args()
#instantiate args before we use it in the following class


#input config.cfg, read it and write it into a config dict
class Config(object):
	def __init__(self):
		self.config=self._read_config()
		#self.config is now a dict in class Config
	def _read_config(self):
		config=configparser.ConfigParser()
		config.read(args.config_path)
		if args.city and args.city.upper() in config.sections():
			return config[args.city.upper()]
		else:
			return config['DEFAULT']

	def _get_config(self, key):
		try:
			return float(self.config[key])
		except (ValueError,KeyError):
			print('Parameter Error')
			exit()

	@property
	def insurance_base_threshold(self):
		return self._get_config('JiShuL')
	@property
	def insurance_base_ceiling(self):
		return self._get_config('JiShuH')
	@property
	def insurance_rate(self):
		return sum([
			self._get_config('YangLao'),
			self._get_config('YiLiao'),
			self._get_config('ShiYe'),
			self._get_config('GongShang'),
			self._get_config('ShengYu'),
			self._get_config('GongJiJin'),
		])
config=Config()

#inpu: userdata file, output: userdata list
class UserData(Process):
	#Userdata inherites class Process, so init can be omitted

	def _read_users_data(self):
		userdata_path=args.userdata_path
		with open(userdata_path) as f:
			for line in f.readlines():
				EmployeeNumber,income_string = line.strip().split(',')
				try:
					income=int(income_string)
				except ValueError:
					print('Parameter Error')
					exit()
				yield (EmployeeNumber, income)
	def run(self):
		for data in self._read_users_data():
			q_user.put(data)
			#put the result of yield in q_user


#calculate EAT and wirte it into salary.csv
class IncomeTaxCalculator(Process):

	@staticmethod
	def calc_social_insurance(income):
		if income<config.insurance_base_threshold:
			return config.insurance_base_threshold*config.insurance_rate
		if income>config.insurance_base_ceiling:
			return config.insurance_base_ceiling*config.insurance_rate
		return income*config.insurance_rate
	@classmethod
	def calc_EAT(cls, income):
		social_insurance=cls.calc_social_insurance(income)
		#here we use calc_social_insuarance, which is a method in class IncomeTaxCalculator, so we have to use classmethod
		EarningsAfterInsurance=income- social_insurance
		Payable=EarningsAfterInsurance- Threshold
		if Payable<=0:
			return '0.00', '{:.2f}'.format(EarningsAfterInsurance)
		for item in QUICK_LOOKUP:
			if Payable > item.TaxableBracket:
				TAX = Payable*item.TaxRate-item.Subtractor
				EAT=EarningsAfterInsurance-TAX
				return '{:.2f}'.format(TAX), '{:.2f}'.format(EAT)

	def calc_for_all_userdata(self):
		while True:
			try:
				EmployeeNumber, income=q_user.get(timeout=1)
				#wait a second just to make sure the putting part is done before we get it
			except queue.Empty:
				#after 1 second and still no data, raise empty Error
				return
			data=[EmployeeNumber,income]
			#no for loop needed because we only deal with one line at a time
			social_insurance='{:.2f}'.format(self.calc_social_insurance(income))
			TAX, Salary=self.calc_EAT(income)
			data+= [social_insurance, TAX, Salary]
			data.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
			yield data

	def run(self):
		for data in self.calc_for_all_userdata():
			q_result.put(data)

class export_to_file(Process):
	def run(self):
			with open(args.export_path, 'w', newline='') as f:
				while True:
					writer=csv.writer(f)
					#if we don't use csv, we have to add comma to separate items in list
					try:
						item = q_result.get(timeout=1)
					except queue.Empty:
						return
					writer.writerow(item)
					#note: not writerows here


if __name__=='__main__':
	workers = [
		UserData(),
		IncomeTaxCalculator(),
		export_to_file()
	]
	for worker in workers:
		worker.run()