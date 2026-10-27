"""Unit tests for the R&D project analysis tool."""

import pandas as pd
import pytest

from src.project_analyzer import analyze_projects, load_projects


def sample_dataframe():
    return pd.DataFrame(
        {
            "project_id": ["P001", "P002"],
            "project_name": ["Example A", "Example B"],
            "planned_budget": [100_000, 200_000],
            "actual_budget": [110_000, 180_000],
            "planned_progress": [80, 50],
            "actual_progress": [70, 60],
            "planned_end_date": pd.to_datetime(["2026-12-01", "2026-11-01"]),
            "forecast_end_date": pd.to_datetime(["2026-12-11", "2026-10-25"]),
        }
    )


def test_budget_variance_and_flags():
    report = analyze_projects(sample_dataframe())
    first = report.iloc[0]
    assert first["budget_difference"] == 10_000
    assert first["budget_variance_pct"] == 10.0
    assert bool(first["over_budget"]) is True
    assert bool(first["behind_schedule_progress"]) is True
    assert first["delay_days"] == 10
    assert bool(first["forecast_delayed"]) is True


def test_under_budget_and_early_forecast():
    report = analyze_projects(sample_dataframe())
    second = report.iloc[1]
    assert second["budget_difference"] == -20_000
    assert second["budget_variance_pct"] == -10.0
    assert bool(second["over_budget"]) is False
    assert bool(second["behind_schedule_progress"]) is False
    assert second["delay_days"] == -7
    assert bool(second["forecast_delayed"]) is False


def test_load_projects_rejects_progress_above_100(tmp_path):
    csv_path = tmp_path / "invalid.csv"
    df = sample_dataframe()
    df.loc[0, "actual_progress"] = 120
    df.to_csv(csv_path, index=False)

    with pytest.raises(ValueError, match="between 0 and 100"):
        load_projects(csv_path)


def test_load_projects_rejects_duplicate_ids(tmp_path):
    csv_path = tmp_path / "duplicate.csv"
    df = sample_dataframe()
    df.loc[1, "project_id"] = "P001"
    df.to_csv(csv_path, index=False)

    with pytest.raises(ValueError, match="unique"):
        load_projects(csv_path)
