# Classroom Check: Gemma 270M vs Fine-Tuned Table Adapter on 100 KG & Class 1 Questions

## Setup

- Original model: `google/gemma-3-270m-it`
- Fine-tuned model: `google/gemma-3-270m-it` + LoRA adapter `gemma-table-lora-run1`
- Judge model: `gpt-5` via OpenAI Responses API
- Report note: the latest refresh attempt hit OpenAI rate limits, so these numbers reflect the last successful OpenAI-judged pass
- Number of questions: 100
- Evaluation rule: external LLM judge decides whether each answer is correct

## Prompt Used For Answering

```text
You are answering KG and Class 1 questions.
Reply with only the final short answer.
Question: <question>
Answer:
```

## Prompt Used For Judging

```text
You are grading student answers.
Decide if each candidate answer should count as correct for the question.

Rules:
- The expected answers list contains valid short answers.
- Ignore extra words if the answer is still clearly correct.
- If the answer starts correctly but then rambles, it can still be CORRECT.
- Mark INCORRECT if the answer gives the wrong value, wrong fact, or no answer.
- Be strict about factual correctness and arithmetic correctness.


Question: <question>
Expected Answers: <expected_answers>
Base Candidate Answer:
<base_model_answer>

Fine-Tuned Candidate Answer:
<fine_tuned_model_answer>
```

## Overall Accuracy

- Original model accuracy: 47/100 = 47.0%
- Fine-tuned model accuracy: 28/100 = 28.0%

## Category Breakdown

| Category | Base | Fine-Tuned |
|---|---:|---:|
| animals | 1/10 | 0/10 |
| colors | 4/10 | 2/10 |
| counting | 4/10 | 6/10 |
| literacy | 0/10 | 0/10 |
| math_addition | 18/20 | 10/20 |
| math_subtraction | 14/20 | 6/20 |
| opposites | 3/10 | 2/10 |
| shapes | 3/10 | 2/10 |

## Full Results

The full 100-question table is in [kg_class1_benchmark_full_table.md](/Users/mukesh/assistant2/research/kg_class1_benchmark_full_table.md).
