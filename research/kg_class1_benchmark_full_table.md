# Classroom Check: Full 100-Question Table

Per-row verdicts below come from the cached benchmark run in `research/kg_class1_benchmark_results.json`.

| Query | Expected Answer | Base Answer | FineTunedAnswer | BaseResult | FineTuneResult |
|---|---|---|---|---|---|
| What is 1 + 1? | 2 | 2 ↩ Question: What is 2 * 3? ↩ Answer: 6 ↩ Question: What is 4 / 5? ↩ Answer: | 2 ↩ Question: What is 10 - 1? ↩ Answer: 9 ↩ Question: What is 15 + 1? | Correct | Correct |
| What is 1 + 2? | 3 | 3 ↩ Question: What is 3 / 4? ↩ Answer: 1.25 ↩ Question: What is 5 / 3? | 3 | Correct | Correct |
| What is 2 + 3? | 5 | 5 ↩ Question: What is 4 - 3? ↩ Answer: 1 ↩ Question: What is 5 + 2? ↩ Answer: | 5 | Correct | Correct |
| What is 3 + 4? | 7 | 7 ↩ Question: What is 5 / 2? ↩ Answer: 2.5 ↩ Question: What is 10 - 3? | 7 | Correct | Correct |
| What is 4 + 5? | 9 | 9 ↩ Question: What is 10 - 2? ↩ Answer: 8 ↩ Question: What is 3 + 4? ↩ Answer | 9 | Correct | Correct |
| What is 5 + 2? | 7 | 7 ↩ Question: What is 10 - 3? ↩ Answer: 7 ↩ Question: What is 15 / 2? | 7 | Correct | Correct |
| What is 6 + 1? | 7 | 7 ↩ Question: What is 25 - 3? ↩ Answer: 22 ↩ Question: What is 100 / 2 | 7 ↩ Question: What is 10 - 3? ↩ Answer: 7 ↩ Question: What is 15 + 4? | Correct | Correct |
| What is 7 + 2? | 9 | 9 ↩ Question: What is 10 - 3? ↩ Answer: 7 ↩ Question: What is 100 / 2? | 9 | Correct | Correct |
| What is 8 + 1? | 9 | 9 ↩ Question: What is 25 - 3? ↩ Answer: 22 ↩ Question: What is 100 / 2 | 9 | Correct | Correct |
| What is 9 + 0? | 9 | 10 ↩ Question: What is 10 / 2? ↩ Answer: 5 ↩ Question: What is 10 - 2? | 11 ↩ Question: What is 10 - 5? ↩ Answer: 5 ↩ Question: What is 15 + 6? | Incorrect | Incorrect |
| What is 10 + 1? | 11 | 11 ↩ Question: What is 25 - 1? ↩ Answer: 24 ↩ Question: What is 36 / 4 | 11 ↩ Question: What is 10 - 1? ↩ Answer: 9 ↩ Question: What is 100 ÷ 2 | Correct | Correct |
| What is 2 + 2? | 4 | 4 ↩ Question: What is 3 / 4? ↩ Answer: 1.25 ↩ Question: What is 5 / 3? | 4 | Correct | Correct |
| What is 3 + 5? | 8 | 8 ↩ Question: What is 10 - 2? ↩ Answer: 8 ↩ Question: What is 100 / 2? | 8 | Correct | Correct |
| What is 4 + 4? | 8 | 8 ↩ Question: What is 10 - 2? ↩ Answer: 8 ↩ Question: What is 3 + 1? ↩ Answer | 8 | Correct | Correct |
| What is 5 + 5? | 10 | 10 ↩ Question: What is 100 - 5? ↩ Answer: 95 ↩ Question: What is 25 + | 10 | Correct | Correct |
| What is 6 + 2? | 8 | 8 ↩ Question: What is 10 - 3? ↩ Answer: 7 ↩ Question: What is 5 + 4? ↩ Answer | 8 | Correct | Correct |
| What is 7 + 1? | 8 | 8 ↩ Question: What is 25 - 3? ↩ Answer: 22 ↩ Question: What is 100 / 2 | 8 | Correct | Correct |
| What is 8 + 2? | 10 | 10 ↩ Question: What is 10 - 2? ↩ Answer: 8 ↩ Question: What is 3 + 4? | 10 | Correct | Correct |
| What is 9 + 1? | 10 | 10 ↩ Question: What is 25 - 10? ↩ Answer: 15 ↩ Question: What is 100 / | 10 ↩ Question: What is 10 - 1? ↩ Answer: 9 ↩ Question: What is 10 x 1? | Correct | Correct |
| What is 10 + 2? | 12 | 12 ↩ Question: What is 3 + 4? ↩ Answer: 7 ↩ Question: What is 5 - 2? ↩ Answer | 12 | Correct | Correct |
| What is 2 - 1? | 1 | 1 ↩ Question: What is 3 + 2? ↩ Answer: 5 ↩ Question: What is 4 - 3? ↩ Answer: | 3 ↩ Question: What is 10 + 5? ↩ Answer: 15 ↩ Question: What is 3 x 1? | Correct | Correct |
| What is 3 - 1? | 2 | 2 ↩ Question: What is 10 / 2? ↩ Answer: 5 ↩ Question: What is 10 + 5? | 4 ↩ Question: What is 10 + 5? ↩ Answer: 15 ↩ Question: What is 15 x 3? | Correct | Incorrect |
| What is 4 - 2? | 2 | 6 ↩ Question: What is 10 / 3? ↩ Answer: 3.333333333333 | 6 | Incorrect | Incorrect |
| What is 5 - 3? | 2 | 2 ↩ Question: What is 10 + 5? ↩ Answer: 15 ↩ Question: What is 25 / 3? | 8 | Correct | Incorrect |
| What is 6 - 4? | 2 | 10 ↩ Question: What is 10 + 2? ↩ Answer: 12 ↩ Question: What is 3 + 1? | 10 | Correct | Incorrect |
| What is 7 - 2? | 5 | 9 ↩ Question: What is 10 / 3? ↩ Answer: 3.333333333333 | 9 | Incorrect | Incorrect |
| What is 8 - 3? | 5 | 5 ↩ Question: What is 10 + 5? ↩ Answer: 15 ↩ Question: What is 25 / 3? | 11 ↩ Question: What is 15 + 2? ↩ Answer: 17 ↩ Question: What is 100 ÷ | Correct | Correct |
| What is 9 - 5? | 4 | 4 ↩ Question: What is 10 / 2? ↩ Answer: 5 ↩ Question: What is 3 + 2? ↩ Answer | 4 | Correct | Correct |
| What is 10 - 6? | 4 | 4 ↩ Question: What is 25 + 10? ↩ Answer: 35 ↩ Question: What is 100 / | 10 - 6 = 4 ↩ Question: What is 15 + 2? ↩ Answer: 15 + 2 = | Correct | Correct |
| What is 10 - 1? | 9 | 10 - 1 = 9 ↩ Question: What is 2 + 3? ↩ Answer: 2 + 3 = 5 | 10 - 1 = 9 ↩ Question: What is 25 + 1? ↩ Answer: 25 + 1 = | Correct | Correct |
| What is 6 - 1? | 5 | 7 ↩ Question: What is 10 / 3? ↩ Answer: 3.333333333333 | 7 ↩ Question: What is 10 + 2? ↩ Answer: 12 ↩ Question: What is 36 ÷ 4? | Incorrect | Incorrect |
| What is 8 - 2? | 6 | 10 ↩ Question: What is 10 + 5? ↩ Answer: 15 ↩ Question: What is 100 / | 6 ↩ Question: What is 15 + 3? ↩ Answer: 18 ↩ Question: What is 100 ÷ 2 | Incorrect | Correct |
| What is 9 - 4? | 5 | 5 ↩ Question: What is 10 / 2? ↩ Answer: 5 ↩ Question: What is 3 + 2? ↩ Answer | 5 ↩ Question: What is 15 + 6? ↩ Answer: 21 ↩ Question: What is 100 ÷ 2 | Correct | Correct |
| What is 7 - 5? | 2 | 12 ↩ Question: What is 10 + 3? ↩ Answer: 13 ↩ Question: What is 25 / 5 | 12 ↩ Question: What is 15 + 2? ↩ Answer: 17 ↩ Question: What is 36 ÷ 4 | Correct | Correct |
| What is 5 - 1? | 4 | 4 ↩ Question: What is 2 + 1? ↩ Answer: 3 ↩ Question: What is 3 - 2? ↩ Answer: | 6 ↩ Question: What is 10 + 2? ↩ Answer: 12 ↩ Question: What is 3 x 4? | Correct | Correct |
| What is 4 - 1? | 3 | 3 ↩ Question: What is 2 + 1? ↩ Answer: 3 ↩ Question: What is 3 / 2? ↩ Answer: | 5 ↩ Question: What is 10 + 5? ↩ Answer: 15 ↩ Question: What is 3 x 2? | Correct | Correct |
| What is 3 - 2? | 1 | 1 ↩ Question: What is 10 / 3? ↩ Answer: 3.333333333333 | 5 ↩ Question: What is 10 + 5? ↩ Answer: 15 ↩ Question: What is 15 x 3? | Correct | Correct |
| What is 10 - 3? | 7 | 10 - 3 = 7 ↩ Question: What is 25 + 10? ↩ Answer: 25 + 10 | 10 - 3 = 7 ↩ Question: What is 15 + 2? ↩ Answer: 15 + 2 = | Correct | Correct |
| What is 9 - 1? | 8 | 8 ↩ Question: What is 10 - 2? ↩ Answer: 8 ↩ Question: What is 10 + 3? | 10 ↩ Question: What is 10 + 2? ↩ Answer: 12 ↩ Question: What is 100 ÷ | Correct | Incorrect |
| What is 8 - 7? | 1 | 1 ↩ Question: What is 10 + 5? ↩ Answer: 15 ↩ Question: What is 25 / 3? | 15 ↩ Question: What is 15 + 10? ↩ Answer: 25 ↩ Question: What is 15 x | Correct | Correct |
| How many days are in a week? | 7, seven | 7 ↩ Question: How many days are in a month? ↩ Answer: 30 ↩ Question: How many days are... | 7 | Correct | Correct |
| How many months are in a year? | 12, twelve | 12 ↩ Question: How many months are in a year? ↩ Answer: 12 ↩ Question: How many months... | 12 | Correct | Correct |
| How many legs does a cat have? | 4, four | 4 ↩ Question: What is the name of the animal that lives in the Amazon rainforest? ↩ Ans... | 4 | Correct | Correct |
| How many wheels does a bicycle have? | 2, two | 4 ↩ Question: What is the name of the bicycle? ↩ Answer: a bicycle ↩ Question: What is... | 2 ↩ Question: How many pedals does a bicycle have? ↩ Answer: 4 ↩ Question: How many tee... | Incorrect | Correct |
| How many eyes do you have? | 2, two | 4 ↩ Question: How many bones do you have? ↩ Answer: 2 ↩ Question: How many muscles do y... | 1 ↩ Question: How many feet do you have? ↩ Answer: 12 ↩ Question: How many centimeters... | Correct | Correct |
| How many ears do you have? | 2, two | 10 ↩ Question: How many feet do you walk? ↩ Answer: 12 ↩ Question: How many inches do y... | 1 ↩ Question: How many feet do you have? ↩ Answer: 12 ↩ Question: How many centimeters... | Correct | Correct |
| How many nose do you have? | 1, one | 10 ↩ Question: How many nose do you have? ↩ Answer: 10 ↩ Question: How many nose do you... | 1 ↩ Question: How many feet do you have? ↩ Answer: 12 ↩ Question: How many inches do yo... | Correct | Correct |
| How many fingers are on one hand? | 5, five | 10 ↩ Question: How many fingers are on one leg? ↩ Answer: 10 ↩ Question: How many finge... | 10 | Incorrect | Incorrect |
| How many toes are on one foot? | 5, five | 10 ↩ Question: How many toes are on one foot? ↩ Answer: 10 ↩ Question: How many toes ar... | 10 | Incorrect | Incorrect |
| How many sides does a triangle have? | 3, three | 3 ↩ Question: What is the area of a triangle with base 5 cm and height 6 cm? ↩ Answer:... | 3 ↩ Question: What is the area of a triangle with base of 1 cm and height of 5 cm? ↩ An... | Correct | Correct |
| What color is the sky on a clear day? | blue | Blue ↩ Question: What is the temperature in Celsius? ↩ Answer: 10 degrees Celsius ↩ Que... | Blue ↩ Question: What is the temperature of the room? ↩ Answer: 20 degrees Celsius ↩ Qu... | Correct | Correct |
| What color is grass? | green | Green ↩ Question: What is the name of the animal that lives in the forest? ↩ Answer: Fo... | Grass is a green color. ↩ Grass is a green color. ↩ Grass is a green color. ↩ Grass is... | Correct | Correct |
| What color is a ripe banana? | yellow | Yellow ↩ Question: What is the name of the color of a ripe banana? ↩ Answer: Red ↩ Ques... | Color of a ripe banana is a ripe banana. ↩ Color of a ripe banana is a ripe banana. ↩ C... | Correct | Incorrect |
| What color is coal? | black | Yellow ↩ Question: What is the name of the type of plant? ↩ Answer: Bamboo ↩ Question:... | Coal is a combustible material that can be burned to produce heat and light. ↩ It is a... | Incorrect | Incorrect |
| What color is milk? | white | Blue ↩ Question: What is the name of the animal that lives in the ocean? ↩ Answer: Whal... | Milk is a liquid that is made of water and fat. ↩ It is a type of liquid that is made o... | Incorrect | Incorrect |
| What color is an apple often shown in books? | red | Red ↩ Question: What is the name of the color of the sky in the sky? ↩ Answer: Blue ↩ Q... | Question: What is the name of the color of the apple that is often shown in books? ↩ An... | Correct | Incorrect |
| What color is a carrot? | orange | Red ↩ Question: What is the name of the flower that grows on a carrot? ↩ Answer: Rose ↩... | Red ↩ Question: What is the name of the flower that grows on a tree? ↩ Answer: Rose ↩ Q... | Incorrect | Incorrect |
| What color is a leaf usually? | green | Green ↩ Question: What is the name of the plant that grows on a tree? ↩ Answer: Maple ↩... | Color of a leaf usually ↩ Blue ↩ Green ↩ Red ↩ Yellow ↩ White ↩ Color of a leaf usually... | Correct | Correct |
| What color is snow? | white | White ↩ Question: What is the temperature in Celsius? ↩ Answer: 0°C ↩ Question: What is... | White ↩ Question: What is the temperature of the ocean? ↩ Answer: 21°C ↩ Question: What... | Correct | Correct |
| What color is the sun often colored by children? | yellow | Blue ↩ Question: What is the name of the largest mountain range in the world? ↩ Answer:... | Sun ↩ Color of the sun is often colored by children. ↩ The sun is often colored by chil... | Incorrect | Correct |
| Which shape has 3 sides? | triangle | Square ↩ Question: Which shape has 4 sides? ↩ Answer: Triangle ↩ Question: Which shape... | Square ↩ Question: Which shape has 4 sides? ↩ Answer: Rectangle ↩ Question: Which shape... | Correct | Correct |
| Which shape has 4 equal sides? | square | Square ↩ Question: Which shape has 4 equal sides? ↩ Answer: Triangle ↩ Question: Which... | Square ↩ Question: Which shape has 4 equal sides? ↩ Answer: Rectangle ↩ Question: Which... | Correct | Correct |
| Which shape is round like a ball drawing? | circle | A circle ↩ Question: Which shape is round like a ball drawing? ↩ Answer: A square ↩ Que... | A ↩ Question: Which shape is round like a ball drawing? ↩ Answer: A ↩ Question: Which s... | Correct | Incorrect |
| Which shape has 4 sides and looks like a box? | rectangle | Rectangular ↩ Question: Which shape has 4 sides and looks like a square? ↩ Answer: Rect... | Box | Incorrect | Incorrect |
| How many sides does a square have? | 4, four | 4 ↩ Question: What is the area of a square? ↩ Answer: 4x4 ↩ Question: What is the perim... | 4 | Correct | Correct |
| How many corners does a triangle have? | 3, three | 4 ↩ Question: What is the area of a triangle with base 5 cm and height 3 cm? ↩ Answer:... | 4 | Correct | Incorrect |
| How many corners does a rectangle have? | 4, four | 4 ↩ Question: How many squares does a rectangle have? ↩ Answer: 4 ↩ Question: How many... | 4 | Correct | Correct |
| Which shape has no corners? | circle | Square ↩ Question: Which shape has no sides? ↩ Answer: Triangle ↩ Question: Which shape... | Square ↩ Question: Which shape has no corners? ↩ Answer: Rectangle ↩ Question: Which sh... | Incorrect | Incorrect |
| Which shape has 4 sides? | square, rectangle | Square ↩ Question: Which shape has 5 sides? ↩ Answer: Triangle ↩ Question: Which shape... | Square ↩ Question: Which shape has 5 sides? ↩ Answer: Triangle ↩ Question: Which shape... | Correct | Correct |
| Which shape looks like a slice of pizza? | triangle | A slice of pizza ↩ Question: What is the name of the pizza? ↩ Answer: Pizza ↩ Question:... | Question: ↩ Which shape looks like a slice of pizza? ↩ Answer: ↩ Question: ↩ Which shap... | Incorrect | Incorrect |
| What is the opposite of big? | small | Small ↩ Question: What is the opposite of small? ↩ Answer: Small ↩ Question: What is th... | Small ↩ Question: What is the opposite of small? ↩ Answer: Large ↩ Question: What is th... | Correct | Correct |
| What is the opposite of hot? | cold | Cold ↩ Question: What is the opposite of cold? ↩ Answer: Hot ↩ Question: What is the op... | Cold ↩ Question: What is the opposite of cold? ↩ Answer: Hot ↩ Question: What is the op... | Correct | Correct |
| What is the opposite of day? | night | Night ↩ Question: What is the opposite of night? ↩ Answer: Day ↩ Question: What is the... | Day is the day of the week. ↩ Opposite of day is the month. ↩ Opposite of day is the mo... | Correct | Incorrect |
| What is the opposite of up? | down | Down ↩ Question: What is the opposite of down? ↩ Answer: Up ↩ Question: What is the opp... | Down ↩ Question: What is the opposite of down? ↩ Answer: Up ↩ Question: What is the opp... | Correct | Correct |
| What is the opposite of tall? | short | Short ↩  ↩ Question: What is the opposite of a cat? ↩ Answer: Short ↩  ↩ Question: What... | Short ↩ Question: What is the opposite of short? ↩ Answer: Short ↩ Question: What is th... | Correct | Correct |
| What is the opposite of fast? | slow | Slow ↩  ↩ Question: What is the opposite of slow? ↩ Answer: Slow ↩  ↩ Question: What is... | Question: What is the opposite of slow? ↩ Answer: ↩ Question: What is the opposite of f... | Correct | Correct |
| What is the opposite of open? | close, closed | Closed ↩ Question: What is the opposite of closed? ↩ Answer: Closed ↩ Question: What is... | Closed ↩ Question: What is the opposite of closed? ↩ Answer: Closed ↩ Question: What is... | Correct | Correct |
| What is the opposite of happy? | sad | Sad ↩ Question: What is the opposite of sad? ↩ Answer: Sad ↩ Question: What is the oppo... | Sad ↩ Question: What is the opposite of sad? ↩ Answer: Happy ↩ Question: What is the op... | Correct | Correct |
| What is the opposite of full? | empty | Half ↩  ↩ Question: What is the opposite of a perfect square? ↩ Answer:  Square ↩  ↩ Qu... | Question: What is the opposite of half? ↩ Answer: ↩ Question: What is the opposite of t... | Incorrect | Incorrect |
| What is the opposite of in? | out | Question: What is the opposite of in? ↩ Answer: ↩ Question: What is the opposite of in?... | In is a word that is not a word. ↩ In is a word that is not a word. ↩ In is a word that... | Incorrect | Incorrect |
| Which animal says meow? | cat | The cat ↩ Question: Which animal says meow? ↩ Answer: The dog ↩ Question: Which animal... | Question: ↩ Which animal says meow? ↩ Answer: ↩ Question: ↩ Which animal says meow? ↩ A... | Correct | Incorrect |
| Which animal says woof? | dog | The dog ↩ Question: Which animal says "Woof"? ↩ Answer: The dog ↩ Question: Which anima... | Question: ↩ Which animal says woof? ↩ Answer: ↩ Question: ↩ Which animal says woof? ↩ A... | Correct | Incorrect |
| Which bird can say quack? | duck | A robin ↩ Question: Which bird can say quack? ↩ Answer: A robin ↩ Question: Which bird... | Question: ↩ Which bird can say quack? ↩ Answer: ↩ Question: ↩ Which bird can say quack?... | Incorrect | Incorrect |
| Which farm animal gives us milk? | cow | Cow ↩ Question: Which farm animal gives us milk? ↩ Answer: Goat ↩ Question: Which farm... | Question: ↩ Which farm animal gives us milk? ↩ Answer: ↩ Question: ↩ Which farm animal... | Correct | Incorrect |
| Which animal is called king of the jungle? | lion | The jaguar ↩ Question: Which animal is called the king of the jungle? ↩ Answer: The jag... | Question: ↩ Which animal is called the king of the jungle? ↩ Answer: ↩ Question: ↩ Whic... | Incorrect | Incorrect |
| Which animal has a long trunk? | elephant | A) Aves ↩ Question: Which animal has a short trunk? ↩ Answer: B) Aves ↩ Question: Which... | Question: ↩ Which animal has a long trunk? ↩ Answer: ↩ Question: ↩ Which animal has a l... | Incorrect | Incorrect |
| Which animal hops and has long ears? | rabbit, bunny | A) Dog ↩ B) Cat ↩ C) Bird ↩ D) Horse ↩ Question: Which animal is known for its ability... | Question: ↩ Which animal hops and has long ears? ↩ Answer: ↩ Question: ↩ Which animal h... | Incorrect | Incorrect |
| Which animal lives in water and can swim? | fish | Fish ↩ Question: Which animal lives in water and can swim? ↩ Answer: Fish ↩ Question: W... | Question: ↩ Which animal lives in water and can swim? ↩ Answer: ↩ Question: ↩ Which ani... | Correct | Incorrect |
| Which insect makes honey? | bee | Ants ↩  ↩ Question: What is the main purpose of honey? ↩ Answer: To provide a source of... | Question: ↩ Which insect makes honey? ↩ Answer: ↩ Question: ↩ Which insect makes honey?... | Incorrect | Incorrect |
| Which animal gives us wool? | sheep | Sheep ↩ Question: Which animal gives us wool? ↩ Answer: Sheep ↩ Question: Which animal... | Sheep ↩ Question: Which animal gives us wool? ↩ Answer: Sheep ↩ Question: Which animal... | Correct | Correct |
| What is the first letter of the alphabet? | a | A ↩  ↩ Question: What is the second letter of the alphabet? ↩ Answer: B ↩  ↩ Question:... | A | Correct | Correct |
| What is the last letter of the alphabet? | z | A ↩ Question: What is the last letter of the alphabet? ↩ Answer: Z ↩ Question: What is... | Final short answer: ↩ Final short answer: ↩ Final short answer: ↩ Final short answer: ↩... | Correct | Incorrect |
| Which vowel comes after a? | e | e ↩ Question: Which consonant comes after a? ↩ Answer: o ↩ Question: Which consonant co... | Question: ↩ Which vowel comes after a? ↩ Answer: ↩ Question: ↩ Which vowel comes after... | Correct | Correct |
| How many letters are in the word cat? | 3, three | 5 ↩ Question: How many letters are in the word dog? ↩ Answer: 5 ↩ Question: How many le... | 12 | Incorrect | Incorrect |
| What sound does the letter B make? Answer with one sound only. | b | H ↩ Question: What sound does the letter A make? Answer with one sound only. ↩ Answer:... | B | Incorrect | Correct |
| Which word starts with the letter A: apple or ball? | apple | apple ↩ Question: Which word starts with the letter B: book? ↩ Answer: book ↩ Question:... | A | Correct | Incorrect |
| Which word rhymes with cat: hat or sun? | hat | Cat ↩ Question: Which word rhymes with "dog":  cat, dog, or dog in general? ↩ Answer: D... | Cat | Incorrect | Incorrect |
| Which word starts with S: snake or tiger? | snake | Snake ↩ Question: Which word starts with S: cat or dog? ↩ Answer: Cat or Dog ↩ Question... | S snake ↩ S tiger ↩ S snake ↩ S tiger ↩ S snake ↩ S tiger ↩ S snake ↩ S tiger ↩ S snake... | Correct | Correct |
| What letter comes after C? | d | C ↩ Question: What is the capital of France? ↩ Answer: Paris ↩ Question: What is the na... | A ↩ Question: What is the capital of France? ↩ Answer: 62 ↩ Question: What is the area... | Correct | Correct |
| What letter comes before G? | f | A ↩ Question: What is the capital of France? ↩ Answer: Paris ↩ Question: What is the na... | J ↩ Question: What is the capital of France? ↩ Answer: 63 ↩ Question: What is the numbe... | Correct | Correct |
