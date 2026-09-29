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

Served by the Cloudflare Worker `gustavo-portfolio` as static assets (config in `wrangler.jsonc`), with `gustavo.rhinojedi.dev` attached as its custom domain.

```bash
npx wrangler deploy
```

Every deploy creates a Worker version, so a bad release rolls back with `npx wrangler rollback`.

## Related

- [aegis](https://github.com/rhinolands/aegis), the open-source agent-governance gateway featured on the site
- [github.com/rhinolands](https://github.com/rhinolands) for the other public repositories

Content © 2026 Gustavo Norymberg. All rights reserved.
