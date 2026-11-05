# Research Universe V3 — integrated with your existing website

This ZIP contains the complete existing `solozia-github-pages-v7` website plus a new Research Universe page. Existing page content and images are preserved. Navigation links were added across the site's HTML pages and a homepage call-to-action was added.

## Deploy

1. Back up your GitHub repository first.
2. Extract this ZIP. Upload the **contents** of `zia_website_research_universe_v3/` into the repository root (where `index.html` lives), not the outer folder. Keep existing repository settings.
3. Commit and push. Visit `https://solozia.github.io/ZiaUshShamszaman/research-universe.html` after GitHub Pages finishes building.
4. Verify the navigation, publication list, mobile layout, and graph in a browser.

## Automated publications

1. Find your verified OpenAlex author record at https://openalex.org/ (check affiliation and publication list).
2. In GitHub repository Settings → Secrets and variables → Actions → Variables, create `OPENALEX_AUTHOR_ID` with the ID `A...`. Optionally create `OPENALEX_EMAIL`. If your OpenAlex access requires a key, add `OPENALEX_API_KEY` as an Actions **secret**.
3. In Actions, run `Update research publications` manually to test. The schedule then checks weekly (Monday).
4. New publications are **reviewed by default**: `AUTO_APPROVE_NEW: 'false'`. Check `data/pending_review.json` and confirm records before adding them to `data/publications.json`. Existing matching records can receive updated metadata.
5. If you later want automatic addition of new records, change `AUTO_APPROVE_NEW` to `true` only after verifying the author ID and reviewing the matching logic.

## Important data limitations

- The initial 21 records came from the previous V2 prototype and are flagged `review-needed`. Do not treat them as a complete verified bibliography.
- Collaboration links represent co-authorship in the loaded dataset, not all career collaborations.
- Similarity is text-based TF-IDF, not a validated scientific embedding model.
- Citation edges show only explicitly referenced works within the dataset.
- Citation counts reflect OpenAlex snapshots, not Google Scholar.
- GitHub Pages cannot execute Python itself; GitHub Actions performs the update and commits JSON files.

## Main files

- `research-universe.html`: visualisation page
- `assets/universe.css` and `assets/universe.js`: styling and interactions
- `data/publications.json`: shared publication data
- `scripts/update_publications.py`: metadata updater
- `.github/workflows/update-publications.yml`: scheduled GitHub Action

## Technical checks

The ZIP was assembled from the supplied website archive. Check deployment in a browser; a successful local syntax check does not guarantee correct production data or GitHub permissions.
