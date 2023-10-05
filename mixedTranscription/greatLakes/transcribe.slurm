#!/bin/bash
# The interpreter used to execute the script

#“#SBATCH” directives that convey submission options:

#SBATCH --job-name=transcribe10parallel
#SBATCH --mail-user=blitt@umich.edu
#SBATCH --nodes=10
#SBATCH --ntasks-per-node=4
#SBATCH --mem-per-cpu=20g 
#SBATCH --time=00-2:00:00
#SBATCH --partition=standard
#SBATCH --output=/home/%u/%x-%j.log

# The application(s) to execute along with its input arguments and options:
conda activate transcribePodcasts 

#for conversion of audio formats 
module load ffmpeg/4.4.2

#bring in the relevant files, then transcribe 
#we just need a list of mp3 urls as input 
IN_FILE="/gpfs/accounts/jurgens_root/jurgens0/blitt/podcasts/links/premadeTransLinks10.txt" 
TRANS_PATH="~/projects/podcasts/mixedTranscription/greatLakes/transcribeOne.sh"

time parallel -v --joblog logs/10TEST_CPU.log -j10 -a $IN_FILE bash $TRANS_PATH "{}" 
