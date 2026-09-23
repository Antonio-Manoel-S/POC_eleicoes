import json
#importante para manipular a tabela no google planilha
from google.colab import auth
auth.authenticate_user()
import gspread
from google.auth import default
creds, _ = default()
gc = gspread.authorize(creds)
#importação de autenticação para acessar a planilha
from google import genai
from google.colab import userdata
import os
os.environ["GEMINI_API_KEY"] = "------" #aqui está a chave de API da sua conta, de preferencia da gemini que é gratuita
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
#importação da chave de API para ter acesso aos serviços de IA

!pip install psycopg2-binary pgvector
#geralmente cada sessão no COLAB não vem instalado o pgvector
import psycopg2
from pgvector.psycopg2 import register_vector

DB_URI = "postgresql://neondb_owner:npg_aHdKL6p7QSoc@ep-icy-snow-ace0d0no-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
#link de acesso do postgress
conn = psycopg2.connect(DB_URI)
cur = conn.cursor()
#cur é a fonte principal de execução de códigos sql, basicamente é o "cursor" que fará qualquer execução
cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
#esse comando cria a extensão do vector através do comando sql
register_vector(conn)
#estabelece a conexão do vector com a tabela sql
conn.commit()
#faz commit
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

#CRIAÇÃO DA COLUNA DOS EMBEDDINGS PARA A PLANILHA

planilhaPG = gc.open('seeddata').sheet1
#aqui deve ser o nome exato da tabela
tabelaLIST = planilhaPG.get_all_records()

key = userdata.get('GEMINI_API_KEY')
apikey = genai.Client(api_key=key)
valoresembed = []

if 'embeddings' not in planilhaPG.row_values(1):

    embeddingcol = len(tabelaLIST[0]) + 1

    linhacol = 1

    intervaloo = f"{gspread.utils.rowcol_to_a1(linhacol, embeddingcol)}"

    planilhaPG.update([["embeddings"]], intervaloo)

    for linha in tabelaLIST:
      texto = linha["texto"]
      # Chamada embedding
      valor_em_embeddings = apikey.models.embed_content(
         model="models/gemini-embedding-001",
         contents=texto,
      )
      json_dos_embeddings = json.dumps(valor_em_embeddings.embeddings[0].values)
                                                      #aqui o vetor de números pertence ao item dentro dessa lista, e não ao objeto principal da resposta
      valoresembed.append([json_dos_embeddings])


    linha_inicial = 2
    #linha inicial 2 para não pegar o titulo, para se juntar ao emmbeding col com o valor da coluna (no caso, g, que equivale a 7)
    linha_final = len(tabelaLIST) + 1
    #aqui deve ser 21

    embeddingcol = len(tabelaLIST[0]) + 1  # aqui pega o valor de elementos por dicionários

    # Define o intervalo da nova coluna (ex: D2:D10)
    intervalo = f"{gspread.utils.rowcol_to_a1(linha_inicial, embeddingcol)}:{gspread.utils.rowcol_to_a1(linha_final, embeddingcol)}"

    #aqui o resultado deve ser g1:g21
    #print(intervalo)

    planilhaPG.update(valoresembed, intervalo)

else:
  print("Coluna 'embeddings' já existe.")
#o if é importante para não criar duas colunas

#INSERCAO DOS DADOS NA TABELA, com o código ON CONFLICT DO NOTHING evitando erros de duplicagem

for item in tabelaLIST:
    cur.execute(
        "INSERT INTO documentos (chunk_id, partido, documento, pagina, texto, secao, embedding) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (chunk_id) DO NOTHING;",
        (item["chunk_id"], item["partido"], item["documento"], item["pagina"], item["texto"], item["secao"], item["embeddings"])
        )

conn.commit()


