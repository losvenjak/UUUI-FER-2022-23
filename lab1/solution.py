import sys
from queue import Queue
from queue import PriorityQueue
ssDict = {}
hDict = {}


input = sys.stdin.readline()
input = input.strip().split("--")

start = ''
hPath = ''
checkOpt = False
checkCons = False
for element in input:
	element = element.strip().split(" ")
	
	if len(element) < 2:
		if element[0] == 'check-optimistic':
			checkOpt = True
		elif element[0] == 'check-consistent':
			checkCons = True
	else:
		if element[0] == 'alg':
			algorithm = element[1]
		elif element[0] == 'ss':
			ssPath = element[1]
		elif element[0] == 'h':
			hPath = element[1]
	

ssFile = open(ssPath, 'r')
lines = ssFile.readlines()

for line in lines:
	if line.startswith("#"):
		continue
	else:
		line = line.strip().split(":")
		
		if len(line) < 2:
			if start == '':
				start = line[0]		
				
			else:
				finish = line[0].strip().split(" ")
				
			continue
		else:
			neighbourDict = {}
			neighbourDict.clear()
			neighbours = line[1].strip().split(" ")
			
			for neighbour in neighbours:
				neighbour = neighbour.strip().split(",")
				if len(neighbour) < 2:
					continue
				else:
					neighbourDict[neighbour[0]] = neighbour[1]				
			ssDict[line[0]] = neighbourDict
			
			
ssFile.close()
if not hPath == '':
	hFile = open(hPath, 'r')
	lines = hFile.readlines()

	for line in lines:
		if line.startswith("#"):
			continue
		else:
			line = line.strip().split(":")
			if len(line) < 2:
				continue
			else:				
				hDict[line[0]] = line[1].strip()
		
	hFile.close()

def BFS():
	visited = set()
	q = Queue()
	q.put((start, [start]))
	totalCost = 0.0
	while not q.empty():
		state, path = q.get()
		
		if state in finish:
			visited.add(state)
			for i in range(len(path)):
				if not i==len(path)-1:
					totalCost = totalCost + float(ssDict[path[i]][path[i+1]])
			print("# BFS")
			print("[FOUND_SOLUTION]: yes")
			print("[STATES_VISITED]: " + str(len(visited)))
			print("[PATH_LENGTH]: " + str(len(path)))
			print("[TOTAL_COST]: " + str(totalCost))
			print("[PATH]: ", " => ".join(path))
			
			break
		if state not in visited:
			
			visited.add(state)
			for neighbour, cost in ssDict[state].items():
            			if neighbour not in visited:
                			q.put((neighbour, path + [neighbour]))
                



def UCS():
	visited = set()
	pq = PriorityQueue()
	pq.put((0.0, start, [start]))
	while not pq.empty():
		cost, state, path = pq.get()
		if state in finish:
			visited.add(state)
			print("# UCS")
			print("[FOUND_SOLUTION]: yes")
			print("[STATES_VISITED]: " + str(len(visited)))
			print("[PATH_LENGTH]: " + str(len(path)))
			print("[TOTAL_COST]: " + str(cost))
			print("[PATH]: ", " => ".join(path))
			break
		if state not in visited:
			visited.add(state)
			for neighbour, neighbour_cost in ssDict[state].items():
				if neighbour not in visited:
					priority = (cost + float(neighbour_cost), neighbour)
					pq.put((cost + float(neighbour_cost), neighbour, path + [neighbour]))
					



	
def A_STAR(start):
	pq = PriorityQueue()
	pq.put((0.0, start))
	came_from = {}
	cost_so_far = {start: 0.0}
	visited = set()
    
	while not pq.empty():
		current_cost, current_state = pq.get()
		visited.add(current_state)
		if current_state in finish:
			totalCost = cost_so_far[current_state]
			path = [current_state]
			while current_state != start:
				current_state = came_from[current_state]
				path.append(current_state)
			path.reverse()
			#print("# A-STAR")
			#print("[FOUND_SOLUTION]: yes")
			#print("[STATES_VISITED]: " + str(len(visited)))
			#print("[PATH_LENGTH]: " + str(len(path)))
			#print("[TOTAL_COST]: " + str(totalCost))
			#print("[PATH]: ", " => ".join(path))
			return visited, path, totalCost
        
		for neighbor, cost in ssDict[current_state].items():
			new_cost = float(cost_so_far[current_state]) + float(cost)
			
			if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
				cost_so_far[neighbor] = new_cost
				
				priority = (new_cost + float(hDict[neighbor]), neighbor)
				pq.put((priority, neighbor))
				came_from[neighbor] = current_state
    
	return None
	

def print_A_STAR():
	visited, path, totalCost = A_STAR(start)
	print("# A-STAR " + hPath)
	print("[FOUND_SOLUTION]: yes")
	print("[STATES_VISITED]: " + str(len(visited)))
	print("[PATH_LENGTH]: " + str(len(path)))
	print("[TOTAL_COST]: " + str(totalCost))
	print("[PATH]: ", " => ".join(path))

def checkConsistent():
	consistent = True
	print("# HEURISTIC-CONSISTENT " + hPath)
	for state in ssDict.keys():
		for neighbour, cost in ssDict[state].items():
			if float(hDict[state]) <= float(cost) + float(hDict[neighbour]):
				print("[CONDITION]: [OK] h(" + state + ") <= h(" + neighbour + ") + c: " + str(float(hDict[state])) + " <= " + str(float(hDict[neighbour])) + " + " + str(float(cost)))
			else:
				consistent = False
				print("[CONDITION]: [ERR] h(" + state + ") <= h(" + neighbour + ") + c: " + str(float(hDict[state])) + " <= " + str(float(hDict[neighbour])) + " + " + str(float(cost)))
	if consistent:
		print("[CONCLUSION]: Heuristic is consistent.")
	else:
		print("[CONCLUSION]: Heuristic is not consistent.")



def checkOptimistic():
	optimistic = True
	print("# HEURISTIC-OPTIMISTIC " + hPath)
	for state in ssDict.keys():
		visited, path, realCost = A_STAR(state)
		heuristic = float(hDict[state])
		if heuristic <= realCost:
			print("[CONDITION]: [OK] h(" + state + ") <= h*: " + str(heuristic) + " <= " + str(realCost))
		else:
			print("[CONDITION]: [ERR] h(" + state + ") <= h*: " + str(heuristic) + " <= " + str(realCost))
			optimistic = False
	if optimistic:
		print("[CONCLUSION]: Heuristic is optimistic.")
	else:
		print("[CONCLUSION]: Heuristic is not optimistic.")
		


if algorithm == 'bfs':
	BFS()
elif algorithm == 'ucs':
	UCS()
elif algorithm == 'astar':
	print_A_STAR()
print(checkOpt)
if checkOpt:
	checkOptimistic()
	print(checkOpt)
if checkCons:
	checkConsistent()