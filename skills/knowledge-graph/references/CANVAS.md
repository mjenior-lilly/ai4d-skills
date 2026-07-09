# JSON Canvas (`.canvas`) Reference

Use `.canvas` files for visual artifacts — mind maps, architecture diagrams, concept maps, and flowcharts — when a spatial layout communicates better than prose or a Mermaid block. Canvas nodes can embed vault notes, so a canvas doubles as a visual index that links back into the graph.

Follows the JSON Canvas 1.0 spec (https://jsoncanvas.org/spec/1.0/). Place canvases in the relevant domain folder or `00_Meta/`; centralize any image nodes under `00_Meta/Attachments/`.

## File structure

A `.canvas` file is JSON with two optional top-level arrays:

```json
{
  "nodes": [],
  "edges": []
}
```

## Nodes

Every node requires `id` (unique 16-char hex string), `type`, `x`, `y`, `width`, `height`. Optional `color` is a preset `"1"`–`"6"` or a hex string.

| `type` | Required extra fields | Use |
|--------|-----------------------|-----|
| `text` | `text` (Markdown string) | Free-form note box |
| `file` | `file` (vault-relative path); optional `subpath` like `#Heading` | Embed a note, image, or PDF |
| `link` | `url` | External link card |
| `group` | optional `label` | Visual container for other nodes |

```json
{
  "id": "6f0ad84f44ce9c17",
  "type": "file",
  "file": "20_Permanent/Architecture Overview.md",
  "x": 0, "y": 0, "width": 400, "height": 300
}
```

## Edges

Connect two nodes. Required: `id`, `fromNode`, `toNode`. Optional: `fromSide`/`toSide` (`top`|`right`|`bottom`|`left`), `fromEnd`/`toEnd` (`none`|`arrow`), `color`, `label`.

```json
{
  "id": "a1b2c3d4e5f60718",
  "fromNode": "6f0ad84f44ce9c17",
  "toNode": "9d8c7b6a5e4f3021",
  "toSide": "left",
  "label": "depends on"
}
```

## Authoring rules

1. Generate unique 16-char hex IDs; never collide across nodes and edges.
2. Position nodes to avoid overlap — leave 50–100px spacing.
3. Every `fromNode`/`toNode` must reference an existing node `id`.
4. Prefer `file` nodes that embed real vault notes over duplicating their text, so the canvas stays linked to the graph.
5. Validate: parse the JSON, confirm all IDs are unique, and confirm every edge reference resolves.

## When to prefer Mermaid instead

For small inline diagrams kept *inside* a note, use a Mermaid block (see OBSIDIAN-SYNTAX.md). Reach for `.canvas` when the diagram is a standalone artifact, needs free spatial layout, or should embed whole notes as nodes.
