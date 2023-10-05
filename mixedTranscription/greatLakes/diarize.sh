#!/bin/bash
# The interpreter used to execute the script

#“#SBATCH” directives that convey submission options:

#SBATCH --job-name=transcribe10parallel
#SBATCH --mail-user=blitt@umich.edu
#SBATCH --nodes=10
#SBATCH --ntasks-per-node=2
#SBATCH --mem-per-cpu=5g 
#SBATCH --time=00-0:08:00
#SBATCH --partition=standard
#SBATCH --output=/home/blitt/projects/podcasts/mixedTranscription/greatLakes/logs/%x-%j.log

# The application(s) to execute along with its input arguments and options:
conda activate transcribePodcasts 

#for conversion of audio formats 
module load ffmpeg/4.4.2

#bring in the relevant files, then transcribe 
#we just need a list of mp3 urls as input 
STORAGE_DIR="/gpfs/accounts/jurgens_root/jurgens0/blitt"
IN_FILE=$STORAGE_DIR"/podcasts/links/premadeTransLinks10.txt"
DIARIZE_PATH="~/projects/podcasts/mixedTranscription/greatLakes/diarizeOne.sh"

#parallel -v --joblog logs/100CPU.log -j1 -a $IN_FILE bash $DIARIZE_PATH "{}" 
#parallel -v --joblog logs/100CPU.log -j1 -a $IN_FILE bash $DIARIZE_PATH "{}" 
time parallel -v --joblog logs/10DiarizeGPU.log -j10 -a $IN_FILE bash $DIARIZE_PATH "{}" 
