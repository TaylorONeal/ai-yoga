# Visual toolkit

The public website is https://tayloroneal.github.io/ai-yoga/.
GitHub Pages is configured to deploy `main` from the repository root. Keep that setting: the generated root `index.html` is a complete website, while GitHub's repository view still displays the README.

## Edit and build

- `web/skills.json`: curated labels, descriptions, setup notes, and starter prompts.
- `skills/*/SKILL.md`: canonical, unabridged full prompts. The website does not rewrite them.
- `scripts/build-site.mjs`: static HTML generator and portable skill-creation prompts.
- `web/toolkit.css`, `web/toolkit.js`: responsive appearance and progressive enhancement.

Use Node 22 or newer. No dependency install is needed.

```sh
npm test
npm run build:pages
```

Commit the generated root `index.html`, `toolkit.css`, `toolkit.js`, `source.json`, and `.nojekyll` alongside source edits. The website workflow builds separately and fails on stale generated files. Merging to main triggers the existing GitHub Pages deployment.

For a local preview, `npm run build`, then serve `dist` with `python3 -m http.server 4174 --directory dist`. Use HTTP rather than opening the file directly for clipboard support.

## Personal-site copy

The companion page at https://www.tayloroneal.com/yoga/ai/ uses the same generator and has its own canonical URL. To refresh it from this checkout:

```sh
node scripts/build-site.mjs --personal --out /absolute/path/to/tayloroneal-site/public/yoga/ai
```

Review and commit those generated files in the personal-site repository separately. It requires no live GitHub API call or runtime iframe. `source.json` records the most recent commit touching `skills/`; source links pin that revision. A content change requires regenerating both websites. The generator should run after skill changes are committed so source links identify the published content.

## Behavior and limits

All five skills and full prompts exist in static HTML. JavaScript adds skill selection, deep links, copy feedback, and manual selection when clipboard access fails. Without JavaScript, every skill remains readable and its text can be manually copied. No prompts or user data are uploaded by this website. Typography uses Google Fonts with local fallback fonts.

The primary copy action includes SKILL.md and all supporting Markdown guidance in one portable prompt. It asks the assistant to use its real reusable-skill or project-instruction capability, or continue in the conversation when saving is unavailable. Script-backed tasks still need the complete folder. The page does not assume a specific assistant, filesystem, subscription, or connector.

The five skills include deeper references for reconstruction, evidence-based feedback, biography facts/voice, booking-source reconciliation including Momence, and sustained sutra practice. The tracker does not claim missing output scripts or unimplemented provider APIs. Legacy helpers remain partial collectors requiring review.

## Verification

`npm test` checks catalog completeness, exact prompt fidelity, unique copy targets, portable creation prompts with supporting guidance, both canonical URLs, and relative assets. Browser verification covers desktop/mobile geometry, all five selectors, deep-link history, full-prompt expansion, exact clipboard values, and clipboard-denied fallback. Keep published claims limited to checked functionality.

## Skill links and deeper methods

The generator also writes `skills/*/index.html`, so folder links from the original README no longer produce Pages 404s. These pages select the corresponding skill and use relative assets. Include those HTML files in `build:pages` commits. Source revisions exclude generated skill HTML from the `git log` lookup.

Python regression checks: install `openpyxl` and `pyyaml` in an isolated environment, then run `python -m unittest discover -s tests -p 'test_*.py'`. Checks cover conservative duplicate matching, real multiple-session days, provisional attendance, cancellation precedence, empty workbooks, individual co-teachers and explicit training hours.

The companion personal repository has `scripts/verify-yoga.mjs`, which exercises the actual yoga-page link and copy interactions at desktop and narrow widths. For the standalone site, set `TOOLKIT_URL` to the locally served toolkit root.
