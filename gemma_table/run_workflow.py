from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from gemma_table.research import ResearchLog
from gemma_table.service import GemmaTableService


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the agentic workflow for Gemma table-of-N tuning.")
    parser.add_argument("--workspace-root", default=".")
    parser.add_argument("--skip-train", action="store_true")
    parser.add_argument("--train-command", default=".venv-gemma/bin/python -m gemma_table.train --workspace-root .")
    args = parser.parse_args()

    workspace_root = Path(args.workspace_root).resolve()
    research = ResearchLog(workspace_root / "research")
    service = GemmaTableService(workspace_root=workspace_root)

    benchmark = service.benchmark()
    fine_tune_needed = bool(benchmark["summary"]["fine_tune_needed"])
    research.record(
        title="Workflow decision gate",
        category="workflow",
        status="success",
        summary="Evaluated whether fine-tuning is needed after the benchmark.",
        details={"fine_tune_needed": fine_tune_needed, "summary": benchmark["summary"]},
    )

    if args.skip_train or not fine_tune_needed:
        research.publish_report()
        return

    result = subprocess.run(args.train_command, shell=True, cwd=workspace_root, text=True, capture_output=True)
    research.record(
        title="Training command executed",
        category="training",
        status="success" if result.returncode == 0 else "blocked",
        summary="Executed the configured fine-tuning command.",
        details={
            "command": args.train_command,
            "returncode": result.returncode,
            "stdout": result.stdout[-600:],
            "stderr": result.stderr[-600:],
        },
    )
    research.publish_report()


if __name__ == "__main__":
    main()
