from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

SQLALCHEMY_DATABASE_URI = 'postgres://odzwjrzlprudil:8317735ed8c2403e044449e353a227dbc9ca3a0afc17ba794f37cfc40420558d@ec2-54-161-150-170.compute-1.amazonaws.com:5432/d57q5bus76ls43'
SQLALCHEMY_TRACK_MODIFICATIONS = False
engine = create_engine(SQLALCHEMY_DATABASE_URI)

conn = engine.connect()

import pandas as pd

query = """
SELECT * FROM userspro;
"""

df = pd.read_sql(query, conn)
print(df)