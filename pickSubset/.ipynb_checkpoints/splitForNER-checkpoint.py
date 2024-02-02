"""
This script splits our data into peices so that NER can be run in parallel 
"""
import pandas as pd
import spacy
import numpy as np
from collections import Counter
import csv
from multiprocessing import Pool 

#OLD: inFile = "/shared/3/projects/benlitterer/localNews/mergedNewsData/dataSplits/splitNews27"
inFile = "/shared/3/projects/benlitterer/podcastData/analysis/allEpisodes.csv"
newsDf = pd.read_csv(inFile,  index_col=0, lineterminator='\n')

#only get English pods (to cut down on NER time)
newsDf["language"] = newsDf["language"].str.lower()
newsDf = newsDf.dropna(subset=["language"])
newsDf = newsDf[newsDf["language"].str.contains("en")]

sub_df = newsDf[['key', 'epDescription']]

#we use 160 because that's how many cores we have 
indexList = np.array_split(np.array(list(range(0, len(sub_df)))), 160)
zippedIndices = list(zip(list(range(0, 160)), indexList))

outStem = "/shared/3/projects/benlitterer/podcastData/NER/preSplits/dSplit"

#last file will be missing one row 
def writeFrame(tup):
    i, indices = tup
    outDf = sub_df.iloc[indices, :]
    outDf.to_csv(outStem + str(i), sep="\t", quoting=csv.QUOTE_NONNUMERIC)

with Pool(12) as p: 
    p.map(writeFrame, zippedIndices)