import pandas as pd
import requests as req
from bs4 import BeautifulSoup
import re
import time
from tqdm import tqdm
from datetime import datetime
import os
import sys
import atexit 
import random 

# https://github.com/Podcast-Standards-Project/PSP-1-Podcast-RSS-Specification

def getMP3Links(rssLink): 
    
    try:
        #get the xml for the rss feed   
        response = req.get(rssLink)
        resCode = response.status_code
        rssText = response.text
    
    #if we have an exception related to our request, return an empty list
    except req.exceptions.RequestException as e:  
        print("request error")
        return []
    
    #print output if we get a bad code 
    if resCode != 200: 
        print(f"bad code {resCode} from {rssLink}")
        
    try: 
        #parse the xml 
        rssSoup = BeautifulSoup(rssText, features="xml")
    except: 
        print("xml error")
        return []
    
    items = rssSoup.find_all("item")
    
    forText = ["title", "description", "itunes:duration", "pubDate", "copyright", "itunes:type", "itunes:complete", "guid", "itunes:explicit"]
    forUrl = ["enclosure","itunes:image"]
    
    outList = []
    for item in items: 
        currList = []
        for tag in forText: 
            tagHit = item.find(tag)
            if tagHit != None: 
                currList.append(tagHit.get_text())
            else: 
                currList.append("")
                
        for tag in forUrl:  
            tagHit = item.find(tag)
            if tagHit != None: 
                currList.append(tagHit.get("url"))
            else: 
                currList.append("")
        
        #this might get a little whack when we have to read in the file later
        #but our data isn't that big so should hopefully work out 
        transDict = {}
        for transcript in item.find_all("podcast:transcript"): 
            transType = transcript.get("type")
            transType = transType if transType != None else ""
            
            transLang = transcript.get("language")
            transLang = transLang if transLang != None else ""
            
            transUrl = transcript.get("url")
            
            if transUrl != None: 
                transDict[transUrl] = [transType, transLang]
        
        currList.append(transDict)
        outList.append(currList)
    
    return outList

#load in our RSS data
cols = ["queryName", "title", "url", "originalUrl", "description", "author", "language", \
          "categories", "explicit", "episodeCount"]

#testing 
#IN_FILE = "/shared/3/projects/benlitterer/podcastData/podRss/TESTRSSFeeds.csv"
IN_FILE = sys.argv[1]

rssDf = pd.read_csv(IN_FILE, names=cols)

#we want to write to a file that way we can keep our results as we call the api 

#testing: 
#OUT_FILE = "/shared/3/projects/benlitterer/podcastData/mp3s/RssMp3s.csv"
OUT_FILE = sys.argv[2]

def exit_handler():
    if os.path.exists(OUT_FILE): 
        outHandle.close()

atexit.register(exit_handler)

"""
podLevel = ["podName", "rssUrl"]
forText = ["epTitle", "description", "itunes:duration", "pubDate"]
forUrl = ["enclosure","podcast:transcript"] 
OUT_COLS = podLevel + forText + forUrl
"""

OUT_COLS = ["rssUrl", "title", "description", "itunes:duration", "pubDate", "copyright", \
            "itunes:type", "itunes:complete", "guid", "itunes:explicit", "enclosure","itunes:image", "transDict"]


#a set of url's to query for rss feeds 
toProcess = set(rssDf["url"])

#we want to either write a new file, or append 
#to a file we've already written 
if os.path.exists(OUT_FILE): 
    outHandle = open(OUT_FILE, "a+")
    
    #IF the file exists, we want to decide where to start searching and appending 
    outDf = pd.read_csv(OUT_FILE, names=OUT_COLS)
    
    #get what we've written to output file
    #rssUrl will be our unique key for each feed 
    #randomize ordering 
    processed = set(outDf["rssUrl"].sample(len(outDf)))
    
    #update what needs to be processed according to what we've already done 
    toProcess = toProcess - processed 
    print(f"{len(processed)} already processed")
else: 
    outHandle = open(OUT_FILE, "w+")
    
print(f"processing {len(toProcess)} rss feeds")

TOTAL_WAIT = float(sys.argv[3]) 

hostDict = {}
podList = []
for url in tqdm(toProcess): 
    
    #get the host 
    host = url.strip("https://").split("/")[0]
    
    #find out how long it's been since we last scraped this host
    #and update the time at which we are scraping this host 
    if host in hostDict: 
        
        #time since we last called this host 
        timeLag = datetime.now() - hostDict[host]
        timeLag = timeLag.seconds 
        
        #current time now 
        hostDict[host] =  datetime.now()
    
    else: 
        #set when we called this host
        hostDict[host] = datetime.now()
        timeLag = TOTAL_WAIT 
        
    #our remaining wait is the total wait - how much we've already waited 
    rWait = TOTAL_WAIT - timeLag
    
    if rWait > 0: 
        time.sleep(rWait + (random.random() / 10))
    
    #get the mp3 links for this page 
    podInfs = getMP3Links(url)
    
    for podInf in podInfs: 
        outList = [url] + podInf
        outStr = '","'.join([str(item).replace('"', '\'').replace("\n", "") for item in outList])
        outStr = f'"{outStr}"'
        outHandle.write(outStr + "\n")
    
    if len(podInfs) == 0: 
        outStr = '","'.join('' for item in range(len(OUT_COLS)-1))
        outStr = f'"{url}","{outStr}"'
        outHandle.write(outStr + "\n") 
        
    outHandle.flush()