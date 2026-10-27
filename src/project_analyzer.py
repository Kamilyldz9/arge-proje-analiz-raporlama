"""Analyze synthetic R&D project data and export a simple report."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Allows saving charts in environments without a display.
import matplotlib.pyplot as plt
import pandas as pd


REQUIRED_COLUMNS = {
    "project_id",
    "project_name",
    "planned_budget",
    "actual_budget",
    "planned_progress",
    "actual_progress",
    "planned_end_date",
    "forecast_end_date",
}


def load_projects(csv_path: str | Path) -> pd.DataFrame:
    """Load a CSV file and validate required columns and basic numeric values."""
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"Input CSV file was not found: {path}")

    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    numeric_columns = [
        "planned_budget",
        "actual_budget",
        "planned_progress",
        "actual_progress",
    ]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="raise")

    if (df["planned_budget"] <= 0).any():
        raise ValueError("planned_budget values must be greater than zero.")

    for column in ("planned_progress", "actual_progress"):
        if not df[column].between(0, 100).all():
            raise ValueError(f"{column} values must be between 0 and 100.")

    for column in ("planned_end_date", "forecast_end_date"):
        df[column] = pd.to_datetime(df[column], errors="raise")

    if df["project_id"].duplicated().any():
        raise ValueError("project_id values must be unique.")

    return df


def analyze_projects(projects: pd.DataFrame) -> pd.DataFrame:
    """Return project-level budget, progress, schedule metrics and flags."""
    missing = REQUIRED_COLUMNS - set(projects.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    result = projects.copy()
    result["budget_difference"] = result["actual_budget"] - result["planned_budget"]
    result["budget_variance_pct"] = (
        result["budget_difference"] / result["planned_budget"] * 100
    ).round(2)
    result["progress_difference_pp"] = (
        result["actual_progress"] - result["planned_progress"]
    ).round(2)
    result["delay_days"] = (
        result["forecast_end_date"] - result["planned_end_date"]
    ).dt.days

    result["over_budget"] = result["budget_difference"] > 0
    result["behind_schedule_progress"] = result["progress_difference_pp"] < 0
    result["forecast_delayed"] = result["delay_days"] > 0

    return result


def save_budget_chart(report: pd.DataFrame, output_path: str | Path) -> None:
    """Save a bar chart comparing planned and actual budgets."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    x = range(len(report))
    width = 0.38
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar([i - width / 2 for i in x], report["planned_budget"], width, label="Planned")
    ax.bar([i + width / 2 for i in x], report["actual_budget"], width, label="Actual")
    ax.set_title("Planned vs Actual Project Budget")
    ax.set_xlabel("Project")
    ax.set_ylabel("Budget (TL)")
    ax.set_xticks(list(x))
    ax.set_xticklabels(report["project_id"], rotation=0)
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def build_report(input_path: str | Path, output_dir: str | Path) -> pd.DataFrame:
    """Load, analyze, and export the report and budget chart."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    projects = load_projects(input_path)
    report = analyze_projects(projects)

    # Keep dates readable in the exported CSV.
    report_to_save = report.copy()
    for column in ("planned_end_date", "forecast_end_date"):
        report_to_save[column] = pd.to_datetime(report_to_save[column]).dt.strftime("%Y-%m-%d")

    report_to_save.to_csv(output_dir / "analysis_report.csv", index=False)
    save_budget_chart(report, output_dir / "budget_comparison.png")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze synthetic R&D project budget, progress, and schedule data."
    )
    parser.add_argument(
        "--input",
        default="data/sample_projects.csv",
        help="Path to the input CSV (default: data/sample_projects.csv)",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="Directory for generated report files (default: outputs)",
    )
    args = parser.parse_args()

    report = build_report(args.input, args.output_dir)
    print(f"Analyzed projects: {len(report)}")
    print(f"Over budget: {int(report['over_budget'].sum())}")
    print(f"Behind schedule progress: {int(report['behind_schedule_progress'].sum())}")
    print(f"Forecast delayed: {int(report['forecast_delayed'].sum())}")
    print(f"Report saved to: {Path(args.output_dir) / 'analysis_report.csv'}")
    print(f"Chart saved to: {Path(args.output_dir) / 'budget_comparison.png'}")


if __name__ == "__main__":
    main()
