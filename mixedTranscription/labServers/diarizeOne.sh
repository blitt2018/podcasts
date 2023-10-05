#the goal is to download a file, transcribe it, then delete it in one file 
#we then run this file in parallel!

#since  this is the cpu version, make gpus unaccessable 
export CUDA_VISIBLE_DEVICES=$1

#IN_STEM="/shared/4/projects/podcasts/"
MP3_LOC="/shared/3/projects/benlitterer/podcastData/mp3s/diarization"
URL_KEY_PATH="/home/blitt/projects/testing/podcasts/transcription/cleanURL.py"
PYANNOTE_PATH="/home/blitt/projects/testing/podcasts/mixedTranscription/pyAnnoteGPU.py"
DIARIZE_PATH="/shared/3/projects/benlitterer/podcastData/diarization/premadeTransDiarized"

inURL=$2
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
