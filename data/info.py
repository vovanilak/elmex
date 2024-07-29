import pandas as pd
import numpy as np
import math
def get_role(articul):
    df = pd.read_excel('data/elmex.xlsx', sheet_name='Тариф')
    row = df.loc[df['Артикул'] == articul].to_dict(orient="records")[0]
    row['Артикул'] = int(row['Артикул'])
    result=""
    yup=list(row.keys())
    for u in range(0, len(yup), 2):
        if not yup[u].startswith('Unnamed') and isinstance(row[yup[u]], (str, int, float)):
            if isinstance(row[yup[u]], float) and math.isnan(row[yup[u]]):
                continue
            result+=f"<b>{yup[u]}</b>\n{row[yup[u]]} - {row[yup[u+1]]}\n\n"
            
    return result

if __name__ == "__main__":
    print(get_role(4313450000))
    
    
    