# Create a knowledge-corpus benchmark

Orchestrate a multi-agent pipeline that analyzes a raw knowledge corpus and produces a corpus-grounded, adversarial evaluation dataset.

Use specialized generation subagents to divide the workload and stay within context limits.

---

## Architecture and orchestration

Use this execution structure to avoid quality loss and truncated output:

### 1. Tier 1: Orchestrator and analyst
* **Model:** GPT-5.5 with high thinking, or Claude Opus-4.8 with high thinking.
* **Reasoning:** High reasoning.
* **Responsibilities:** Execute Phase 1 & 2. Generate a strict distribution matrix. Assign batches to Tier 2 agents. Aggregate, validate, and normalize final outputs.

### 2. Tier 2: Item-generation subagents
* **Model:** GPT-5.5 with low thinking, or Claude Sonnet-4.6 with low thinking.
* **Reasoning:** Fast inference.
* **Workers:** 5 to 10 concurrent instances.
* **Responsibilities:** Consume a targeted item specification from the Orchestrator and output exactly 10-15 high-quality questions per batch according to a strict JSON schema.

---

## Phase 1: Corpus analysis (orchestrator only)

Analyze the source corpus. Do not invent information; every concept must map to a direct citation or a logical inference that follows necessarily from the text.

Generate the following two artifacts:

### 1. Structured knowledge map
* **Taxonomy Tree:** Map out Major Domains -> Subdomains -> Core Concepts -> Explicit Procedures.
* **Dependencies:** Document which concepts or procedures are strict prerequisites for others.

### 2. Corpus statistics and distribution matrix
Calculate the approximate text volume weight of each domain and map out your generation targets based on a total benchmark size of **[User Input Target, e.g., 150]** questions.

Apply these distribution constraints:
* **Difficulty Distribution:** 20% Easy, 35% Medium, 30% Hard, 15% Expert.
* **Question Type Mix:** Balance across Factual, Conceptual, Multi-Hop Reasoning, Procedural, Application, Decision-Making, Troubleshooting, Edge Cases, and Cross-Domain Synthesis.

---

## Phase 2: Subagent workload allocation (orchestrator only)

Divide your calculated Distribution Matrix into discrete batches of **10 to 15 questions** per assignment.

For each batch, construct a targeted instruction block for a Tier 2 Subagent.
*Example Assignment:* "Subagent 3: Generate 12 Hard, Multi-Hop Reasoning questions covering Domain B (Subdomain B.2: Troubleshooting Protocols)."

Each assignment must explicitly require one or more negative response examples per item. Negative responses should represent plausible model failures, not random wrong answers.

---

## Phases 3 and 4: Subagent generation instructions
*(The following instructions are passed to each Tier 2 Subagent worker along with their batch assignment)*

Generate a batch of evaluation items from the assigned parameters and corpus slice.

### Question quality and adversarial constraints:
1. **Corpus dependence:** Every item must require information from the corpus and must not be answerable from generic domain knowledge alone.
2. **Discriminative Power:** Hard and Expert questions must require multi-hop logic or synthesis of distant corpus sections. Do not use obscure, trivial wording to simulate difficulty.
3. **Adversarial design:** Write questions that expose shallow semantic matching, surface-level hallucinations, and ungrounded inferences.
4. **No ambiguity:** Ensure the corpus supports exactly one objectively correct answer.
5. **Negative Response Utility:** Include at least one plausible incorrect response for each item. It must be close enough to expose a real judging failure mode, and its explanation must identify the specific fact, constraint, or reasoning step it violates.

### Output format
For each generated item, output one self-contained JSON object following this exact schema, except that `domain_context` must be omitted when it is not applicable. Do not include Markdown outside the JSON block.

