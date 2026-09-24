import pandas as pd

import psycopg2
from pgvector.psycopg2 import register_vector

DB_URI = "postgresql://neondb_owner:npg_wmRn2h9EWHTX@ep-late-dust-b6oif5bp-pooler.c-2.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

conn = psycopg2.connect(DB_URI)
cur = conn.cursor()

#-----------instalacao do vetor

cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
register_vector(conn)
conn.commit()

#-----------instalacao do vetor

#-----------criacao da tabela

DIMENSAO_VETOR = 1536  # Ajuste conforme a dimensão dos seus embeddings

cur.execute(f"""
    CREATE TABLE IF NOT EXISTS documentos (
        chunk_id SERIAL PRIMARY KEY,
        partido TEXT,
        documento TEXT,
        pagina INTEGER,
        secao TEXT,
        texto TEXT,
        embedding vector({DIMENSAO_VETOR})

    );
""")
conn.commit()
#-----------criacao da tabela

#-----------INSERT da tabela

seedPLAN = pd.read_excel('seeddata.xlsx', sheet_name='pg1')

for item in seedPLAN:
    cur.execute(
        "INSERT INTO documentos (chunk_id, partido, documento, pagina, texto, secao, embedding) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (chunk_id) DO NOTHING;",
        (item["chunk_id"], item["partido"], item["documento"], item["pagina"], item["texto"], item["secao"], item["embeddings"])
        )
#-----------INSERT da tabela

#-----------INSERT da tabela