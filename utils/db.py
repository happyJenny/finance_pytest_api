import psycopg2
from config.loader import load_config

CFG=load_config()

DB_CONFIG={
    "host":CFG["db_host"],
    "port":CFG["db_port"],
    "dbname":CFG["db_name"],
    "user":CFG["db_user"],
    "password":CFG["db_password"]
}


print("DB_CONFIG:", DB_CONFIG)

def _login_db():
    return psycopg2.connect(**DB_CONFIG)

def query_select(sql,params=None,fetch_all=False):
    conn=_login_db()
    try:
        with conn.cursor() as cur:
            cur.execute(sql,params)
            if fetch_all==True:
              return cur.fetchall()
            else:
              return cur.fetchone()  
    finally:
        conn.close()          

def count(sql, params=None):
    row=query_select(sql,params=params)
    return row[0] if row else 0

