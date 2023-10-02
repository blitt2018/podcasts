import torch
from pyannote.audio import Pipeline
import sys

device = torch.device("cpu") 
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1",use_auth_token="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").to(device) 


FILE_PATH=sys.argv[1]
OUT_PATH=sys.argv[2]

# apply the pipeline to an audio file
diarization = pipeline(FILE_PATH)

# dump the diarization output to disk using RTTM format
with open(OUT_PATH, "w") as rttm:
    diarization.write_rttm(rttm)
