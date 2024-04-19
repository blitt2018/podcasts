#!/bin/bash
# The interpreter used to execute the script

#“#SBATCH” directives that convey submission options:

#SBATCH --job-name=transcribe5
#SBATCH --mail-user=blitt@umich.edu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=3g 
#SBATCH --time=00-3:00:00
#SBATCH --partition=standard
#SBATCH --output=/home/blitt/projects/podcasts/mixedTranscription/greatLakes/logs/%x-%j.log

# The application(s) to execute along with its input arguments and options:
module load conda 
source /home/${USER}/.bashrc
conda activate transcribePodcasts 

#for conversion of audio formats 
module load ffmpeg/4.4.2

#bring in the relevant files, then transcribe 
#we just need a list of mp3 urls as input 
#IN_FILE="/gpfs/accounts/jurgens_root/jurgens0/blitt/podcasts/links/premadeTransLinks10.txt" 
URL_PATH="/gpfs/accounts/jurgens_root/jurgens0/blitt/podcasts/links/premadeTransLinks1000.txt"
FINISHED_PATH="/gpfs/accounts/jurgens_root/jurgens0/blitt/podcasts/transcripts/finished/premadeTranscripts.txt"
TRANS_PATH=~/projects/podcasts/mixedTranscription/greatLakes/transcribeOne.sh

#time parallel -v --joblog logs/transcribe1_4_1.log -j1 -a $IN_FILE bash $TRANS_PATH "{}" 
for i in {1..2}:
do
    bash $TRANS_PATH $URL_PATH $FINISHED_PATH
done
