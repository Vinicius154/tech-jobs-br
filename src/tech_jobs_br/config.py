from pathlib import Path

# API
KEYWORDS = ["python", "django", "typescript", "data science", "machine learning"]
API_URL = "https://remotive.com/api/remote-jobs"
TIMEOUT = 15.0
LIMIT = 100

# Colunas esperadas da API, reindex garante que não quebra se a API mudar
COLUMNS = [
    "id",
    "title",
    "company_name",
    "category",
    "tags",
    "job_type",
    "publication_date",
    "salary",
]

# Paths
RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
CHARTS_DIR = Path("assets")
