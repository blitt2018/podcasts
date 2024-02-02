import sys
from urllib.parse import urlparse 
import re

inPath = sys.argv[0]

host = urlparse(inPath).netloc

#remove anything that isn't a letter, number, or . 
host = re.sub("[^\w\d.]","", host)

print(host)