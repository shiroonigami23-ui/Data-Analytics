import json
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd


def _load_table(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix == ".json":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return pd.DataFrame(data)
        if isinstance(data, dict):
            return pd.json_normalize(data)
    raise ValueError(f"Unsupported file type: {suffix}. Use CSV or JSON.")


def _top_correlations(df: pd.DataFrame, limit: int = 5) -> List[Dict[str, Any]]:
    numeric = df.select_dtypes(include=["number"])
    if numeric.shape[1] < 2:
        return []
    corr = numeric.corr(numeric_only=True).abs()
    pairs = []
    cols = list(corr.columns)
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            pairs.append((cols[i], cols[j], float(corr.iloc[i, j])))
    pairs.sort(key=lambda x: x[2], reverse=True)
    return [{"x": x, "y": y, "corr": v} for x, y, v in pairs[:limit]]


def _anomaly_counts(df: pd.DataFrame, z_threshold: float = 3.0) -> Dict[str, int]:
    result: Dict[str, int] = {}
    numeric = df.select_dtypes(include=["number"])
    if numeric.empty:
        return result
    for col in numeric.columns:
        series = numeric[col].dropna()
        if series.empty:
            result[col] = 0
            continue
        std = series.std()
        if std == 0 or pd.isna(std):
            result[col] = 0
            continue
        z_scores = ((series - series.mean()) / std).abs()
        result[col] = int((z_scores > z_threshold).sum())
    return result


def analyze_file(path_str: str) -> Dict[str, Any]:
    path = Path(path_str).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    df = _load_table(path)
    numeric = df.select_dtypes(include=["number"])

    hashable_df = df.copy()
    for col in hashable_df.columns:
        hashable_df[col] = hashable_df[col].apply(
            lambda x: json.dumps(x, sort_keys=True) if isinstance(x, (list, dict)) else x
        )

    report = {
        "file": str(path),
        "shape": {"rows": int(df.shape[0]), "columns": int(df.shape[1])},
        "columns": df.columns.tolist(),
        "missing_values": {k: int(v) for k, v in df.isna().sum().to_dict().items()},
        "duplicate_rows": int(hashable_df.duplicated().sum()),
        "numeric_summary": numeric.describe(include="all").to_dict() if not numeric.empty else {},
        "top_correlations": _top_correlations(df),
        "anomaly_counts": _anomaly_counts(df),
    }
    return report
