import sys

allUrlsPath = sys.argv[1] 
finishedUrlsPath = sys.argv[2] 


with open(finishedUrlsPath) as finishedUrlsFile: 
    finishedUrls = list(finishedUrlsFile.readlines()) 

with open(allUrlsPath) as allUrlsFile: 
    for url in allUrlsFile.readlines(): 
        if url not in finishedUrls: 
            print(url)
            break

with open(finishedUrlsPath, "a") as finishedUrlsFile: 
    finishedUrlsFile.write(url)  
