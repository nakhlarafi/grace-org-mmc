import subprocess
from tqdm import tqdm
import time
import os, sys
import pickle
project = sys.argv[1]
card = [0]
lst = list(range(len(pickle.load(open(project + '.pkl', 'rb')))))
singlenums = {'Time':5, 'Math':2, "Lang":10, "Chart":3, "Mockito":4, "Closure":1, "Codec":1, 'Compress':1, 'Gson':1}
singlenum = singlenums[project]
totalnum = len(card) * singlenum
lr = 1e-2
seed = 0
batch_size = 60


for i in tqdm(range(int(len(lst) / totalnum) + 1)):
    jobs = []
    for j in range(totalnum):
        if totalnum * i + j >= len(lst):
            continue
        cardn =int(j / singlenum)
        p = subprocess.Popen("CUDA_VISIBLE_DEVICES="+str(card[cardn]) + " python3 run.py %d %s %f %d %d"%(lst[totalnum * i + j], project, lr, seed, batch_size), shell=True)
        jobs.append(p)
        time.sleep(10)
    for p in jobs:
        p.wait()
        # stdout, _ = p.communicate()
        # stdout = stdout.decode('utf-8').strip()
        # timing_info = re.search(r"TIMING_INFO: Training Time: (\d+.\d+), Testing Time: (\d+.\d+)", stdout)
        # if timing_info:
        #     train_time, test_time = map(float, timing_info.groups())
        #     total_training_time += train_time
        #     total_testing_time += test_time



p = subprocess.Popen("python3 sum.py %s %d %f %d"%(project, seed, lr, batch_size), shell=True)
p.wait()
subprocess.Popen("python3 watch.py %s %d %f %d"%(project, seed, lr, batch_size),shell=True)       

# print(f"The overall training time is {total_training_time} seconds.")
# print(f"The overall testing time is {total_testing_time} seconds.")