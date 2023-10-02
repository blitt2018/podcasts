#bring in the relevant files, then transcribe 
#we just need a list of mp3 urls as input 
IN_FILE="/shared/3/projects/benlitterer/podcastData/mp3s/links/premadeTransLinks.txt"
TRANS_PATH="~/projects/testing/podcasts/transcription/transcribeOne.sh"
parallel -P 20 -a $IN_FILE bash $TRANS_PATH 