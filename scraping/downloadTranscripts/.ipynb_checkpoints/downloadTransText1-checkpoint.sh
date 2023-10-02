transcriptPaths="/shared/4/projects/podcasts/transcripts/transcriptLinks"
scriptPath="/home/blitt/projects/testing/podcasts/scraping/downloadTranscripts.py"
paths=$(ls $transcriptPaths | head -20)  

for path in $paths
do 
    python3 $scriptPath $path &
done