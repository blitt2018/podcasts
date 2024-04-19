#the goal is to download a file, transcribe it, then delete it in one file 
#we then run this file in parallel!

#since  this is the cpu version, make gpus inaccessable 
#export CUDA_VISIBLE_DEVICES=$1

#TODO: change 
STORAGE_DIR=/scratch/jurgens_root/jurgens0/blitt
MP3_LOC=$STORAGE_DIR/podcasts/mp3s/diarization
URL_KEY_PATH=~/projects/podcasts/transcription/greatLakes/cleanURL.py
PYANNOTE_PATH=~/projects/podcasts/mixedTranscription/greatLakes/pyAnnote.py
DIARIZE_PATH=$STORAGE_DIR/podcasts/diarization/premadeTransDiarized
GET_URL_PATH=/home/blitt/projects/podcasts/mixedTranscription/greatLakes/getNextURL.py

#this searches the urls to find the first one 
#that hasn't been written to the finshed file
inURL=`python3 $GET_URL_PATH $1 $2`
kURL=`python3 $URL_KEY_PATH $inURL`

#echo "downloading" 
#download the file to MP3 location
curl -L $inURL --output $MP3_LOC/$kURL

#echo "converting"
#forcibly overwrite using the -y flag
#turn that file into .wav format
ffmpeg -y -i $MP3_LOC/$kURL -ar 16000 -ac 1 -c:a pcm_s16le $MP3_LOC/$kURL.wav

echo "removing mp3"
#delete the mp3
rm $MP3_LOC/$kURL

#echo "diarizing"
python3 $PYANNOTE_PATH $MP3_LOC/$kURL.wav $DIARIZE_PATH/$kURL.rttm

#echo "removing wav"
#delete the wav
rm $MP3_LOC/$kURL.wav
