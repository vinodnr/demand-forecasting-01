# GitHub Release Notes - v1.0.0

## What's included
See Sprint-13/RELEASE_NOTES.md for full details. Key points:
- Full project bundle (sprints 0→13) with infra skeleton and docs
- Master ZIP: /mnt/data/demand_forecasting_master_sprints_0_13.zip (sha256 in Sprint-13/HANDOVER_PACKAGE.md)
- Run QA in dev as per Sprint-13/QA_CHECKLIST.md before promoting to production

## How to publish this release on GitHub
1. Push your final branch to GitHub (e.g., `git push origin main`).
2. Create a signed annotated tag locally:
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0 - Sprint 0→13"
   git push origin v1.0.0
   ```
3. In GitHub UI, create a Release named v1.0.0 and paste Sprint-13/RELEASE_NOTES.md content as the release notes.
4. Attach the master ZIP if desired (or upload to GitHub Releases Assets).

## Release artifacts to attach
- demand_forecasting_master_sprints_0_13.zip
- Sprint-13/RELEASE_NOTES.md
- Sprint-13/HANDOVER_PACKAGE.md
