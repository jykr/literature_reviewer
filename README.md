# Literature Reviewer Agent

[![Server status](https://img.shields.io/website?url=https%3A%2F%2Fliterature-reviewer-4055136070.us-central1.run.app%2Fhealth&up_message=online&down_message=offline&label=server)](https://literature-reviewer-4055136070.us-central1.run.app/reviewer)

Literature review is often a daunting task. This concierge agent runs as a hosted web app on **Google Cloud Run** — point it at your field of interest (a CV, a seed paper, or a few keywords) and it returns a single ranked, structured review of the last ~12 months of computational-biology papers. The public server generates reviews on **your own API key**, used per-request and never stored.

**Live server:** https://literature-reviewer-4055136070.us-central1.run.app/reviewer

## Example output

The server renders your review as a single self-contained page — an interactive queue you can tag, filter, and export notes from (state persists in `localStorage`). It's served same-origin at `/reviewer`; because it makes no external calls once loaded, you can also save the page ([`literature-reviewer.html`](literature-reviewer.html)) and reopen it offline.

**Overall layout** — ranked queue, sidebar, interests panel, and per-paper cards:

![Literature Reviewer — overall layout](docs/example-overview.png)

**Paper card (detail)** — Aim → Main approach → Evaluation → Results (with quantitative task/data/metric/result bullets) → Limitation:

![Literature Reviewer — paper card detail](docs/example-card.png)

See [`compbio-paper-review-SPEC.md`](compbio-paper-review-SPEC.md) for the complete specification of this output.

## Deploy your own server

The app ships as a container ([`Dockerfile`](Dockerfile)) and deploys to **Google Cloud Run** with the [Agents CLI](https://github.com/google/agents-cli). Infrastructure is Terraform under [`deployment/terraform/`](deployment/terraform/). See [`compbio-paper-review-SPEC.md`](compbio-paper-review-SPEC.md) for the full specification of the generated review app.

1. Set your API keys in the `.env` file. See `.env.example` for usage.
2. Install `agents-cli`: `uv tool install google-agents-cli`.
3. Scaffold & deploy with `agents-cli deploy`, or run the server locally.

## Agent workflow

![1783389818754](image/README/1783389818754.png)

Generated with `agents-cli playground`. `root-agent` sequentially runs `scope_agent`, `research_fanout`, and `rank_agent`.
