import pandas as pd

# -- 1 --
df_gas_2000_over = pd.read_csv('gasolina_2000+.csv', index_col=0)
df_gas_2010_over = pd.read_csv('gasolina_2010+.csv', index_col=0)
df_gas_2000_2010_over = pd.concat([df_gas_2000_over, df_gas_2010_over])
df_gas_2000_2010_over.to_csv('gasolina_2000_2010_over.csv')

# -- 2 --
print(df_gas_2000_2010_over.head())
print(df_gas_2000_2010_over.info())

# -- 3 -- 
print(type(df_gas_2000_2010_over['DATA INICIAL'].iloc[2]))

# -- 4 --
df_gas_2000_2010_over['DATA INICIAL'] = pd.to_datetime(df_gas_2000_2010_over['DATA INICIAL'])
df_gas_2000_2010_over['DATA FINAL'] = pd.to_datetime(df_gas_2000_2010_over['DATA FINAL'])

# -- 5 --
df_gas_2000_2010_over['ANO-MES'] = df_gas_2000_2010_over['DATA FINAL'].dt.strftime('%Y-%m')

# -- 6 --
print(df_gas_2000_2010_over['PRODUTO'].value_counts())

# -- 7 --
df_gas_comum = df_gas_2000_2010_over[df_gas_2000_2010_over['PRODUTO'] == 'GASOLINA COMUM']

# -- 8 --
print(df_gas_2000_2010_over[df_gas_2000_2010_over['ANO-MES'] == '2008-08']['PREÇO MÉDIO REVENDA'].mean())

# -- 9 --
print(df_gas_comum[(df_gas_comum["ANO-MES"] == '2008-08') & (df_gas_comum["ESTADO"] == 'SAO PAULO')]["PREÇO MÉDIO REVENDA"].mean())

# -- 10 --
print(df_gas_comum[df_gas_comum['PREÇO MÉDIO REVENDA'] > 5][['ESTADO', 'ANO-MES', 'PREÇO MÉDIO REVENDA']]
)
# -- 11 -- 
gas_comum_2012 = df_gas_comum[(df_gas_comum['ANO-MES'].str[:4] == '2012') & (df_gas_comum['REGIÃO'] == 'SUL')]
media_preco_revenda = gas_comum_2012['PREÇO MÉDIO REVENDA'].mean()
print(media_preco_revenda)

# -- 12 -- 
df_gas_comum["MES"] = df_gas_comum["ANO-MES"].str[5:]
df_rio = df_gas_comum[df_gas_comum["ESTADO"] == "RIO DE JANEIRO"]
df_month_rio = df_rio.groupby('ANO-MES')[['PREÇO MÉDIO REVENDA', 'MES']].last()
df_last_month = df_month_rio[df_month_rio['MES'] == '12']

var_percentual = ((df_last_month['PREÇO MÉDIO REVENDA'] - df_last_month['PREÇO MÉDIO REVENDA'].shift(1)) / (df_last_month['PREÇO MÉDIO REVENDA'].shift(1))) * 100
print(var_percentual)

# -- 13 --
df_max = df_gas_comum.groupby("ANO-MES").max()["PREÇO MÉDIO REVENDA"]
df_min = df_gas_comum.groupby("ANO-MES").min()["PREÇO MÉDIO REVENDA"]

idx_max = df_gas_comum.groupby('ANO-MES')["PREÇO MÉDIO REVENDA"].idxmin()
idx_min = df_gas_comum.groupby('ANO-MES')["PREÇO MÉDIO REVENDA"].idxmax()

df_diff = pd.DataFrame()

df_diff["abs_diff"] = df_max - df_min
df_diff["perct_diff"] = (df_max - df_min) / df_min * 100
df_diff["max"] = df_max
df_diff["min"] = df_min

print(df_gas_comum.loc[idx_max, :][["ESTADO", "PREÇO MÉDIO REVENDA", "ANO-MES"]])

df_diff["ESTADO_MAX"] = df_gas_comum.loc[idx_max, :]["ESTADO"].values
df_diff["ESTADO_MIN"] = df_gas_comum.loc[idx_min, :]["ESTADO"].values
print(df_diff)

print(df_diff["ESTADO_MAX"].value_counts())
print(df_diff["ESTADO_MIN"].value_counts())




