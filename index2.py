import streamlit as st
import pandas as pd
import json
import openai
from helm.common.authentication import Authentication
from helm.common.request import Request, RequestResult
from helm.proxy.services.remote_service import RemoteService
import problems
import prompts
import sub
import constraints
from main import one_off
import pyperclip


## auth -- 
helm_key = open('apikeys.txt').readlines()[0].strip()
open_api_key = open('apikeys.txt').readlines()[1].strip()

openai.api_key = open_api_key
auth = Authentication(api_key=helm_key)
service = RemoteService("https://crfm-models.stanford.edu")
###


###global vars 
initial_themes = ["sports", "cats", "unicorns", "art"]
initial_question = {
"question": "There were 28 bales of hay in the barn. Tim stacked more bales in the barn today. There are now 54 bales of hay in the barn. How many bales did he store in the barn ?",
"generic": "There were ___A___ bales of hay in the barn. Tim stacked more bales in the barn today. There are now ___B___ bales of hay in the barn. How many bales did he store in the barn ?",
"numbers": [
    28,
    54
],
"constraints": "A=randint(20,40)\nB=randint(40,50)\nanswer= B - A",
"lEquations": [
    "28+x=54"
],
"lSolutions": [
    26.0
],
"grammarCheck": 0,
"templateNumber": 0,
"sQuestion": "There were 28 bales of hay in the barn. Tim stacked more bales in the barn today. There are now 54 bales of hay in the barn. How many bales did he store in the barn ?",
"iIndex": 1
}
###

def stWriteWordProblem(problem, critique, id, theme):
    c1_, c2_, c3_= st.columns([5, 1, 1])
    # with c0_:
    #     st.write("<h3 style='text-align: center; visibility: hidden;'>"+str(id)+"</h3>", unsafe_allow_html=True)
    with c1_:
        st.write(problem)
    with c2_:
        st.write("<p style='text-align: center;'>"+theme+"</p>", unsafe_allow_html=True)
    with c3_:
        if critique:
            text = "⚠️"
            st.write("<p style='text-align: center;'>"+text+"</p>", unsafe_allow_html=True)
        else:
            text = "✅"
            st.write("<p style='text-align: center;'>"+text+"</p>", unsafe_allow_html=True)


def fillProblemTable(problem, constraints, new_theme):
    vars = ""
    problem = problem.strip() ## clean whitespace
    for var in constraints:
        vars += var + " = " + str(constraints[var])
        if var != "answer":
            vars +=  ", "
  
    return {"Generic Problem": problem, "Contraints": vars, "Theme": new_theme}

# Input like A = 28, B = 54, answer = ?
# return like A=30|B=40|answer=10
def generate_contraint_key(constraints) -> str:
    no_space = constraints.replace(" ", "")
    res = no_space.replace(",", "|")
    return res

def generate_word_problems(): ## make themes global state? need constraints
    with text_spinner_placeholder:
        with st.spinner("Generating new questions..."):
            themes = st.session_state.theme_input.split(",")
            theme_results_dict = {}

            for index, [generic_form, c] in subbed_df.iterrows():
                constraints_ = c
                constraints_key = generate_contraint_key(constraints_)
                for theme in themes:
                    problem = st.session_state.input_problems[index]
                    results = one_off(problem, theme, constraints_key, helm_key)
                    [rewritten, critique, revision, intro, combined, answer, generic] = results
                    theme_results_dict[(index, theme)] = results

            #display problems
            st.session_state.problems = theme_results_dict


# def processInputForm(themes):
#     themes = themes.split(",")
#     generic_table_rows = []
#     theme_results_dict = {} # stores str -> list. Associating theme to results from one_off()
#     for theme in themes:
#         c = constraints.parse_constraints(initial_question['constraints'])
#         constraints_key = generate_contraint_key(c) 
#         problem = initial_question["question"]
#         results = one_off(problem, theme, constraints_key, helm_key)
#         [rewritten, critique, revision, intro, combined, answer, generic ] = results
#         theme_results_dict[theme] = results
#         generic_table_rows.append(fillProblemTable(generic, c, theme))

#     #display generic table
#     st.session_state.generic_table = generic_table_rows
#     st.session_state.problems = theme_results_dict

#     theme_id = 0 # for check box purposes
#     return theme_results_dict


# def main(doc, theme_input): 
#     with text_spinner_placeholder:
#         with st.spinner("Generating new problems..."):
#             theme_results_dict = processInputForm(theme_input)

def generate_generic_table(doc, theme_input): #used to have theme_input as param
    st.session_state.input_problems.append(doc)
    generic, og_numbers = sub.problem_to_generic(doc)
    c = constraints.default_constraint_text(og_numbers)
    st.session_state.generic_table.append((generic, c))
    st.session_state.theme_input = theme_input

def batch_input_problems():
    # first clear previous tables
    reset_params()

    themes = st.session_state.theme_input.split(",")
    for index, problem in gdf.iterrows():
        generate_generic_table(problem["Problem Description"], themes)

### state variables
if "input_problems" not in st.session_state:
    st.session_state.input_problems = []
if "generic_table" not in st.session_state:
    st.session_state.generic_table = []
