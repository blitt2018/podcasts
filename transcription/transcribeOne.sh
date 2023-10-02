#the goal is to download a file, transcribe it, then delete it in one file 
#we then run this file in parallel!

#since  this is the cpu version, make gpus unaccessable 
export CUDA_VISIBLE_DEVICES=""

#IN_STEM="/shared/4/projects/podcasts/"
MP3_LOC="/shared/3/projects/benlitterer/podcastData/mp3s/testRound"
WHISPER_PATH="/shared/4/projects/podcasts/whisper.cpp"
MODEL_NAME="ggml-base.en.bin"
TRANSCRIPTS_PATH="/shared/3/projects/benlitterer/podcastData/transcripts/premadeTransTranscripts"
PROSODY_PATH="/shared/3/projects/benlitterer/podcastData/prosody/premadeTransProsody"
OPENSMILE_PATH="/home/blitt/projects/testing/podcasts/transcription/extractProsodicFeatures.py"
URL_KEY_PATH="/home/blitt/projects/testing/podcasts/transcription/cleanURL.py"
PYANNOTE_PATH="/home/blitt/projects/testing/podcasts/transcription/pyAnnoteCPU.py"
DIARIZE_PATH="/shared/3/projects/benlitterer/podcastData/diarization/premadeTransDiarized"

inURL=$1
kURL=`python3 $URL_KEY_PATH $inURL`
#outName=${inURL//[\/\$]/}

#echo "downloading" 
#download the file to MP3 location
#wget -O $MP3_LOC/$kURL $inURL
curl -L $inURL --output $MP3_LOC/$kURL

#echo "converting" 
#forcibly overwrite using the -y flag 
#turn that file into .wav format 
ffmpeg -y -i $MP3_LOC/$kURL -t 60 -ar 16000 -ac 1 -c:a pcm_s16le $MP3_LOC/$kURL.wav

echo "removing mp3" 
#delete the mp3
rm $MP3_LOC/$kURL

#echo "transcribing" 
#transcribe the file
#$WHISPER_PATH/main -osrt -p 1 -t 1  -m $WHISPER_PATH/models/$MODEL_NAME -f $MP3_LOC/$kURL.wav -of $TRANSCRIPTS_PATH/$kURL

#echo "prosody" 
#python3 $OPENSMILE_PATH $MP3_LOC/$kURL.wav $PROSODY_PATH/$kURL

#echo "diarizing" 
python3 $PYANNOTE_PATH $MP3_LOC/$kURL.wav $DIARIZE_PATH/$kURL.rttm

#echo "removing wav" 
#delete the wav
rm $MP3_LOC/$kURL.wav
