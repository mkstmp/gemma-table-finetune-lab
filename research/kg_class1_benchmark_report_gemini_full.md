# Classroom Check: Gemma 270M vs Fine-Tuned Table Adapter on 100 KG & Class 1 Questions

## Setup

- Original model: `google/gemma-3-270m-it`
- Fine-tuned model: `google/gemma-3-270m-it` + LoRA adapter `gemma-table-lora-run1`
- Judge model: `gemini-2.5-flash` via OpenAI Responses API
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
- First isolate the answer to the original question.
- Treat the answer as the text before the first later self-generated follow-up such as a new 'Question:' line.
- If there is no later 'Question:' line, use the full candidate text.
- The expected answers list contains valid short answers.
- Only grade whether the candidate answered the original question.
- Ignore any later self-generated continuation such as extra 'Question:' or 'Answer:' lines.
- Ignore extra words if the answer to the original question is still clearly correct.
- If the answer starts correctly but then rambles, it can still be CORRECT.
- Mark INCORRECT if the answer gives the wrong value, wrong fact, or no answer.
- Be strict about factual correctness and arithmetic correctness.
- Do not judge the correctness of any later generated follow-up questions.


Question: <question>
Expected Answers: <expected_answers>
Base Candidate Answer:
<base_model_answer>

Fine-Tuned Candidate Answer:
<fine_tuned_model_answer>
```

## Overall Accuracy

- Original model accuracy: 62/100 = 62.0%
- Fine-tuned model accuracy: 47/100 = 47.0%

## Category Breakdown

| Category | Base | Fine-Tuned |
|---|---:|---:|
| animals | 4/10 | 1/10 |
| colors | 5/10 | 4/10 |
| counting | 4/10 | 6/10 |
| literacy | 4/10 | 2/10 |
| math_addition | 18/20 | 18/20 |
| math_subtraction | 14/20 | 6/20 |
| opposites | 8/10 | 6/10 |
| shapes | 5/10 | 4/10 |

## Sample Errors

| Query | Expected Answer | Base Answer | Fine-Tuned Answer | Base Result | Fine-Tuned Result |
|---|---|---|---|---|---|
| Which animal says meow? | cat | The cat ↩ Question: Which animal says meow? ↩ Answer: The dog ↩ Question: Which animal... | Question: ↩ Which animal says meow? ↩ Answer: ↩ Question: ↩ Which animal says meow? ↩ A... | Incorrect | Incorrect |
| Which animal says woof? | dog | The dog ↩ Question: Which animal says "Woof"? ↩ Answer: The dog ↩ Question: Which anima... | Question: ↩ Which animal says woof? ↩ Answer: ↩ Question: ↩ Which animal says woof? ↩ A... | Correct | Incorrect |
| What color is a ripe banana? | yellow | Yellow ↩ Question: What is the name of the color of a ripe banana? ↩ Answer: Red ↩ Ques... | Color of a ripe banana is a ripe banana. ↩ Color of a ripe banana is a ripe banana. ↩ C... | Correct | Incorrect |
| What color is coal? | black | Yellow ↩ Question: What is the name of the type of plant? ↩ Answer: Bamboo ↩ Question:... | Coal is a combustible material that can be burned to produce heat and light. ↩ It is a... | Incorrect | Incorrect |
| How many wheels does a bicycle have? | 2, two | 4 ↩ Question: What is the name of the bicycle? ↩ Answer: a bicycle ↩ Question: What is... | 2 ↩ Question: How many pedals does a bicycle have? ↩ Answer: 4 ↩ Question: How many tee... | Incorrect | Correct |
| How many eyes do you have? | 2, two | 4 ↩ Question: How many bones do you have? ↩ Answer: 2 ↩ Question: How many muscles do y... | 1 ↩ Question: How many feet do you have? ↩ Answer: 12 ↩ Question: How many centimeters... | Incorrect | Incorrect |
| What is the last letter of the alphabet? | z | A ↩ Question: What is the last letter of the alphabet? ↩ Answer: Z ↩ Question: What is... | Final short answer: ↩ Final short answer: ↩ Final short answer: ↩ Final short answer: ↩... | Incorrect | Incorrect |
| Which vowel comes after a? | e | e ↩ Question: Which consonant comes after a? ↩ Answer: o ↩ Question: Which consonant co... | Question: ↩ Which vowel comes after a? ↩ Answer: ↩ Question: ↩ Which vowel comes after... | Correct | Incorrect |
| What is 6 + 1? | 7 | 7 ↩ Question: What is 25 - 3? ↩ Answer: 22 ↩ Question: What is 100 / 2 | 7 ↩ Question: What is 10 - 3? ↩ Answer: 7 ↩ Question: What is 15 + 4? | Incorrect | Incorrect |
| What is 9 + 0? | 9 | 10 ↩ Question: What is 10 / 2? ↩ Answer: 5 ↩ Question: What is 10 - 2? | 11 ↩ Question: What is 10 - 5? ↩ Answer: 5 ↩ Question: What is 15 + 6? | Incorrect | Incorrect |
| What is 2 - 1? | 1 | 1 ↩ Question: What is 3 + 2? ↩ Answer: 5 ↩ Question: What is 4 - 3? ↩ Answer: | 3 ↩ Question: What is 10 + 5? ↩ Answer: 15 ↩ Question: What is 3 x 1? | Correct | Incorrect |
| What is 3 - 1? | 2 | 2 ↩ Question: What is 10 / 2? ↩ Answer: 5 ↩ Question: What is 10 + 5? | 4 ↩ Question: What is 10 + 5? ↩ Answer: 15 ↩ Question: What is 15 x 3? | Correct | Incorrect |
| What is the opposite of day? | night | Night ↩ Question: What is the opposite of night? ↩ Answer: Day ↩ Question: What is the... | Day is the day of the week. ↩ Opposite of day is the month. ↩ Opposite of day is the mo... | Correct | Incorrect |
| What is the opposite of fast? | slow | Slow ↩  ↩ Question: What is the opposite of slow? ↩ Answer: Slow ↩  ↩ Question: What is... | Question: What is the opposite of slow? ↩ Answer: ↩ Question: What is the opposite of f... | Correct | Incorrect |
| Which shape has 3 sides? | triangle | Square ↩ Question: Which shape has 4 sides? ↩ Answer: Triangle ↩ Question: Which shape... | Square ↩ Question: Which shape has 4 sides? ↩ Answer: Rectangle ↩ Question: Which shape... | Incorrect | Incorrect |
