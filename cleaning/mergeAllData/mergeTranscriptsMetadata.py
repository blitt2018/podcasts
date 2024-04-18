# %%
import pandas as pd

# %%
transcriptDf = pd.read_csv("/shared/3/projects/benlitterer/podcastData/processed/mayJune/mayJuneTranscripts.tsv", sep="\t")

# %%
metaDf = pd.read_json("/shared/3/projects/benlitterer/podcastData/processed/mayJune/mayJuneMetadata.jsonl", orient="records", lines=True)

# %%
transcriptDf.columns = ["fullPotentialOutPath", "transcript"]

# %%
metaDf.head()["potentialOutPath"]

# %%
test = transcriptDf.iloc[1,0]
"/" + "/".join(test.split("/")[8:])

# %%
transcriptDf["potentialOutPath"] = transcriptDf["fullPotentialOutPath"].apply(lambda x: "/" + "/".join(x.split("/")[8:]))

# %%
print(metaDf.shape)
metaDf = metaDf.drop_duplicates(subset=["potentialOutPath"])
print(metaDf.shape)

# %%
merged = pd.merge(transcriptDf, metaDf, on="potentialOutPath", how="left")

# %%
merged.to_json("/shared/3/projects/benlitterer/podcastData/processed/mayJune/mayJuneMetaTranscripts.jsonl", orient="records", lines=True)

# %%



