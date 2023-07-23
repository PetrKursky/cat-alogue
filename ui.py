import utils, time
import pandas as pd
from pydantic import HttpUrl

import streamlit as st 
from utils import CatModel 

# HOME page with a list of cats

# hide pages sidebar
st.set_page_config(initial_sidebar_state="collapsed")

def load_data():
    return utils.load_data()

def create_row(row,record):
    
    col1,col2 = st.columns(2)
    with col1:
        clickable_image = f"""
        <a href="/detail?id={record.Index}" target="_blank">  
            <img src="{record.img_uri}" style="width:100%;"> 
        </a>"""
        # st.image(record.img_uri)
        st.markdown(clickable_image,unsafe_allow_html=True)
    with col2:
        st.header(record.name)
        st.write(record.sex)
        st.write(record.age)

def custom_write_df(df):
    for record in df.itertuples():
        with st.container():
            row = st.columns(1)
            minus = st.empty()
            if minus.button(":heavy_minus_sign:", key=record):
                df = df[df.index != record.Index]
                df = df.reset_index(drop=True)
                st.success("Cat deleted successfully!")
                utils.save_data(df)
                minus.empty()
                continue
            create_row(row,record)
    return df

def submitted():
    st.session_state.submitted = True
def reset():
    st.session_state.submitted = False
    
# Read cats' data
df = load_data()
query = st.text_input("Search")

if st.button(":heavy_plus_sign:"):
    with st.form(key="add_cat_form"):
        name = st.text_input("Name", key="name")
        sex = st.text_input("Sex", key="sex")
        age = st.number_input("Age", key="age")
        image = st.text_input("URL Image", key="image")
        st.form_submit_button(label="Add Cat", on_click=submitted)
if 'submitted' in st.session_state:
    if st.session_state.submitted == True:
        try:
            cat = CatModel(name=st.session_state.name, sex=st.session_state.sex, age=float(st.session_state.age), img_uri=HttpUrl(st.session_state.image))
            df = df.drop(columns=['_concatenated'])
            df.loc[len(df.index)] = [cat.name, cat.sex, cat.age, cat.img_uri]
            df['_concatenated'] = pd.Series(df.astype(str).fillna('').values.tolist()).str.join(' ')
            success = st.success("New cat added successfully!")
            utils.save_data(df)
        except: st.error("Something went wrong. You probably didn't fill in the url button.")
        reset()

if query is None or query.strip() == "":
    # print all cats
    df = custom_write_df(df)
else:
    # print filtered cats only 
    df_filtered = utils.search_all(df,query)
    custom_write_df(df_filtered)
