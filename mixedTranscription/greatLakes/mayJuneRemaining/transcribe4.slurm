#!/bin/bash
# The interpreter used to execute the script

#“#SBATCH” directives that convey submission options:

#SBATCH --job-name=transcribe10
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=8000m 
#SBATCH --time=90:00
#SBATCH --account=jurgens0
#SBATCH --partition=standard
#SBATCH --output=/scratch/jurgens_root/jurgens0/blitt/podcasts/transcriptionLogs/%u/%x-%j.log

# The application(s) to execute along with its input arguments and options:
conda activate transcribePodcasts 

for i in $(seq 1 4); 
do  
    bash /home/blitt/projects/podcasts/mixedTranscription/greatLakes/mayJuneRemaining/transcribeOne.sh 
done
