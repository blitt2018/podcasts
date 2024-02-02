import argparse
from datetime import date
import hashlib
import json
import requests
import time
import pandas as pd
from tqdm import tqdm 
import os 
import random
import atexit

# setup some basic vars for the search api. 
# for more information, see https://api.podcastindex.org/developer_docs
api_key = 'GVPMQGU2ZDRKNED8JNXT'
api_secret = 'sNV7XMKy#JGVeZeMbGh4bGqnsnW63XCx8VY7cbgY'

# uncomment these to make debugging easier.
# print ('api key: ' + api_key);
# print ('api secret: ' + api_secret);
# print ('query: ' + query);
# print ('url: ' + url);

# the api follows the Amazon style authentication
# see https://docs.aws.amazon.com/AmazonS3/latest/dev/S3_Authentication2.html


def getPod(query): 
    # we'll need the unix time
    epoch_time = int(time.time())

    # our hash here is the api key + secret + time 
    data_to_hash = api_key + api_secret + str(epoch_time)
    # which is then sha-1'd
    sha_1 = hashlib.sha1(data_to_hash.encode()).hexdigest()

    # now we build our request headers
    headers = {
        'X-Auth-Date': str(epoch_time),
        'X-Auth-Key': api_key,
        'Authorization': sha_1,
        'User-Agent': 'postcasting-index-python-cli'
    }

    
    url = "https://api.podcastindex.org/api/1.0/search/bytitle?q=" + query.replace(" ", "+")
    
    # perform the actual post request
    r = requests.post(url, headers=headers)

    # if it's successful, dump the contents (in a prettified json-format)
    # else, dump the error code we received
    if r.status_code == 200:
        pretty_json = json.loads(r.text)
        return r.status_code, pretty_json 
        #print (json.dumps(pretty_json, indent=2))
    else:
        print(f"bad status code {r.status_code}")
        return r.status_code, {}
    
toKeep = ["title", "url", "originalUrl", "description", "author", "language", \
          "categories", "explicit", "episodeCount"]

#reload the file to get an updated name list 
def reload(epCount=10): 
    IN_PATH = "/shared/3/projects/benlitterer/podcastData/podNames/podinfo1hr.csv"
    colNames = ["searchName", "hitName", "type", "languages", "description", "is_externally_hosted", "total_episodes"]
    df = pd.read_csv(IN_PATH, names=colNames)
    
    #we only want those podcasts for which we have 10 or more eps 
    df = df[df["total_episodes"] >= epCount]
    
    #drops duplicates for us
    names = set(df["hitName"])
    return names

def exit_handler():
    if os.path.exists(OUT_FILE): 
        outHandle.close()

atexit.register(exit_handler)

#we want to write to a file that way we can keep our results as we call the api 
OUT_FILE = "/shared/3/projects/benlitterer/podcastData/podRss/TESTRSSFeeds.csv"

#what needs to be processed? 
#note: names is  a set
names = reload()

#we want to either write a new file, or append 
#to a file we've already written 
if os.path.exists(OUT_FILE): 
    outHandle = open(OUT_FILE, "a+")
    
    #IF the file exists, we want to decide where to start searching and appending 
    outDf = pd.read_csv(OUT_FILE, names=["queryName"] + toKeep)
    
    #get what's already been processed 
    processed = set(outDf["queryName"]) 
    
    #if we've already processed some names, 
    #then we can remove those from our set 
    names = names - processed 
    
else: 
    #if we haven't processed any names, then just open outHandle
    #and use the set of names defined above 
    processed = set([])
    outHandle = open(OUT_FILE, "w+")
    
print(f"Processing {len(names)} Records")

MIN_TIME = .1
waitTime = MIN_TIME
podInfo = []

toKeep = ["title", "url", "originalUrl", "description", "author", "language", \
          "categories", "explicit", "episodeCount"]

#iterate through the podcasts in our set of names 
nameList = list(names)
i = 0
while True: 
    podName = nameList[i]
    
    #emulating a do-while loop 
    #keep trying to request until we got a non 200 exit code 
    #and progressively wait longer each attempt 
    while True: 
        
        time.sleep(waitTime + (random.random()/10))
        
        #grab the dictionary of information for the first search result
        statusCode, podDict = getPod(podName)
        
        #stop trying to re-request whenever we get a 200 response 
        #a 400 response could result from special characters etc.. in podcast title 
        if statusCode == 200 or statusCode == 400: 
            if statusCode == 400: 
                print("400 code!")
                
            #decrease wait time if we are getting successful request 
            #are are above our min wait time 
            if waitTime > MIN_TIME: 
                waitTime = np.sqrt(waitTime)
            break 
        
        #if we continue re-requesting, then increase the wait time
        #need to make sure that time is greater than 1 when squaring
        print("increasing time")
        waitTime = (waitTime + 1) ** 2
        
    #only if we have something to process 
    if "feeds" in podDict and len(podDict["feeds"]) > 0: 
        podDict = podDict["feeds"][0]

        #grab just the fields we want 
        currInfo = []
        for key in toKeep: 
            if key in podDict: 
                currInfo.append(podDict[key])
            else: 
                currInfo.append("")

        #add the query to currInfo 
        currInfo = [podName] + currInfo

        #turn genres into a string  
        if currInfo[7] != "": 
            currInfo[7] = ",".join([v for k,v in currInfo[7].items()])

        #format the string to write to output file
        #and turn double quotes into singles
        currStr = '","'.join([str(item).replace('"', '\'').replace("\n", " ") for item in currInfo])
        currStr = f'"{currStr}"'

        outHandle.write(currStr + "\n")
    
    #keep track of what's going on 
    i += 1
    processed.add(podName)
    
    #flush buffer to file so we can see progress
    if i % 10 == 0: 
        outHandle.flush()
    
    if i % 5000 == 0: 
        print(f"{i} processed")
        
    #how long to wait before 
    #reading in input again to check if we have new records 
    streamWait = 60
    
    #if we finish processing all of the names 
    while len(processed) == len(names): 
        time.sleep(streamWait)
        #this gives us the updated names 
        #from our input file which could still be running
        names = reload()
    
        #if we got new names to process, break the loop 
        #and process those 
        if len(processed) < len(nameList): 
            
            #redefine iterator and names so we start at the beginning 
            #of the list 
            i = 0 
            names = names - processed 
            nameList = list(names)
            break 
        
        #if we don't find anything new, wait longer and try again 
        streamWait = streamWait **2 
        