import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import re
import numpy as np
from tqdm import tqdm 

#~20 minutes to load everything 
#meta data for floyd month (change this to the mayJune metadata eventually)
metaDf = pd.read_csv("/shared/3/projects/benlitterer/podcastData/processed/floydMonth/floydMonthEn.csv", lineterminator="\n")

#load in the entities for the full transcripts 
transcriptEnts = pd.read_csv("/shared/3/projects/benlitterer/podcastData/NER/transcripts/transcriptNEs.csv", sep="\t", names=["potentialOutPath", "ent", "start", "end", "type"], lineterminator="\n")

#episode description entities 
epDescEnts = pd.read_csv("/shared/3/projects/benlitterer/podcastData/NER/epDescriptions/epDescriptionNEs.csv", sep="\t", names=["potentialOutPath", "ent", "start", "end", "type"], lineterminator="\n")

#pod description entities 
descEntDf = pd.read_csv("/shared/3/projects/benlitterer/podcastData/NER/podDescriptions/floydMonthNEs.tsv", sep="\t",
                        names=["potentialOutPath", "ent", "start", "end", "type"], lineterminator="\n")

#transcripts that we have so far 
transcriptDf = pd.read_csv("/shared/3/projects/benlitterer/podcastData/processed/floydMonth/allTranscripts.tsv", sep="\t", names=["potentialOutPath", "transcript"], lineterminator="\n")

print(f"transcript df shape:{transcriptDf.shape}") 
transDups = transcriptDf[transcriptDf.duplicated(subset=["potentialOutPath"], keep=False)]

#remove the /shared/3/... outPath beginning
transcriptDf["potentialOutPath"] = transcriptDf["potentialOutPath"].apply(lambda x: x[67:])

print(f"number of duplicated outpaths: {len(transDups)}")

scriptDups = transcriptDf[transcriptDf.duplicated(subset=["transcript"], keep=False)]

#what is the length of these duplicate transcripts 
scriptDups["scriptLen"] = scriptDups["transcript"].apply(lambda x: len(x.split()))

#do we have any NaN or None values in the transcripts or outPaths? 
#drop duplicates in transcript df
#note that this removes duplicates on the (outPath, transcript) columns
#which ones we keep doesn't matter because they're perfect duplicates of eachother
transcriptDf = transcriptDf.drop_duplicates(keep="first")

#only one row!? 
#and no NaN values for potentialOutPath
print(transcriptDf[transcriptDf["transcript"].isna()].shape)
print(transcriptDf[transcriptDf["potentialOutPath"].isna()].shape) 

#drop the na's (one row atm) 
transcriptDf = transcriptDf.dropna()

#are there transcripts that are too short? 
transcriptDf["wCount"] = transcriptDf["transcript"].apply(lambda x: len(x.split()))

print(f'average word count: {np.mean(transcriptDf["wCount"])}') 
print(f'median word count: {np.median(transcriptDf["wCount"])}') 
print(f'total word count: {sum(transcriptDf["wCount"])}')

#do we have transcripts that have no real content?
#we had about 5,800 transcripts with word counts under or equal to 10
print(transcriptDf[transcriptDf["wCount"] > 10].shape)

#duplicates on potentialOutPath in metadata
print(metaDf[metaDf.duplicated(subset=["potentialOutPath"], keep=False)].shape) 

#drop duplicates on potential out path 
metaDf = metaDf.drop_duplicates(subset=["potentialOutPath"], keep="first")

#for parsing the metadata durations 
def parseDurations(inDuration): 
    #if na value, just return na value 
    if inDuration != inDuration: 
        return inDuration 
    
    inDuration = str(inDuration)
    inDuration = re.sub("[A-z]", "", inDuration)
    colonCount = inDuration.count(":")
    
    try: 
        
        #parse different strings into number of seconds 
        if colonCount == 0: 
            return int(inDuration)

        elif colonCount == 1: 
            mins, seconds = [int(item) for item in inDuration.split(":")]
            return (60*mins) + seconds 

        elif colonCount == 2: 
            hours, mins, seconds = [int(item) for item in inDuration.split(":")]
            return (hours*60*60) + (mins*60) + seconds
        else: 
            return np.nan
    except: 
        return np.nan

