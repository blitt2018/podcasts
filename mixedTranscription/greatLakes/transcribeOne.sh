#the goal is to download a file, transcribe it, then delete it in one file 
#we then run this file in parallel!

STORAGE_DIR=/scratch/jurgens_root/jurgens0/blitt
MP3_LOC=$STORAGE_DIR/podcasts/mp3s/transcription
WHISPER_PATH=~/projects/podcasts/whisper.cpp
MODEL_NAME="ggml-base.en.bin"
TRANSCRIPTS_PATH=$STORAGE_DIR/podcasts/transcripts/premadeTransTranscripts
PROSODY_PATH=$STORAGE_DIR/podcasts/prosody/premadeTransProsody
OPENSMILE_PATH=~/projects/podcasts/transcription/greatLakes/extractProsodicFeatures.py
URL_KEY_PATH=~/projects/podcasts/transcription/greatLakes/cleanURL.py
GET_URL_PATH=/home/blitt/projects/podcasts/mixedTranscription/greatLakes/getNextURL.py

#this searches the urls to find the first one 
#that hasn't been written to the finshed file
inURL=`python3 $GET_URL_PATH $1 $2`
kURL=`python3 $URL_KEY_PATH $inURL`
#outName=${inURL//[\/\$]/}

#echo "downloading" 
#download the file to MP3 location
curl -L $inURL --output $MP3_LOC/$kURL

#echo "converting" 
#forcibly overwrite using the -y flag 
#turn that file into .wav format 
ffmpeg -y -i $MP3_LOC/$kURL -ar 16000 -ac 1 -c:a pcm_s16le $MP3_LOC/$kURL.wav

#echo "removing mp3" 
#delete the mp3
rm $MP3_LOC/$kURL

#echo "transcribing" 
#transcribe the file
$WHISPER_PATH/main -osrt -p 1 -t 1 -ml 1 -m $WHISPER_PATH/models/$MODEL_NAME -f $MP3_LOC/$kURL.wav -of $TRANSCRIPTS_PATH/$kURL

#echo "prosody" 
python3 $OPENSMILE_PATH $MP3_LOC/$kURL.wav $PROSODY_PATH/$kURL


#echo "removing wav" 
#delete the wav
rm $MP3_LOC/$kURL.wav
