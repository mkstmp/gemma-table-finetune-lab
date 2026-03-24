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


class ReviewSaveRequest(BaseModel):
    question_id: str
    base_human_result: str | None = None
    fine_tuned_human_result: str | None = None
    reviewer: str = ""
    note: str = ""


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
        <a href="/gemma-table/review" style="display:inline-flex;align-items:center;justify-content:center;border-radius:999px;padding:12px 18px;background:#f6d9c7;color:#1f2933;text-decoration:none;">Review Judgments</a>
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


@router.get("/review", response_class=HTMLResponse)
async def review_ui() -> str:
    return """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>KG/Class 1 Judgment Review</title>
  <style>
    :root {
      --bg: #f4efe7;
      --panel: #fffaf2;
      --ink: #1f2933;
      --muted: #52606d;
      --accent: #0f766e;
      --accent-soft: #d7f2ee;
      --border: #d8ccb8;
      --good: #156f3d;
      --bad: #9b1c1c;
    }
    * { box-sizing: border-box; }
    body { margin: 0; font-family: Georgia, "Times New Roman", serif; color: var(--ink); background: linear-gradient(180deg, #f8f4ec 0%, var(--bg) 100%); }
    main { max-width: 1500px; margin: 0 auto; padding: 24px 18px 56px; }
    h1 { margin: 0 0 8px; font-size: clamp(2rem, 4vw, 3.5rem); }
    p { color: var(--muted); max-width: 900px; line-height: 1.5; }
    .toolbar, .summary, .table-wrap { background: var(--panel); border: 1px solid var(--border); border-radius: 18px; box-shadow: 0 14px 32px rgba(36, 24, 10, 0.08); }
    .toolbar, .summary { padding: 16px; margin: 18px 0; }
    .toolbar-grid, .summary-grid { display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); }
    label { display: block; font-size: 0.92rem; margin-bottom: 6px; color: var(--muted); }
    input, select, textarea { width: 100%; border: 1px solid var(--border); border-radius: 10px; padding: 10px; font: inherit; background: #fffdf8; color: var(--ink); }
    textarea { min-height: 72px; }
    .table-wrap { overflow: auto; }
    table { width: 100%; border-collapse: collapse; min-width: 1400px; }
    th, td { padding: 12px; border-bottom: 1px solid var(--border); vertical-align: top; text-align: left; }
    th { position: sticky; top: 0; background: #fff7eb; z-index: 1; }
    .mono { font-family: "SFMono-Regular", Consolas, monospace; white-space: pre-wrap; word-break: break-word; font-size: 0.9rem; line-height: 1.4; }
    .badge { display: inline-block; border-radius: 999px; padding: 4px 8px; font-size: 0.78rem; font-weight: 700; }
    .good { background: #dcfce7; color: var(--good); }
    .bad { background: #fee2e2; color: var(--bad); }
    .unknown { background: #e5e7eb; color: #374151; }
    .actions { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
    button { border: none; border-radius: 999px; padding: 10px 14px; cursor: pointer; font: inherit; background: var(--accent); color: white; }
    .secondary-link { color: var(--accent); text-decoration: none; }
    .status { margin-top: 10px; color: var(--muted); }
    .mini { color: var(--muted); font-size: 0.8rem; margin-top: 6px; }
  </style>
</head>
<body>
  <main>
    <a class="secondary-link" href="/gemma-table">Back to Lab</a>
    <h1>KG/Class 1 Judgment Review</h1>
    <p>Review LLM verdicts, override them where needed, and build a verified judgment layer before generating final reports.</p>
    <section class="summary">
      <div class="summary-grid" id="summaryGrid"></div>
    </section>
    <section class="toolbar">
      <div class="toolbar-grid">
        <div>
          <label for="filterText">Search</label>
          <input id="filterText" placeholder="question id, query, expected answer">
        </div>
        <div>
          <label for="filterCategory">Category</label>
          <select id="filterCategory"><option value="">All</option></select>
        </div>
        <div>
          <label for="filterReview">Review Status</label>
          <select id="filterReview">
            <option value="">All</option>
            <option value="needs_review">Needs Review</option>
            <option value="human_verified">Human Verified</option>
            <option value="llm_available">LLM Verdict Available</option>
            <option value="disagreement">Human/LLM Disagreement</option>
          </select>
        </div>
        <div>
          <label for="reviewer">Reviewer</label>
          <input id="reviewer" placeholder="human-agent-1">
        </div>
        <div>
          <label>Actions</label>
          <div class="actions">
            <button id="nextUnreviewed">Next Unreviewed</button>
            <button id="publishVerified">Publish Verified Report</button>
          </div>
        </div>
      </div>
      <div class="status" id="statusBox">Loading review rows...</div>
    </section>
    <section class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>QID</th>
            <th>Category</th>
            <th>Query</th>
            <th>Expected</th>
            <th>Base Answer</th>
            <th>Base LLM</th>
            <th>Base Human</th>
            <th>Base Effective</th>
            <th>FT Answer</th>
            <th>FT LLM</th>
            <th>FT Human</th>
            <th>FT Effective</th>
            <th>Notes</th>
            <th>Save</th>
          </tr>
        </thead>
        <tbody id="rows"></tbody>
      </table>
    </section>
  </main>
  <script>
    let reviewRows = [];

    function badge(value) {
      if (value === "correct") return `<span class="badge good">Correct</span>`;
      if (value === "incorrect") return `<span class="badge bad">Incorrect</span>`;
      return `<span class="badge unknown">Unknown</span>`;
    }

    function optionMarkup(value) {
      return `
        <option value="" ${!value ? "selected" : ""}>Unset</option>
        <option value="correct" ${value === "correct" ? "selected" : ""}>Correct</option>
        <option value="incorrect" ${value === "incorrect" ? "selected" : ""}>Incorrect</option>
      `;
    }

    function renderSummary(summary) {
      const items = [
        ["Questions", summary.total_questions],
        ["Base LLM", summary.base_llm_available],
        ["FT LLM", summary.ft_llm_available],
        ["Base Human", summary.base_human_verified],
        ["FT Human", summary.ft_human_verified],
        ["Need Review", summary.rows_needing_review],
        ["Disagreements", summary.rows_with_disagreement],
        ["Base Effective Correct", `${summary.base_effective_correct}/${summary.total_questions}`],
        ["FT Effective Correct", `${summary.ft_effective_correct}/${summary.total_questions}`],
      ];
      document.getElementById("summaryGrid").innerHTML = items.map(([label, value]) => `
        <div>
          <div style="color:#52606d;font-size:0.85rem;">${label}</div>
          <div style="font-size:1.6rem;font-weight:700;">${value}</div>
        </div>
      `).join("");
    }

    function applyFilters() {
      const text = document.getElementById("filterText").value.trim().toLowerCase();
      const category = document.getElementById("filterCategory").value;
      const review = document.getElementById("filterReview").value;
      const filtered = reviewRows.filter((row) => {
        const textMatch = !text || [row.question_id, row.category, row.question, row.expected_answers.join(", ")].join(" ").toLowerCase().includes(text);
        const categoryMatch = !category || row.category === category;
        const reviewMatch =
          !review ||
          (review === "needs_review" && (!row.base_human_result || !row.fine_tuned_human_result)) ||
          (review === "human_verified" && (row.base_human_result || row.fine_tuned_human_result)) ||
          (review === "llm_available" && (row.base_llm_result || row.fine_tuned_llm_result)) ||
          (review === "disagreement" && row.has_disagreement);
        return textMatch && categoryMatch && reviewMatch;
      });
      renderRows(filtered);
      document.getElementById("statusBox").textContent = `${filtered.length} row(s) shown.`;
    }

    function renderRows(rows) {
      const tbody = document.getElementById("rows");
      tbody.innerHTML = rows.map((row) => `
        <tr>
          <td class="mono">${row.question_id}</td>
          <td>${row.category}</td>
          <td>${row.question}</td>
          <td>${row.expected_answers.join(", ")}</td>
          <td class="mono">${row.base_answer || "<NO_ANSWER>"}</td>
          <td>${badge(row.base_llm_result)}<div class="mono">${row.base_llm_reason || ""}</div></td>
          <td>
            <select data-role="base-human" data-qid="${row.question_id}">
              ${optionMarkup(row.base_human_result)}
            </select>
          </td>
          <td>${badge(row.base_effective_result)}<div class="mini">${row.base_human_result ? "human override" : row.base_llm_result ? "llm" : "unset"}</div></td>
          <td class="mono">${row.fine_tuned_answer || "<NO_ANSWER>"}</td>
          <td>${badge(row.fine_tuned_llm_result)}<div class="mono">${row.fine_tuned_llm_reason || ""}</div></td>
          <td>
            <select data-role="ft-human" data-qid="${row.question_id}">
              ${optionMarkup(row.fine_tuned_human_result)}
            </select>
          </td>
          <td>${badge(row.fine_tuned_effective_result)}<div class="mini">${row.fine_tuned_human_result ? "human override" : row.fine_tuned_llm_result ? "llm" : "unset"}</div></td>
          <td>
            <textarea data-role="note" data-qid="${row.question_id}">${row.note || ""}</textarea>
            <div class="mono">${row.reviewer || ""} ${row.updated_at || ""}</div>
            ${row.has_disagreement ? '<div class="mini">LLM/human disagreement</div>' : ''}
          </td>
          <td>
            <div class="actions">
              <button data-role="save" data-qid="${row.question_id}">Save</button>
            </div>
          </td>
        </tr>
      `).join("");

      for (const button of tbody.querySelectorAll('button[data-role="save"]')) {
        button.addEventListener("click", async () => {
          const qid = button.dataset.qid;
          const base = tbody.querySelector(`select[data-role="base-human"][data-qid="${qid}"]`).value || null;
          const ft = tbody.querySelector(`select[data-role="ft-human"][data-qid="${qid}"]`).value || null;
          const note = tbody.querySelector(`textarea[data-role="note"][data-qid="${qid}"]`).value;
          const reviewer = document.getElementById("reviewer").value;
          document.getElementById("statusBox").textContent = `Saving ${qid}...`;
          const response = await fetch("/gemma-table/review/save", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
              question_id: qid,
              base_human_result: base,
              fine_tuned_human_result: ft,
              reviewer,
              note
            })
          });
          if (!response.ok) {
            document.getElementById("statusBox").textContent = `Save failed for ${qid}`;
            return;
          }
          await loadData();
          document.getElementById("statusBox").textContent = `Saved ${qid}.`;
        });
      }
    }

    async function loadData() {
      const response = await fetch("/gemma-table/review/data");
      const data = await response.json();
      reviewRows = data.rows;
      renderSummary(data.summary);
      const categorySelect = document.getElementById("filterCategory");
      const selected = categorySelect.value;
      categorySelect.innerHTML = '<option value="">All</option>' + Array.from(new Set(reviewRows.map((row) => row.category))).sort().map((value) => `<option value="${value}">${value}</option>`).join("");
      categorySelect.value = selected;
      applyFilters();
    }

    document.getElementById("filterText").addEventListener("input", applyFilters);
    document.getElementById("filterCategory").addEventListener("change", applyFilters);
    document.getElementById("filterReview").addEventListener("change", applyFilters);
    document.getElementById("nextUnreviewed").addEventListener("click", async () => {
      const response = await fetch("/gemma-table/review/next");
      const data = await response.json();
      if (!data.question_id) {
        document.getElementById("statusBox").textContent = "No review target found.";
        return;
      }
      document.getElementById("filterText").value = data.question_id;
      applyFilters();
      document.getElementById("statusBox").textContent = `Focused ${data.question_id}.`;
    });
    document.getElementById("publishVerified").addEventListener("click", async () => {
      document.getElementById("statusBox").textContent = "Publishing verified report...";
      const response = await fetch("/gemma-table/review/report", {method: "POST"});
      const data = await response.json();
      document.getElementById("statusBox").textContent = `Verified report written to ${data.path}`;
    });
    loadData();
  </script>
</body>
</html>
"""


@router.get("/review/data")
async def review_data() -> dict[str, object]:
    return service.review_dataset()


@router.post("/review/save")
async def review_save(request: ReviewSaveRequest) -> dict[str, object]:
    return service.save_review_decision(
        question_id=request.question_id,
        base_human_result=request.base_human_result,
        fine_tuned_human_result=request.fine_tuned_human_result,
        reviewer=request.reviewer,
        note=request.note,
    )


@router.get("/review/next")
async def review_next() -> dict[str, object]:
    return {"question_id": service.next_review_question_id()}


@router.post("/review/report")
async def review_report() -> dict[str, str]:
    return service.publish_verified_review_report()
