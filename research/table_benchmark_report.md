# Table Mastery Check: Gemma 270M vs Fine-Tuned Table Adapter

## Setup

- Original model: `google/gemma-3-270m-it`
- Fine-tuned model: `google/gemma-3-270m-it` + LoRA adapter `gemma-table-lora-run1`
- Number of prompts: 10
- Evaluation rule: exact table-match plus arithmetic/format validation

## Prompt Used For Both Models

```text
User: <question>
Assistant:
```

## Overall Accuracy

- Original model exact-match accuracy: 0/10 = 0.0%
- Fine-tuned model exact-match accuracy: 10/10 = 100.0%

## Case Results

| Prompt | Base | Fine-Tuned |
|---|---:|---:|
| table of 2 | FAIL | PASS |
| table of 3 | FAIL | PASS |
| table of 5 | FAIL | PASS |
| table of 7 | FAIL | PASS |
| table of 9 | FAIL | PASS |
| table of 11 | FAIL | PASS |
| table of 12 | FAIL | PASS |
| table of 15 | FAIL | PASS |
| table of 17 | FAIL | PASS |
| table of 19 | FAIL | PASS |

## Sample Outputs

### table of 2

**Original Model**

```text
User: table of 2
Assistant:
User: table of 2
Assistant:
User: table of 2
Assistant:
User: table of 2
Assistant:
User: table of 2
Assistant:
User: table of 2
Assistant:
User: table of 2
Assistant:
User: table of 2
Assistant:
User: table of 2
Assistant:
User: table of 2
Assistant:
User: table of 2
Assistant:
User: table of 2
Assistant:
User: table of 2
Assistant:
User: table of 2
Assistant:
User: table of 2
Assistant:
User: table of 2
Assistant:
User: table of 2
Assistant:
User: table of 2
Assistant:
```

**Fine-Tuned Model**

```text
Table of 2
2 x 1 = 2
2 x 2 = 4
2 x 3 = 6
2 x 4 = 8
2 x 5 = 10
2 x 6 = 12
2 x 7 = 14
2 x 8 = 16
2 x 9 = 18
2 x 10 = 20
```

### table of 3

**Original Model**

```text
User: table of 3
Assistant:
User: table of 3
Assistant:
User: table of 3
Assistant:
User: table of 3
Assistant:
User: table of 3
Assistant:
User: table of 3
Assistant:
User: table of 3
Assistant:
User: table of 3
Assistant:
User: table of 3
Assistant:
User: table of 3
Assistant:
User: table of 3
Assistant:
User: table of 3
Assistant:
User: table of 3
Assistant:
User: table of 3
Assistant:
User: table of 3
Assistant:
User: table of 3
Assistant:
User: table of 3
Assistant:
User: table of 3
Assistant:
```

**Fine-Tuned Model**

```text
Table of 3
3 x 1 = 3
3 x 2 = 6
3 x 3 = 9
3 x 4 = 12
3 x 5 = 15
3 x 6 = 18
3 x 7 = 21
3 x 8 = 24
3 x 9 = 27
3 x 10 = 30
```

### table of 5

**Original Model**

```text
User: table of 5
Assistant:
User: table of 5
Assistant:
User: table of 5
Assistant:
User: table of 5
Assistant:
User: table of 5
Assistant:
User: table of 5
Assistant:
User: table of 5
Assistant:
User: table of 5
Assistant:
User: table of 5
Assistant:
User: table of 5
Assistant:
User: table of 5
Assistant:
User: table of 5
Assistant:
User: table of 5
Assistant:
User: table of 5
Assistant:
User: table of 5
Assistant:
User: table of 5
Assistant:
User: table of 5
Assistant:
User: table of 5
Assistant:
```

**Fine-Tuned Model**

```text
Table of 5
5 x 1 = 5
5 x 2 = 10
5 x 3 = 15
5 x 4 = 20
5 x 5 = 25
5 x 6 = 30
5 x 7 = 35
5 x 8 = 40
5 x 9 = 45
5 x 10 = 50
```

### table of 7

**Original Model**

```text
User: table of 7
Assistant:
User: table of 7
Assistant:
User: table of 7
Assistant:
User: table of 7
Assistant:
User: table of 7
Assistant:
User: table of 7
Assistant:
User: table of 7
Assistant:
User: table of 7
Assistant:
User: table of 7
Assistant:
User: table of 7
Assistant:
User: table of 7
Assistant:
User: table of 7
Assistant:
User: table of 7
Assistant:
User: table of 7
Assistant:
User: table of 7
Assistant:
User: table of 7
Assistant:
User: table of 7
Assistant:
User: table of 7
Assistant:
```

**Fine-Tuned Model**

```text
Table of 7
7 x 1 = 7
7 x 2 = 14
7 x 3 = 21
7 x 4 = 28
7 x 5 = 35
7 x 6 = 42
7 x 7 = 49
7 x 8 = 56
7 x 9 = 63
7 x 10 = 70
```
