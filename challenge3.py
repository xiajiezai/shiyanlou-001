# -*- coding: utf-8 -*-
import sys
import csv
from collections import namedtuple

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

#input: c, output:config.cfg,etc.
class Args(object):
	def __init__(self):
		self.args=sys.argv[1:]
		#a list
	def _value_after_option(self,option):
	#methods in a class usually start with an underline
		try:
			index=self.args.index(option)
			return self.args.index(index+1)
		except(ValueError, IndexError):
			print('Parameter Error')
			exit()

	@property
	def config_path(self):
		return self._value_after_option('-c')
	#if we don't use property, when we use config_path, we have to write args.config_path(), with the bracket.

	def userdata_path(self):
		return self._value_after_option('-d')

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
		config_path=args.config_path
		config={}
		with open(config_path) as f:
			for line in f.readlines():
				key, value= line.split('=')
				try:
					config[key.strip()]=float(value().split())
					#make them a key and a value in dict config
					except ValueError:
					print('Parameter Error')
		return config

	def _get_config(self, key):
		try:
			return self.config[key]
		except KeyError:
			print('Config Error')
			exit()

	@property
	def insurance_base_threshold(self):
		return self._get_config('JishuL')
	@property
	def insurance_base_ceiling(self):
	return self._get_config('JishuH')
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
class UserData(object):
	def __init__(self):
		self.userdata=self._read_users_data()
	def _read_users_data(self):
		userdata_path=args.userdata_path
		userdata=[]
		with open(userdata_path) as f:
			for line in f:
				EmployeeNumber,income_string = line.strip().split(',')
				try:
					income=int(income_string)
				except ValueError:
					print('Parameter Error')
					exit()
				userdata=append((EmployeeNumber,income))
		return userdata
	def __iter__(self):
		return iter(self.userdata)
		#error


#calculate EAT and wirte it into salary.csv
class IncomeTaxCalculator(object):
	def __init__(self,userdata):
		self.userdata=userdata
	@staticmethod
	def calc_social_insurance(income):
		if income<config.insurance_base_threshold:
			return config.insurance_base_threshold*config.insurance_rate
		if income>config.insurance_base_ceiling:
			return config.insurance_base_ceiling*config.insurance_rate
		return income*config.insurance_rate
	@classmethod
	def calc_EAT(cls, income):
		social_insurance=cls.calc_social_insurance(income):
		#here we use calc_social_insuarance, which is a method in class IncomeTaxCalculator, so we have to use classmethod
		EarningsAfterInsurance=income- social_insurance
		Payable=earningsafterinsurance- Threshold
		if Payable<=0:
			return EarningsAfterInsurance
		for item in QUICK_LOOKUP:
			if Payable > item.TaxableBracket:
				TAX = Payable*item.TaxRate-item.Subtractor
				EAT=EarningsAfterInsurance-TAX
				return TAX, EAT

	def calc_for_all_userdata(self):
		result=[]
		for EmployeeNumber, income in self.userdata:
			data=[EmployeeNumber,income]
			social_insurance=self.calc_social_insurance(income)
			tax, Salary=self.calc_EAT(income)
			data+= [social_insurance, TAX, Salary]
			result.append.data
		return result

	def export_to_file(self, default='csv'):
		result=self.calc_for_all_userdata()
		with open(args.export_path, 'w', newline='') as f:
			write=csv.write(f)
			#if we don't use csv, we have to add comma to separate items in list
			write.writerows(result)


if __name__=='__main__':
	calculator=IncomeTaxCalculator(UserData())
	calculator.export_to_file()





#####################
'''
from collections import namedtuple

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

def earningsafterinsurance(EBT):
	EndowmentRate=.08
	MedicalRate=.02
	UnemploymentRate=.005
	EmploymentInjuryRate=0
	MaternityRate=0
	HousingFundRate=0.06
	TotalRate=EndowmentRate+MedicalRate+ UnemploymentRate + \
	EmploymentInjuryRate + MaternityRate+ HousingFundRate
	EarningsAfterInsurance=EBT*(1-TotalRate)
	return EarningsAfterInsurance


def EAT(EarningsAfterInsurance):
	Payable=EarningsAfterInsurance-Threshold
	if Payable<=0:
		return EarningsAfterInsurance
	for item in QUICK_LOOKUP:
		if Payable > item.TaxableBracket:
			TAX = Payable*item.TaxRate-item.Subtractor
			EAT=EarningsAfterInsurance-TAX
			return EAT



def main():
	import sys
	item=sys.argv[1:]
	for argv in item:
		EmployeeNumber, EBTString=argv.split(':')
		try:
			EBT=int(EBTString)
		except ValueError:
			print('Parameter Error')
			exit()
		Salary=float(EAT(earningsafterinsurance(EBT)))
		print('{}:{:.2f}'.format(EmployeeNumber,Salary))
	
'''