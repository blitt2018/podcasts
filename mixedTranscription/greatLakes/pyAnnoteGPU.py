import torch
from pyannote.audio import Pipeline
import sys

#we control which gpu is used 
#by setting it's visibility in bash script calling this script
device = torch.device("cuda")
device = "cuda" if torch.cuda.is_available() else "cpu" 
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1",use_auth_token="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").to(device) 

print(device)

FILE_PATH=sys.argv[1]
OUT_PATH=sys.argv[2]

# apply the pipeline to an audio file
diarization = pipeline(FILE_PATH)

# dump the diarization output to disk using RTTM format
with open(OUT_PATH, "w") as rttm:
    diarization.write_rttm(rttm)
