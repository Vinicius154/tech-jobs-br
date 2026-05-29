import logging
from datetime import datetime

import httpx
import pandas as pd

from tech_jobs_br.config import (
    API_URL,
    COLUMNS,
    KEYWORDS,
    LIMIT,
    RAW_DIR,
    TIMEOUT,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)


def fetch_jobs(
    client: httpx.Client, keyword: str, collected_at: str
) -> pd.DataFrame | None:
    try:
        response = client.get(
            API_URL,
            params={"search": keyword, "limit": LIMIT},
        )
        response.raise_for_status()
        jobs = response.json().get("jobs", [])

        if not jobs:
            log.warning("Nenhuma vaga encontrada para '%s'", keyword)
            return None

        return (
            pd.DataFrame(jobs)
            .reindex(columns=COLUMNS)  # Caso a API mude.
            .assign(
                keyword=keyword,
                collected_at=collected_at,
            )
        )

    except httpx.HTTPStatusError as e:
        log.error("HTTP %s ao buscar '%s': %s", e.response.status_code, keyword, e)
    except httpx.RequestError as e:
        log.error("Erro de conexão ao buscar '%s': %s", keyword, e)

    return None


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    collected_at = datetime.now().strftime("%Y-%m-%d")

    frames: list[pd.DataFrame] = []

    with httpx.Client(timeout=TIMEOUT) as client:
        for keyword in KEYWORDS:
            log.info("Coletando vagas para '%s'...", keyword)
            df = fetch_jobs(client, keyword, collected_at)
            if df is not None:
                frames.append(df)

    if not frames:
        log.error("Nenhuma vaga coletada. Verifique a API e tente novamente.")
        return

    result = pd.concat(frames, ignore_index=True).drop_duplicates(subset="id")

    output = RAW_DIR / f"jobs_{collected_at}.csv"
    result.to_csv(output, index=False)
    log.info("%d vagas salvas -> %s", len(result), output)


if __name__ == "__main__":
    main()
