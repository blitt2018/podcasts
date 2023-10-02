#WHISPER_GPU_PATH="/home/blitt/projects/testing/podcasts/openai-whisper-cpu/whisper/whisper"
#TEST_PATH="/shared/3/projects/benlitterer/podcastData/mp3s/testRound/httpsdts.podtrac.comredirect.mp3api.spreaker.comdownloadepisode56597897romanos_99.mp3.wav"
#IN_STEM="/shared/4/projects/podcasts/"
MP3_LOC="/shared/3/projects/benlitterer/podcastData/mp3s/testRound"
WHISPER_PATH="/shared/4/projects/podcasts/whisper.cpp"
MODEL_NAME="ggml-small.en.bin"
TRANSCRIPTS_PATH="/shared/3/projects/benlitterer/podcastData/transcripts/premadeTransTranscripts"
PROSODY_PATH="/shared/3/projects/benlitterer/podcastData/prosody/premadeTransProsody"
OPENSMILE_PATH="/home/blitt/projects/testing/podcasts/transcription/extractProsodicFeatures.py"
URL_KEY_PATH="/home/blitt/projects/testing/podcasts/transcription/cleanURL.py"
GPU_SCRIPT_PATH="/home/blitt/projects/testing/podcasts/transcription/evalGPUMem.py" 
DIARIZE_PATH="/shared/3/projects/benlitterer/podcastData/diarization/premadeTransDiarized"
PYANNOTE_PATH="/home/blitt/projects/testing/podcasts/transcription/pyAnnoteGPU.py"

inURL=$1
kURL=`python3 $URL_KEY_PATH $inURL`
#outName=${inURL//[\/\$]/}

#echo "downloading" 
#download the file to MP3 location
#wget -O $MP3_LOC/$kURL $inURL
curl -L $inURL --output $MP3_LOC/$kURL

#echo "converting" 
#turn that file into .wav format 
#NOTE: to shorten, use -t number_of_seconds
ffmpeg -i $MP3_LOC/$kURL -t 1200 -ar 16000 -ac 1 -c:a pcm_s16le $MP3_LOC/$kURL.wav

echo "removing mp3" 
#delete the mp3
rm $MP3_LOC/$kURL

#export CUDA_VISIBLE_DEVICES=5

#get the gpu with the most available memory 
#AND, wait if we don't have enough memory on the gpu
gpu=`python3 $GPU_SCRIPT_PATH`  
#gpu=$2
gpuStr=cuda:"$gpu"
echo $gpuStr

echo "transcribing" 
#transcribe the file
#$WHISPER_PATH/main -osrt -p 1 -t 1  -m $WHISPER_PATH/models/$MODEL_NAME -f $MP3_LOC/$kURL.wav -of $TRANSCRIPTS_PATH/$kURL
/home/blitt/.local/bin/whisper $MP3_LOC/$kURL.wav --device $gpuStr --model base.en --output_dir $TRANSCRIPTS_PATH/$kURL

#echo "diarizing"
python3 $PYANNOTE_PATH $MP3_LOC/$kURL.wav $DIARIZE_PATH/$kURL.rttm

python3 $OPENSMILE_PATH $MP3_LOC/$kURL.wav $PROSODY_PATH/$kURL

#echo "removing wav" 
#delete the wav
rm $MP3_LOC/$kURL.wav
