import pandas as pd

seedPLAN = pd.read_excel('seeddata.xlsx', sheet_name='pg1')


# 3. Caminho do arquivo Parquet de saída
seedParq = "seeddata.parquet"

# 4. Salvar como Parquet
seedPLAN.to_parquet(seedParq, engine="pyarrow", index=False)

print("Conversão concluída com sucesso!")