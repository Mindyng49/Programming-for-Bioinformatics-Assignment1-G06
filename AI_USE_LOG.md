# AI USE LOG

<!-- SECB3203 prompt log. Policy: PROPOSED - for approval by the SECB3203 course team before circulation to students. Fill in, then run: python tools/check_ai_log.py AI_USE_LOG.md --assessment <key> -->

- Course: SECB3203
- Assessment: Assignment 1
- Student name: MINDY NG YU FANG, ELEANOR TING PIK EN, WONG ZI NING, HUSNA SAFIYYAH BINTI MUHAMMAD FAROUK
- Matric no: A24CS0267, A24CS0247, A24CS0313, A24CS0083
- Group ID: G06
- AI level: 1
- Tools cited: UTM format, OpenAI (2026). ChatGPT (GPT-6). Retrieved 22 November 2026 from https://chat.openai.com

## Declaration (tick exactly one)

- [ ] NIL RETURN: I did not use any generative AI tool for this assessment.
- [x] I used AI. Every interaction that influenced my work is logged below. The log is true and complete.

## Entry 1

- Date: 21 November 2026 11:48pm
- Tool: OpenAI (2026). ChatGPT (GPT-6). Retrieved 21 November 2026 from https://chat.openai.com
- Purpose: debug
- Prompt: why my pseudocode look like this help me to fix it
- Output: ChatGPT explained the problems with my pseudocode and guided me on how to improve its structure
- Verified by: Compared the corrected pseudocode with the six classification rules in the assignment requirements
- My change: Revised the pseudocode to make the steps clearer
- Used in: docs/design.md

## Entry 2

- Date: 22 November 2026 12:01am
- Tool: OpenAI (2026). ChatGPT (GPT-6). Retrieved 22 November 2026 from https://chat.openai.com
- Purpose: review
- Prompt: check my pseudocode
- Output: ChatGPT reviewed my pseudocode and provided feedback on the logic, rule order, conditions and missing details
- Verified by: Checked the feedback against the assignment brief and the required classification rules
- My change: Reviewed the suggestions and corrected the pseudocode to improve its accuracy and readability
- Used in: docs/design.md

## Entry 3

- Date: 22 November 2026 12:06am
- Tool: OpenAI (2026). ChatGPT (GPT-6). Retrieved 22 November 2026 from https://chat.openai.com
- Purpose: review
- Prompt: check my docs/design.md and tell me what I need to improve
- Output: ChatGPT reviewed the decomposition table, pseudocode, hand trace, test plan and work plan and then suggested improvements to clarity and formatting
- Verified by: Compared the feedback with the assignment requirements and reviewed my updated document
- My change: Corrected headings and fixed spelling and formatting
- Used in: docs/design.md

## Entry 4

- Date: 22 November 2026 3:20am
- Tool: OpenAI (2026). ChatGPT (GPT-6). Retrieved 22 November 2026 from https://chat.openai.com
- Purpose: debug
- Prompt: check my code and explain what is wrong and how to fix it?
- Output: ChatGPT explained mistakes in my code, including overwriting function parameters and using a variable before defining it
- Verified by: Reviewed the suggested corrections and checked
- My change: Corrected the variable assignments
- Used in: src/a1_triage.py – classify_variant()

## Entry 5

- Student: WONG ZI NING (A24CS0313), Member 3
- Date: 22 November 2026 1:10am
- Tool: OpenAI (2026). ChatGPT (GPT-6). https://chat.openai.com
- Purpose: design guidance
- Prompt: "can u guide me on the rank_variants test plan based on the assignment requirement? what cases should i include?"
- Output: ChatGPT explained the required ranking order and suggested test categories such as excluded records, tie-breaking, k = 0, negative k, large k and input preservation.
- Verified by: Checked the requirements for `rank_variants()` and compared the planned cases with the assignment brief.
- My change: Wrote the ranking test-plan section for `docs/design.md`.
- Used in: `docs/design.md`

## Entry 6

- Student: WONG ZI NING (A24CS0313), Member 3
- Date: 22 November 2026 2:13am
- Tool: OpenAI (2026). ChatGPT (GPT-6). https://chat.openai.com
- Purpose: programming guidance and review
- Prompt: "help me check my rank_variants function. does my sorting follow decision, impact, quality, depth and pos correctly?"
- Output: ChatGPT discussed filtering excluded records, sorting priorities, numeric comparisons and checking that the original inputs are not changed.
- Verified by: Reviewed the ranking conditions against the brief and ran the available ranking tests.
- My change: Implemented and reviewed `rank_variants(results, k)` as my assigned function.
- Used in: `src/a1_triage.py`

## Entry 7

- Student: WONG ZI NING (A24CS0313), Member 3
- Date: 22 November 2026 3:20am
- Tool: OpenAI (2026). ChatGPT (GPT-6). https://chat.openai.com
- Purpose: testing and debugging
- Prompt : "i already added the ranking tests, can u check the pytest and ruff output? is there anything missing?"
- Output: ChatGPT explained the test results, checking sorting tie-breaks and boundary cases, and the meaning of Ruff formatting and lint feedback.
- Verified by: Ran pytest for the ranking tests; all 11 of my ranking tests passed. Ran Ruff to check code quality during the workflow.
- My change: Completed and checked ranking tests covering decision, impact, quality, depth, position, exclusions, k values, empty input and preservation of input data.
- Used in: `tests/test_a1_triage.py`

## Entry 8

