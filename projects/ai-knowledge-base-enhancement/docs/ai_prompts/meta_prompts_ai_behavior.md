# Meta-Prompts (AI Behavior): Shaping AI Reasoning

Meta-prompts focused on AI behavior are advanced instructions designed to influence the cognitive processes and reasoning styles of the AI agents themselves. Unlike standard prompts that instruct *what* to do, meta-prompts guide *how* the AI should think, analyze, and approach problem-solving. They are crucial for enabling more sophisticated and nuanced AI responses, especially in complex tasks.

## Purpose and Functionality

*   **Cognitive Scaffolding**: They provide a framework for the AI's internal thought process, breaking down complex problems into manageable steps.
*   **Reasoning Style**: They can direct the AI to adopt specific reasoning styles (e.g., analytical, creative, systematic, exploratory) based on the problem domain.
*   **Metacognition**: They encourage the AI to reflect on its own assumptions and reasoning, leading to more robust and less biased outputs.
*   **Problem Decomposition**: They guide the AI in deconstructing problems, gathering information, identifying patterns, forming hypotheses, and validating conclusions.

## Example: `ai/prompts/meta/adaptive_chain_of_thought.md`

This prompt defines a structured reasoning framework for AI agents, encouraging them to break down problems, gather information, identify patterns, form hypotheses, and validate their conclusions. It emphasizes metacognitive checks to improve reasoning quality. This meta-prompt acts as a blueprint for how an AI agent should approach any given problem, making its thought process more transparent and controllable.

```markdown
You are a cognitive scaffolding specialist. Generate prompts that create optimal reasoning pathways for AI agents tackling complex problems.

**Signature**: problem_domain + complexity_level + reasoning_style → structured_prompt

**Input Variables**:

- Problem Domain: [specific field/topic]
- Complexity Level: [beginner/intermediate/expert]
- Reasoning Style: [analytical/creative/systematic/exploratory]

**Generated Prompt Components**:

1. **Cognitive Framework Setup**:
   "Before proceeding, establish your reasoning framework by..."

2. **Step-by-Step Scaffolding**:

   - Step 1: Problem decomposition ("First, break this into...")
   - Step 2: Information gathering ("Next, identify key data points...")
   - Step 3: Pattern recognition ("Then, analyze relationships between...")
   - Step 4: Hypothesis formation ("Based on patterns, hypothesize...")
   - Step 5: Validation ("Test your hypothesis by...")
   - Step 6: Synthesis ("Finally, integrate findings to...")

3. **Metacognitive Checks**:
   "At each step, pause and ask: 'What assumptions am I making?' and 'What evidence contradicts my current thinking?'"

4. **Output Validation**:
   "Before concluding, verify your reasoning chain by working backwards from your conclusion."

**Example Output**:
For researching "Blockchain scalability solutions":
"You are analyzing blockchain scalability solutions. Before proceeding, establish your reasoning framework by defining 'scalability' in blockchain context and identifying key performance metrics..."
```

## Advanced Concepts

*   **Chain-of-Thought (CoT)**: This meta-prompt is a form of CoT prompting, where the AI is instructed to show its intermediate reasoning steps. Adaptive CoT allows the AI to adjust its reasoning path based on the problem's complexity or domain.
*   **Self-Correction**: By including metacognitive checks, the AI is encouraged to identify and correct its own errors or biases during the reasoning process.
*   **Dynamic Prompt Generation**: The meta-prompt itself can generate more specific prompts based on input variables, allowing for highly customized and context-aware AI interactions.
