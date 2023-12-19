import sys
from collections import deque

def non(element):
	if element.startswith('~'):
		element = element[1:]		
	else:
		element = '~' + element
	return element	
def getKey(value, dictionary):
	for k, v in dictionary.items():
		if value == v:		
			return k			
def checkTautology(clause):
	for element in clause:
		if ('~' + element) in clause:
			return True
	return False	
def checkDeletion(newClause, clauseList, sosList, clauseDict):	
	newClauseDeleted = 0
	deletionList = []	
	deletionList2 = []	
	delDictSet = set()
	for clause in clauseList:
		if all(elements in clause for elements in newClause):
			deletionList.append(clause)			
		elif all(elements in newClause for elements in clause):			
			newClauseDeleted = 1		
	for element in deletionList:
		clauseList.remove(element)
		for k,v in clauseDict.items():
			if all(elements in element for elements in v) and len(v) == len(element):			
				delDictSet.add(k)
	for clause in sosList:
		if all(elements in clause for elements in newClause) and len(clause) != len(newClause):		
			deletionList2.append(clause)					
		elif all(elements in newClause for elements in clause):			
			newClauseDeleted = 1			
	for element in deletionList2:
		sosList.remove(element)
		for k,v in clauseDict.items():
			if all(elements in element for elements in v):
				delDictSet.add(k)
	for key in delDictSet:	
		clauseDict[key] = ''	
	return newClauseDeleted


def calculate(printDict, printcount, clauseList, arg):	
	clauseDict = {}
	pomPrintDict = {}	
	deletionList = []
	sosList = []	
	
	if arg == 'r':
		printDict.popitem()
		
	for i in range(len(clauseList)-1):
		for j in range(len(clauseList)-1):
			if all(elements in clauseList[i] for elements in clauseList[j]) and i!=j and clauseList[i] not in deletionList:
				deletionList.append(clauseList[i])
							
	for element in deletionList:
		clauseList.remove(element)	
	goals = clauseList.pop()
	printcount = len(printDict)

	for i in range(len(goals)):
		element = goals[i]
		element = non(element)
		goals[i] = element
		sosList.append([goals[i]])
		printcount = printcount + 1
		printDict[printcount] = [goals[i]]
	
	for i in range(len(clauseList)):
		clauseDict[i+1] = clauseList[i]

	for i in range(len(sosList)):
		clauseDict[len(clauseList)+1+i] = sosList[i]

	d = deque()
	
	for goal in sosList:	
		for clause in clauseList:		
			if non(goal[0]) in clause:
				pair = (getKey([goal[0]], clauseDict),getKey(clause, clauseDict))
				d.append((getKey([goal[0]], clauseDict),getKey(clause, clauseDict)))
	checked = set()
	added = set()
	unknown = 0
	newClause = 'ggrg'

	while d:	
		deleted=''	
		pair = d.popleft()	
		if clauseDict[pair[0]] == '' or clauseDict[pair[1]] == '':
			continue
		checked.add(pair)	
		clause1 = clauseDict[pair[0]]
		clause2 = clauseDict[pair[1]]
		newClause = clause1[:]	
		for element in clause1:
			if non(element) in clause2:
				deleted = element
				newClause.remove(element)
				break	
		for e in clause2:
			if e not in newClause and e != non(deleted):
				newClause.append(e)		
		if checkDeletion(newClause, clauseList, sosList, clauseDict) == 0 and not checkTautology(newClause):
			sosList.append(newClause)		
			clauseDict[len(clauseDict)+1] = newClause				
			printcount = printcount + 1
			printDict[printcount] = newClause
			pomPrintDict[printcount] = (clause1, clause2)		
			if newClause in goals:			
				unknown = 1
				break
			for element in newClause:			
				for k, v in clauseDict.items():
					if non(element) in v:					
						newPair = ((getKey(newClause, clauseDict),k))					
						newPair2 = ((k,getKey(newClause, clauseDict)))
						if newPair not in checked and newPair2 not in checked and newPair not in added and newPair2 not in added:
							d.append(newPair)
							added.add(newPair)	
	printSet = set()	

	for k, v in pomPrintDict.items():
		pair = []
		pair.append(getKey(v[0], printDict))
		pair.append(getKey(v[1], printDict))
		pair = tuple(pair)
		pomPrintDict[k] = pair		

	pomDeque = deque()
	d.append(len(printDict))
	while d:
		usedClause = d.popleft()
		printSet.add(usedClause)
		if usedClause in pomPrintDict.keys():
			parents = pomPrintDict[usedClause]
			d.append(parents[0])
			d.append(parents[1])	
	rbr = 0
	a = 0
	for i in printSet:
		if i in pomPrintDict.keys():
			a = a + 1
	num = len(printSet) - a - 1

	for k, v in printDict.items():
		if len(printDict[k]) == 0 and k==len(printDict):
			v = 'NIL'
		if k in printSet:
			if num > 0:
				num = num - 1
				rbr = rbr + 1
				if v != 'NIL':
					vPrint = ' v '.join(v)
				else:
					vPrint = v
				print( str(rbr) + " : " + vPrint + "\n")
				if num == 0:
					print("==================================\n")
			else:
				if k in pomPrintDict.keys():
					parents = pomPrintDict[k]
					rbr = rbr + 1
					if v != 'NIL':
						vPrint = ' v '.join(v)
					else:
						vPrint = v
					parent1 = ' v '.join(printDict[parents[0]])
					parent2 = ' v '.join(printDict[parents[1]])
					print( str(rbr) + " : " + vPrint + " <------------   " + parent1 + ",  " + parent2 + "\n")
				else:
					rbr = rbr + 1
					if v != 'NIL':
						vPrint = ' v '.join(v)
					else:
						vPrint = v
					print( str(rbr) + " : " + vPrint + "\n")		
	startGoals = []
	for goal in goals:
		startGoals.append(non(goal))				
	
	result = ' v '.join(startGoals)				

	if newClause == []:
		print("[CONCLUSION]: " + result +" is true\n")
	else:

		print("[CONCLUSION]: " + result +" is unknown\n")
	
