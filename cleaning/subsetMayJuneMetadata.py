import pandas as pd
import csv
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm
from collections import Counter

#read in huge amount of metadata 
df = pd.read_csv("/shared/3/projects/benlitterer/podcastData/processed/mergedMetaDataClean.csv", quoting=csv.QUOTE_NONNUMERIC)

#get dates in the right format 
df["cleanDatesLoc"] = pd.to_datetime(df["cleanDatesLoc"])

#subset to the dates we want 
df = df[(df["cleanDatesLoc"] >= "2020-5-1") & (df["cleanDatesLoc"] <= "2020-6-30")]

#write the data 
df.to_json("/shared/3/projects/benlitterer/podcastData/processed/mayJune/mayJuneMetadata.jsonl", orient="records", lines=True)