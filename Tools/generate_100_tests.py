import os
from multiprocessing import Pool
import time
command1 = "python3 /home/yutil15/Checkers_ShallowBlue/Tools/AI_Runner.py 7 7 2 l /home/yutil15/Checkers_ShallowBlue/src/checkers-python/main.py /home/yutil15/Checkers_ShallowBlue/Tools/Sample_AIs/Poor_AI_368/main.py | tail -n 1"
commandsecond1 = "python3 /home/yutil15/Checkers_ShallowBlue/Tools/AI_Runner.py 7 7 2 l /home/yutil15/Checkers_ShallowBlue/Tools/Sample_AIs/Poor_AI_368/main.py /home/yutil15/Checkers_ShallowBlue/src/checkers-python/main.py | tail -n 1"


command2 = "python3 /home/yutil15/Checkers_ShallowBlue/Tools/AI_Runner.py 9 8 2 l /home/yutil15/Checkers_ShallowBlue/src/checkers-python/main.py /home/yutil15/Checkers_ShallowBlue/Tools/Sample_AIs/Poor_AI_368/main.py | tail -n 1"
command3 = "python3 /home/yutil15/Checkers_ShallowBlue/Tools/AI_Runner.py 7 7 2 l /home/yutil15/Checkers_ShallowBlue/src/checkers-python/main.py /home/yutil15/Checkers_ShallowBlue/Tools/Sample_AIs/Average_AI_368/main.py | tail -n 1"
test_time = 10

def run(i):
	start = time.time()
	os.system(command1)
	print(i,time.time()-start)

if __name__ == '__main__':
	p = Pool(test_time)
	for i in range(test_time+1):
		p.apply_async(run, args=(i,))
	print("Start Running")
	p.close()
	p.join()
	print("Done")
