transcriptPaths="/shared/4/projects/podcasts/transcripts/transcriptLinks"
scriptPath="/home/blitt/projects/testing/podcasts/scraping/downloadTranscripts.py"

#get the 21-40th file 
paths=$(ls $transcriptPaths | tail -21)  

for path in $paths
do 
    python3 $scriptPath $path &
done
