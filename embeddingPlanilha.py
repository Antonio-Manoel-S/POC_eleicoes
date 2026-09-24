#CRIAÇÃO DA COLUNA DOS EMBEDDINGS PARA A PLANILHA
import pandas as pd
import os
import json
from google import genai
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

seedPLAN = pd.read_excel('seeddata.xlsx', sheet_name='pg1')

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

else:
  print("Coluna 'embeddings' já existe.")
#o if é importante para não criar duas colunas