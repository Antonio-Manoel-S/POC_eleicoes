#CRIAÇÃO DA COLUNA DOS EMBEDDINGS PARA A PLANILHA
import pandas as pd
import os
import json
import openai
from openai import OpenAI
api_key = os.getenv("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")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

seedPLAN = pd.read_excel('seeddata.xlsx', sheet_name='pg1')

valoresembed = []

if 'embeddings' not in seedPLAN.columns:

    for linha in seedPLAN:
      texto = linha["texto"]
      # Chamada embedding
      valor_em_embeddings = client.models.embed_content(
         model="text-embedding-3-small",
          contents=valor_em_embeddings
        )
      json_dos_embeddings = json.dumps(valor_em_embeddings.embeddings[0].values)
                                                      #aqui o vetor de números pertence ao item dentro dessa lista, e não ao objeto principal da resposta
      valoresembed.append([json_dos_embeddings])
    seedPLAN['embeddings'] = valoresembed
    seedPLAN.to_excel('seeddata.xlsx', sheet_name='pg1', index=False)

else:
  print("Coluna 'embeddings' já existe.")
#o if é importante para não criar duas colunas