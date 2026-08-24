# Dr Zia Ush Shamszaman website, V5

Custom GitHub Pages site at `https://solozia.github.io`.

## V5 additions

V5 adds a CMS-managed `Insights` section. You can add future LinkedIn and other professional posts without editing HTML.

The site uses GitHub Pages and Jekyll for the Insights collection. Existing pages remain normal HTML.

## One-time Pages CMS setup

1. Upload all V5 files to the root of the `solozia.github.io` repository.
2. Wait for GitHub Pages to deploy.
3. Visit `https://app.pagescms.org`.
4. Sign in with your GitHub account.
5. Install or authorise the Pages CMS GitHub App for the `solozia.github.io` repository.
6. Open the repository in Pages CMS.
7. Pages CMS will read `.pages.yml` automatically.
8. Choose `Insights & Social Posts`.
9. Click `New`.
10. Add the title, date, topic, short summary, original LinkedIn or other URL, optional image, and post text.
11. Keep `Published` switched on, then save.

Saving writes a Markdown file into `_insights/`. GitHub Pages rebuilds automatically. The new item appears on `insights.html`, and the three newest items also appear on the homepage.

## Important

The file `_insights/example-insight.md` is intentionally `published: false`. It is a private example and will not appear on the public website. You can edit it in Pages CMS or leave it as a guide.

## Insights content model

Each entry can store:

* title
* date
* published status
* platform
* topic
* short summary
* original social or media URL
* image
* full text or a short website note

This lets the website act as a permanent archive even when the original post lives on LinkedIn or another network.


## V6

V6 changes the Insights area into a blog and social-feed style page.

The public page now includes:
* a profile panel
* a Create / Manage Posts button
* a post composer style entry point
* a chronological feed
* topic labels
* image posts
* original social post links
* full article pages

Actual editing remains private through Pages CMS, which keeps GitHub credentials off the public website.

Incomplete public placeholders now use only `TBA`.

## V7
V7 strengthens the site as an evidence-rich academic profile. It adds profile metrics, research-theme navigation, clearer teaching evidence, collaboration networks, leadership categories and structured professional service, while retaining the V6 blog-style Insights publishing workflow.
