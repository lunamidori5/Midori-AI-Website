# Website CI and pull-request screenshots

- `hugo-ci.yml` runs on pull requests and pushes to `master`: Hugo production build, generated-site smoke checks, YAML lint, Python lint, and actionlint.
- `pr-site-screenshots.yml` builds the **PR version** of the site, starts a local Hugo server, and captures desktop homepage, mobile homepage, and the first changed Markdown content page (or `/about-us/`). It uploads these PNGs to the workflow run for 14 days. The workflow has **read-only** permissions.
- `pr-site-preview-comment.yml` runs after a successful screenshot workflow. It uses only scripts from `master`, validates the screenshot metadata against the current PR head, publishes PNGs under `previews/pr-<number>/` on the dedicated `pr-previews` branch, and creates or updates a single PR comment with inline images.

The `pr-previews` branch is automatically created the first time the trusted workflow runs. No GitHub Pages, deployment credentials, third-party image hosting, or repo secrets are required. Published images are public because this repository is public. Images persist on the preview branch until cleaned up; only the newest screenshots are shown in the PR comment.

GitHub only starts a `workflow_run` workflow after its definition exists on the **default branch**. The PR introducing these workflows can produce the screenshot artifact, but automatic inline PR comments begin after the workflows merge into `master`.

Hugo version: `0.170.1`. Playwright version: `1.65.2`. Python tooling is installed through `uv` in CI. These are pinned so future upstream changes do not silently change the build.
