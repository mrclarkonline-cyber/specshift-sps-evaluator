import importlib.util
from pathlib import Path
from types import SimpleNamespace

MODULE_PATH = Path("tools/pilot_intake/evidence_ledger.py")

def load_module():
    spec = importlib.util.spec_from_file_location("evidence_ledger", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_sample_evidence_ledger_has_nine_records():
    module = load_module()
    ledger = Path("tests/fixtures/buyer_artifact_simulator/sample_evidence_ledger.jsonl")
    rows = module.read_rows(ledger)
    assert len(rows) == 9
    assert {row["event_type"] for row in rows} >= {
        "artifact_received",
        "classification",
        "risk_decision",
        "route",
        "reviewer_output",
        "delivery_file",
        "buyer_label_reveal_status",
        "validation_result",
        "closeout_recommendation",
    }

def test_evidence_ledger_append_and_summary(tmp_path):
    module = load_module()
    ledger = tmp_path / "ledger.jsonl"
    args = SimpleNamespace(
        project_id="pytest_demo",
        event_type="artifact_received",
        artifact_id="artifact-001",
        artifact_path="",
        classification="trace_data",
        risk_decision="ACCEPT",
        route="01_received_observable_traces",
        reviewer_output="",
        delivery_file="",
        buyer_label_reveal_status="",
        validation_result="",
        closeout_recommendation="",
        notes="pytest smoke test",
    )
    record = module.make_record(args)
    module.append_record(ledger, record)
    summary = module.summarize(ledger)
    assert summary["record_count"] == 1
    assert summary["event_counts"]["artifact_received"] == 1
