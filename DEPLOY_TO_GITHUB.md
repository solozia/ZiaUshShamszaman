# Upload the updated website to GitHub Pages

Repository: https://github.com/solozia/ZiaUshShamszaman

## Recommended: Git on your computer (reliably uploads hidden workflow files)

1. Download and extract the ZIP. Confirm `index.html`, `research-universe.html`, `assets/`, `data/`, `scripts/`, and `.github/` are at the extracted folder root.
2. Make a backup of your existing GitHub repository or create a new branch before replacing files.
3. In a terminal, run:

```bash
git clone https://github.com/solozia/ZiaUshShamszaman.git
cd ZiaUshShamszaman
```

4. Copy **the contents** of the extracted ZIP into the cloned repository folder, merging folders. Do not delete existing files not included in the ZIP.
5. Review the changes, then run:

```bash
git status
git add -A
git commit -m "Add Research Universe V3 and November Scholar impact snapshot"
git push origin HEAD
```

6. Open GitHub > repository > Settings > Pages and confirm the publishing source. If using Deploy from a branch, select the correct branch and `/ (root)` folder. Wait for the deployment to finish.
7. Visit https://solozia.github.io/ZiaUshShamszaman/research-universe.html

## Browser-only alternative

On GitHub, open the repository and choose **Add file > Upload files**. Drag the extracted site files and folders (not the ZIP itself) into the upload area. Review the changed-file list and commit. Check carefully that nested files and the hidden `.github/workflows/update-publications.yml` are included; if the browser upload does not preserve them, use Git instead.

## Enable automatic publication updates

1. Confirm your OpenAlex author ID by checking its works and affiliation.
2. Repository > Settings > Secrets and variables > Actions > Variables > New repository variable: `OPENALEX_AUTHOR_ID`. Enter the verified ID.
3. Repository > Actions > `Update research publications` > Run workflow.
4. Review `data/pending_review.json` and `data/sync_status.json`. The updater does not automatically approve ambiguous publication matches.
5. If the workflow cannot push, check repository Actions permissions and branch protection.

The Google Scholar figures on Research Universe are explicitly a 5 November 2026 snapshot and **do not** auto-refresh. OpenAlex publication records can refresh through the workflow, but OpenAlex and Google Scholar citation counts must not be conflated.

Do not upload the ZIP as a single file to the GitHub repository: GitHub Pages needs the extracted files.
