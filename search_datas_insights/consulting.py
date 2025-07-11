# %% 

import pandas as pd
from google import genai
from google.genai import types

from config import API_KEY

read_key = API_KEY
df = pd.read_csv('../data/anomalies_bc.csv', parse_dates=['ds'])
df = pd.DataFrame(df)
print(df.head())

client = genai.Client(api_key=read_key)

def consulting_insight(df):
    
    appended = []
    for i, row in df.iterrows():
        #print(i)
        row_date = row['ds']
        row_y = row['y']
        print(f"value date: {row_date}")
        print(f"y value: {row_y}")
        response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"whats happening {row_date}, why this valuable is {row_y}?", 
                config=types.GenerateContentConfig(system_instruction="You are specialist in topic of trade balance in brazil. " \
                "I will send to you informations about trade balance days, explain to me whats happening in this days, look " \
                "for anomalies and give me insights about it"),
            )
        
        appended.append({
            'ds': row_date,
            'y': row_y,
            'insights': response.text if response.candidates else "No insights found"
        })
    
    return pd.DataFrame(appended, columns=['insights'])

insights = consulting_insight(df)
print(insights)

# %%

insights.to_csv('../data/insights.csv', index=False)
print("Insights saved to ../data/insights.csv")

# %%
