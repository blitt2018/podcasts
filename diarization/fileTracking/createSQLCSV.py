from sqlalchemy import create_engine
import pymysql
import pandas as pd

df = pd.read_json("/shared/3/projects/benlitterer/podcastData/processed/mayJune/mayJuneMetadata.jsonl", orient="records", lines=True)
print(df.shape)

df = df[["enclosure"]]
df["processed"] = 0
df = df.rename(columns={"enclosure":"url"}).reset_index(drop=True)

# Import dataframe into MySQL
import sqlalchemy
database_username = 'blitt'
database_password = 'podcasts'
database_ip       = 'curry'
database_name     = 'podcasts'

#establish connection to podcasts database
sqlEngine = sqlalchemy.create_engine('mysql+pymysql://blitt:password@curry:3306/podcasts', pool_recycle=3600)
conn = sqlEngine.connect()

#write the dataframe to mysql table named "diarize" 
df.to_sql(con=conn, name='diarize', if_exists='replace')
#df.to_sql(con=conn, name='diarize')

conn.close()