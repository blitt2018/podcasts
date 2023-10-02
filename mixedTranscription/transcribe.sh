#bring in the relevant files, then transcribe 
#we just need a list of mp3 urls as input 
IN_FILE="/shared/3/projects/benlitterer/podcastData/mp3s/links/premadeTransLinks100.txt"
TRANS_PATH="~/projects/testing/podcasts/mixedTranscription/transcribeOne.sh"
#parallel 1000testCORRECT.log -j40 -a $IN_FILE bash $TRANS_PATH "{}" 
time parallel -v --joblog logs/100CPU.log -j30 -a $IN_FILE bash $TRANS_PATH "{}" 
#xargs -a $IN_FILE -n 1 -P 10 bash $TRANS_PATH
