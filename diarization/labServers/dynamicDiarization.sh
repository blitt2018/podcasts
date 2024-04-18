GPU_NUM=$1
mem_buff=5500
count=0 

while (($count < 100)); 
do
    #check that over a period of XX seconds we have enough memory both times we check 
    free_count=0
    free_mem=$(nvidia-smi --query-gpu=memory.free --format=csv | sed ${GPU_NUM+3}'q;d' | grep -Eo [0-9]+)
    if (($free_mem > $mem_buff)); then
        free_count=$(($free_count+1))
    fi 

    #sleep
    sleep 30; 

    #second check 
    free_mem=$(nvidia-smi --query-gpu=memory.free --format=csv | sed ${GPU_NUM+3}'q;d' | grep -Eo [0-9]+)
    if (($free_mem > $mem_buff)); then
        free_count=$(($free_count+1))
    fi
    
    #run if space available 
    if (($free_count==2)); then
        echo "adding job"
        echo $GPU_NUM
        echo $free_mem
        echo $count;
        bash diarizeOne.sh $GPU_NUM &
        count=$(($count + 1)) 
    fi
done;

     
    