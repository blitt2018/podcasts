#first we need to get all of the different output files to one place 
transcriptsToDfFile=/home/blitt/projects/podcasts/cleaning/outFilesToDf/mayJuneToDf.py
python3 $transcriptsToDfFile

#concatenate the transcript output chunks to a single file 
transParallelChunksPath=/shared/3/projects/benlitterer/podcastData/intermediary/
cat $transParallelChunksPath/* > /shared/3/projects/benlitterer/podcastData/processed/mayJune/mayJuneTranscripts.tsv

#merge metadata with transcripts 
mergeTransMetadata=/home/blitt/projects/podcasts/cleaning/mergeAllData/mergeTranscriptsMetadata.py
python3 $mergeTransMetadata

#get named entities

#merge named entities

