import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('default_of_credit_card_clients__courseware_version_1_21_19.xls')
# print(df.columns)
# print(df.shape)

print(df['ID'].nunique()) # Verificar ID's únicos dentro da Serie 'ID'
# Nota-se que nem todos os ID's são unicos, dos 30000, apenas 29687 são únicos
# print(id_counts.value_counts()) # Demonstra que cada id duplicado aparece somente 2 vezes, 313 id's duplicados 2 vezes

id_counts = df['ID'].value_counts() 
dupe_mask = id_counts == 2

dupe_ids = id_counts.index[dupe_mask] # Colocando os ID's com a máscara dupe_mask (id's == 2) e pegando os index
dupe_ids = list(dupe_ids)

# print(dupe_ids[:3])
# print(df.loc[df['ID'].isin(dupe_ids[0:3]), :])
# Os prints acima, mostra alguns id's duplicados e posteriormente no df 

df_zero_mask = df == 0
feature_zero_mask = df_zero_mask.iloc[:, 1:].all(axis=1)

df_clean_1 = df.loc[~feature_zero_mask, :].copy()
# O operador ~ serve para inverter valores booleanos, 
# Criando um DataFrame com as linhas not true, ou seja,
# as linhas que não possui somente 0

# print(df_clean_1.shape) -> (29685, 25)
# print(df_clean_1['ID'].nunique()) -> 29685

valid_pay_1_mask = df_clean_1['PAY_1'] != 'Not available'
df_clean_2 = df_clean_1.loc[valid_pay_1_mask, :].copy() # Criando um novo df, com a máscara booleana que retorna True, quando não tiver a string 'Not Available'
# df_clean_2.shape -> (26664, 25)

df_clean_2['PAY_1'] = df_clean_2['PAY_1'].astype('int64')
# Converter para o datatype(int64) no df

# df_clean_2[['LIMIT_BAL', 'AGE']].hist()
# plt.show()

# print(df_clean_2[['LIMIT_BAL', 'AGE']].describe())

df_clean_2['EDUCATION'].replace(to_replace=[0, 5, 6], value=4, inplace=True) # Há dados não documentados [0, 5, 6], dando replace para 4 (Outros)
# print(df_clean_2['EDUCATION'].value_counts())

df_clean_2['MARRIAGE'].replace(to_replace=0, value=3, inplace=True)
# print(df_clean_2['MARRIAGE'].value_counts())

# df_clean_2.groupby('EDUCATION').agg({'default payment next month':'mean'}).plot.bar()
# plt.ylabel('Default rate')
# plt.xlabel('Education level: ordinal encoding')
# plt.show()

dict_name = {
    1:'Graduate School',
    2:'University',
    3:'High School',
    4:'Others'
}
df_clean_2['EDUCATION_CAT'] = df_clean_2['EDUCATION'].map(dict_name)
# Criando uma nova coluna a partir da coluna Education, contendo string

edu_ohe = pd.get_dummies(df_clean_2['EDUCATION_CAT'])
# print(edu_ohe.head(10))

df_with_ohe = pd.concat([df_clean_2, edu_ohe], axis=1)
# print(df_with_ohe[['EDUCATION_CAT', 'Graduate School', 'High School', 'University', 'Others']].head(10)
# )

df_with_ohe.to_csv(r'C:\Users\higor\Desktop\Projetos Python\datascience_projects\df_with_ohe.csv', index=False)
