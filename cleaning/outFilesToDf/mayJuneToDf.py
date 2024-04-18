# %%

import pandas as pd
import os
from tqdm import tqdm
from multiprocessing import Pool 
import numpy as np


#stem where we put output files 
OUT_STEM = "/shared/3/projects/benlitterer/podcastData/intermediary/beforeFMonth/splitsFromParallel/fullTextSplit"

#read in metadata 
df = pd.read_json("/shared/3/projects/benlitterer/podcastData/processed/mayJune/mayJuneMetadata.jsonl", orient="records", lines=True)

print(df.shape)

#get column for whether files exist 
def fileExists(fPath): 
    STEM_1 = "/shared/3/projects/benlitterer/podcastData/prosodyMerged/floydMonth"
    STEM_2 = "/shared/3/projects/benlitterer/podcastData/prosodyMerged/5_4_5_10"
    STEM_3 = "/shared/3/projects/benlitterer/podcastData/prosodyMerged/6_9_6_15"
    STEM_4 = "/shared/3/projects/benlitterer/podcastData/prosodyMerged/mayJuneRemaining"
    stemList = [STEM_1, STEM_2, STEM_3, STEM_4]
    for stem in stemList: 
        potPath = stem + fPath
        if os.path.exists(potPath): 
            return potPath 
    return "" 

#get the place we need to look for the file 
df["fullPotPath"] = df["potentialOutPath"].apply(fileExists)
df = df[df["fullPotPath"] != ""]
print(df.shape)
potPathDf = df[["fullPotPath"]]
dfList = np.array_split(potPathDf, 12)

#go through a list of files, read the transcript information, and write the transcript to a single file 
def outputDataFile(i): 
    currDf = dfList[i]
    OUT_PATH = f"{OUT_STEM}{i}.tsv"
    with open(OUT_PATH, "w") as outFile: 
        if i == 0: 
            for path in tqdm(currDf["fullPotPath"]): 
                with open(path) as currFile: 
                    fullText =  "".join([row.split(",")[4] for row in currFile.readlines()])

                    #remove tabs and all types of newlines 
                    fullText = fullText.replace("\t", "")
                    fullText = " ".join(fullText.splitlines())
                    
                    outFile.write(f"{path}\t{fullText}\n")
        else: 
            for path in currDf["fullPotPath"]: 
                with open(path) as currFile: 
                    fullText =  "".join([row.split(",")[4] for row in currFile.readlines()])

                    #remove tabs and all types of newlines 
                    fullText = fullText.replace("\t", "")
                    fullText = " ".join(fullText.splitlines())
                    
                    outFile.write(f"{path}\t{fullText}\n")


#map the task to 12 seperate processes 
pool = Pool(processes=12)
pool.map(outputDataFile, list(range(12)))
