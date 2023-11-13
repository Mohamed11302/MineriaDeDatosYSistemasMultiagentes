import pandas as pd
from sqlalchemy import create_engine, URL

local = False

db_url = URL.create(
    "mysql+pymysql",
    username="minero",
    password="MineriaMultiagentes2324*",
    host="db.programadormanchego.es",
    port=3306,
    database="raw",
)

if local:
    connect_args = {"ssl": {"fake_flag_to_enable_tls": True}}
    conn = create_engine(db_url, connect_args=connect_args)
else:
    ssl_args = {"ssl_ca": "../ca.pem", "ssl_verify_identity": False, "ssl_verify_cert": True}
    conn = create_engine(db_url, connect_args=ssl_args)

conn.connect()

df = pd.read_csv("data.csv")
df.to_sql("electricity_in_all_countries", conn, if_exists="replace", index=False)
