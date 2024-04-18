import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool 
import seaborn as sns

#take in the merged json file with all of the data, clean the transcripts, and re-write
df = pd.read_json("/shared/4/projects/podcasts/processed/floydMonthData.jsonl", orient="records", lines=True)

def getGrams(inStr, gramLen=4): 
    wordList = inStr.split()
    numWords = len(wordList)
    gramList = []
    gramDict = {}
    gramCount = 0
    maxCount = 0
    maxGram = ""
    for i, word in enumerate(wordList): 
        
        j = i + gramLen

        #if we have enough words left, append the gram
        if j < numWords: 
            
            gram = " ".join(list(wordList[i:j])).lower()
            
            
            if gram not in gramDict: 
                gramDict[gram] = 1
            else: 
                gramDict[gram] += 1

            #if this is the new most common gram, update
            currGramCount = gramDict[gram]
            if currGramCount > maxCount: 
                maxCount = currGramCount
                maxGram = gram
            
            gramCount += 1

    return [gramCount, maxCount, maxGram]
    


def getGramsWrapper(tup): 
    i, indices=tup
    currDf = df.iloc[indices]
    gramOutput = currDf["transcript"].apply(getGrams)
    return gramOutput

# %%
N_SPLITS=15
indexList = np.array_split(np.array(list(range(0, len(df)))), N_SPLITS)
zippedIndices = list(zip(list(range(0, N_SPLITS)), indexList))

# %%
with Pool(N_SPLITS) as p: 
    outFrames = p.map(getGramsWrapper, zippedIndices)

# %%
catOut= np.concatenate(outFrames)
gramDf = pd.DataFrame.from_records(catOut) 

# %%
gramDf.columns = ["totalGramCount", "topGramCount", "topGram"]

# %%
df = pd.concat([df, gramDf], axis=1)

# %%
df = df[df["topGramCount"] > 0]

# %%
df["gramFrac"] = df["topGramCount"] / df["totalGramCount"]


THRESHOLD=.05
overThresh = np.mean(df["gramFrac"] > THRESHOLD)
print(f"proportion of transcript over cleaning threshold:{overThresh}")

# %%
#seems like 5% is a decent cutoff? 
cleanDf = df[df["gramFrac"] < THRESHOLD]

# %%
test = cleanDf.sample(3000)

# %%
cleanDf.shape

# %%
df.shape

# %%
cleanDf.to_json("/shared/3/projects/benlitterer/podcastData/processed/floydMonth/floydMonthDataClean.jsonl", orient="records", lines=True)


