diarizePath="/shared/3/projects/benlitterer/podcastData/diarization/mayJune/"
#diarizePath="/shared/3/projects/benlitterer/podcastData/diarization/mayJune/zionsermons.sermon.net/"
mergeScript="/home/blitt/projects/podcasts/merging/mergeDiarization.py"
find $diarizePath -type f | parallel -j 15 python3 $mergeScript