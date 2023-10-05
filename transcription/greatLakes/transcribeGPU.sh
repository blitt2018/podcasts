#bring in the relevant files, then transcribe 
#we just need a list of mp3 urls as input 
IN_FILE="/shared/3/projects/benlitterer/podcastData/mp3s/links/premadeTransLinks100.txt"
TRANS_PATH="~/projects/testing/podcasts/transcription/transcribeOneGPU.sh"
#parallel 1000testCORRECT.log -j40 -a $IN_FILE bash $TRANS_PATH "{}" 
parallel --dryrun --joblog GPUtestLog.log -j10 -a $IN_FILE bash $TRANS_PATH "{}" 
