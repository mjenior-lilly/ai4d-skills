# notebooklm/

Copy-paste prompts for NotebookLM's output customization fields, rather than slash-command or skill invocation. Both target the same source material — machine learning, AI architecture, and computational research papers — and share the same posture: neutral, quantitative, information-dense output with no hype or marketing framing.

- `podcast.md` - Audio Overview prompt for a measured, structured, technically precise episode. Enforces a subdued host tone, precise academic language over evaluative adjectives, concise first-use definitions of field-specific terms, and a fixed structure: title/authors/central hypothesis, methodology and architecture, experimental setup and benchmarks, core metrics, neutrally framed limitations and ablations, and a succinct closing technical claim.

- `infographic.md` - Infographic prompt for a dense, diagram-first visual summary. Maximizes technical information per unit of visual space: concrete facts in every panel (parameter counts, dataset sizes, benchmark scores, ablation deltas), a visual hierarchy mirroring the paper's logical structure, and diagrams over prose — labeled pipelines, architecture stacks, and side-by-side baseline comparisons using the paper's own terminology.

- `report.md` - Briefing Report prompt for a rigorous, peer-review-grade written analysis. Produces a structured Markdown document covering metadata and core thesis, architectural and methodological framework, empirical evaluation with benchmark tables, objective error analysis and ablation results, and domain contribution — all in a neutral, dispassionate tone with exact quantitative language and no evaluative adjectives.

## How to use

1. choose the prompt file for the target output type,
2. paste it into NotebookLM's instruction or customization field,
3. attach the research paper the prompt expects.
