from transformers import RobertaTokenizer, RobertaModel
import pandas as pd
import importlib
import torch
from tqdm import tqdm 
import os 

OUT_PATH = "/shared/3/projects/benlitterer/podcastData/embeddings/floydMonth/robertaEmbeddings.pkl"

#load in the george floyd data
df = pd.read_csv("/shared/3/projects/benlitterer/podcastData/processed/floydMonth/floydMonthEnSHORT.csv",lineterminator='\n')

spec=importlib.util.spec_from_file_location("getURLstorageLocation","/home/blitt/projects/podcasts/mergeTransMetadata/getURLstorageLocation.py")
 
# creates a new module based on spec
foo = importlib.util.module_from_spec(spec)
 
# executes the module in its own namespace
# when a module is imported or reloaded.
spec.loader.exec_module(foo)

META_PATH= "/shared/3/projects/benlitterer/podcastData/prosodyMerged/floydMonth" 

df = df.dropna(subset=["enclosure"])
df["transcriptPath"] = df["enclosure"].apply(foo.getUrlTranscriptPath, args=[META_PATH])

df["exists"] = df["transcriptPath"].apply(os.path.exists)

#foo.getUrlTranscriptPath("helloWorld", META_PATH) 
paths = df.loc[df["exists"] == True, "transcriptPath"] 

device = "cuda:" + str(2)
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
model = RobertaModel.from_pretrained('roberta-base').to(device)

def mean_pooling(token_embeddings, attention_mask): 
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    
transcriptEmbeddings = []
finishedPaths = []
for path in tqdm(paths): 
    try: 
        currFile = open(path, "r")
        currText = "".join([row.split(",")[4] for row in currFile.readlines()])
        
        encoded_input = tokenizer(currText, return_tensors='pt', max_length=512, truncation=True).to(device)
        output = model(**encoded_input)
        
        embeddings = output["last_hidden_state"]
        transcriptEmbedding = mean_pooling(embeddings, encoded_input["attention_mask"]).detach().to("cpu")
        
        transcriptEmbeddings.append(transcriptEmbedding)
        finishedPaths.append(path)
        del transcriptEmbedding
        del embeddings
        del output
        del encoded_input
        torch.cuda.empty_cache()
    except Exception as e:
        pass
    
outDf = pd.DataFrame({"transcriptPath":finishedPaths, "embedding":transcriptEmbeddings}) 
outDf.to_pickle(OUT_PATH)