import os
from multiprocessing import Pool
import time

runner = "python3 /home/yutil15/Checkers_ShallowBlue/Tools/AI_Runner.py "
size1 = "7 7 2 l "
size2 = "9 8 2 l "
our_AI = "/home/yutil15/Checkers_ShallowBlue/src/checkers-python/main.py "
our_cpp = "/home/yutil15/Checkers_ShallowBlue/src/checkers-cpp/main "
Average_AI = "/home/yutil15/Checkers_ShallowBlue/Tools/Sample_AIs/Average_AI_368/main.py "
Random_AI = "/home/yutil15/Checkers_ShallowBlue/Tools/Sample_AIs/Random_AI/main.py "
Good_AI = "/home/yutil15/Checkers_ShallowBlue/Tools/Sample_AIs/Good_AI_368/main.py "
tail = "| tail -n 1"

dc1 = runner + size1 + our_AI + Random_AI
dc2 = runner + size1 + Random_AI + our_AI
dc3 = runner + size2 + our_AI + Random_AI
dc4 = runner + size2 + Random_AI + our_AI

dc_commands = [dc1, dc2, dc3, dc4]

test1 = runner + size1 + our_AI + Average_AI
test2 = runner + size1 + Average_AI + our_AI
test3 = runner + size2 + our_AI + Average_AI
test4 = runner + size2 + Average_AI + our_AI

good1 = runner + size1 + our_AI + Good_AI
good2 = runner + size1 + Good_AI + our_AI
good3 = runner + size2 + our_AI + Good_AI
good4 = runner + size2 + Good_AI + our_AI

test1cpp = runner + size1 + our_cpp + Average_AI
test2cpp = runner + size1 + Average_AI + our_cpp
test3cpp = runner + size2 + our_cpp + Average_AI
test4cpp = runner + size2 + Average_AI + our_cpp

test_commands = [test1, test2, test3, test4]
#test_commands = [good1, good2, good3, good4]

test_cpps = [test1cpp, test2cpp, test3cpp, test4cpp]

test_time = 10

def rundc(j, dc):
	# for dc in dc_commands:
	start = time.time()
	os.system(dc+tail)
	t = time.time() - start
	print(i,time.time()-start)

def runtest(j, tests):
	for i, t in enumerate(tests, 1):
		start = time.time()
		os.system(t+tail+' >> result'+str(i)+'.txt')
		print(i, time.time()-start)


if __name__ == '__main__':
	# for _ in range(10):
	# 	for dc in dc_commands:
	# 		p = Pool(test_time)
	# 		for i in range(test_time+1):
	# 			p.apply_async(rundc, args=(i,dc))
	# 		print("Start Running")
	# 		p.close()
	# 		p.join()
	# 		print("Done")

	p = Pool(test_time)
	for i in range(test_time+1):
		p.apply_async(runtest, args=(i,test_cpps))
	print("Start Running")
	p.close()
	p.join()
	print("Done")