from sqlalchemy import create_engine, text
import sqlalchemy
import pandas as pd
import sys
#import atexit

inURL = sys.argv[1]

# Import dataframe into MySQL
database_username = 'blitt'
database_password = 'podcasts'
database_ip       = 'curry'
database_name     = 'podcasts'

#establish connection to podcasts database
sqlEngine = sqlalchemy.create_engine('mysql+pymysql://blitt:password@curry:3306/podcasts', pool_recycle=3600)
#conn = sqlEngine.connect()

print("new version")
with sqlEngine.begin() as conn:

    def update(): 
        #replace 1 with 2
        updateSQL = f"UPDATE podcasts.floydLinks SET processed = 2 WHERE url = '{inURL}';"
        print(updateSQL)
        record = conn.execute(text(updateSQL))
        pass

    #rows = conn.execute(text(f"SELECT * FROM podcasts.floydLinks WHERE url = '{inURL}';"))
    #print([row for row in rows])
    worked = False
    nTries = 0 
    MAX_TRIES = 5
    while worked != True and nTries < MAX_TRIES: 
        try: 
            update()
            worked = True
        except: 
            print("failed")
            pass 
        nTries += 1
            
            
        #rows = conn.execute(text(f"SELECT * FROM podcasts.floydLinks WHERE url = '{inURL}';"))
        #print([row for row in rows])

#conn.close()
