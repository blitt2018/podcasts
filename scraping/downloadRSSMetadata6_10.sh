linkDf="/shared/3/projects/benlitterer/podcastData/podcastIndex/20splits"
outDf="/shared/3/projects/benlitterer/podcastData/podRss/floydFeeds"
stdOut="/shared/3/projects/benlitterer/podcastData/podRss/floydStdOut"

#for item in fSplitaf fSplitag fSplitah fSplitai fSplitaj
#do 
#    python3 0.2-downloadRSSMetadata.py $linkDf/$item $outDf/$item 1 >> $stdOut/$item & 
    #head $linkDf/$item 
#done
parallel --joblog 6_10Out.txt -j5 "python3 0.2-downloadRSSMetadata.py $linkDf/{} $outDf/{} 1 > $stdOut/{}" ::: fSplitaf fSplitag fSplitah fSplitai fSplitaj
