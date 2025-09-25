## Requirements
- Python 3.11+
- Virtual environment recommended

## Setup
1. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. **Install dependencies:**
   No external dependencies required (uses Python standard library).

## Usage
Run the script to generate mock data:
```bash
python scripts/generate_mock_data.py
```

### Optional Arguments
- `--start-date YYYY-MM-DD` : Start date for data generation
- `--end-date YYYY-MM-DD`   : End date for data generation
- `--rows N`                : Number of rows to generate

**Example:**
```bash
python scripts/generate_mock_data.py --start-date 2025-09-01 --end-date 2025-09-25 --rows 100
```

## Output
- The generated CSV file is saved as `data/mock_retail_data.csv`.

## Project Structure
```
LIDA/
├── data/
│   └── mock_retail_data.csv
├── scripts/
│   └── generate_mock_data.py
└── README.md
```