for i in range(len(sys.argv)):
	if sys.argv[i] == 'resolution':
		arg = 'r'
		rPath = sys.argv[i+1]			
		printDict = {}		
		printcount = 0
		rFile = open(rPath, 'r')
		clauseList = []
		for line in rFile.readlines():
				if line.startswith("#"):	
					continue
				line = line.lower()
				line = line.strip().split(" v ")
				printcount = printcount + 1
				printDict[printcount] = line
				if checkTautology(line) == False:
					clauseList.append(line)			
		calculate(printDict, printcount, clauseList, arg)

for i in range(len(sys.argv)):
	if sys.argv[i] == 'cooking':
		arg = 'c'
		rPath = sys.argv[i+1]			
		cPath = sys.argv[i+2]
		cFile = open(cPath, 'r')
		lines = cFile.readlines()
		#print(lines)
		ind = 0
		for line in lines:
			ind = ind + 1	
			print("Users command: " + line)		
			if line.endswith('?\n'):			
				rFile = open(rPath, 'r')
				clauseList = []
				printDict = {}		
				printcount = 0
				for line2 in rFile.readlines():
					if line2.startswith("#"):	
						continue
					line2 = line2.lower()
					line2 = line2.strip().split(" v ")
					printcount = printcount + 1
					printDict[printcount] = line2
					if checkTautology(line2) == False:
						clauseList.append(line2)		
				for pomLine in lines[:ind]:
					if pomLine.endswith('+\n'):
						pomLine = pomLine.strip().split("+")
						pomLine = pomLine[0].lower()
						pomLine = pomLine.strip().split(" v ")
						clauseList.append(pomLine)
						printcount = printcount + 1
						printDict[printcount] = pomLine
						
					elif pomLine.endswith('-\n'):
						pomLine = pomLine.strip().split("-")
						pomLine = pomLine[0].lower()
						pomLine = pomLine.strip().split(" v ")
						for i in range(len(clauseList)):
							if all(elements in clauseList[i] for elements in pomLine) and len(clauseList[i]) == len(pomLine):
								remIndex = i
						clauseList.pop(remIndex)
						key = getKey(pomLine, printDict)
						printDict[key] = ''
				
				line = line.lower()
				line = line.strip().split("?")
				clauseList.append([line[0].strip()])
				calculate(printDict, printcount, clauseList, arg)
		
