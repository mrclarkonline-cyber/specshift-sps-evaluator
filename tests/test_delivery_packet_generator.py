import importlib.util
from pathlib import Path
import pytest

MODULE_PATH = Path("tools/pilot_intake/delivery_packet_generator.py")

def load_module():
    spec = importlib.util.spec_from_file_location("delivery_packet_generator", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_safe_delivery_packet_generates(tmp_path):
    module = load_module()
    project = Path("tests/fixtures/buyer_artifact_simulator/delivery_packet_sample_project")
    output = tmp_path / "packet.md"
    report = module.build_packet(project, output, "REPEAT_WITH_CLEANER_DATA")
    text = output.read_text(encoding="utf-8")
    assert output.exists()
    assert report["claim_logic_scan"]["blocked_count"] == 0
    assert "This packet does not provide production validation." in text
    assert "Buyer retains labels" in text

def test_unsafe_delivery_packet_blocks(tmp_path):
    module = load_module()
    project = tmp_path / "bad_project"
    project.mkdir()
    (project / "01_received_manifest.md").write_text("# Manifest\n\nSynthetic artifact.\n", encoding="utf-8")
    (project / "02_scope_boundary_check.md").write_text("# Scope\n\nObservable-only.\n", encoding="utf-8")
    (project / "04_candidate_discrepancy_memo_draft.md").write_text("# Bad Memo\n\nWe certify that your AI is compliant.\n", encoding="utf-8")
    (project / "06_buyer_questions.md").write_text("# Questions\n\nBuyer review required.\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        module.build_packet(project, tmp_path / "bad_packet.md", "REPEAT_WITH_CLEANER_DATA")
