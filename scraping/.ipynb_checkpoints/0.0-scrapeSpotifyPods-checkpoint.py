#imports 
from bs4 import BeautifulSoup
import requests as req
from tqdm import tqdm 
import time
import pandas as pd
import base64
import random
import pickle
import os
import numpy as np
import atexit

clientId = "29eecbec66ab437a87aa008be0c6755e"
clientSecret = "4e7e3bd31b634a85981d3191e686409c"
clientCreds = f"{clientId}:{clientSecret}"
clientCredsB64 = base64.b64encode(clientCreds.encode())

#get token for api access during this session 
url = 'https://accounts.spotify.com/api/token'
tokenHeads = {"Authorization":f"Basic {clientCredsB64.decode()}"}
tokenParams = {"grant_type":"client_credentials"}

def getToken(): 
    tokResponse = req.post(url, data=tokenParams, headers=tokenHeads)
    tokData = tokResponse.json()
    token = tokData["access_token"]
    return token 

#now that we have our access token we can use the spotify api!
baseUrl = "https://api.spotify.com/"

#give search information, get the json object returned 
def searchPod(searchQ, inToken, limit=50, market="US", type_="show"): 
    headers = {"Authorization": f"Bearer {inToken}"}
    #format our url appropriately 
    fUrl = f'{baseUrl}v1/search?q={searchQ.replace(" ", "+")}&type={type_}&market={market}&limit={limit}'
    searchRes = req.get(fUrl, headers=headers)
    
    #return response code, dictionary of podcast information 
    return [searchRes.status_code, searchRes.json()]
    
MAX_HITS = 100

#set up an output file, if this file already exists, decide where to start searching from 
#we want to either write a new file, or append 
#to a file we've already written 
OUT_FILE =  "/shared/3/projects/benlitterer/podcastData/podNames/podinfo1hr.csv"
SEARCH_LIST = "/shared/3/projects/benlitterer/podcastData/podNames/hits1hr.csv"

#get the podcasts we've already searched an initialize searched 
if os.path.exists(OUT_FILE): 
    outHandle = open(OUT_FILE, "a+")
    
    #IF the file exists, we want to decide where to start searching and appending 
    #prevDf = pd.read_csv(OUT_FILE, names=OUT_COLS)
    colNames = ["searchName", "hitName", "type", "languages", "description", "is_externally_hosted", "total_episodes"]
    prevDf = pd.read_csv(OUT_FILE, names=colNames)
    
    #get all of the podcasts which have already been searched 
    #so we don't search them again 
    searched = set(prevDf["searchName"])
        
    
else: 
    outHandle = open(OUT_FILE, "w+")
    searched = set([]) 
    
#if we have a previous search set, use that
#if not, default to our seeds 
if os.path.exists(SEARCH_LIST): 
    #get the list of hits to keep searching 
    hits = pd.read_csv(SEARCH_LIST, names=["hitName"], index_col=False)
    hits = list(hits["hitName"])
    
    #but we only want the last X number of hits 
else: 
    hitsHandle = open(SEARCH_LIST, "w+")
    #if we don't have previous hits to use, 
    #seed with the top 20 podcasts on spotify 
    hits = ["Joe Rogan", 
            "The Really Good Podcast", 
            "Huberman Lab", 
            "anything goes with emma chamberlain", 
            "This Past Weekend", 
            "Crime Junkie", 
            "Smartless", 
            "Shawn Ryan Show", 
            "Scamanda", 
            "Call Her Daddy", 
            "PBD Podcast", 
            "Rotten Mango", 
            "Date Yourself Instead", 
            "Distractible", 
            "The Retrievals", 
            "The Daily", 
            "2 Bears, 1 Cave with Tom Segura & Bert Kreischer", 
            "Morbid", 
            "The Broski Report with Brittany Broski", 
            "The LOL Podcast"]

#we want to close our files on exit
def exit_handler():
    if os.path.exists(OUT_FILE): 
        outHandle.close()
        
    if os.path.exists(SEARCH_LIST):
        hitsHandle.close()

