for i in {1..100}: 
do
    sleep 10
    sbatch transcribe.slurm 
done 
