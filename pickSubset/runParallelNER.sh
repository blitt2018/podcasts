#ls /shared/3/projects/newsDiffusion/data/interim/NEREmbedding/NERSplits/ | xargs -i -n 1 -P 160 python3 2.1-bl-applyNERsingleInput.py {} /shared/3/projects/newsDiffusion/data/interim/NEREmbedding/NERSplitsComplete/
ls /shared/3/projects/benlitterer/podcastData/NER/preSplits/ | parallel -j160 --joblog runParallelNER.txt python3 runNERSingleFile.py {} /shared/3/projects/benlitterer/podcastData/NER/finishedSplits/
