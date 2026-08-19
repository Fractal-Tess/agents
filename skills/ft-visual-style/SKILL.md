---
name: ft-visual-style
description: Create image directions and prompts in Fractal Tess's dark, technical, sculptural visual language. Use for project logos, hero art, social cards, product illustrations, and image-generation prompts that should feel consistent with Faber, Znake, ClipSync, Scorch, or Shadoword.
---

# FT Visual Style

## Core direction

Create a single iconic visual on a near-black, charcoal, or otherwise restrained field. The image should feel nocturnal, technical, and intentional: generous negative space, a clear focal discontinuity, and a limited palette with one identity hue carrying most of the energy.

Use one primary motif, not a collage. Favor faceted or sculptural forms, translucent energy, signal geometry, flowing line bundles, mesh/network connections, or precise technical marks. Render with controlled depth: crisp silhouette, selective rim light, a soft localized glow, and subtle atmospheric color blooms. Treat darkness and quiet zones as composition, not unused space.

## Palette and material

- Start with an obsidian or cool-charcoal base.
- Choose the project’s signature hue; keep saturation concentrated at the focal point.
- Use a second hue only when it clarifies a relationship, direction, or data flow.
- Keep neutrals near-white, soft gray, and dark plate tones.
- Prefer faceted matte surfaces, smoky/translucent ribbons, fine grids, grain, or glass-like layers over generic smooth gradients.
- Use the project-specific palette when it is known. Typical identity directions include ember orange, vivid green, cyan with coral, ultraviolet, or magenta/cyan signal light.

## Composition

- Reserve broad quiet space for product copy or UI overlay, but do not render text into generated artwork.
- Center or offset one hero object; support it with only a few particles, hairlines, nodes, or directional traces.
- Use a deliberate void, dark channel, or clean field to create contrast with the luminous subject.
- For social cards, keep the mark/object distinct and leave a calm copy zone rather than filling the frame.
- Make small-scale silhouettes survive favicon or app-icon reduction.

## Logos and marks

For a logo, app mark, or favicon, request a fully transparent background by default. State that the alpha channel must remain transparent around the mark and that the image must not simulate transparency with a dark, white, checkerboard, or scenic field. Use an opaque background only when the user explicitly asks for a lockup, social card, or other composed artwork.

Keep the silhouette simple enough to survive small-size reduction. Avoid rendered words beyond the exact text the user explicitly requests.

## Prompt structure

Write prompts in this order: subject, concept, composition, material/light, palette, texture, and exclusions. Name the chosen project hue and what it represents. Explain why the negative space exists.

Example direction:

> A single faceted violet core suspended in a near-black field, with two translucent signal ribbons curling around it and a narrow vertical quiet channel beside the core. Sparse cyan and magenta frequency marks imply data flow without becoming a dashboard. Sculptural matte depth, sharp rim highlights, fine technical grain, generous empty space for adjacent copy. No text, no stock-photo people, no generic blue SaaS gradient, no busy collage.

## Avoid

- Generic blue-purple SaaS gradients or undirected neon.
- Flat clip art, glossy plastic, photorealistic stock scenes, or crowded dashboard fragments.
- More than one dominant object.
- Dense decoration across the whole canvas.
- Rendered text, logos copied from an existing project, or project-specific mascots unless explicitly requested.
- Treating all projects as violet: the shared language is dark restraint and concentrated identity color, not one fixed palette.

## Cost-aware generation

fal gpt-image-2 bills per size and quality. Drafts are cheap; finals are not. Never default to high.

Reference pricing (per image, from fal):

| Size | low | medium | high |
|---|---|---|---|
| 1024x768 | $0.005 | $0.037 | $0.145 |
| 1024x1024 | $0.006 | $0.053 | $0.211 |
| 1024x1536 | $0.005 | $0.042 | $0.165 |

Protocol:

1. Draft default: `image_size: "square"` (512x512), `quality: "low"`, `output_format: "png"`, `num_images: 1`. A 512x512 low draft costs a fraction of a cent.
2. Present the result, then ask the user before any pricier regeneration. Quote the price of the upgrade, e.g. "regenerate at medium 1024x1024? +$0.047".
3. Use `image_size: "square_hd"` (1024x1024) and `quality: "medium"` only on explicit request. Reserve `quality: "high"` for final hero assets.
4. The model ignores transparent-background prompts: it always paints an opaque field. Expect it and plan post-processing: global color key (ImageMagick `-fuzz 7% -transparent`) for uniform fields, `fal-ai/imageutils/rembg` for photos. Saliency removers drop thin structural lines, so keying beats rembg for line-art logos.
