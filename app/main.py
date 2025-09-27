import os
import streamlit as st
import pandas as pd
from lida_utils import LidaManager

def render_summary(summary):
    if "name" in summary:
        st.write(f"**Dataset Name:** {summary['name']}")
    
    if "dataset_description" in summary:
        st.write(summary["dataset_description"])

    if "fields" in summary:
        fields = summary["fields"]
        nfields = []
        for field in fields:
            flatted_fields = {}
            flatted_fields["column"] = field["column"]
            for row in field["properties"].keys():
                if row != "samples":
                    flatted_fields[row] = field["properties"][row]
                else:
                    flatted_fields[row] = str(field["properties"][row])
            nfields.append(flatted_fields)
        nfields_df = pd.DataFrame(nfields)
        st.write(nfields_df)
    else:
        st.write(str(summary))

def render_goals(goals, selected_goal=None):
    goal_questions = [goal.question for goal in goals]
    selected_goal = st.selectbox('Choose a generated goal', options=goal_questions, index=0)
    selected_goal_index = goal_questions.index(selected_goal)
    st.write(goals[selected_goal_index].rationale)
    st.write(goals[selected_goal_index].visualization)
    return goals[selected_goal_index]

def render_chart(code):
    import matplotlib.pyplot as plt
    local_ns = {'df': df, 'data': df, 'plt': plt, 'pd': pd}
    exec(code, local_ns)
    if 'plot' in local_ns:
        local_ns['plot'](df)
        st.pyplot(plt.gcf())
    else:
        st.warning("No plot function found in the generated code.")

st.set_page_config(layout="wide")
st.title("LIDA demonstration")
st.write("Automatic Generation of Visualizations and Infographics using Large Language Models")

openai_api_key = os.environ.get("OPENAI_API_KEY")
if not openai_api_key:
    st.error("OPENAI_API_KEY environment variable not found. Please set it before running the app.")
    st.stop()

if "lida_mgr" not in st.session_state:
    st.session_state.lida_mgr = LidaManager(openai_api_key)
lida_mgr = st.session_state.lida_mgr

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"], key="uploaded_file")
if uploaded_file is None:
    st.info("Please upload a CSV file to continue.")
    st.stop()

df = pd.read_csv(uploaded_file)
st.subheader("Preview of top 15 rows of uploaded data")
st.dataframe(df.head(15))

summarize_tab, goals_tab, viz_tab = st.tabs(["Summarize", "Goals", "Visualizations"])

with summarize_tab:
    if st.button("Generate Summary"):
        with st.spinner("Generating summary with LIDA..."):
            lida_mgr.summarize(df)
            render_summary(lida_mgr.summary)
    elif lida_mgr.summary:
        render_summary(lida_mgr.summary)

with goals_tab:
    if lida_mgr.summary:
        persona = st.text_input("Enter persona for goal generation (e.g., Store Manager, Category Manager, etc.)")
        if persona:
            if lida_mgr.persona != persona or not lida_mgr.goals:
                with st.spinner("Generating goals for persona..."):
                    lida_mgr.generate_goals(persona)
            if lida_mgr.goals:
                lida_mgr.selected_goal = render_goals(lida_mgr.goals, lida_mgr.selected_goal)
    else:
        st.info("Please generate the summary in the 'Summarize' tab first to enable goals.")

with viz_tab:
    if lida_mgr.selected_goal:
        goal = lida_mgr.selected_goal
        st.write(f"**{goal.question}**")
        st.write(goal.rationale)
        with st.spinner("Generating visualizations..."):
            vizs = lida_mgr.generate_chart()
        viz_titles = [f'Visualization {i+1}' for i in range(len(vizs))]
        selected_viz_title = st.selectbox('Choose a visualization', options=viz_titles, index=0)
        selected_viz = vizs[viz_titles.index(selected_viz_title)]
        lida_mgr.chart_code = selected_viz.code
        chart, chart_edits = st.columns([2, 1])
        with chart_edits:
            modifications = st.text_area(
                "Enter any modifications you want in the generated chart (e.g., change color, add title, etc.). Each modification should be on a separate line.",
                value="",
                key="chart_modifications"
            )
            if st.button("Apply Modifications"):
                mod_list = [m.strip() for m in modifications.splitlines() if m.strip()]
                if mod_list:
                    with st.spinner("Editing visualization..."):
                        edited_vizs = lida_mgr.edit_chart(mod_list)
                    if edited_vizs:
                        lida_mgr.chart_code = edited_vizs[0].code
                        st.write("You requested the following modifications:")
                        for mod in mod_list:
                            st.write(f"- {mod}")
                    else:
                        st.warning("No edited visualizations returned.")
        with chart:
            if lida_mgr.chart_code:
                render_chart(lida_mgr.chart_code)
            else:
                st.warning("No code found for the selected visualization.")

        with st.expander("Show Visualization Code", expanded=False):
            st.code(lida_mgr.chart_code)
    else:
        st.info("Select a goal in the 'Goals' tab to enable visualizations.")