#!/bin/bash

# The application(s) to execute along with its input arguments and options:
module load conda 
#source /home/${USER}/.bashrc
conda activate transcribePodcasts 

#for conversion of audio formats 
module load ffmpeg/4.4.2

#bring in the relevant files, then transcribe 
#we just need a list of mp3 urls as input 
#IN_FILE="/gpfs/accounts/jurgens_root/jurgens0/blitt/podcasts/links/premadeTransLinks10.txt" 
#URL_PATH="/shared/3/projects/benlitterer/podcastData/mp3s/links/floydMonth/floydMonthLinks.txt"
#FINISHED_PATH="/shared/3/projects/benlitterer/podcastData/transcripts/floydMonth/finished.txt"
TRANS_PATH=~/projects/podcasts/mixedTranscription/labServers/forBowen/transcribeOne.sh

#time parallel -v --joblog logs/transcribe1_4_1.log -j1 -a $IN_FILE bash $TRANS_PATH "{}" 
for i in {1..14}:
do
    nice -3 bash $TRANS_PATH &
    sleep 3 
done
