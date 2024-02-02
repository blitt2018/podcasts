import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import re
from tqdm import tqdm

#load in data 
metaDf = pd.read_csv("/shared/3/projects/benlitterer/podcastData/processed/floydMonth/floydMonthEn.csv",lineterminator="\n")
entDf = pd.read_csv("/shared/3/projects/benlitterer/podcastData/NER/podIntroductions/floydMonth500wordNEs.csv", names=["potentialOutPath", "ent", "start", "end", "type"], lineterminator="\n")
descEntDf = pd.read_csv("/shared/3/projects/benlitterer/podcastData/NER/podDescriptions/floydMonthNEs.tsv", sep="\t",
                        names=["potentialOutPath", "ent", "start", "end", "type"], lineterminator="\n")
transcriptDf = pd.read_csv("/shared/3/projects/benlitterer/podcastData/processed/floydMonth/allTranscripts.tsv", sep="\t", names=["potentialOutPath", "transcript"], lineterminator="\n")

#de-duplicate rows in metadata 
metaDf = metaDf.drop_duplicates(subset=["potentialOutPath"]) 
transcriptDf = transcriptDf.drop_duplicates(subset=["potentialOutPath"])

#first merge 
metaDf["potentialOutPath"] = "/shared/3/projects/benlitterer/podcastData/prosodyMerged/floydMonth" + metaDf["potentialOutPath"]
df = pd.merge(transcriptDf, metaDf, on="potentialOutPath", how="left") 

#add the entities in, but first check on duplicates 
entDf = entDf.groupby(by="potentialOutPath").agg(list)
entDf = entDf.reset_index() 

#second merge 
df = pd.merge(df, entDf, on="potentialOutPath", how="left") 

#get entities from descriptions formatted 
descEntDf = descEntDf.groupby(by="potentialOutPath").agg(list)
descEntDf = descEntDf.reset_index() 

#make this the full path 
descEntDf["potentialOutPath"] = "/shared/3/projects/benlitterer/podcastData/prosodyMerged/floydMonth" + descEntDf["potentialOutPath"]

#clean up column names
df = df.rename(columns={"ent":"500ent", "start":"500start", "end":"500end", "type":"500type"})
df = df.drop(columns=['Unnamed: 0']) 

#final merge (description entities) 
df = pd.merge(df, descEntDf, on="potentialOutPath", how="left") 
df = df.rename(columns={"ent":"DescEnt", "start":"DescStart", "end":"DescEnd", "type":"DescType"})

#now clean up the transcripts a bit 
def cleanQuotes(inStr): 
    if inStr != inStr: 
        return inStr 
    outStr = re.sub('(?<!")"(?!")', ',',inStr) 
    return re.sub('"""', '"', outStr)[8:]

outList = []
for i, row in tqdm(df.iterrows()): 
    outList.append(cleanQuotes(row["transcript"]))
    
df["transcript"] = outList

#output as json lines 
df.to_json("/shared/3/projects/benlitterer/podcastData/processed/floydMonth/floydMonthData.json]l", orient="records", lines=True)