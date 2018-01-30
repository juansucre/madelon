import psycopg2 as pg2
from psycopg2.extras import RealDictCursor
import pandas as pd

class ConnectionHelper:
    
    """
    Helps establish a connection to a server given a host, database and username.

    Input: 
        - host name (IP)
        - database name
        - username

    Output:
        - established connection
    """
    
    def __init__(self, host, dbname, user):
        self.host   = host
        self.dbname = dbname
        self.user   = user
        
    
    def connect_and_fetch(self, query, df = False):
        """
        Establishes a connection to the given server and fetches data from a given query. Closes connection once finished.
        
        Input:
            - query
            - df (default = False)
        
        Output:
            - dictionary (default)
                    OR
            - DataFrame (if df = True)
        """
        con = pg2.connect(host   = self.host,
                          dbname = self.dbname,
                          user   = self.user)
        cur = con.cursor(cursor_factory=RealDictCursor)
        cur.execute(query)
        results = cur.fetchall()
        con.close()
        
        if df:
            results = pd.DataFrame(results)
        
        return results
    
    
    def max_min_avg_std_column(self, database, column, df = True):
        """
        Summary stats for a given column.
        """
        con = pg2.connect(host= self.host,
                      dbname= self.dbname,
                      user= self.user)
        cur = con.cursor(cursor_factory = RealDictCursor)
        query = "SELECT MAX({}), MIN({}), AVG({}), STDDEV({}) FROM {}".format(column, column, column, column, database)
        cur.execute(query)
        results = cur.fetchall()
        
        con.close()
        
        
        if df:
            results = pd.DataFrame(results)
            
        return results
