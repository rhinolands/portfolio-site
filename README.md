# portfolio-site

Source for [gustavo.rhinojedi.dev](https://gustavo.rhinojedi.dev), the portfolio of Gustavo Norymberg, Principal AI Platform & Governance Architect.

## Layout

| Path | What it is |
|---|---|
| `site/index.html` | The current site. One hand-written HTML file, no build step, no framework. |
| `index.html` | The previous bundled version, kept for rollback until the new one is live. |
| `tools/check_site.py` | Pre-publish gate: HTML well-formedness, AI-tell scan of the visible text, leak patterns. |

## Checks

Every push runs two gates in CI:

1. `tools/check_site.py` against `site/index.html`
2. gitleaks over the full history

Run the site check locally with `python3 tools/check_site.py site/index.html`.

## Deploy

Static hosting on Cloudflare Pages. The site is a single file, so a deploy is an upload of `site/index.html`.

## Related

- [aegis](https://github.com/rhinolands/aegis), the open-source agent-governance gateway featured on the site
- [github.com/rhinolands](https://github.com/rhinolands) for the other public repositories

Content © 2026 Gustavo Norymberg. All rights reserved.
