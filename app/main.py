import os
import streamlit as st
import pandas as pd
from app.lida_utils import LidaManager

def render_summary(summary_json):
    st.markdown(f"**Dataset Name:** {summary_json.get('name', '')}")
    st.markdown(f"**Description:** {summary_json.get('dataset_description', '')}")
    for field in summary_json.get('fields', []):
        col = field.get('column', '')
        props = field.get('properties', {})
        st.markdown(f"### {col}")
        st.markdown(f"*{props.get('description', '')}*")
        card_body = ""
        for k, v in props.items():
            if k != 'description':
                card_body += f"**{k}:** {v}  "
        st.info(card_body)

st.title("LIDA demonstration")
st.write("Automatic Generation of Visualizations and Infographics using Large Language Models")

openai_api_key = os.environ.get("OPENAI_API_KEY")
if not openai_api_key:
    st.error("OPENAI_API_KEY environment variable not found. Please set it before running the app.")
    st.stop()

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file is None:
    st.info("Please upload a CSV file to continue.")
    st.stop()

df = pd.read_csv(uploaded_file)
st.subheader("Preview of top 15 rows of uploaded data")
st.dataframe(df.head(15))

lida_mgr = LidaManager(openai_api_key)
if st.button("Summarize"):
    summary_json = lida_mgr.summarize(df)
    render_summary(summary_json)