linkDf="/shared/3/projects/benlitterer/podcastData/podcastIndex/20splits"
outDf="/shared/3/projects/benlitterer/podcastData/podRss/floydFeeds"
stdOut="/shared/3/projects/benlitterer/podcastData/podRss/floydStdOut"

#for item in fSplitap fSplitaq fSplitar fSplitas fSplitat fSplitau fSplitav
#do 
#    python3 0.2-downloadRSSMetadata.py $linkDf/$item $outDf/$item 1 >> $stdOut/$item & 
#    #head $linkDf/$item 
#done
#parallel --joblog 16_22Out.txt -j7 "python3 0.2-downloadRSSMetadata.py $linkDf/{} $outDf/{} 1 > $stdOut/{}" ::: fSplitap fSplitaq fSplitar fSplitas fSplitat fSplitau fSplitav

parallel --joblog fSplitatOut.txt -j1 "python3 0.2-downloadRSSMetadata.py $linkDf/{} $outDf/{} 1 > $stdOut/{}" ::: fSplitat #fSplitap fSplitaq fSplitar fSplitas fSplitat fSplitau fSplitav
