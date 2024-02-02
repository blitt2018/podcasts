import sqlalchemy 
from sqlalchemy import create_engine, text
import pandas as pd
import atexit

# Import dataframe into MySQL
database_username = 'blitt'
database_password = 'podcasts'
database_ip       = 'curry'
database_name     = 'podcasts'

"""
#establish connection to podcasts database
sqlEngine = sqlalchemy.create_engine('mysql+pymysql://blitt:podcasts@localhost/podcasts', pool_recycle=3600, future=True)
#conn = sqlEngine.connect()

with sqlEngine.connect() as conn:
    with conn.begin():
        
        conn.execute(text("LOCK TABLES podcasts.floydLinks WRITE;"))
        df = pd.read_sql("select * from podcasts.floydLinks", conn, index_col="index")

        remaining = df[df["processed"] == 0]

        nextURL = remaining.iloc[0, 0]

        updateSQL = f"UPDATE podcasts.floydLinks SET processed = 1 WHERE url = '{nextURL}';"
        record = conn.execute(text(updateSQL))
        print(nextURL)

        conn.execute(text("UNLOCK TABLES;"))
        conn.close()
"""

sqlEngine = sqlalchemy.create_engine('mysql+pymysql://blitt:podcasts@localhost/podcasts', pool_recycle=3600, future=True)
with sqlEngine.connect() as conn:
    with conn.begin():
        
        def beforeExiting(): 
            conn.execute(text("UNLOCK TABLES;"))
            conn.close()
        
        atexit.register(beforeExiting)
        
        conn.execute(text("LOCK TABLES podcasts.floydLinks WRITE;"))
        df = pd.read_sql("select * from podcasts.floydLinks WHERE processed = 0 LIMIT 1", conn, index_col="index")
        
        #url value 
        url = df.iloc[0, 0]
        print(url)
        
        #index value corresponding to url (this is a key)
        iVal = df.index.item() 
        
        #use key for faster search 
        updateSQL = conn.execute(text(f"UPDATE podcasts.floydLinks SET processed = 1 WHERE `index` = {iVal};"))
        
        conn.execute(text("UNLOCK TABLES;"))
        conn.close()