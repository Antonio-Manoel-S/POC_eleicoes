#para esse teste usei o neon.tech postgresql
# postgresql://neondb_owner:npg_aHdKL6p7QSoc@ep-icy-snow-ace0d0no-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require

# link do site
# https://console.neon.tech/app/projects/delicate-mountain-11959365/branches/br-blue-night-acs9xghg/tables
# se n tiver instalado o pgvector
!pip install psycopg2-binary pgvector
import psycopg2
from pgvector.psycopg2 import register_vector

DB_URI = "postgresql://neondb_owner:npg_aHdKL6p7QSoc@ep-icy-snow-ace0d0no-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# Estabelece a conexão
conn = psycopg2.connect(DB_URI)
cur = conn.cursor()

# Habilita o pgvector no banco de dados e registra no adaptador do Python
cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
register_vector(conn)
conn.commit()

DIMENSAO_VETOR = 3072  # Ajuste conforme a dimensão dos seus embeddings
#CRIACAO DA TABELA
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

#INSERCAO DOS DADOS NA TABELA
planilhaPG = gc.open('seeddata').sheet1

tabelaLIST = planilhaPG.get_all_records()

for item in tabelaLIST:
    cur.execute(
        "INSERT INTO documentos (chunk_id, partido, documento, pagina, texto, secao, embedding) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (chunk_id) DO NOTHING;",
        (item["chunk_id"], item["partido"], item["documento"], item["pagina"], item["texto"], item["secao"], item["embeddings"])
        )

conn.commit()
print("Dados gravados com sucesso!")