if "problems" not in st.session_state:
    st.session_state.problems = {} #theme -> one_off res
if "theme_input" not in st.session_state:
    st.session_state.theme_input = ""

def reset_params():
    st.session_state.generic_table = []
    st.session_state.problems = {} 


# Set page title
st.title("Math Word Problem Generator")
# cfrm_key = st.text_input("cfrm key")
with st.expander("**Instructions**"):
    instructs = '''
    <ol>
        <li>Select whether you would like to add problems one at a time, or in a batch</li>
        <li>If you select “Single”
            <ul>
                <li>Enter a word problem in the text area</li>
                <li>Enter a desired themes for your problem to be converted to (I.e sports, cats, unicorns)</li>
                <li>Select whether or not you would like each word problem to have an introduction (an introduction adds a little bit more background story to the word problems)</li>
            </ul>
        </li>
        <li>If you select “Batch”
            <ul>
                <li>Enter or copy and paste each word problem into a new line in the data Fram</li>
                <li>Enter a desired themes for your problem to be converted to (I.e sports, cats, unicorns)</li>
                <li>Select whether or not you would like each word problem to have an introduction (an introduction adds a little bit more background story to the word problems)</li>
            </ul>
        </li>
        <li>Press “Process Input Word Problem”</li>
        <li>Make any desired changes to the generic form or constraints generated for your problem(s)</li>
        <li>Press “Generate New Word Problems”</li>
        <li>Review Outputted Problems. Problems requiring revision will be flagged.</li>
    </ol>
    '''
    st.markdown(instructs, unsafe_allow_html=True)
    
st.subheader('Input Word Problem')
problem_mode = st.radio(
    "Single or Batch Input?",
    ('Single', 'Batch'), on_change= reset_params)

if problem_mode == 'Single':
    with st.container():
        c1, c2 = st.columns([3, 1])
        with c1:
            doc = st.text_area("Enter a word problem here", height = 150, value = initial_question["question"])
        with c2:
            theme_input = st.text_input("Enter new theme(s)", value = ", ".join(initial_themes))
            intro_checkbox_result = st.checkbox('Include problem introduction')
    
        single_submit_btn = st.button(
            label="Process Input Word Problem",
            type="primary",
            on_click=generate_generic_table,
            args = (doc, theme_input)
        )
else:
    df_info = {"Problem Description": [initial_question["question"]]}
    df = pd.DataFrame(df_info)
    gdf = st.experimental_data_editor(df, use_container_width=True, num_rows= "dynamic")
    # theme_input = st.text_input("Enter new theme(s)", value = ", ".join(initial_themes))
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
        use_container_width=True
    )
    
    theme_input = [x for _, x in versions.to_dict()["themes"].items()]
    theme_input = ", ".join(theme_input)
    intro_checkbox_result = st.checkbox('Include Problem Introduction')
    st.session_state.theme_input = theme_input

    batch_submit_btn = st.button(
            label="Process Input Word Problems",
            type="primary",
            on_click= batch_input_problems,
            # args = (str(theme_input))
        )




if st.session_state.generic_table:
     #display generic table
    st.subheader('Generic Problem and Contraints')
    subbed_df = st.experimental_data_editor(
    pd.DataFrame(
        [
            {"Generic Form": x[0], "Constraints": x[1]}
            for x in st.session_state.generic_table
        ],
    ),
    num_rows="fixed",
    use_container_width=True, key = "gdf"
    )

    generate_problems_btn = st.button(
        label="Generate New Word Problems",
        type="primary",
        on_click=generate_word_problems,
        # args = subbed_df
    )

text_spinner_placeholder = st.empty()

if st.session_state.problems:
    st.subheader('New Problems')
    tabs = st.tabs([x for _, x in versions.to_dict()["version"].items()])
    for i, tab in enumerate(tabs):
        with tab:
            h1, h2, h3= st.columns([5, 1, 1])
            # with h0:
            #     st.write("<p style='text-align: center; visibility: hidden;'>"+"0"+"</p>", unsafe_allow_html=True)
            with h1:
                st.write("<p style='text-align: center;font-weight: bold;'>"+"Problem Description"+"</p>", unsafe_allow_html=True)
            with h2:
                st.write("<p style='text-align: center;font-weight: bold;'>"+"Theme"+"</p>", unsafe_allow_html=True)
                # st.write("<p>"+"Theme"+"</p>", unsafe_allow_html=True)
            with h3:
                st.write("<p style='text-align: center;font-weight: bold;'>"+"Status"+"</p>", unsafe_allow_html=True)

            theme_id = 0
            problems_to_copy = ""
            for index,theme in st.session_state.problems:
                results = st.session_state.problems[(index,theme)]
                [rewritten, critique, revision, intro, combined, answer, generic ] = results
                problem = revision if revision else rewritten
                if intro_checkbox_result:
                    problem = intro + " " + problem

                stWriteWordProblem(problem, critique, theme_id, theme)
                theme_id += 1
                problems_to_copy += problem + "\n"

            if st.button("Copy Problems to clipboard"):
                pyperclip.copy(problems_to_copy)
                st.success("Problems copied to clipboard!")









