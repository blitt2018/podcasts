import gensim
import pandas as pd
import os
from tqdm import tqdm

df = pd.read_csv("/shared/3/projects/benlitterer/podcastData/processed/floydMonth/floydMonthEnSHORT.csv")

basePath = "/shared/3/projects/benlitterer/podcastData/prosodyMerged/floydMonth"
df["potentialOutPathFull"] = basePath + df["potentialOutPath"] 

df["exists"] = df["potentialOutPathFull"].apply(os.path.exists)
df = df[df["exists"] == True] 

CUTOFF = 1000
finishedPaths = []

def readCorpus():
    i = 0
    for path in tqdm(df.head(20000)["potentialOutPathFull"]):
        try:
            currFile = open(path, "r")
            #get tokens as processed by gensim
            tokens = [row.split(",")[4] for row in currFile.readlines()]
            currText = "".join(tokens)
            tokens = gensim.utils.simple_preprocess(currText)
            yield gensim.models.doc2vec.TaggedDocument(tokens, [i])
            i += 1
        except Exception as e:
            print(e)
            pass

train_corpus = list(readCorpus())

model = gensim.models.doc2vec.Doc2Vec(vector_size=50, min_count=50, epochs=40)
model.build_vocab(train_corpus)

model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)

from gensim.test.utils import get_tmpfile
OUT_PATH = "/shared/3/projects/benlitterer/podcastData/embeddings/floydMonth/doc2vecModel20000"
fname = get_tmpfile(OUT_PATH)
model.save(fname)
