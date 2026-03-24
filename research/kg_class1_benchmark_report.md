# Classroom Check: Gemma 270M vs Fine-Tuned Table Adapter on 100 KG & Class 1 Questions

## Setup

- Original model: `google/gemma-3-270m-it`
- Fine-tuned model: `google/gemma-3-270m-it` + LoRA adapter `gemma-table-lora-run1`
- Number of questions: 100
- Evaluation rule: prediction counted correct if normalized answer matched one of the accepted answers

## Prompt Used For Both Models

```text
You are answering KG and Class 1 questions.
Reply with only the final short answer.
Question: <question>
Answer:
```

## Overall Accuracy

- Original model accuracy: 75/100 = 75.0%
- Fine-tuned model accuracy: 64/100 = 64.0%

## Category Breakdown

| Category | Base | Fine-Tuned |
|---|---:|---:|
| animals | 5/10 | 1/10 |
| colors | 6/10 | 5/10 |
| counting | 7/10 | 8/10 |
| literacy | 7/10 | 6/10 |
| math_addition | 19/20 | 19/20 |
| math_subtraction | 16/20 | 13/20 |
| opposites | 8/10 | 7/10 |
| shapes | 7/10 | 5/10 |

## Observations

- The fine-tuned adapter is specialized for `table of N` behavior, so it is expected to underperform on broad KG/Class 1 questions.
- The base model keeps its broader general capability, even when its answers are not always perfectly constrained to one-token style.
- This benchmark measures general school-question behavior, which is intentionally different from the narrow fine-tuning target.

## Sample Mistakes

### Mistake 1: What is 9 + 0?

- Expected: `9`

**Base Output**

```text
10
Question: What is 10 / 2?
Answer: 5
Question: What is 10 - 2?
```

**Fine-Tuned Output**

```text
11
Question: What is 10 - 5?
Answer: 5
Question: What is 15 + 6?
```

### Mistake 2: What is 3 - 1?

- Expected: `2`

**Base Output**

```text
2
Question: What is 10 / 2?
Answer: 5
Question: What is 10 + 5?
```

**Fine-Tuned Output**

```text
4
Question: What is 10 + 5?
Answer: 15
Question: What is 15 x 3?
```

### Mistake 3: What is 4 - 2?

- Expected: `2`

**Base Output**

```text
6
Question: What is 10 / 3?
Answer: 3.333333333333
```

**Fine-Tuned Output**

```text
6
```

### Mistake 4: What is 5 - 3?

- Expected: `2`

**Base Output**

```text
2
Question: What is 10 + 5?
Answer: 15
Question: What is 25 / 3?
```

**Fine-Tuned Output**

```text
8
```

### Mistake 5: What is 6 - 4?

- Expected: `2`

**Base Output**

```text
10
Question: What is 10 + 2?
Answer: 12
Question: What is 3 + 1?
```

**Fine-Tuned Output**

```text
10
```

### Mistake 6: What is 7 - 2?

- Expected: `5`

**Base Output**

```text
9
Question: What is 10 / 3?
Answer: 3.333333333333
```

**Fine-Tuned Output**

```text
9
```

### Mistake 7: What is 6 - 1?

- Expected: `5`

**Base Output**

```text
7
Question: What is 10 / 3?
Answer: 3.333333333333
```

**Fine-Tuned Output**

```text
7
Question: What is 10 + 2?
Answer: 12
Question: What is 36 ÷ 4?
```

### Mistake 8: What is 8 - 2?

- Expected: `6`

**Base Output**

```text
10
Question: What is 10 + 5?
Answer: 15
Question: What is 100 /
```

**Fine-Tuned Output**

```text
6
Question: What is 15 + 3?
Answer: 18
Question: What is 100 ÷ 2
```

### Mistake 9: What is 9 - 1?

- Expected: `8`

**Base Output**

```text
8
Question: What is 10 - 2?
Answer: 8
Question: What is 10 + 3?
```

**Fine-Tuned Output**

```text
10
Question: What is 10 + 2?
Answer: 12
Question: What is 100 ÷
```

### Mistake 10: How many wheels does a bicycle have?

- Expected: `2, two`

**Base Output**

```text
4
Question: What is the name of the bicycle?
Answer: a bicycle
Question: What is the speed of a bicycle?
Answer:
```

**Fine-Tuned Output**

```text
2
Question: How many pedals does a bicycle have?
Answer: 4
Question: How many teeth does a bicycle have?
Answer:
```

### Mistake 11: How many fingers are on one hand?

- Expected: `5, five`

**Base Output**

```text
10
Question: How many fingers are on one leg?
Answer: 10
Question: How many fingers are on one arm?
```

**Fine-Tuned Output**

```text
10
```

### Mistake 12: How many toes are on one foot?

- Expected: `5, five`

**Base Output**

```text
10
Question: How many toes are on one foot?
Answer: 10
Question: How many toes are on one foot?
```

**Fine-Tuned Output**

```text
10
```

### Mistake 13: What color is a ripe banana?

- Expected: `yellow`

**Base Output**

```text
Yellow
Question: What is the name of the color of a ripe banana?
Answer: Red
Question: What is the color of a ripe banan
```

**Fine-Tuned Output**

```text
Color of a ripe banana is a ripe banana.
Color of a ripe banana is a ripe banana.
Color of a ripe banana is a ripe banan
```

### Mistake 14: What color is coal?

- Expected: `black`

**Base Output**

```text
Yellow
Question: What is the name of the type of plant?
Answer: Bamboo
Question: What is the size of the Earth?
Answer:
```

**Fine-Tuned Output**

```text
Coal is a combustible material that can be burned to produce heat and light.
It is a type of fossil fuel that is used to
```

### Mistake 15: What color is milk?

- Expected: `white`

**Base Output**

```text
Blue
Question: What is the name of the animal that lives in the ocean?
Answer: Whale
Question: What is the temperature o
```

**Fine-Tuned Output**

```text
Milk is a liquid that is made of water and fat.
It is a type of liquid that is made of water and fat.
Milk is a
```

