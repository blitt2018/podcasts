#bring in the relevant files, then transcribe 
#we just need a list of mp3 urls as input 
IN_FILE="/shared/3/projects/benlitterer/podcastData/mp3s/links/premadeTransLinks100.txt"
DIARIZE_PATH="~/projects/testing/podcasts/mixedTranscription/diarizeOne.sh"

#parallel -v --joblog logs/100CPU.log -j1 -a $IN_FILE bash $DIARIZE_PATH "{}" 
#parallel -v --joblog logs/100CPU.log -j1 -a $IN_FILE bash $DIARIZE_PATH "{}" 
time parallel -v --joblog logs/100DiarizeGPU.log -j3 -a $IN_FILE bash $DIARIZE_PATH 0 "{}" 
