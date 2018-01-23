import sys
import csv

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
				try:
					key, value= line.split('=')
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

		#error


#calculate EAT and wirte it into salary.csv
class IncomeTaxCalculator(object):
	def __init__(self)


if __name__=='__main__':





#####################

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
	
if __name__=='__main__':
	main()