- Student: WONG ZI NING (A24CS0313), Member 3
- Date: 22 November 2026 4:10am
- Tool: OpenAI (2026). ChatGPT (GPT-6). https://chat.openai.com
- Purpose: documentation review and revision
- Prompt: "compare is there any thing left on by checking the origin(the deault with)lecturer version"
- Output: ChatGPT compared the group's design to the lecturer's template and generated revised text.
- Verified by: Reviewed `git diff -- docs/design.md`.
- My change: Incorporated AI-generated documentation edits, committed them as `e7b67ec`, pushed `zining` and merged the change through the group workflow.
- Used in: `docs/design.md`

## Entry 9

- Student: HUSNA SAFIYYAH BINTI MUHAMMAD FAROUK (A24CS0083), Member 4
- Date: 23 November 2026
- Tool: OpenAI (2026). ChatGPT (GPT-6). https://chat.openai.com
- Purpose: Software testing and output validation
- Prompt: "How can I verify the correctness and reliability of my CSV export and report generation functions?"
- Output: ChatGPT provided guidance on validating CSV formatting, output consistency, report content, decision summaries and top-k variant presentation. It also explained how to interpret automated test results.
- Verified by: Executed the automated test suite and confirmed that all 38 tests passed successfully.
- My change: Developed and evaluated test cases for the CSV export and report generation functions to verify their expected output and handling of different input conditions.
- Used in: `test_a1_triage.py`

## Entry 10

- Student: HUSNA SAFIYYAH BINTI MUHAMMAD FAROUK (A24CS0083), Member 4
- Date: 23 November 2026
- Tool: OpenAI (2026). ChatGPT (GPT-6). https://chat.openai.com
- Purpose: Software configuration management and version control
- Prompt: "How should I manage and synchronize my development changes with the group's GitHub repository?"
- Output: ChatGPT provided guidance on Git branching, staging, committing and synchronizing local changes with the remote repository.
- Verified by: Checked the active development branch, reviewed the working tree status and verified synchronization with the remote GitHub repository.
- My change: Managed the development workflow within the assigned member4-output branch and verified that the local repository was synchronized with the remote branch.
- Used in: GitHub repository, member4-output branch
- Date: 22 November 2026
- Tool: OpenAI (2026). ChatGPT (GPT-6). Retrieved [date] from https://chat.openai.com
- Purpose: programming guidance
- Prompt: "Can you guide me on how to implement decision_counts(results) based on the assignment requirements?"
- Output: ChatGPT explained how to use dictionaries to count the occurrences of each decision category and handle empty input lists and zero counts.
- Verified by: Compared the suggested counting logic with the assignment requirements and checked the expected output structure.
- My change: Implemented the decision_counts(results) function and handled cases where the input list is empty.
- Used in: src/a1_triage.py


## Entry 10
- Date: 22 November
- Tool: OpenAI (2026). ChatGPT (GPT-6). Retrieved [date] from https://chat.openai.com
- Purpose: programming guidance and debugging
- Prompt: "Help me understand how to implement impact_counts(results) using dictionaries. How should I handle zero counts?"
- Output: ChatGPT explained how to iterate through the results, count impact categories using a dictionary and ensure that categories with no occurrences are handled correctly.
- Verified by: Checked the dictionary keys and counting results against the expected impact categories in the assignment requirements.
- My change: Implemented impact_counts(results) and checked its behaviour with normal and empty input cases.
- Used in: src/a1_triage.py

## Entry 11
- Date: 22 November 2026
- Tool: OpenAI (2026). ChatGPT (GPT-6). Retrieved [date] from https://chat.openai.com
- Purpose: programming guidance and algorithm review
- Prompt: "Can you guide me on implementing gene_summary(results)? I need to summarise genes, sort them alphabetically and calculate the mean depth correctly."
- Output: ChatGPT explained how to group records by gene using dictionaries, calculate summary values and sort gene names alphabetically. It also discussed handling empty inputs and calculating mean depth.
- Verified by: Compared the grouping, sorting and mean depth calculations with the assignment requirements and manually checked sample results.
- My change: Implemented gene_summary(results) with dictionary-based grouping, alphabetical gene ordering and mean depth calculation.
- Used in: src/a1_triage.py

## Entry 12
- Date: 22 November 2026
- Tool: OpenAI (2026). ChatGPT (GPT-6). Retrieved [date] from https://chat.openai.com
- Purpose: testing and debugging
- Prompt: "Help me plan and check the test cases for decision_counts(), impact_counts() and gene_summary(). What edge cases should I include?"
- Output: ChatGPT suggested test cases covering normal inputs, empty lists, zero counts, multiple categories, alphabetical gene sorting and mean depth calculations.
- Verified by: Compared the proposed test cases with the three summary function requirements and checked the expected outputs.
- My change: Wrote tests for all three summary functions, including normal cases and relevant boundary cases.
- Used in: tests/test_a1_triage.py

## Entry 13
- Date: 22 November 2026
- Tool: OpenAI (2026). ChatGPT (GPT-6). Retrieved [date] from https://chat.openai.com
- Purpose: documentation review and revision
- Prompt: "Can you check my summary functions test plan and explain how I should document the use of dictionaries for counting and summarising in docs/design.md?"
- Output: ChatGPT reviewed the test plan and explained how dictionaries support category counting, gene grouping and summary calculations. It suggested improvements to the documentation's clarity and completeness.
- Verified by: Compared the revised test plan and dictionary explanation with the assignment requirements and reviewed the updated documentation.
- My change: Updated the test plan and added an explanation of how dictionaries are used in the three summary functions.
- Used in: docs/design.md
