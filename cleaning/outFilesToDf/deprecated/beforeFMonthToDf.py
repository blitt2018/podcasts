import pandas as pd
import os
from tqdm import tqdm
from multiprocessing import Pool 
import numpy as np

#this is where our stems will be written to 
OUT_STEM = "/shared/3/projects/benlitterer/podcastData/intermediary/beforeFMonth/splitsFromParallel/fullTextSplit"

#read in file telling us where to look for finished transcripts 
print("reading file") 
df = pd.read_csv("/shared/3/projects/benlitterer/podcastData/processed/beforeFloydMonth/beforeFMonth.tsv") 

print("finding existing paths") 
df["potentialOutPathFull"] = "/shared/3/projects/benlitterer/podcastData/prosodyMerged/beforeFMonth" + df["potentialOutPath"] 
df["exists"] = df["potentialOutPathFull"].apply(lambda x: os.path.exists(x)) 
df = df[df["exists"] == True]

#split up df
print("splitting dataframe") 
dfList = np.array_split(df, 12)

def outputDataFile(i): 
    currDf = dfList[i]
    OUT_PATH = f"{OUT_STEM}{i}.tsv"
    with open(OUT_PATH, "w") as outFile: 
        for path in tqdm(currDf["potentialOutPathFull"]): 
            with open(path) as currFile: 
                fullText =  "".join([row.split(",")[4] for row in currFile.readlines()])
                firstBit = fullText.replace("\t", "").replace("\n", "") 
                outFile.write(f"{path}\t{firstBit}\n")

#writing csvs in parallel 
print("writing csv's in parallel") 
pool = Pool(processes=12)
pool.map(outputDataFile, list(range(12)))