""" 
We have a very small (like 300) number of podcasts that are over 10 hours. 
No discernable reason why, so we must assume a data entry error... 
"""

#now parse durations
metaDf["parsedDuration"] = metaDf["duration"].apply(parseDurations) 

#2% of the values parsed are na 
print(np.mean(metaDf["parsedDuration"].isna()))

metaDf["hours"] = metaDf["parsedDuration"] / (60 * 60) 

#merge transcripts and metadata
#keeping only the metadata for which we have transcripts 
df = pd.merge(transcriptDf, metaDf, on="potentialOutPath", how="left") 
df.shape

#three entity Dfs 
#transcriptEnts, epDescEnts, descEntDf

"""
sampling entDf and descEntDf, they both seem fine... 
we do get duplicates though, which is odd. I assume this comes from 
reading the same file twice when running NER? didn't drop duplicates before doing NER potentially?

entDf dups -> 150,000
desEntDf dups -> 40,000 
(both are tiny fractions of all entities extracted) 
"""
sum(transcriptEnts.duplicated()) 
sum(epDescEnts.duplicated())
sum(descEntDf.duplicated())

transcriptEnts = transcriptEnts.drop_duplicates() 
epDescEnts = epDescEnts.drop_duplicates() 
descEntDf = descEntDf.drop_duplicates() 

#add the entities in, but first check on duplicates 
transcriptEnts = transcriptEnts.groupby(by="potentialOutPath").agg(list)
transcriptEnts = transcriptEnts.reset_index() 
transcriptEnts = transcriptEnts.rename(columns={"ent":"transEnts", "start":"transStarts", "end":"transEnds", "type":"transTypes"})

#correct potentialOutPath to get rid of /shared/3/... prefix
transcriptEnts["potentialOutPath"] = transcriptEnts["potentialOutPath"].apply(lambda x: x[67:])
df = pd.merge(df, transcriptEnts, on="potentialOutPath", how="left") 

#group and merge description entities
descEntDf = descEntDf.groupby(by="potentialOutPath").agg(list)
descEntDf = descEntDf.reset_index() 
descEntDf = descEntDf.rename(columns={"ent":"descEnts", "start":"descStarts", "end":"descEnds", "type":"descTypes"})
df = pd.merge(df, descEntDf, on="potentialOutPath", how="left") 

#group and merge episode description entities 
epDescEnts= epDescEnts.groupby(by="potentialOutPath").agg(list)
epDescEnts = epDescEnts.reset_index() 
epDescEnts = epDescEnts.rename(columns={"ent":"epDescEnts", "start":"epDescStarts", "end":"epDescEnds", "type":"epDescTypes"})
df = pd.merge(df, epDescEnts, on="potentialOutPath", how="left") 

df = df.drop(columns=['Unnamed: 0']) 

print(f"shape after merging:{df.shape}")
"""
We have some duplicates on the outPaths and these are not all identical in terms of
the (outPath, transcript) pair 
"""

def cleanQuotes(inStr): 
    if inStr != inStr: 
        return inStr 
    outStr = re.sub('(?<!")"(?!")', ',',inStr) 
    return re.sub('"""', '"', outStr)[8:]


outList = []
for i, row in tqdm(df.iterrows()): 
    outList.append(cleanQuotes(row["transcript"]))

df["transcript"] = outList

print(f"writing dataframe with shape:{df.shape}")
#write output file 

#df.to_json("/shared/3/projects/benlitterer/podcastData/floydMonthData.jsonl", orient="records", lines=True)
df.to_json("/shared/4/projects/podcasts/processed/floydMonthData.jsonl", orient="records", lines=True)