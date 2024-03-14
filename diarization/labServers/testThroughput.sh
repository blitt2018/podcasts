PYANNOTE_PATH=~/projects/podcasts/diarization/pyAnnoteGPU.py
STORAGE_DIR=/data/blitt/podcastData/mp3s/diarization/

F1=httpsmcdn.podbean.commfwebcjkfegHow_anxiety_affects_memory_99onh.mp3.wav
F2=httpsmcdn.podbean.commfweb33wqr8How_to_use_visualisation_to_improve_performance_7s4x1.mp3.wav
F3=httpsmcdn.podbean.commfwebx4sqihAnxiety_motivation_and_procrastination_bsma6.mp3.wav

time python3 $PYANNOTE_PATH 0 $STORAGE_DIR/$F1 /data/blitt/podcastData/random/diarize1.rttm & 
time python3 $PYANNOTE_PATH 1 $STORAGE_DIR/$F2 /data/blitt/podcastData/random/diarize2.rttm &
time python3 $PYANNOTE_PATH 2 $STORAGE_DIR/$F3 /data/blitt/podcastData/random/diarize3.rttm &