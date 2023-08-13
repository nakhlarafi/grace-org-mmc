import subprocess
from tqdm import tqdm
import time
import os, sys
import pickle
project = sys.argv[1]
card = [0]
lst = list(range(len(pickle.load(open(project + '.pkl', 'rb')))))
singlenums = {'Time':5, 'Math':2, "Lang":10, "Chart":3, "Mockito":4, "Closure":1}
singlenum = singlenums[project]
totalnum = len(card) * singlenum
lr = 1e-2
seed = 0
batch_size = 60

total_training_time_across_all_iterations = 0
total_testing_time_across_all_iterations = 0

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
        stdout, _ = p.communicate()
        for line in stdout.decode('utf-8').strip().split("\n"):
            if line.startswith("TRAIN_TIME"):
                train_time, test_time = line.split(":")[1].split(",")
                train_time = float(train_time.strip())
                test_time = float(test_time.strip())
                total_training_time_across_all_iterations += train_time
                total_testing_time_across_all_iterations += test_time


p = subprocess.Popen("python3 sum.py %s %d %f %d"%(project, seed, lr, batch_size), shell=True)
p.wait()
subprocess.Popen("python3 watch.py %s %d %f %d"%(project, seed, lr, batch_size),shell=True)       

print(f"Total training time across all iterations: {total_training_time_across_all_iterations} seconds")
print(f"Total testing time across all iterations: {total_testing_time_across_all_iterations} seconds")