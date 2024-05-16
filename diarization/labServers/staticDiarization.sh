GPU_NUM=$1
for i in $(seq 1 80000); 
do 
    time bash diarizeOne.sh $GPU_NUM 
    echo $i
done
