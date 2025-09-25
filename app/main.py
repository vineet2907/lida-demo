import streamlit as st
import pandas as pd

st.title("LIDA demonstration")
st.write("Automatic Generation of Visualizations and Infographics using Large Language Models")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file is None:
    st.info("Please upload a CSV file to continue.")
    st.stop()

df = pd.read_csv(uploaded_file)
st.subheader("Preview of top 15 rows of uploaded data")
st.dataframe(df.head(15))
