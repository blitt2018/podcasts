GPU_NUM=$1
for i in $(seq 1 30000); 
do 
    time bash diarizeOne.sh $GPU_NUM 
    echo $i
done
