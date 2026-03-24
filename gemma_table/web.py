from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from gemma_table import GemmaTableService

router = APIRouter(prefix="/gemma-table", tags=["gemma-table"])
service = GemmaTableService(workspace_root=Path(__file__).resolve().parents[1])


class CompareRequest(BaseModel):
    query: str


@router.get("", response_class=HTMLResponse)
async def gemma_table_ui() -> str:
    return """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Gemma Table Workflow</title>
  <style>
    :root {
      --bg: #f3efe6;
      --panel: #fffaf1;
      --ink: #1f2933;
      --muted: #52606d;
      --accent: #b44d12;
      --accent-soft: #f6d9c7;
      --border: #d9cbb7;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, #fff7eb 0%, transparent 35%),
        linear-gradient(135deg, #efe7d8 0%, var(--bg) 55%, #e7dcc8 100%);
      min-height: 100vh;
    }
    main {
      max-width: 1100px;
      margin: 0 auto;
      padding: 32px 20px 56px;
    }
    h1 {
      font-size: clamp(2.2rem, 4vw, 4rem);
      margin: 0 0 12px;
      letter-spacing: -0.03em;
    }
    p {
      color: var(--muted);
      max-width: 780px;
      line-height: 1.5;
    }
    .controls, .panel {
      background: rgba(255, 250, 241, 0.9);
      border: 1px solid var(--border);
      border-radius: 20px;
      box-shadow: 0 20px 40px rgba(68, 35, 12, 0.08);
      backdrop-filter: blur(8px);
    }
    .controls {
      padding: 20px;
      margin: 24px 0;
    }
    textarea {
      width: 100%;
      min-height: 88px;
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 14px;
      font: inherit;
      background: #fffdf8;
      color: var(--ink);
      resize: vertical;
    }
    .actions {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 14px;
    }
    button {
      border: none;
      border-radius: 999px;
      padding: 12px 18px;
      font: inherit;
      cursor: pointer;
      background: var(--accent);
      color: white;
    }
    button.secondary {
      background: var(--accent-soft);
      color: var(--ink);
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
      margin-top: 18px;
    }
    .panel {
      padding: 18px;
    }
    .eyebrow {
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.12em;
      font-size: 0.75rem;
      margin-bottom: 8px;
    }
    pre {
      white-space: pre-wrap;
      word-break: break-word;
      margin: 0;
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 0.95rem;
      line-height: 1.45;
    }
    .status {
      margin-top: 20px;
      padding: 14px 16px;
      border-left: 4px solid var(--accent);
      background: rgba(246, 217, 199, 0.6);
      border-radius: 10px;
      color: var(--ink);
    }
  </style>
</head>
<body>
  <main>
    <h1>Gemma 270M Table-of-N Lab</h1>
    <p>Compare the original model against the currently selected solution, inspect benchmark results, and keep a local research trail of every attempt and failure while the workflow evolves.</p>
    <section class="controls">
      <label for="query">Query</label>
      <textarea id="query">table of 7</textarea>
      <div class="actions">
        <button id="compare">Compare Outputs</button>
        <button class="secondary" id="benchmark">Run Benchmark</button>
        <button class="secondary" id="status">Workflow Status</button>
        <button class="secondary" id="report">Publish Research Report</button>
      </div>
      <div id="statusBox" class="status">Ready.</div>
    </section>
    <section class="grid">
      <article class="panel">
        <div class="eyebrow">Original Model</div>
        <pre id="original">No output yet.</pre>
      </article>
      <article class="panel">
        <div class="eyebrow">New Solution</div>
        <pre id="newSolution">No output yet.</pre>
      </article>
      <article class="panel">
        <div class="eyebrow">Notes</div>
        <pre id="notes">No results yet.</pre>
      </article>
    </section>
  </main>
  <script>
    async function postJson(url, payload) {
      const response = await fetch(url, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
      });
      if (!response.ok) {
        throw new Error(await response.text());
      }
      return response.json();
    }

    async function getJson(url) {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(await response.text());
      }
      return response.json();
    }

function renderBackend(result) {
      const lines = [
        `Backend: ${result.backend}`,
        `Success: ${result.success}`,
      ];
      if (result.error) lines.push(`Error: ${result.error}`);
      if (result.output) {
        lines.push("", result.output);
      }
      return lines.join("\\n");
    }

    function renderEvaluation(result) {
      if (!result) return "No table-of-N evaluation for this query.";
      const lines = [
        `Exact Match: ${result.exact_match}`,
        `Header OK: ${result.header_ok}`,
        `Line Count OK: ${result.line_count_ok}`,
        `Arithmetic OK: ${result.arithmetic_ok}`,
      ];
      if (result.details && result.details.length) {
        lines.push("", "Judge Notes:");
        for (const item of result.details) lines.push(`- ${item}`);
      }
      return lines.join("\\n");
    }

    document.getElementById("compare").addEventListener("click", async () => {
      const query = document.getElementById("query").value;
      document.getElementById("statusBox").textContent = "Comparing original and new solution...";
      try {
        const data = await postJson("/gemma-table/compare", {query});
        document.getElementById("original").textContent = renderBackend(data.original);
        document.getElementById("newSolution").textContent = renderBackend(data.new_solution);
        document.getElementById("notes").textContent =
          `${data.recommendation}\n\nOriginal Evaluation\n${renderEvaluation(data.original_evaluation)}\n\nNew Solution Evaluation\n${renderEvaluation(data.new_solution_evaluation)}`;
        document.getElementById("statusBox").textContent = "Compare finished.";
      } catch (error) {
        document.getElementById("statusBox").textContent = `Compare failed: ${error.message}`;
      }
    });

    document.getElementById("benchmark").addEventListener("click", async () => {
      document.getElementById("statusBox").textContent = "Running benchmark...";
      try {
        const data = await postJson("/gemma-table/benchmark", {});
        document.getElementById("notes").textContent = JSON.stringify(data.summary, null, 2);
        document.getElementById("statusBox").textContent = "Benchmark finished.";
      } catch (error) {
        document.getElementById("statusBox").textContent = `Benchmark failed: ${error.message}`;
      }
    });

    document.getElementById("status").addEventListener("click", async () => {
      document.getElementById("statusBox").textContent = "Loading workflow status...";
      try {
        const data = await getJson("/gemma-table/status");
        document.getElementById("notes").textContent = JSON.stringify(data, null, 2);
        document.getElementById("statusBox").textContent = "Status loaded.";
      } catch (error) {
        document.getElementById("statusBox").textContent = `Status failed: ${error.message}`;
      }
    });

    document.getElementById("report").addEventListener("click", async () => {
      document.getElementById("statusBox").textContent = "Publishing report...";
      try {
        const data = await postJson("/gemma-table/report", {});
        document.getElementById("notes").textContent = data.path + "\\n\\n" + data.content;
        document.getElementById("statusBox").textContent = "Report published.";
      } catch (error) {
        document.getElementById("statusBox").textContent = `Report failed: ${error.message}`;
      }
    });
  </script>
</body>
</html>
"""


@router.get("/status")
async def status() -> dict[str, object]:
    return service.workflow_status()


@router.post("/compare")
async def compare(request: CompareRequest) -> dict[str, object]:
    result = service.compare(request.query)
    return {
        "query": result.query,
        "original": result.original,
        "new_solution": result.new_solution,
        "original_evaluation": result.original_evaluation,
        "new_solution_evaluation": result.new_solution_evaluation,
        "recommendation": result.recommendation,
    }


@router.post("/benchmark")
async def benchmark() -> dict[str, object]:
    return service.benchmark()


@router.post("/report")
async def publish_report() -> dict[str, str]:
    return service.publish_report()
