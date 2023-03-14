import streamlit as st
import pandas as pd
import numpy as np
import sub
import json
from st_aggrid import AgGrid

TITLE = 'CS 324'
problems = json.load(open('problems.json'))
with open("questions_with_generics_50.json") as f:
    questions = json.load(f)
df = pd.DataFrame([{"original problem": q['question']} for _, q in list(questions.items())[:5]])

edited_df = AgGrid(df, fit_columns_on_grid_load=True)
print([x for x in edited_df.data])
def set_og_problems():
   st.session_state['original problems'] = [sub.problem_to_generic(x) for _, x in edited_df.data.items() if x['original_problem'].strip()]


st.button('set problems', on_click=set_og_problems)

st.warning('This is a warning', icon="⚠️")
print()
subbed_df = st.experimental_data_editor([{'generic': x[0]} for x in st.session_state['original problems']], num_rows='static')
