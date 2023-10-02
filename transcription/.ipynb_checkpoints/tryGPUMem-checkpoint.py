import subprocess as sp
import os

def get_gpu_memory():
    command = "nvidia-smi --query-gpu=memory.free --format=csv"
    memory_free_info = sp.check_output(command.split()).decode('ascii').split('\n')[:-1][1:]
    memory_free_values = [int(x.split()[0]) for i, x in enumerate(memory_free_info)]
    
    #command = "nvidia-smi --query-gpu=memory.total --format=csv"
    return memory_free_values

#keep getting the gpu with the most available memory 
#if this gpu has enough memory to support our job, then we return its number 
MEM_REQUIRED = 20000
SLEEP_TIME = 30
total_free = 0
while total_free < MEM_REQUIRED: 
    free_mem = get_gpu_memory()
    for i, cFree in enumerate(free_mem): 
        if cFree > total_free: 
            total_free = cFree
            gpuNum = i

    #we only wait if we don't have enough mem. 
    if total_free < MEM_REQUIRED: 
        time.sleep(SLEEP_TIME)
    
print(gpuNum) 
