# Project – Phase R Submission
**Software Testing – Research in Software Testing**

---

**Group:** 20

**Members:**
- Md Tawfiq Bashar
- Saimon Chowdhury Fahim
- S M Khasrul Alam Shakil

---

> **Instructions:** Do not modify the task descriptions or section headings.
> Fill in your answers only where indicated. Replace placeholder text but leave
> everything else intact. Each answer should be annotated with the contributing
> group member where applicable.

---

## Task R – Research in Software Testing

### Selected Paper

**Title:**
> Enhanced Prompting Framework for Code Summarization with Large Language Models

**Authors:**
> Minying Fang, Xing Yuan, Yuying Li, Haojie Li, Chunrong, Fang, Junwei Du

**Venue / Year:**
> ISSTA 2025

**Why did you choose this paper? (2–3 sentences)**
> We selected this paper because it tackles the critical issue of software maintainability by automating code summarization, a process often neglected by developers under tight deadlines. It addresses the limitations of standard Large Language Models (LLMs)—which struggle with the structural differences between programming and natural languages—by introducing an innovative Enhanced Prompting framework (EP4CS) that does not require computationally expensive fine-tuning.

---

### Presentation

Upload your slides to the repository under `research/`. Your **~15-minute presentation** should cover:
1. The problem the paper addresses
2. The proposed approach
3. Key results and takeaways

**Presentation date and submission deadline will be announced via the exercise session announcements on StudIP.**

**Presentation date (per announcement):** <!-- fill in your assigned date -->

**Slide file:** <!-- e.g. research/slides_groupXX.pdf -->

---

## AI Review Task

### Part 1 – AI-Generated Paper Summary

Select a **core section** of your paper (e.g. the approach or method section) and prompt an LLM to produce a **400–500 word summary** of it.

**LLM used:**
> Gemini 3.1 Pro

**Section summarised:**
> Section 3 – Framework

**Prompt used:**
> "Act as an academic assistant. Generate a 400-500 word summary of Section 3 (Framework) from the provided EP4CS research paper. Focus on the architecture and the two-stage training process."

**LLM-generated summary:**
> The EP4CS (Enhanced Prompting framework for Code Summarization) operates through a specialized two-stage training process utilizing four primary components: a Code Encoder, a Mapper, a Struct-Agent, and a frozen Large Language Model (LLM). This architecture is designed to dynamically adjust continuous prompt vectors to improve the LLM's task-specific understanding.
> 
> In the first stage, the framework tackles the challenge of providing specialized background knowledge to the LLM. The Mapper aligns code snippets with corresponding background knowledge using multiple pre-training tasks. It utilizes a Left Transformer (LT) encoder to process background knowledge and a Right Transformer (RT) encoder to integrate virtual tokens with the code representation. To optimize this alignment, the Mapper employs contrastive learning (maximizing mutual information to distinguish between positive and negative samples), knowledge-grounded text generation, and a bidirectional code-knowledge matching loss.
>
> The second stage focuses on generating structured prompts that capture the structural semantics of the code—a noted weakness in standard LLM decoding. The Struct-Agent employs Variational Autoencoders (VAEs) to translate the code's structural representation into a probability distribution via variational inference. During inference, the Mapper outputs a knowledge vector, while the Struct-Agent outputs a structural vector. These vectors are fed into a projector to align their dimensions with the LLM's embedding space. Finally, these information-rich continuous prompts guide the frozen LLM to generate highly accurate code summaries, minimizing the discrepancy between the generated output and the ground-truth summaries.

**Quality evaluation:**

> Compare the AI-generated summary with the original text. Address:
> - **Correctness:** Are all key claims accurately reproduced?
> - **Completeness:** Are important aspects missing?
> - **Peculiarities:** Any hallucinations, overgeneralisations, or misleading statements?

