#the goal is to download a file, transcribe it, then delete it in one file 
#we then run this file in parallel!

#IN_STEM="/shared/4/projects/podcasts/"
MP3_LOC="/shared/3/projects/benlitterer/podcastData/mp3s/testRound"
WHISPER_PATH="/shared/4/projects/podcasts/whisper.cpp"
MODEL_NAME="ggml-base.en.bin"
TRANSCRIPTS_PATH="/shared/3/projects/benlitterer/podcastData/transcripts/premadeTransTranscripts"
PROSODY_PATH="/shared/3/projects/benlitterer/podcastData/prosody/premadeTransProsody"
OPENSMILE_PATH="/home/blitt/projects/testing/podcasts/transcription/extractProsodicFeatures.py"

inURL=$1
baseName=$(basename "$inURL")
#outName=${inURL//[\/\$]/}

#download the file to MP3 location
wget -O $MP3_LOC/$baseName $inURL

#turn that file into .wav format 
ffmpeg -i $MP3_LOC/$baseName -ar 16000 -ac 1 -c:a pcm_s16le $MP3_LOC/$baseName.wav

#delete the mp3
rm $MP3_LOC/$baseName

#transcribe the file
$WHISPER_PATH/main -osrt -p 2 -t 1 -m $WHISPER_PATH/models/$MODEL_NAME  -f $MP3_LOC/$baseName.wav -of $TRANSCRIPTS_PATH/$baseName

python3 $OPENSMILE_PATH $MP3_LOC/$baseName.wav $PROSODY_PATH/$baseName

#delete the wav
rm $MP3_LOC/$baseName.wav
