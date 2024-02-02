"""
apply NER to just a single file (we run in parallel so we will have many files)
"""
import pandas as pd
import spacy
import numpy as np
from collections import Counter
import csv
from multiprocessing import Pool
import sys
import time
import re

inFile = "/shared/3/projects/benlitterer/podcastData/NER/preSplits/" + sys.argv[1]
#inFile = "/shared/3/projects/benlitterer/podcastData/NER/preSplits/dSplit" + "0"
inDf = pd.read_csv(inFile, sep="\t", index_col=0)

#remove rows with no description
inDf = inDf.dropna()

#remove xml/html tags
def cleanDescription(inStr): 
    return re.sub("<.*?>", "", inStr)

inDf["epDescription"] = inDf["epDescription"].apply(cleanDescription)

currTime = time.time()
contentList = list(inDf["epDescription"].astype(str))

nlp = spacy.load("en_core_web_md")
docs = nlp.pipe(contentList, batch_size=1, n_process=1)

NERList = []
for doc in docs:
    outList = [[ent.label_, ent.text] for ent in doc.ents]
    NERList.append(outList)

inDf["NE"] = NERList
inDf = inDf[["key", "NE"]]
inDf = inDf.explode("NE").dropna()
inDf[["type", "namedEnt"]] = inDf["NE"].tolist()
inDf = inDf[["key", "type", "namedEnt"]]

#extract number from in path, write to output path
fNumber = re.sub("[A-z]", "", sys.argv[1].split("/")[-1])
inDf.to_csv(sys.argv[2] + "NE" + fNumber + ".tsv" , sep="\t",  quoting=csv.QUOTE_NONNUMERIC)
