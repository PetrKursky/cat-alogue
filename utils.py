from thefuzz import fuzz, process
import pandas as pd

from pydantic import BaseModel,Field,HttpUrl
from typing import Optional


# Object representing a cat
# used by detail.py to generate web-form
class CatModel(BaseModel):
    name:str
    sex:str
    age:float
    img_uri:HttpUrl

    def from_df_record(df_record):
        return CatModel(
            name=df_record['name'],
            sex = df_record['sex'],
            age = df_record['age'],
            img_uri = df_record['img_uri']
        )
    
def search_all(df, query, top_n = 5): 
    scores = process.extract(
        query, 
        df['_concatenated'], 
        scorer=fuzz.partial_ratio,
        limit=top_n
    )
    
    ids = [ score[-1] for score in scores ]
        
    return df.iloc[ids]
    

def load_data():
    df = pd.read_csv('data.csv')
    # create column for fuzzy search
    df['_concatenated'] = pd.Series(df.astype(str).fillna('').values.tolist()).str.join(' ')
    return df

def save_data(df):
    # drop the column so it doesn't pollute the search
    df = df.drop(columns=['_concatenated'])
    df.to_csv('data.csv', index=False)
