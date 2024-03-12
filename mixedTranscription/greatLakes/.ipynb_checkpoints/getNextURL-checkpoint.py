import sys

allUrlsPath = sys.argv[1] 
finishedUrlsPath = sys.argv[2] 


with open(finishedUrlsPath) as finishedUrlsFile: 
    finishedUrls = list(finishedUrlsFile.readlines()) 

with open(allUrlsPath) as allUrlsFile: 
    for line in allUrlsFile.readlines(): 
        url = line
        if url not in finished Urls: 
            print(url)
            break
