import csv

import pytest

from src.cli import batch_triage
from src.ingest import build_index


@pytest.mark.llm
def test_batch_triage_writes_csv(tmp_path):
    build_index()
    input_file = tmp_path / "incidents.txt"
    input_file.write_text("site 03 backhaul link shows link down\nsite 07 has high latency\n")
    output_file = tmp_path / "results.csv"

    batch_triage(str(input_file), str(output_file))

    with open(output_file) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2
    assert rows[0]["severity"] in {"low", "medium", "high", "critical"}
    assert rows[0]["site_id"] == "site_03"
