#pip install -r requirements.txt

# Exemplo de consulta buscando os 3 itens mais parecidos com um vetor de busca
import psycopg2
import os
from google import genai
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

DB_URI = "postgresql://neondb_owner:npg_wmRn2h9EWHTX@ep-late-dust-b6oif5bp-pooler.c-2.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

conn = psycopg2.connect(DB_URI)
cur = conn.cursor()

# Reseta a transação se o código falhou
conn.rollback()

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