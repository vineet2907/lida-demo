# LIDA Retail Data Analytics App

This project demonstrates an AI-powered data analytics app for retailers/CPGs using [LIDA](https://github.com/microsoft/lida), OpenAI, and Streamlit.

## Features
- Upload and preview CSV retail data
- Summarize dataset using LIDA and OpenAI GPT models
- Generate goals for a selected persona
- Select a goal and generate visualizations using LIDA
- View and execute generated matplotlib code for visualizations

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

## Generating Mock Data
To generate example retail data for testing, run:
```zsh
python scripts/generate_mock_data.py
```
This will create a CSV file in the `data/` directory.

