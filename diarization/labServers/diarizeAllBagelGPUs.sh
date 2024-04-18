for i in $(seq 1 7); 
do 
    #bash dynamicDiarization.sh $i &
    bash staticDiarization.sh $i &
done