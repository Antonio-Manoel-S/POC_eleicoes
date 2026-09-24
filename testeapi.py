import os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# --- 1. TESTE DE TEXTO ---
print("--- 1. Testando Geração de Texto ---")
try:
    response = client.models.generate_content(
        model="gemini-3.6-flash",  # Modelo ativo na sua lista
        contents="Responda apenas: 'API OK'"
    )
    print("✅ Resposta:", response.text.strip())
except Exception as e:
    print("❌ Erro na geração de texto:", e)

# --- 2. TESTE DE EMBEDDING ---
print("\n--- 2. Testando Embedding ---")
try:
    emb_response = client.models.embed_content(
        model="gemini-embedding-001",
        contents="Texto de teste para a planilha"
    )
    # Ajustado para a sintaxe da biblioteca google-genai (embeddings no plural)
    vetor = emb_response.embeddings[0].values
    print("✅ Embedding gerado com sucesso!")
    print(f"Dimensão do vetor: {len(vetor)}")
    print(f"Amostra dos 3 primeiros números: {vetor[:3]}")
except Exception as e:
    print("❌ Erro no embedding:", e)