```json
{
  "id": "BENCH-XYZ-[Sequential_Number]",
  "domain": "String",
  "subdomain": "String",
  "difficulty": "Easy | Medium | Hard | Expert",
  "question_type": "Factual | Conceptual | Multi-Hop | Procedural | Application | Decision-Making | Troubleshooting | Edge_Case | Synthesis",
  "question": "Clear, unambiguous prompt text.",
  "canonical_answer": "Concise, direct, objective answer string.",
  "expanded_answer": "Comprehensive, expert-level explanation detailing why this is correct and why common misconceptions fail.",
  "required_facts": [
    "Minimum atomic fact 1 required for a full score.",
    "Minimum atomic fact 2 required for a full score."
  ],
  "negative_responses": [
    {
      "response": "Plausible but incorrect answer a model might give.",
      "failure_mode": "The specific misconception, missing constraint, unsupported inference, or reasoning error this response represents.",
      "violated_facts": [
        "Required fact or source-backed constraint contradicted or omitted by the negative response."
      ]
    }
  ],
  "reasoning_path": {
    "evidence_summary": "Summary of source text proof points.",
    "logical_steps": [
      "Step 1: Locate concept X in section Y.",
      "Step 2: Synthesize with constraint Z found in section W."
    ]
  },
  "source_references": [
    "Section 3.2.1",
    "Page 45 / Paragraph 2"
  ],
  "domain_context": {
    "specialized_terminology": [
      {
        "term": "Domain-specific term used in the question or answer.",
        "definition": "Corpus-grounded definition of the term.",
        "source_reference": "Section or page reference."
      }
    ],
    "domain_assumptions": [
      "Convention, default, or baseline assumption specific to this corpus domain that a general-purpose judge may not know."
    ],
    "novel_claims": [
      {
        "claim": "A factual claim from the corpus that may appear novel, counterintuitive, or unsupported without corpus access.",
        "evidence": "Direct supporting evidence from the corpus.",
        "source_reference": "Section or page reference."
      }
    ],
    "evaluation_notes": "Optional free-text guidance for the judge about domain-specific scoring considerations for this item."
  }
}
```

### Negative response requirements

Each `negative_responses` entry must:

* Be objectively wrong or materially incomplete according to the cited corpus.
* Be plausible for a model using shallow semantic matching, generic domain knowledge, or incomplete multi-hop reasoning.
* Avoid straw-man nonsense, joke answers, and purely formatting-invalid responses.
* Include enough diagnostic detail for a downstream judge to compare a candidate response against both the gold answer and known failure modes.
* Use the same level of specificity expected from real model outputs for the item.

For Hard and Expert items, prefer two negative responses when useful: one that misses a source constraint and one that makes an unsupported synthesis or overgeneralization.

### Domain context requirements

The `domain_context` field is optional per item. Include it when the item involves any of the following:

* **Specialized terminology** that a general-purpose judge model is unlikely to know or may misinterpret. Document each term with its corpus-grounded definition and source reference.
* **Domain assumptions**: conventions, defaults, units, naming schemes, or baseline expectations that are standard within the corpus domain but not common knowledge. A judge without this context may incorrectly flag valid claims as unsupported.
* **Novel claims**: factual statements from the corpus that may appear counterintuitive, surprising, or hallucinated to a model without access to the source material. Each novel claim must include direct evidence and a source reference so the judge can accept it rather than penalize it.
* **Evaluation notes**: free-text guidance when the item has domain-specific scoring considerations that do not fit the structured fields above. For example, noting that a particular field uses non-standard measurement units or that a procedure described in the corpus contradicts widely-held assumptions.

Omit `domain_context` when no supplementary context is needed to evaluate the item.

When included, every entry in `specialized_terminology` and `novel_claims` must trace back to a specific corpus location. Do not use `domain_context` to add outside knowledge or relax answer requirements. Its only purpose is to prevent false-positive hallucination penalties on correct, corpus-grounded responses.

---

## Phase 5: Aggregation and validation (orchestrator only)

Merge all subagent batches into one dataset and validate every item before final output.

Required checks:

* Every item conforms exactly to the production schema.
* Every item has at least one `negative_responses` entry with `response`, `failure_mode`, and non-empty `violated_facts`.
* Each negative response is actually incorrect under the corpus and is not a paraphrase of the canonical answer.
* Required facts, reasoning paths, negative response explanations, and source references are mutually consistent.
* If `domain_context` is present, every `specialized_terminology` and `novel_claims` entry includes a non-empty `source_reference` that maps to the corpus. `domain_context` does not contradict the item's canonical answer, required facts, or reasoning path.
* IDs are unique and sequential within the benchmark namespace.
* The final dataset matches the target size and distribution matrix unless a deviation is explicitly recorded.
