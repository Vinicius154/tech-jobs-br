import ast
import logging

import pandas as pd

from tech_jobs_br.config import PROCESSED_DIR, RAW_DIR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)


def parse_tags(value: str | list) -> list[str]:
    if isinstance(value, list):
        return value
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return []


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    files = list(RAW_DIR.glob("*.csv"))
    if not files:
        log.error("Nenhum arquivo encontrado em %s. Rode o scraper primeiro.", RAW_DIR)
        return

    df = pd.concat(
        [pd.read_csv(f) for f in files],
        ignore_index=True,
    )

    df = df.drop_duplicates(subset="id").assign(
        tags=lambda d: d["tags"].map(parse_tags),
        category=lambda d: d["category"].str.strip().str.title(),
        publication_date=lambda d: (
            pd.to_datetime(d["publication_date"], errors="coerce").dt.date
        ),
    )

    output = PROCESSED_DIR / "jobs_clean.csv"
    df.to_csv(output, index=False)
    log.info("%d vagas limpas -> %s", len(df), output)


if __name__ == "__main__":
    main()
