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

#-----------criacao da tabela no postgree

DIMENSAO_VETOR = 3072  # Ajuste conforme a dimensão dos seus embeddings

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

#-----------criacao da tabela no postgree

#-----------criacao dos embeddings em cache
import pandas as pd

import os
import json
from google import genai
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


seedPLAN = pd.read_parquet('seeddata.parquet')

valoresembed = []

if 'embeddings' not in seedPLAN.columns:

    # Função para obter o embedding de cada texto
    def gerar_embedding(texto):
      if not texto or pd.isna(texto):
        return None
        
      resposta = client.models.embed_content(
      model="gemini-embedding-001",  
      contents=texto
      )
      # Extrai a lista de vetores do objeto de resposta
      return resposta.embeddings[0].values

    # Aplica a função em toda a coluna "texto" e grava no DataFrame
    
    seedPLAN["embeddings"] = seedPLAN["texto"].apply(gerar_embedding)
    seedPLAN.to_parquet(engine="pyarrow", index=False)

else:
  print("Coluna 'embeddings' já existe.")

#-----------criacao dos embeddings em cache

#-----------INSERT da tabela parquet em cache
for row in seedPLAN.itertuples():
    cur.execute(
        """
        INSERT INTO documentos (chunk_id, partido, documento, pagina, texto, secao, embedding) 
        VALUES (%s, %s, %s, %s, %s, %s, %s) 
        ON CONFLICT (chunk_id) DO NOTHING;
        """,
        (
            row.chunk_id, 
            row.partido, 
            row.documento, 
            row.pagina, 
            row.texto, 
            row.secao, 
            row.embeddings
        )
    )
conn.commit()
#-----------INSERT da tabela parquet em cache
