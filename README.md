# LIDA Retail Data Analytics App

This project demonstrates an AI-powered data analytics app using [LIDA](https://github.com/microsoft/lida), OpenAI, and Streamlit.

## Features
- Summarize dataset using LIDA and OpenAI GPT models

## Setup
1. **Clone the repository**
2. **Create and activate a Python virtual environment:**
   ```zsh
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies:**
   ```zsh
   pip install -r requirements.txt
   ```
4. **Set your OpenAI API key as an environment variable:**
   ```zsh
   export OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage
Run the Streamlit app:
```zsh
streamlit run app/main.py
```
