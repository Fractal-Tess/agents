---
name: fal-image-gen
description: Generate and edit images through fal.ai. Use when the user wants to generate, regenerate, or edit an image via fal, asks for gpt-image-2, gpt-img-2, rembg, or a transparent PNG, or wants a logo, hero art, or mockup rendered. Covers the queue API, cost-aware quality selection, and transparency post-processing.
---

# fal image generation

Generate and edit images through fal.ai using the FAL_AI key. Draft cheap, upgrade on request.

## Auth

The key lives in the environment as `FAL_AI`. Never hardcode it, never print it. Send it as a header:

```
Authorization: Key $FAL_AI
```

## Models

| Purpose | Endpoint |
|---|---|
| Text to image | `fal-ai/gpt-image-2` |
| Image edit (mask/inpaint) | `fal-ai/gpt-image-2/image-to-image` |
| Background removal | `fal-ai/imageutils/rembg` |
| Transparency conversion | `fal-ai/imageutils/transparency` |

## Request flow

Submit to the queue, poll the status URL until `COMPLETED`, fetch the result. Use the `status_url` and `response_url` from the submit response; they are authoritative even when they sit under a different model path.

```bash
# 1. submit
curl -s -H "Authorization: Key $FAL_AI" -H "Content-Type: application/json" \
  -d '{"prompt": "...", "image_size": "square", "quality": "low", "output_format": "png", "num_images": 1}' \
  https://queue.fal.run/fal-ai/gpt-image-2
# -> {"request_id": "...", "status_url": "...", "response_url": "..."}

# 2. poll status_url until status == COMPLETED (sleep 5 between polls)

# 3. fetch result
curl -s -H "Authorization: Key $FAL_AI" "$RESPONSE_URL" | jq -r '.images[0].url'
```

Large inputs, like base64 images, go in a body file, never on the command line:

```bash
B64=$(base64 -w0 image.png)
jq -nc --arg u "data:image/png;base64,$B64" '{image_url: $u}' > body.json
curl -s -H "Authorization: Key $FAL_AI" -H "Content-Type: application/json" \
  -d @body.json https://queue.fal.run/fal-ai/imageutils/rembg
```

The sync endpoint `https://fal.run/<model>` works for short jobs but times out on image generation; prefer the queue.

## Parameters (gpt-image-2)

- `prompt`: required
- `image_size`: preset or `{"width": N, "height": N}`. Presets: `square` (512x512), `square_hd` (1024x1024), `portrait_4_3`, `portrait_16_9`, `landscape_4_3`, `landscape_16_9`, `auto`. Custom dims: both edges multiples of 16, max edge 3840, total pixels 655,360 to 8,294,400
- `quality`: `low` | `medium` | `high` (default `high`, the cost driver)
- `num_images`: 1-4
- `output_format`: `jpeg` | `png` | `webp`
- `sync_mode`: true returns data URIs and skips request history
- `openai_api_key`: optional BYOK, routes through your own OpenAI quota

## Pricing (per image)

| Size | low | medium | high |
|---|---|---|---|
| 1024x768 | $0.005 | $0.037 | $0.145 |
| 1024x1024 | $0.006 | $0.053 | $0.211 |
| 1024x1536 | $0.005 | $0.042 | $0.165 |

A 512x512 `square` low draft costs a fraction of a cent.

## Cost protocol

1. Draft default: `image_size: "square"`, `quality: "low"`, `output_format: "png"`, `num_images: 1`.
2. Show the result, then ask the user before any pricier regeneration. Quote the upgrade, e.g. "regenerate at medium 1024x1024? +$0.047".
3. `square_hd` + `medium` only on explicit request. Reserve `quality: "high"` for final hero assets.
4. Never default to high.

## Transparency

gpt-image-2 ignores transparent-background prompts and always paints an opaque field. Expect it and post-process:

- Uniform field: global color key. `magick in.png -fuzz 7% -transparent '<bg>' out.png`. Flood-fill alone is not enough; it leaves background enclosed by the subject, so use the global key.
- Photos: `fal-ai/imageutils/rembg` (input `image_url`, output `image.url`).
- Saliency removers drop thin structural lines, so keying beats rembg for line art and logos.
- ChatGPT image generation does honor transparency prompts (alpha comes out real), so it is the better route when native alpha is required.
