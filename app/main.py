import logging
import os
import sys
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from lida_utils import LidaManager

def render_summary(summary):
    logger.info("Rendering summary")
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
    logger.info("Rendering goals")
    goal_questions = [goal.question for goal in goals]
    st.selectbox('Choose a generated goal', options=goal_questions, index=None, key="goal_selectbox", accept_new_options=True, on_change=handle_goal_selection_change)

def handle_goal_selection_change():
    selected_goal = st.session_state.goal_selectbox
    if selected_goal:
        goal_questions = [goal.question for goal in lida_mgr.goals]
        selected_goal_index = goal_questions.index(selected_goal)
        lida_mgr.update_goal_selection(lida_mgr.goals[selected_goal_index])

def render_chart(code):
    import matplotlib.pyplot as plt
    local_ns = {'df': df, 'data': df, 'plt': plt, 'pd': pd}
    exec(code, local_ns)
    if 'plot' in local_ns:
        local_ns['plot'](df)
        st.pyplot(plt.gcf())
    else:
        st.warning("No plot function found in the generated code.")

def render_chart_as_image(raster):
    logger.info("Rendering chart as image")
    if raster:
        from PIL import Image
        import io
        import base64

        imgdata = base64.b64decode(raster)
        img = Image.open(io.BytesIO(imgdata))
        st.image(img, use_container_width=True, width="stretch")
    else:
        st.warning("No plot function found in the generated code.")

load_dotenv()

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")
st.title("LIDA demonstration")
st.write("Automatic Generation of Visualizations and Infographics using Large Language Models")

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("OPENAI_API_KEY environment variable not found.")
    st.stop()

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"], key="uploaded_file")
if uploaded_file is None:
    st.info("Please upload a CSV file to continue.")
    if "lida_mgr" in st.session_state:
        logger.info("Clearing session state")
        st.session_state.lida_mgr = None
    st.stop()

if "lida_mgr" not in st.session_state or st.session_state.lida_mgr is None:
    logger.info("Setting session state")
    st.session_state.lida_mgr = LidaManager(openai_api_key)

lida_mgr = st.session_state.lida_mgr

df = pd.read_csv(uploaded_file)
st.write("Preview (top 15 rows)")
st.dataframe(df.head(15), hide_index=True)

summarize_tab, goals_tab, viz_tab = st.tabs(["Summary", "Goals", "Visualizations"])

with summarize_tab:
    if lida_mgr.summary is None:
        with st.spinner("Generating summary with LIDA..."):
            lida_mgr.summarize(df)
    render_summary(lida_mgr.summary)

with goals_tab:
    if lida_mgr.summary:
        if len(lida_mgr.example_personas) == 0:
            with st.spinner("Generating example personas..."):
                lida_mgr.personas()
        persona = st.text_input("Enter persona for goal generation")
        st.write("Example personas:")
        for p in lida_mgr.example_personas:
            st.write(f"- **{p.persona}**: {p.rationale}")
        if persona:
            if lida_mgr.persona != persona or not lida_mgr.goals:
                with st.spinner("Generating goals for persona..."):
                    lida_mgr.generate_goals(persona)
            render_goals(lida_mgr.goals, lida_mgr.selected_goal)
            if lida_mgr.selected_goal:
                st.write(lida_mgr.selected_goal.rationale)
                st.write(lida_mgr.selected_goal.visualization)
    else:
        st.info("Please generate the summary in the 'Summarize' tab first to enable goals.")

with viz_tab:
    if lida_mgr.selected_goal:
        st.write(f"**{lida_mgr.persona}**")
        goal = lida_mgr.selected_goal
        st.write(goal.question)
        st.write(goal.rationale)
        st.write(goal.visualization)
        if lida_mgr.selected_visualization is None:
            lida_mgr.chart()
        chart, chart_edits = st.columns([2, 1])
        with chart_edits:
            if lida_mgr.selected_visualization:
                modifications = st.text_area(
                    "Enter any modifications you want in the generated chart (e.g., change color, add title, etc.). Each modification should be on a separate line.",
                    value="",
                    key="chart_modifications"
                )
                if st.button("Apply Modifications"):
                    mod_list = [m.strip() for m in modifications.splitlines() if m.strip()]
                    if mod_list:
                        with st.spinner("Editing visualization..."):
                            lida_mgr.edit_chart(mod_list)
                        st.write("You requested the following modifications:")
                        for mod in mod_list:
                            st.write(f"- {mod}")
            else:
                st.warning("No visualization found for selected goal.")
        with chart:
            if lida_mgr.selected_visualization:
                if len(lida_mgr.evaluations) == 0:
                    with st.spinner("Evaluating visualization and repairing if required..."):
                        lida_mgr.evaluate()
                        lida_mgr.repair(lida_mgr.evaluations[0])
                #render_chart(lida_mgr.chart_code)
                render_chart_as_image(lida_mgr.selected_visualization.raster)
        
        with st.expander("Visualization Code", expanded=False):
            st.code(lida_mgr.selected_visualization.code, language='python')
            if len(lida_mgr.evaluations) > 0:
                for eval in lida_mgr.evaluations:
                    st.write("Evaluation:")
                    eval_df = pd.DataFrame(eval)
                    st.dataframe(eval_df, hide_index=True)
                
        with st.expander("Recommendations", expanded=False):
            if st.button("Generate / Refresh Recommendations"):
                with st.spinner("Generating recommendations..."):
                    recommendations = lida_mgr.recommend()
                if recommendations:
                    for rec in recommendations:
                        if rec.raster:
                            #render_chart(rec.code)
                            render_chart_as_image(rec.raster)
                else:
                    st.write("No recommendations available.")
    else:
        st.info("Select a goal in the 'Goals' tab to enable visualizations.")