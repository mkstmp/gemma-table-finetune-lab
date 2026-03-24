from pathlib import Path

from assistant_platform.gemma_table.core import parse_table_request, render_table
from assistant_platform.gemma_table.evaluation import evaluate_table_response
from assistant_platform.gemma_table.service import GemmaTableService


def test_parse_table_request_variants() -> None:
    assert parse_table_request("table of 9").value == 9
    assert parse_table_request("show me the table of 6").value == 6
    assert parse_table_request("multiplication table of 12").value == 12
    assert parse_table_request("hello there") is None


def test_evaluate_table_response_exact_match() -> None:
    actual = render_table(7)
    evaluation = evaluate_table_response("table of 7", actual)
    assert evaluation.exact_match
    assert evaluation.arithmetic_ok
    assert evaluation.header_ok
    assert evaluation.line_count_ok


def test_service_selects_prompted_model_solution_when_fine_tune_is_not_ready(tmp_path: Path) -> None:
    service = GemmaTableService(workspace_root=tmp_path)
    status = service.workflow_status()
    assert status["new_solution_backend"] == "prompted:ollama:gemma3:270m"
