linkDf="/shared/3/projects/benlitterer/podcastData/podcastIndex/20splits"
outDf="/shared/3/projects/benlitterer/podcastData/podRss/floydFeeds"
stdOut="/shared/3/projects/benlitterer/podcastData/podRss/floydStdOut"

#for item in fSplitaa fSplitab fSplitac fSplitad fSplitae
#do 
    #python3 testStdOut.py > $stdOut/$item & disown 
    #python3 0.2-downloadRSSMetadata.py $linkDf/$item $outDf/$item 1 > $stdOut/$item & disown 
    #head $linkDf/$item 
#done
parallel --joblog 1_5Out.txt -j5 "python3 0.2-downloadRSSMetadata.py $linkDf/{} $outDf/{} 1 > $stdOut/{}" ::: fSplitab #fSplitaa fSplitab fSplitac fSplitad fSplitae
#parallel "python3 testStdOut.py > $stdOut/{}" ::: fSplitaa fSplitab fSplitac fSplitad fSplitae

