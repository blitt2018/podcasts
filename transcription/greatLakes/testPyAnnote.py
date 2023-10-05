import torch
from pyannote.audio import Pipeline
device = torch.device("cpu") 
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",use_auth_token="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").to(device) 


FILE_PATH="/shared/3/projects/benlitterer/podcastData/mp3s/testRound/httpsaudio1.redcircle.comepisodes3c3e73af49ff41a29d84f83c51a6de9dstream.mp3.wav"
OUT_PATH="/shared/3/projects/benlitterer/podcastData/transcripts/premadeTransTranscripts/testPyannote.rttm"

# apply the pipeline to an audio file
diarization = pipeline(FILE_PATH)

# dump the diarization output to disk using RTTM format
with open(OUT_PATH, "w") as rttm:
    diarization.write_rttm(rttm)
