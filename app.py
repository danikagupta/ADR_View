import warnings
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import streamlit as st
import csv
import base64
from PIL import Image

drug_smiles={}

def yes_no(s):
  if(int(s)>0):
    return "Yes"
  return ""

def get_dict(fname):
  global drug_smiles
  dd={}
  keys_to_skip=['drug','SMILES']
  with open(fname) as f:
    DictReader_obj=csv.DictReader(f)
    for item in DictReader_obj:
      new_dict={k: yes_no(v) for k,v in item.items() if k not in keys_to_skip}
      drug_name=item['drug']
      dd[drug_name]=new_dict
      if 'SMILES' in item.keys():
        smiles=item['SMILES']
        drug_smiles[drug_name]=smiles
  return dd


def list_side_effects(dict_row):
  l=[]
  print(f"Processing row {dict_row}")
  for k,v in dict_row.items():
    if k not in ['drug','SMILES']:
      if(int(v)>0):
        l.append(k)
  print(f"About to return {l} for {dict_row}")
  return l

def show_record(drug_name):
  ac=drugs_actual[drug_name]
  kg=drugs_kg[drug_name]
  mt=drugs_mt[drug_name]
  en=drugs_en[drug_name]
  df=pd.DataFrame({
                   'Actual Side-effects':pd.Series(ac),
                   'Ensemble':pd.Series(en),
                   'Multi-Task':pd.Series(mt),
                   'Knowledge Graph':pd.Series(kg),
                   })
  st.table(df)


def get_video_code(drug_name):
  #file_ = open(f"/Users/amitamit/Documents/Code/Python/Streamlit/adr_synopsys2023/{drug_name}.gif", "rb")
  file_ = open(f"data/{drug_name}.gif", "rb")
  contents = file_.read()
  data_url = base64.b64encode(contents).decode("utf-8")
  file_.close()
  return data_url

drugs_actual=get_dict('data/drugs_actual.csv')
drugs_kg=get_dict('data/drugs_kg.csv')
drugs_mt=get_dict('data/drugs_mt.csv')
drugs_en=get_dict('data/drugs_en.csv')
drug_list=drug_smiles.keys()

drug_chosen = st.selectbox('Pick a drug', options=drug_list)
print(f"Drug chosen is {drug_chosen}")
d_url=get_video_code(drug_chosen)

with st.container():
  col1,col2=st.columns(2)
  col1.title(f"{drug_chosen}")
  col1.header(f"{drug_smiles[drug_chosen]}")

  col2.markdown(
    f'<img src="data:image/gif;base64,{d_url}" alt="molecule structure" width=600>',
    unsafe_allow_html=True,
  )
#st.sidebar.title("RAW DATA")
#st.sidebar.json(drugs_actual)
#st.sidebar.json(drugs_kg)
#st.sidebar.json(drugs_mt)
#st.sidebar.json(drugs_en)
with st.container():
  show_record(drug_chosen)


