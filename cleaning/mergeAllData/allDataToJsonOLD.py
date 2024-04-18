#!/usr/bin/env python
# coding: utf-8



import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import re
import numpy as np



metaDf = pd.read_csv("/shared/3/projects/benlitterer/podcastData/processed/floydMonth/floydMonthEn.csv", lineterminator="\n")

entDf = pd.read_csv("/shared/3/projects/benlitterer/podcastData/NER/podIntroductions/floydMonth500wordNEs.csv", names=["potentialOutPath", "ent", "start", "end", "type"], lineterminator="\n")

descEntDf = pd.read_csv("/shared/3/projects/benlitterer/podcastData/NER/podDescriptions/floydMonthNEs.tsv", sep="\t",
                        names=["potentialOutPath", "ent", "start", "end", "type"], lineterminator="\n")

introDf = pd.read_csv("/shared/3/projects/benlitterer/podcastData/NER/floydIntroductions.tsv", sep="\t", names=["potentialOutPath", "first500"]) 

transcriptDf = pd.read_csv("/shared/3/projects/benlitterer/podcastData/processed/floydMonth/allTranscripts.tsv", sep="\t", names=["potentialOutPath", "transcript"], lineterminator="\n")


"""
random info
we have 828 gb of data in transcripts + prosodic information right now
"""


# ## Clean Each Dataframe


transcriptDf.shape

transDups = transcriptDf[transcriptDf.duplicated(subset=["potentialOutPath"], keep=False)]


"""
out of the 601,207 transcripts, 18,124 of the paths are duplicates.
(that's 3.01%), but only half of those get dropped 

not exactly sure where these come from is the thing... 
"""


#this shows that they're all exact duplicates on both the outpath and the transcript
print(transDups[transDups.duplicated(keep=False)].sort_values("potentialOutPath").shape)
print(transDups.shape)

scriptDups = transcriptDf[transcriptDf.duplicated(subset=["transcript"], keep=False)]


"""
Duplicated transcripts.. 
we have 53,211 transcripts that are duplicates, which is 8.85%
we only need to remove half of these which gives 4.425% that are removed \

about one third of the duplicates are very short 

from qualitative review of dups we are getting some amount of music-only and blank audio, which could have something
to do with this problem 

i.e. "content [silence]" or "content [music]" 
"""


#what is the length of these duplicate transcripts 
scriptDups["scriptLen"] = scriptDups["transcript"].apply(lambda x: len(x.split()))


print(scriptDups.shape)
sns.ecdfplot(data=scriptDups, x="scriptLen")

#drop duplicates in transcript df
#note that this removes duplicates on the (outPath, transcript) columns
#which ones we keep doesn't matter because they're perfect duplicates of eachother
transcriptDf = transcriptDf.drop_duplicates(keep="first")

#do we have any NaN or None values in the transcripts or outPaths? 
#only one row!? 
#and no NaN values for potentialOutPath
print(transcriptDf[transcriptDf["transcript"].isna()].shape)
print(transcriptDf[transcriptDf["potentialOutPath"].isna()].shape) 

#no "None" values 
transcriptDf[transcriptDf["transcript"] == None]
transcriptDf[transcriptDf["potentialOutPath"] == None]

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
transcriptDf = transcriptDf[transcriptDf["wCount"] > 10]


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
np.mean(metaDf["parsedDuration"].isna()) 


metaDf["hours"] = metaDf["parsedDuration"] / (60 * 60) 


longPods = metaDf.loc[metaDf["hours"] > 10]
longPods[["duration", "parsedDuration"]]


#longPods[["epTitle"]]


sns.ecdfplot(data=metaDf[metaDf["hours"] < (10)], x="hours")
plt.title("(all) podcast durations ecdf")


metaDf["potentialOutPath"] = "/shared/3/projects/benlitterer/podcastData/prosodyMerged/floydMonth" + metaDf["potentialOutPath"]

df = pd.merge(transcriptDf, metaDf, on="potentialOutPath", how="left") 


"""
sampling entDf and descEntDf, they both seem fine... 
we do get duplicates though, which is odd. I assume this comes from 
reading the same file twice when running NER? didn't drop duplicates before doing NER potentially?

entDf dups -> 150,000
desEntDf dups -> 40,000 
(both are tiny fractions of all entities extracted) 
"""
sum(entDf.duplicated()) 
sum(descEntDf.duplicated())

entDf = entDf.drop_duplicates() 
descEntDf = descEntDf.drop_duplicates() 


#add the entities in, but first check on duplicates 
entDf = entDf.groupby(by="potentialOutPath").agg(list)
entDf = entDf.reset_index() 

df = pd.merge(df, entDf, on="potentialOutPath", how="left") 

descEntDf = descEntDf.groupby(by="potentialOutPath").agg(list)
descEntDf = descEntDf.reset_index() 

descEntDf["potentialOutPath"] = "/shared/3/projects/benlitterer/podcastData/prosodyMerged/floydMonth" + descEntDf["potentialOutPath"]

#check for duplicates on the indices of descEntDf and entDf
#all good!
sum(entDf["potentialOutPath"].duplicated())
sum(descEntDf["potentialOutPath"].duplicated())

df = df.rename(columns={"ent":"500ent", "start":"500start", "end":"500end", "type":"500type"})

df = df.drop(columns=['Unnamed: 0']) 

df = pd.merge(df, descEntDf, on="potentialOutPath", how="left") 

df = df.rename(columns={"ent":"DescEnt", "start":"DescStart", "end":"DescEnd", "type":"DescType"})

#validating that we have as many rows in our dataframe as we do transcripts that we've processed 
df.shape

"""
We have some duplicates on the outPaths and these are not all identical in terms of
the (outPath, transcript) pair 
"""

#get David's stuff 
print(sum(df.dropna(subset=["hours"])["hours"]))
print(np.mean(df.dropna(subset=["hours"])["hours"]))
print(np.median(df.dropna(subset=["hours"])["hours"]))

min(df["cleanDates"]) 

max(df["cleanDates"]) 


259438 * 60


#number of episodes 
len(df["rssUrl"].unique())


df.shape


sns.ecdfplot(data=df, x="hours")
plt.title("ecdf: duration of collected podcasts") 


#now merge in the first 500 words that we got the entities from 
introDups = introDf[introDf.duplicated(subset=["potentialOutPath"], keep=False)]


print(introDups.shape) 
print(sum(introDups.duplicated())) 

introDf = introDf.drop_duplicates(subset=["potentialOutPath"]) 


df = pd.merge(df, introDf, on ="potentialOutPath", how="left") 


def cleanQuotes(inStr): 
    if inStr != inStr: 
        return inStr 
    outStr = re.sub('(?<!")"(?!")', ',',inStr) 
    return re.sub('"""', '"', outStr)

from tqdm import tqdm


outList = []
for i, row in tqdm(df.iterrows()): 
    outList.append(cleanQuotes(row["transcript"])[8:])


df["transcript"] = outList

df.to_json("/shared/3/projects/benlitterer/podcastData/processed/floydMonth/floydMonthData.jsonl", orient="records", lines=True)

