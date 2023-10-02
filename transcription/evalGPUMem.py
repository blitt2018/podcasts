import subprocess as sp
import os
import time

#because of an error with one of the gpus, we can only 
#get memory for some of them 
def get_gpu_memory():
    memDict = {}
    for i in range(4): 
        command = f"nvidia-smi --id={i} --query-gpu=memory.free --format=csv"
        try: 
            memory_free_info = sp.check_output(command.split()).decode('ascii').split('\n')[:-1][1:]
            memory_free_values = [int(x.split()[0]) for i, x in enumerate(memory_free_info)]
            memDict[i] = memory_free_values[0]
        except: 
            pass 



    
    return memDict 

#keep getting the gpu with the most available memory 
#if this gpu has enough memory to support our job, then we return its number 
MEM_REQUIRED = 4000 
SLEEP_TIME = 30
total_free = 0
while total_free < MEM_REQUIRED: 
    memDict = get_gpu_memory()
    for i, cFree in memDict.items(): 
        if cFree > total_free: 
            total_free = cFree
            gpuNum = i

    #we only wait if we don't have enough mem. 
    if total_free < MEM_REQUIRED: 
        time.sleep(SLEEP_TIME)
    
print(gpuNum) 
