#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import datetime
import numpy as np
import pytz
import time
import csv
import importlib

#load in the metadata dataframe 
colNames = ["epTitle", "epDescription", "duration", "pubDate", "copyright", "itunes:type", 
           "itunes:complete", "guid", "itunes:explicit", "enclosure","itunes:image", "transDict"]

#this *appears* to be loading correctly 
META_PATH= "/shared/3/projects/benlitterer/podcastData/podRss/floydFeeds/floydMetadata.csv"
metaDf = pd.read_csv(META_PATH, names=colNames).reset_index(names=["rssUrl"])

POD_PATH = "/shared/3/projects/benlitterer/podcastData/podcastIndex/floydSubset.csv"
podDf = pd.read_csv(POD_PATH, index_col=0).drop(columns=["Unnamed: 0"]).rename(columns={"url":"rssUrl", "description":"podDescription"})

LOG_PATH = "/home/blitt/projects/podcasts/mergeTransMetadata/logs/mergeTransMetadata/Jan2_2024.txt"
logFile = open(LOG_PATH, "w") 
logFile.write(f"shape of RSS scraped metadata: {metaDf.shape}\n")
logFile.write(f"shape of podcastIndex metadata: {podDf.shape}\n")
logFile.flush()

#merge the metadata onto the podcast episode data 
merged = pd.merge(metaDf, podDf, on=["rssUrl"], how="left")

logFile.write(f"shape of data merged on rssUrl: {merged.shape}\n") 
logFile.flush()

def parseTime(inStr, inFormat):
    try: 
        return datetime.datetime.strptime(inStr, inFormat)

        return pd.to_datetime(inStr, format=inFormat).tz_localize(None)
    except Exception as E:
        #print(E)
        return np.nan

#get just the english first to save time
merged = merged.dropna(subset=["language"])
logFile.write(f"shape of data without NA's in language column: {merged.shape}\n") 

merged = merged[merged["language"].str.lower().str.contains('en')]
logFile.write(f"shape of data with only English: {merged.shape}\n") 

# clean date using only one format, leaving NaTs for unmatched format 
# tz_localize(None) means that our times are local to the places that they originated 
merged['date_formats_with_offset'] = merged["pubDate"].apply(parseTime, inFormat="%a, %d %b %Y %H:%M:%S %z")
merged["date_formats_without_offset"] = merged["pubDate"].apply(parseTime, inFormat="%a, %d %b %Y %H:%M:%S %Z") 
merged["cleanDates"] = merged['date_formats_with_offset'].fillna(merged["date_formats_without_offset"])

logFile.write(f"finished date formatting\n") 

naDates = sum(merged["cleanDates"].isna())
logFile.write(f"# of date NA values: {naDates}\n")
logFile.flush()

#TODO: find appropriate cleaning to do at this step 
#get function to give transcript file path of urls
spec=importlib.util.spec_from_file_location("getURLstorageLocation","/home/blitt/projects/podcasts/mergeTransMetadata/getURLstorageLocation.py")
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)

#get path to transcripts for each url 
#we will have to add META_PATH later, since we could be sending output to different plcaes 
META_PATH= ""
merged = merged.dropna(subset=["enclosure"])
logFile.write(f"shape of data after removing NA urls: {merged.shape}\n") 

merged["potentialOutPath"] = merged["enclosure"].apply(foo.getUrlTranscriptPath, args=[META_PATH])
logFile.flush()

#keep only non-NA dates 
merged = merged.dropna(subset=["cleanDates"]) 
logFile.write(f"shape after removing cleanDate NA values: {merged.shape}\n") 

merged = merged.drop(columns=['date_formats_with_offset', 'date_formats_without_offset'])

#send dates to utc 
merged["cleanDatesLoc"] = pd.to_datetime(merged["cleanDates"], utc=True, errors="coerce")
logFile.write(f"forcing clean dates to UTC format (no offset assumes +00:00)\n") 

logFile.write(f"writing merged file to disk\n") 
merged.to_csv("/shared/3/projects/benlitterer/podcastData/processed/mergedMetaDataClean.csv", quoting=csv.QUOTE_NONNUMERIC)
logFile.flush()

#subset week before the month surrounding George Floyd's Death 
firstCutoff = pd.to_datetime("05-03-2020", format="%m-%d-%Y", utc=True)
lastCutoff = pd.to_datetime("05-09-2020", format="%m-%d-%Y", utc=True)

beforeFMonth = merged[(merged["cleanDatesLoc"] >= firstCutoff) & (merged["cleanDatesLoc"] <= lastCutoff)]
logFile.write(f"dates for beforeFMonth are [05-03-2020, 05-09-2020], inclusive\n") 
logFile.write(f"writing week before Floyd Month file to disk\n") 
logFile.flush()
beforeFMonth.to_csv("/shared/3/projects/benlitterer/podcastData/processed/beforeFloydMonth/beforeFMonth.tsv", quoting=csv.QUOTE_NONNUMERIC)

#get the four weeks surrounding George Floyd's Death 
#two weeks before was Monday, May 11, 2020
#two weeks after was Monday, June 8, 2020
logFile.write(f"dates for Floyd Month are [05-11-2020, 06-08-2020], inclusive\n") 
logFile.write(f"writing Floyd Month file to disk\n") 
logFile.flush()

#specify month surrounding George Floyd's murder 
firstCutoff = pd.to_datetime("05-11-2020", format="%m-%d-%Y", utc=True)
lastCutoff = pd.to_datetime("06-08-2020", format="%m-%d-%Y", utc=True)

#subset to time period 
floydMonths = merged[(merged["cleanDatesLoc"] >= firstCutoff) & (merged["cleanDatesLoc"] <= lastCutoff)]

floydMonths.to_csv("/shared/3/projects/benlitterer/podcastData/processed/floydMonth/floydMonthEnSHORT.csv", quoting=csv.QUOTE_NONNUMERIC)
logFile.write("finished") 
logFile.close()