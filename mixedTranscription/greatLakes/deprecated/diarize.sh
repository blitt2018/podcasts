#!/bin/bash
# The interpreter used to execute the script

#“#SBATCH” directives that convey submission options:

#SBATCH --job-name=diarize2_8
#SBATCH --mail-user=blitt@umich.edu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --mem-per-cpu=10g 
#SBATCH --time=00-8:00:00
#SBATCH --partition=standard
#SBATCH --output=/home/blitt/projects/podcasts/mixedTranscription/greatLakes/logs/%x-%j.log

# The application(s) to execute along with its input arguments and options:
conda activate transcribePodcasts 

#for conversion of audio formats 
module load ffmpeg/4.4.2

#bring in the relevant files, then transcribe 
#we just need a list of mp3 urls as input 
#STORAGE_DIR="/gpfs/accounts/jurgens_root/jurgens0/blitt"
#IN_FILE=$STORAGE_DIR"/podcasts/links/premadeTransLinks10.txt"
URL_PATH="/gpfs/accounts/jurgens_root/jurgens0/blitt/podcasts/links/premadeTransLinks1000.txt"
FINISHED_PATH="/gpfs/accounts/jurgens_root/jurgens0/blitt/podcasts/diarization/finished/premadeTranscripts.txt"
DIARIZE_PATH=~/projects/podcasts/mixedTranscription/greatLakes/diarizeOne.sh


#time parallel -v --joblog logs/diarize1_20_10.log -j10 -a $IN_FILE bash $DIARIZE_PATH "{}" 
for i in {1..2}:
do
    time bash $DIARIZE_PATH $URL_PATH $FINISHED_PATH
done

