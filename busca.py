#pip install -r requirements.txt

# Exemplo de consulta buscando os 3 itens mais parecidos com um vetor de busca
import psycopg2
import os
from openai import OpenAI
api_key = os.getenv("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")
DB_URI = "postgresql://neondb_owner:npg_aHdKL6p7QSoc@ep-icy-snow-ace0d0no-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

conn = psycopg2.connect(DB_URI)
cur = conn.cursor()

# Reseta a transação se o código falhou
conn.rollback()

# 1. Inicializa o cliente oficial
client = OpenAI(api_key=os.environ.get("genaiapi"))
# 2. Define a pergunta em texto
pergunta = "melhoria da segurança publica"

resposta = client.models.embed_content(
    model="models/gemini-embedding-001",
    contents=pergunta
)
# 3. Definição da variável: converte a pergunta no vetor de busca
vetor_da_busca = resposta.embeddings[0].values

# 4. Executa a busca no pgvector usando a distância de cosseno (<=>)
cur.execute(
    """
    SELECT chunk_id, texto, 1 - (embedding <=> %s::vector) AS pontuacao_similaridade
    FROM documentos
    ORDER BY embedding <=> %s::vector
    LIMIT 3;
    """,
    (vetor_da_busca, vetor_da_busca)
)

# 5. Recupera os resultados
resultados = cur.fetchall()

for linha in resultados:
    print(f"chunk_id: {linha[0]}")
    print(f"Texto: {linha[1]}")
    print(f"Similaridade: {linha[2]:.4f}")
    print("-" * 30)