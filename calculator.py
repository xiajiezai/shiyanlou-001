from collections import namedtuple

# IncomeTaxQuickLookupItem = namedtuple(

# )

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
		print(EmployeeNumberAndEBT)
	# print(EmployeeNumberAndEBT)
if __name__=='__main__':
	main()
