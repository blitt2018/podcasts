#!/bin/bash

# The application(s) to execute along with its input arguments and options:
module load conda 
#source /home/${USER}/.bashrc
conda activate transcribePodcasts 

#for conversion of audio formats 
module load ffmpeg/4.4.2

#path to a script which runs the script that does all of the transcription 
TRANS_PATH=~/projects/podcasts/mixedTranscription/labServers/mayJuneRemaining/transcribeOneWrapper.sh

#time parallel -v --joblog logs/transcribe1_4_1.log -j1 -a $IN_FILE bash $TRANS_PATH "{}" 
for i in {1..16}:
do
    nice -19 bash $TRANS_PATH &   
    #bash $TRANS_PATH &   
    
    sleep 3 
done
