import ast
import logging
from collections import Counter

import pandas as pd
import plotly.express as px

from tech_jobs_br.config import CHARTS_DIR, PROCESSED_DIR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

DARK_LAYOUT = dict(
    plot_bgcolor="#0d1117",
    paper_bgcolor="#0d1117",
    font_color="#cccccc",
    showlegend=False,
)


def to_list(v: str | list) -> list[str]:
    if isinstance(v, list):
        return v
    try:
        return ast.literal_eval(v)
    except Exception:
        return []


def chart_top_categories(df: pd.DataFrame) -> None:
    top = df["category"].value_counts().head(10).reset_index()
    top.columns = ["Categoria", "Vagas"]
    fig = px.bar(
        top,
        x="Vagas",
        y="Categoria",
        orientation="h",
        title="Top 10 Categorias de Vagas Tech Remotas",
        color="Vagas",
        color_continuous_scale="Blues",
        template="plotly_dark",
    )
    fig.update_layout(**DARK_LAYOUT)
    output = CHARTS_DIR / "top_categories.png"
    fig.write_image(output, width=900, height=500)
    log.info("✓ %s", output)


def chart_top_technologies(df: pd.DataFrame) -> None:
    all_tags = [tag for tags in df["tags"].map(to_list) for tag in tags]
    top = pd.DataFrame(Counter(all_tags).most_common(15), columns=["Tech", "Menções"])
    fig = px.bar(
        top,
        x="Menções",
        y="Tech",
        orientation="h",
        title="Tecnologias Mais Pedidas em Vagas Remotas",
        color="Menções",
        color_continuous_scale="Teal",
        template="plotly_dark",
    )
    fig.update_layout(**DARK_LAYOUT)
    output = CHARTS_DIR / "top_technologies.png"
    fig.write_image(output, width=900, height=500)
    log.info("✓ %s", output)


def main() -> None:
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    processed = PROCESSED_DIR / "jobs_clean.csv"

    if not processed.exists():
        log.error("Arquivo não encontrado: %s. Rode o cleaner primeiro.", processed)
        return

    df = pd.read_csv(processed)
    chart_top_categories(df)
    chart_top_technologies(df)


if __name__ == "__main__":
    main()