> - **Correctness:** The summary accurately captures the core technical claims of the paper, specifically the roles of the LT/RT encoders, the loss functions (contrastive, generative, matching), and the use of VAEs in the Struct-Agent.
> - **Completeness:** The summary effectively condenses the highly technical mathematical equations of Section 3 into readable text, though it understandably skips the precise algorithmic formulations (like KL divergence and InfoNCE equations) to fit the word limit constraints. 
> - **Peculiarities:** The summary avoids hallucinations, staying strictly grounded in the provided text without overgeneralizing the capabilities of the frozen LLM.

---

### Part 2 – LLM Answers to Research Exercise Questions

Select **one of the five research exercise papers** covered during the course and one column of guiding questions from the corresponding exercise sheet.

**Paper selected:**
> Code-Aware Prompting: A Study of Coverage-Guided Test Generation in Regression Setting using LLM

**Question column selected:**
> Guiding Questions (Path Constraints & Minimization)

**LLM used:**
> Gemini

**Prompt used:**
> Answer the following questions based on the provided research paper:
What is a path constraint in the context of test generation?
Why does the number of paths grow exponentially and how is this addressed?
What is a basis path and why is it important?
Explain and interpret Figure 5 in the paper.


**LLM-generated answers:**
> 1. What is a path constraint in the context of test generation? In the context of test generation, a path constraint is a specific condition (or set of conditions) that must be satisfied to steer a program's execution along a particular control path. Finding a concrete solution—meaning specific input values—that meets these constraints allows that specific path to be executed and tested in a regression setting.

> 2. Why does the number of paths grow exponentially and how is this addressed? The number of execution paths grows exponentially because each new branch condition (such as an if statement) multiplies the potential routes through the code. The paper addresses this through a technique called "path minimization". Instead of attempting to collect and test every single path variation, the system only collects a linearly independent subset of paths that actively increase overall branch coverage, discarding redundant paths.

> 3. What is a basis path and why is it important? A basis path is a path that forms part of a "linear basis" for all possible paths within a method's control-flow graph. It is highly important for software testing because if a test suite can successfully execute a complete set of basis paths for a method, it is guaranteed to achieve full branch coverage for that method without needing to test every redundant path combination.

> 4. Explain and interpret Figure 5 in the paper. Figure 5 illustrates how the path minimization algorithm prevents exponential path explosion. Figure 5a outlines the pseudocode for the algorithm, which splits paths into constraints and filters out redundancies. Figure 5b provides a visual interpretation: a method with 3 sequential if conditions normally yields 8 possible execution paths (2^3 = 8). However, applying the minimization algorithm successfully reduces the required testing to just 4 paths (n + 1 = 4), ensuring every unique branch condition is still tested efficiently.


**Evaluation:**

> Compare the LLM's answers with your own (if available) or evaluate them independently. Address:
> - **Correctness:** Are the answers factually accurate with respect to the paper?
> - **Quality:** Are the answers sufficiently detailed and well-reasoned?
> - **Differences:** Where does the LLM diverge from your answers or from the paper?

> Correctness: The LLM's answers are factually accurate and directly aligned with the claims made in Section 3 of the paper. It correctly defines path constraints, the exponential growth problem, and basis paths.

> Quality: The answers are highly detailed and well-reasoned. The LLM effectively broke down the theoretical concepts (like basis paths ensuring full branch coverage) and practically applied them to the visual evidence in Figure 5 without unnecessary jargon.
> Differences: The LLM did not diverge from the paper. It accurately summarized the paper's specific methodology for approximating path constraints statically rather than inventing external definitions.


---

## Contribution Overview

Fill in the **Member** column headers with each group member's name and mark with an **×**
who contributed to which sub-task. Add or remove rows as needed for your group.

| Sub-task / Item | Saimon | Shakil | Tawfiq | Member 4 | Member 5 |
|-----------------|:--------:|:--------:|:--------:|:--------:|:--------:|
| Paper selection (PR-I) | | | × | | |
| Presentation (PR-II) | | × | | | |
| AI summary evaluation (PR-III, Part 1) | × | | × | | |
| LLM answers evaluation (PR-III, Part 2) | × | × | | | |
