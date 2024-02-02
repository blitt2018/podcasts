import sys
from urllib.parse import urlparse 
import re
from collections import Counter
import pandas as pd
import re

def getUrlTranscriptPath(inUrl, inStem): 
    cleanUrl = re.sub("[^\w\d.]","", inUrl)

    rootPath = inStem
    host = urlparse(inUrl).netloc

    #remove anything that isn't a letter, number, or . 
    host = re.sub("[^\w\d.]","", host)

    #get the first few chars of the path 
    path = urlparse(inUrl).path
    path = re.sub("[^\w]","", path)

    counted = dict(Counter(path))

    sortedLetters = sorted(list(counted.keys()), key=lambda x: counted[x], reverse=True)

    outStr = ""
    length = 2
    while len(outStr) == 0 and length > 0: 
        if len(sortedLetters) >= length: 
            outStr = "".join(sortedLetters[:length])
        length = length - 1

    #the full path to this transcript 
    transcriptPath = rootPath + "/" + host + "/" + outStr + "/" + cleanUrl + "MERGED"
    return transcriptPath