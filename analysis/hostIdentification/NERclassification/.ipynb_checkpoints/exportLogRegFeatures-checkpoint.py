import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
import json
import numpy as np

IN_PATH = "/shared/3/projects/benlitterer/podcastData/processed/floydMonth/floydMonthData.jsonl"
#with open(IN_PATH) as f:
#    df = pd.DataFrame(json.loads(line) for line in f)
    
df = pd.read_json("/shared/3/projects/benlitterer/podcastData/processed/floydMonth/floydMonthData.jsonl", orient="records", lines=True)

print(df.shape) 

df = df[["potentialOutPath", "rssUrl", "transcript", "epTitle", "epDescription", "itunesAuthor", "title", "popularityScore", "episodeCount", "podDescription", "cleanDatesLoc", '500ent', '500start', '500end', '500type', 'DescEnt',
       'DescStart', 'DescEnd', 'DescType']]

#we want to use the frequency of entities in the transcripts and the descriptions to make a prediction 
#so first check out the frequency of entities in the transcript beginnings? 
print("getting transcript features") 
transcriptEnts = df[["rssUrl", "500ent","500type"]]
transcriptEnts = transcriptEnts.explode(["500ent", "500type"]) 
transcriptEnts = transcriptEnts[transcriptEnts["500type"] == "PERSON"]

#get podMentions, the # of mentions of a given ent across episodes of a podcast 
transcriptEnts = transcriptEnts.groupby(by=["rssUrl", "500ent"]).agg(len).reset_index().rename(columns={"500type":"podMentions"}) 
transcriptEnts = transcriptEnts.sort_values("podMentions", ascending=False)


#get totalPodMentions, the total entity mentions in this podcast across all episodes 
transcriptEnts = transcriptEnts.groupby(by=["rssUrl"]).agg(list) 
transcriptEnts["totalPodMentions"] = transcriptEnts["podMentions"].apply(sum) 
transcriptEnts = transcriptEnts.explode(["500ent", "podMentions"]) 

#get totalEntMentions, the total number of mentions of this entity across all podcasts 
transcriptEnts = transcriptEnts.reset_index().groupby(by=["500ent"]).agg(list)
transcriptEnts["totalEntMentions"] = transcriptEnts["totalPodMentions"].apply(sum)
transcriptEnts = transcriptEnts.explode(["rssUrl", "podMentions", "totalPodMentions"])
transcriptEnts = transcriptEnts.reset_index()

#now look at unique mentions within transcripts 
transcriptUnique = df[["rssUrl", "potentialOutPath", "500ent","500type"]]
transcriptUnique = transcriptUnique.explode(["500ent", "500type"])
transcriptUnique = transcriptUnique[transcriptUnique["500type"] == "PERSON"]

print("getting unique entity features") 
#we only want one mention of each entity per episode 
transcriptUnique = transcriptUnique.drop_duplicates(subset=["potentialOutPath", "500ent"])  
transcriptUnique = transcriptUnique.groupby(by=["rssUrl", "500ent"]).agg(list).reset_index()

#transcriptUnique["uniquePodMentions"] = transcriptUnique["rssUrl"]
transcriptUnique["uniquePodMentions"] = transcriptUnique["potentialOutPath"].apply(len)
transcriptUnique = transcriptUnique.drop(columns=["500type", "potentialOutPath"])

print("merging transcript entity counts") 
#get total number of episodes for podcasts 
#after removing same podcast duplicates on unique podcast key
podEpisodes = pd.DataFrame(df.drop_duplicates(subset=["rssUrl", "potentialOutPath"])["rssUrl"].value_counts()).rename(columns={"count":"podEpisodes"})
podEpisodes = podEpisodes.reset_index() 

entDf = pd.merge(transcriptEnts, transcriptUnique, on=["rssUrl", "500ent"], how="inner")
entDf = pd.merge(entDf, podEpisodes, on = "rssUrl", how="inner") 
entDf = entDf.rename(columns={"500ent":"ent"}) 

print("getting description level features") 
#just get one podcast description per podcast 
descDf = df[["rssUrl", "DescEnt", "DescType"]].drop_duplicates(subset=["rssUrl"]).explode(["DescEnt", "DescType"])
descDf = descDf[descDf["DescType"] == "PERSON"].groupby(by=["rssUrl", "DescEnt"]).agg(len).reset_index().rename(columns={"DescEnt":"ent", "DescType":"DescMentions"}) 
descDf.head()

print("merging description level features") 
#merge whether the podcast description mentions this entity into our entity information df 
entDf = pd.merge(entDf, descDf, on=["rssUrl", "ent"], how="left")
entDf["DescMentions"] = entDf["DescMentions"].fillna(0) 

print("getting transcript snippets") 
def getSnippet(inRow): 
    BUFFER = 80
    left = inRow["500start"] - BUFFER
    left = left if left > 0 else 0
    
    right = inRow["500end"] + BUFFER
    right = right if right < len(inRow["transcript"]) else len(inRow["transcript"]) 

    return inRow["transcript"][left:right]

snippetDf = df[["potentialOutPath", "rssUrl", "transcript", "500start", "500end", "500ent", "500type",  "itunesAuthor", "podDescription"]].explode(["500start", "500end", "500ent", "500type"]).dropna()  
snippetDf = snippetDf[snippetDf["500type"] == "PERSON"]
snippetDf["entContext"] = snippetDf.apply(getSnippet, axis=1)
snippetDf = snippetDf.dropna(subset=["transcript"])
snippetDf["transcript"] = snippetDf["transcript"].apply(lambda x: x[:700]) 
snippetDf = snippetDf.rename(columns={"500start":"entStart", "500end":"entEnd", "500ent":"ent", "500type":"type"})
snippetDf.head() 

print("merging transcript features") 
entDf = pd.merge(snippetDf, entDf, on=["rssUrl", "ent"])  

print("getting itunesAuthor matches") 
def cleanAuthors(inStr): 
    #clean up spacing discrepancies
    inStr = " ".join(inStr.split())
    return inStr

def getAuthorMatches(inRow): 
    authors = inRow["itunesAuthor"].split("&")
    authors = [cleanAuthors(author).lower() for author in authors]
    entGuess = cleanAuthors(inRow["ent"]).lower()
    return entGuess in authors 

#figure out when we have an exact match between an entity in NER and the author field 
#helpful for quickly finding ground truth 
entDf["itunesMatch"] = entDf.apply(getAuthorMatches, axis=1) 

print("calculating useful LR features") 
#now add some extra features which will be useful for our logistic regression 
entDf["fracOfPodEntities"] = entDf["podMentions"] / entDf["totalPodMentions"]
entDf["fracOfAllMentions"] = entDf["podMentions"] / entDf["totalEntMentions"]
entDf["propOfEpisodeMentions"] = entDf["uniquePodMentions"] / entDf["podEpisodes"] 

print(entDf.shape) 

entDf.to_json("/shared/3/projects/benlitterer/podcastData/hostIdentification/logisticRegression/allEntityFeatures.jsonl", orient="records", lines=True) 