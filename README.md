# AI Powered Data Analytics

This project demonstrates an AI-powered data analytics app using [LIDA](https://github.com/microsoft/lida), OpenAI, and Streamlit.

## Features
- Upload and preview CSV data
- Summarize dataset
- Generate goals for a selected persona
- Generate and edit visualizations
- Evaluate the visualization code and view recommendations related to selected goal

## Setup
1. **Clone the repository**
2. **Create and activate a Python virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set your OpenAI API key as an environment variable:**
   ```bash
   export OPENAI_API_KEY=your_openai_api_key_here
   ```
5. **Generate mock data (optional)**
   ```bash
   python scripts/generate_mock_data.py
   ```
   Optional Arguments:
   - `start-date`: start date , default - today
   - `end-date`: end date, default - today + 30 days
   - `rows`: no. of rows to generate in the data set, default - 30
   ```bash
   python scripts/generate_mock_data.py --start-date '2025-01-13' --end-date '2025-03-31' --rows 40
   ```
   This will create a CSV file in the `data/` directory.
6. **Run the app**
   ```bash
   streamlit run app/main.py
   ```

## References
- [LIDA](https://github.com/microsoft/lida)
