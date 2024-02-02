import pandas as pd
import random
import os
import sys
import requests 
from tqdm import tqdm 
import atexit
import numpy as np

IN_STEM = "/shared/4/projects/podcasts/transcripts/transcriptLinks/"
IN_PATH = IN_STEM + sys.argv[1]

OUT_STEM = "/shared/4/projects/podcasts/transcripts/transcriptTexts/" 
OUT_PATH = OUT_STEM + sys.argv[1].replace("Links", "Texts")

colNames = []
inDf = pd.read_csv(IN_PATH, names=["index", "podUrl", "mp3Url", "transUrl", "type", "lang", "transHost"])
toProcess = set(inDf["transUrl"])
    
processed = set([])
if os.path.exists(OUT_PATH): 
    outHandle = open(OUT_PATH, "a+")
    outDf = pd.read_csv(OUT_PATH, names=["transUrl", "text"])
    
    processed = set(outDf["transUrl"])
    
else:
    outHandle = open(OUT_PATH, "w+")
    
toProcess = toProcess - processed 
print(f"processing {len(toProcess)} records")

def getTranscript(inUrl): 
    try: 
        response = requests.get(inUrl)
        code = response.status_code
        text = response.text
        return [code, text]
    except: 
        print("request error")
        return [None, None]
    
def exit_handler():
    if os.path.exists(OUT_PATH): 
        outHandle.close()
    print(f"{sys.argv[1]} finished")

atexit.register(exit_handler)

MIN_TIME = .1
waitTime = MIN_TIME
for i, transUrl in enumerate(toProcess): 
    
    if i % 300 == 0: 
        print(f"iteration {i} of file {sys.argv[1]}")
        
    #keep trying to rerequest if we get a bad code 
    while True: 
        code, text = getTranscript(transUrl)
        
        if code != 200: 
            print(f"non 200 code {code}")
            
        #keep requesting till we aren't being rate limited 
        if code != 429: 
            if waitTime > MIN_TIME: 
                waitTime = waitTime / 10
            break 
        
        #increase wait time if being rate limited 
        print("increasing time")
        waitTime = waitTime * 10
        
    if code == 200: 
        outStr = '"' + transUrl.replace('"', '') + '","' + text.replace('"', '') + '"\n'
        outHandle.write(outStr)
        
    #we still want to mark that this was processed 
    else: 
        outHandle.write('"",""\n')
    
    outHandle.flush()
    
outHandle.close()