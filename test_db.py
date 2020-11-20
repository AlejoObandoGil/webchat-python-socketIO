# Codigo para hacer consultas sql a BD con SQLalchemy y ayuda de pandas

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import pandas as pd

SQLALCHEMY_DATABASE_URI = 'postgres://mciebhbvvwkyje:8c7c356e012a9348f9e5257b90e5bad7b0f60085da2f292420464b2edf0abace@ec2-52-5-176-53.compute-1.amazonaws.com:5432/dbor0jn7c62572'
SQLALCHEMY_TRACK_MODIFICATIONS = False
engine = create_engine(SQLALCHEMY_DATABASE_URI)

conn = engine.connect()

query = """
SELECT usuario FROM usuarios2;
"""

df = pd.read_sql(query, conn)
print(df)