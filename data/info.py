import pandas as pd
def get_role(articul):
    df = pd.read_excel('data/elmex.xlsx', sheet_name='Тариф')
    print(df.columns)
    row = df.loc[df['Артикул'] == articul].to_dict(orient="records")[0]
    result=""
    yup=list(row.keys())
    for u in range(len(yup)):
        if yup[u].startswith('Unnamed'):
            #проверка начала названия колонки
            result+=f' - {row[yup[u]]}\n'

        else:
            result+=f'\n{yup[u]}\n{row[yup[u]]}'
    return result
print(get_role(1103270240))



    
    
    
    
    