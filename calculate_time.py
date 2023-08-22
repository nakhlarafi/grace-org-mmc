import re

# After all subprocesses are complete
training_times = []
testing_times = []

# Read the timing data from the file
with open(f'{pp}_timing_data.txt', 'r') as f:
    lines = f.readlines()

    for line in lines:
        match = re.search(r"TIMING_INFO: Training Time: (\d+.\d+), Testing Time: (\d+.\d+)", line)
        if match:
            training_times.append(float(match.group(1)))
            testing_times.append(float(match.group(2)))

# Calculate the total training and testing time
total_training_time = sum(training_times)
total_testing_time = sum(testing_times)

print(f"The overall training time is {total_training_time} seconds.")
print(f"The overall testing time is {total_testing_time} seconds.")