atexit.register(exit_handler)

#TODO: switch this over so that it writes to files rather than staying in memory 

#keep searching over and over exponentially 
#for each episode in hits, search that episode and add the results to the news version of hits 
#keep doing this, while ensuring that we don't search something we've already searched 

#the new hits at each level of search tree
#and all of our hits we've ever gotten 
newHits = []

#for printing reasons
counter = 0 

#for rate limit reasons...
waitTime = 2
MIN_WAIT = 2
goodCode = True

currToken = getToken()

while True: 
    #for each hit, we search 
    for hit in hits: 

        #don't search something we've already searched 
        #TODO: this gets slow as allHits grows 
        if hit not in searched: 

            #we break at the end of this while loop 
            #so long as we get a good response code from the spotify api 
            limitCount = 0 
            while True: 
                time.sleep(waitTime + random.random())
                #search the previous hit using spotify api 
                resCode, hitRes = searchPod(hit, currToken, limit=150)
                
                #only exit if we aren't being rate limited
                if resCode == 429:
                    
                    #increase wait time exponentially if being rate limited 
                    waitTime = waitTime **2
                    print(f"rate limited, wait time = {waitTime}")
            
                elif resCode == 401: 
                    currToken = getToken()
                    print(f"expired token, retrying with new one")
                    
                else: 
                    #just issue a warning if we hit a non 200 response code 
                    if resCode != 200: 
                        print(f"warning! exit code {resCode}")
                    
                    #lower our wait time if it's not at minimum 
                    if waitTime > MIN_WAIT: 
                        waitTime = np.sqrt(waitTime)
                        print(f"wait time = {waitTime}")
                    break 
                    
            searched.update(hit)
            outStr = ""
            #write hit information to file 
            if "shows" in hitRes: 

                #for each show returned from this search 
                for show in hitRes["shows"]["items"]: 

                    #we can get tripped up here if show is None
                    if show != None and show == show: 
                        keepList = ["name", "type", "languages", "description", "is_externally_hosted", "total_episodes"]

                        #if we have the field we want, add to outRow else blank space 
                        #we want to avoid double quotes in our file output as well 
                        outRow = []
                        for k in keepList: 
                            if k in show:
                                val = show[k]
                                if type(val) == list: 
                                    val = ",".join(val)
                                elif type(val) != str: 
                                    val = str(val)
                                    
                                val = val.replace('"', '')
                                outRow.append(val)
                            else: 
                                outRow.append("")
                        
                        #add the search podcast to our output 
                        outRow = [hit] + outRow

                        #the name of the search result podcast 
                        name = outRow[1].replace('"', '')
                        
                        #make outRow a string ready to be written to file 
                        outRow = '","'.join(outRow)
                        outRow = f'"{outRow}"\n'

                        #add the string with this row
                        #to the larger string we will write to output
                        outStr += outRow

                        #update lists of what we've searched and what we will search next 
                        #but only if we haven't already searched this podcast 
                        if name not in searched: 
                            newHits.append(name)
                            #allHits.update({name})

                #write string for podcast information to file 
                outHandle.write(outStr)
                
                #force the buffer to write to file
                outHandle.flush()
        
    #the hits we just got will be our new list to search
    #we will add the results from these new searches to newHits 
    #we also don't want our list of pods to search to get to large, 
    #so we prune out our list randomly as we go
    if len(newHits) > MAX_HITS: 
        hits = random.sample(newHits, MAX_HITS)
    else: 
        hits = newHits 
            
    #write our current hits list to output file 
    hitsHandle = open(SEARCH_LIST, "w+")
    hitsStr = '",\n"'.join(hits)
    hitsStr = f'"{hitsStr}"'
    hitsHandle.write(hitsStr)
    hitsHandle.close()
    #for the next round of hits to go in 
    newHits = []
    print("finished level")
    print(f"now searching through {len(hits)} new hits")
