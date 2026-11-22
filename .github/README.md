# Website CI and pull-request screenshots

- `hugo-ci.yml` runs on PRs and pushes to `master`: Hugo production build and structural/content smoke checks, Python unit tests, YAML lint, Python lint, and `actionlint`.
- `pr-site-screenshots.yml` compares the entire PR with the merge base using the PR's base and head SHAs. It looks only at added, modified, copied, or renamed **`content/**/*.md`** files. It asks `hugo list published` for their actual permalinks (respecting Hugo URL/slug overrides) and takes **one desktop full-page screenshot per distinct published URL**, including the homepage only if `content/_index.md` changed. Deleted or unpublished pages, and changes limited to scripts, themes, styles, or static assets, produce no screenshots. The job uploads an artifact containing a manifest even if no content pages changed.
- `pr-site-preview-comment.yml` runs after a successful screenshot workflow. It uses only code from `master`, validates the artifact and current PR head, publishes PNGs under `previews/pr-<number>/` on the dedicated `pr-previews` branch, and creates or updates a single PR comment with the screenshots. If a PR no longer has changed published pages, the bot removes its previous screenshot comment and preview files.

The `pr-previews` branch is created automatically on first successful preview publication. No GitHub Pages, deployment credentials, third-party image hosting, or repo secrets are needed. Published images are public because this repository is public. The newest preview files replace older images in the preview branch; Git history still retains earlier versions.

GitHub only starts a `workflow_run` workflow after its definition exists on the **default branch**. The PR introducing these workflows can produce screenshot artifacts; automatic inline comments begin after the workflows merge into `master`.

Hugo version: `0.170.1`; Playwright version: `1.65.2`. Python dependencies use `uv` in CI.
