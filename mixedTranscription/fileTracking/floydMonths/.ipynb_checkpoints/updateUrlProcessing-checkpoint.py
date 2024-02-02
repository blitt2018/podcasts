from sqlalchemy import create_engine, text
import sqlalchemy
import pandas as pd
import sys

inURL = sys.argv[1]

# Import dataframe into MySQL
database_username = 'blitt'
database_password = 'podcasts'
database_ip       = 'curry'
database_name     = 'podcasts'

#establish connection to podcasts database
sqlEngine = sqlalchemy.create_engine('mysql+pymysql://blitt:podcasts@localhost/podcasts', pool_recycle=3600)
conn = sqlEngine.connect()

updateSQL = f"UPDATE podcasts.floydLinks SET processed = 1 WHERE url = '{inURL}';"
print(updateSQL)
record = conn.execute(text(updateSQL))

conn.commit()
conn.close()