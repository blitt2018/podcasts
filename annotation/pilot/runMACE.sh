inDir=/shared/3/projects/benlitterer/podcastData/annotation/pilot/MACE/inputs
outDir=/shared/3/projects/benlitterer/podcastData/annotation/pilot/MACE/outputs
macePath=/home/blitt/MACE
for fName in $inDir/*; do 
    baseName=$(basename $fName)
    #mkdir $outDir/$baseName
    java -jar $macePath/MACE.jar --prefix $outDir/$baseName $fName
done 