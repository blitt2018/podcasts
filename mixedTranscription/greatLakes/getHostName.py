import sys
from urllib.parse import urlparse 
import re
from collections import Counter 

inPath = sys.argv[1]

host = urlparse(inPath).netloc

#remove anything that isn't a letter, number, or . 
host = re.sub("[^\w\d.]","", host)

#get the first few chars of the path 
path = urlparse(inPath).path
path = re.sub("[^\w]","", path)

counted = dict(Counter(path))

sortedLetters = sorted(list(counted.keys()), key=lambda x: counted[x], reverse=True)

outStr = ""
length = 3
while len(outStr) == 0 and length > 0: 
    if len(sortedLetters) >= length: 
        outStr = "".join(sortedLetters[:length])
    length = length - 1

print(host + "/" + outStr)