from collections import namedtuple

IncomeTaxQuickLookupItem = namedtuple(
	'IncomeTaxQuickLookupItem',
	['TaxableBracket','TaxRate','Subtractor']
)

Threshold=3500
QUICK_LOOKUP=[
	IncomeTaxQuickLookupItem(80000,0.45,13505),
	IncomeTaxQuickLookupItem(55000,.35,5505),
	IncomeTaxQuickLookupItem(35000,.3,2755),
	IncomeTaxQuickLookupItem(9000,0.25,1005),
	IncomeTaxQuickLookupItem(4500,.2,555),
	IncomeTaxQuickLookupItem(1500,.1,105),
	IncomeTaxQuickLookupItem(0,0.03,0)
]

def payable(EBT):
	EndowmentRate=.08
	MedicalRate=.02
	UnemploymentRate=.005
	EmploymentInjuryRate=0
	MaternityRate=0
	HousingFundRate=0.06
	TotalRate=EndowmentRate+MedicalRate+ UnemploymentRate + MaternityRate+\
	HousingFundRate
	Payable=EBT*(1-TotalRate)-Threshold
	return Payable


def EAT(Payable):
	if Payable<=0:
		return '0.00'
		for item in QUICK_LOOKUP:
			if Payable > item.TaxableBracket:
				EAT = Payable* item.TaxRate- Subtractor
				return ('{:.2f}'.format(EAT))



def main():
	import sys
	item=sys.argv[1:]
	for argv in item:
		EmployeeNumberAndEBT=argv.split(':')
		EmployeeNumber=EmployeeNumberAndEBT[0]
		try:
			EBT=int(EmployeeNumberAndEBT[1])
		except ValueError:
			print('Parameter Error')
			exit()
		Salary=EAT(payable(EBT))
		print(EmployeeNumber)
	
if __name__=='__main__':
	main()
