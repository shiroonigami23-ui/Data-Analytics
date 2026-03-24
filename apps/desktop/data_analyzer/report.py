import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


def format_report(report: Dict[str, Any]) -> str:
    shape = report.get("shape", {})
    lines = [
        "Data Analytics Report",
        f"File: {report.get('file')}",
        f"Rows: {shape.get('rows', 0)}",
        f"Columns: {shape.get('columns', 0)}",
        f"Duplicate Rows: {report.get('duplicate_rows', 0)}",
        "",
        "Top Correlations:",
    ]
    correlations = report.get("top_correlations", [])
    if not correlations:
        lines.append("- Not enough numeric columns.")
    else:
        for c in correlations:
            lines.append(f"- {c['x']} <-> {c['y']}: {c['corr']:.4f}")
    lines.append("")
    lines.append("Anomaly Counts (z-score > 3):")
    anomalies = report.get("anomaly_counts", {})
    if not anomalies:
        lines.append("- No numeric columns available.")
    else:
        for key, value in anomalies.items():
            lines.append(f"- {key}: {value}")
    return "\n".join(lines)


def save_report_json(report: Dict[str, Any], output_path: str) -> str:
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "report": report,
    }
    out = Path(output_path).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return str(out)
