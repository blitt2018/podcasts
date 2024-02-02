linkDf="/shared/3/projects/benlitterer/podcastData/podcastIndex/20splits"
outDf="/shared/3/projects/benlitterer/podcastData/podRss/floydFeeds"
stdOut="/shared/3/projects/benlitterer/podcastData/podRss/floydStdOut"

#for item in fSplitak fSplital fSplitam fSplitan fSplitao
#do 
#    python3 0.2-downloadRSSMetadata.py $linkDf/$item $outDf/$item 1 >> $stdOut/$item & 
    #head $linkDf/$item 
#done
parallel --joblog 11_16Out.txt -j2 "python3 0.2-downloadRSSMetadata.py $linkDf/{} $outDf/{} 1 > $stdOut/{}" ::: fSplitak fSplitan #fSplitaa fSplitab fSplitac fSplitad fSplitae
