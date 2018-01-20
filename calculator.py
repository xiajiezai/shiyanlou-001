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
