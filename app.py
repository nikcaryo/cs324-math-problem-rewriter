import streamlit as st
import pandas as pd
import numpy as np
import sub
import constraints
import json
from st_aggrid import AgGrid


# info

# # for genericizing problems and extracting original numbers
# sub.problem_to_generic("there is 1 dog") -> ("there is ___A___ dog", [1])
# sub.generic_to_problem("there is ___A___ dog", [1]) -> there is 1 dog
# TODO: use something besides ___ underscores since it gets interpreted as italics

# # with those, we can set some hard constraints (e.g. {'A': 1})
# # the user can then loosen those via randint() and python math expressions e.g.
# constraints.parse_constraints("A=randint(20,40)\nB=2*A\nanswer= 2 * A - B") ->  {'A': 23, 'B': 46, 'answer': 0}

# # for a full prompt pipeline, see main.py

# basic flow
# - generic, original_numbers = sub.problem_to_generic(problem) # Ben had 3 dogs. He got 2 more. How many does he have
# - rewritten_generic, critique (if any) = rewrite_and_revise(generic, theme) # revised: Stacy has 3 cats, rewritten: Stacy the Crazy Cat lady has 3 cats. How many does she have, critique: Crazy cat lady is a harmful term
# - intro = add_intro(rewritten_generic) # (nice to have)
# - new_numbers = parse_constraints(constraints) # 3->4
# - rewritten = sub.generic_to_problem(rewritten_generic, new_numbers)
# - final result = (rewritten, new answer, GPT generated critiques we had/have for this problem)


TITLE = "CS 324"
cfrm_key = st.text_input("cfrm key")

problems = json.load(open("problems.json"))
with open("questions_with_generics_50.json") as f:
    questions = json.load(f)
df = pd.DataFrame(
    [{"original problem": q["question"]} for _, q in list(questions.items())[:5]]
)

# AgGrid has some nice extra features like download as CSV/Excel and stuff
edited_df = st.experimental_data_editor(df, num_rows="dynamic")

# st.session_state is how we can manage things being edited etc?
# st.session_state['original problems'] = []
# def set_og_problems():
#   st.session_state['original problems'] =


# st.button('set problems', on_click=set_og_problems)

# st.warning('This is a warning', icon="⚠️")
print()
generic_and_nums = list(
    sub.problem_to_generic(x)
    for _, x in edited_df.to_dict()["original problem"].items()
    if x
)
subbed_df = st.experimental_data_editor(
    pd.DataFrame(
        [
            {"generic": x[0], "constraints": constraints.default_constraint_text(x[1])}
            for x in generic_and_nums
        ],
    ),
    num_rows="fixed",
)

versions = st.experimental_data_editor(
    pd.DataFrame(
        [
            {
                "version": "stem",
                "themes": "science, technology, computers, biology, environment, engineering",
            },
            {
                "version": "fantasy",
                "themes": "unicorns, fairies, warlocks, hobbits, elves",
            },
        ]
    ),
    num_rows="dynamic",
)
import time

tabs = st.tabs([x for _, x in versions.to_dict()["version"].items()])
for i, tab in enumerate(tabs):
    with tab:

      # trigger this with a button or something?
      with st.spinner(text='In progress'):
        for problem in subbed_df.to_records():
          print(problem)
          # do stuff here
          problem[1]
          time.sleep(1)
        st.success('Done')