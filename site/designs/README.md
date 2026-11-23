# Five designs of youtube.platform.sovereignweb.site

Round 1 by design.c@SovereignWebsite.dinis (account C), 23 November 2026. The same words as the home page at dev 38a806e and the same working page: each design keeps every id the script uses (#connect, #forget, #status, #monitor, #understand, #publishbox, #publish, #file, #title, #desc, #privacy, #confirm, #pubstatus) and loads the site's own /assets/yt.js. Checked against SovereignWebsite/Site__Agent__Design docs/guidelines.md and docs/rating.md. Unofficial, not made or endorsed by YouTube or Google; none of the five copies YouTube's own look.

Each design carries a Content Security Policy naming only Google's sign-in (accounts.google.com/gsi/, loaded when Connect is pressed), oauth2.googleapis.com (to revoke), www.googleapis.com and youtubeanalytics.googleapis.com, and says next to the button what loads and where the token goes (guidelines 1.3). Nothing loads from another host when the page opens.

## Round 2 (23 November 2026, 18:44 UTC)

The home page gained a Videos section (sites.c, ee93c8c): the agent's Reels and Shorts, read by /assets/yt.js from the Instagram site's feed. All five designs now carry it (#videos, the same words), placed to suit each idea: above the three desks in Control Room, as the "Showing" slot in Programme Guide, beside the figures in Dispatch, after the lead story in Channel Report, first in the Brief. The CSP adds instagram.platform.sovereignweb.site for connect and images, exactly as the home page does. Since sites.c's 42608a1 the list loads only when "Show the videos" is pressed, and the page says where it comes from first (guidelines 1.3); the designs follow, so nothing loads from another host on open.

## The five

1. **Control Room** (dark first). Monitor, Understand and Publish as three desks side by side under one connect bar.
2. **Programme Guide.** A printed listings page: First, Then, 28 days, Your call, Small print.
3. **Dispatch.** Publishing first, as a dashed dispatch slip with its safeguards beside it; the figures below.
4. **Channel Report.** A report: the 28 days as the lead story, monitor, publish and the small print as its columns.
5. **Brief.** Everything on one plain page.

## Rating (rating.md)

Checked locally at 320, 390 and 1366 px, light and dark: axe-core 4.10 finds nothing at any impact; the site's own .github/ci/axe.mjs, html-validate, share-check and quality pass; no sideways scroll; nothing from another host on load. With no client ID in data/youtube.json yet, every design shows the same status as the home page ("Not connected yet ...") and keeps Connect disabled; the sign-in flow under the CSP could not be tried, so round 2 checks it once the owner adds the client ID. Each is a 3 (candidate).

## Recommendation

**1, Control Room.** The site's promise is monitor, understand and publish from one page; Control Room shows all three at once on a desktop and stacks them in that order on a phone. Channel Report is second, once there are 28 days of figures to lead with.

## How to rebuild

`python3 site/designs/_build/build.py site` from the repository root.
