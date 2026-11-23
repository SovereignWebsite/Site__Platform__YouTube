#!/usr/bin/env python3
"""Five designs of youtube.platform.sovereignweb.site's home page. design.c@SovereignWebsite.dinis, round 1.
Same words and the same working page: each design keeps the page's ids and loads the site's own /assets/yt.js.
Usage: build.py <site dir>"""
import os, sys, html

SITE = sys.argv[1]
OUT = os.path.join(SITE, "designs")
HOST = "https://youtube.platform.sovereignweb.site"
e = html.escape
H1 = "Your YouTube channel, from your own browser"
MARK = "youtube.platform.sovereignweb.site"
INTRO = ("Connect your channel with Google, then monitor it, understand it and publish to it, all from this page, "
         "with YouTube's official API. An unofficial site, not made or endorsed by YouTube or Google.")
MON = "Your channel's subscribers, views and latest uploads appear here once connected."
UND = "The last 28 days, day by day: views, minutes watched, average view and subscribers, from the YouTube Analytics API."
PUBNOTE = "Publishing asks Google for one more permission (upload) the first time, and starts as private unless you choose otherwise."
HOW = [
    'Connecting uses Google\'s own sign-in for web pages, which gives this page a short-lived access token with only a client ID: no client secret, no server (<a href="https://developers.google.com/identity/oauth2/web/guides/use-token-model">token model</a>; the secret is "only for server-side token exchange", <a href="https://developers.google.com/identity/oauth2/web/guides/get-google-api-clientid">client ID set-up</a>). Google\'s sign-in script loads only when you press Connect.',
    "The token is kept in this tab's memory only and is sent only to Google's APIs. Disconnect revokes it; closing the tab forgets it. Nothing is stored and there are no cookies of ours.",
    'It asks for reading first (<code>youtube.readonly</code>, <code>yt-analytics.readonly</code>) and for <code>youtube.upload</code> only when you publish, the narrowest scopes, as Google advises (<a href="https://developers.google.com/youtube/v3/guides/authentication">authentication</a>).',
    'Limits: by default 10,000 quota units a day for reading, and a separate 100 uploads a day (<a href="https://developers.google.com/youtube/v3/determine_quota_cost">quota costs</a>, <a href="https://developers.google.com/youtube/v3/docs/videos/insert">videos.insert</a>). An upload with no visibility set would default to public, so this page always sets one (<a href="https://developers.google.com/youtube/v3/docs/videos/insert">videos.insert</a>).',
    "For the owner: add this site's address to the OAuth client's Authorised JavaScript origins and put the client ID (not the secret) in <code>data/youtube.json</code>.",
]
SENT = ("Pressing Connect loads Google's sign-in from accounts.google.com; after that your token goes only to Google's APIs "
        "(www.googleapis.com, youtubeanalytics.googleapis.com). This page names only those hosts in its security policy.")
DESIGNS = [
    (1, "Control Room", "A channel control room, dark first: monitor, understand and publish as three desks side by side."),
    (2, "Programme Guide", "A printed programme guide: each part of the page a slot in the day's listings."),
    (3, "Dispatch", "Publishing first, as a dispatch slip with its safeguards in view, the figures behind it."),
    (4, "Channel Report", "A channel report: the 28 days as the lead story, the rest as its sections."),
    (5, "Brief", "Everything on one plain page, for reading fast or printing."),
]
FAMILY = [("https://sovereignwebsite.ai/", "Sovereign Website"), ("https://sovereignwebsite.org/", "Principles"),
          ("https://sovereignwebsite.site/", "Hosted"), ("https://hub.sovereignweb.site/", "Hub"),
          ("https://agents.sovereignweb.site/", "Agents"), ("https://vault.sovereignwebsite.site/", "Vault"),
          ("https://agenticcells.ai/", "AgentiCCells"), ("https://riskmandate.ai/", "RiskMandate"),
          ("https://newsroom.sgit.ai/", "Newsroom")]
CSP = ("default-src 'self'; script-src 'self' https://accounts.google.com/gsi/client; "
       "frame-src https://accounts.google.com/gsi/; style-src 'self' 'unsafe-inline' https://accounts.google.com/gsi/style; "
       "connect-src 'self' https://instagram.platform.sovereignweb.site https://accounts.google.com/gsi/ https://oauth2.googleapis.com https://www.googleapis.com https://youtubeanalytics.googleapis.com; "
       "img-src 'self' https://instagram.platform.sovereignweb.site; base-uri 'none'; form-action 'self'")

BASE = """
*{box-sizing:border-box}
html{color-scheme:light dark;-webkit-text-size-adjust:100%}
body{margin:0;font:1.0625rem/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--fg);overflow-wrap:break-word}
a{color:var(--link)}
:focus-visible{outline:3px solid var(--focus);outline-offset:2px}
.skip{position:absolute;left:-999px;top:.5rem;z-index:99;background:var(--bg);color:var(--fg);padding:.5rem .9rem;border:2px solid var(--focus)}
.skip:focus{left:1rem}
main *{min-width:0}
.chrome{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;justify-content:flex-end;position:relative;z-index:5;padding-top:.5rem}
.chrome details{position:relative}
.chrome summary{cursor:pointer;list-style:none;min-height:44px;display:inline-flex;align-items:center;padding:.35rem .8rem;border:1px solid var(--ctl);border-radius:999px;font-size:.9rem;background:var(--bg);color:var(--fg)}
.chrome summary::-webkit-details-marker{display:none}
.chrome summary::after{content:"";width:.45rem;height:.45rem;margin-left:.5rem;border-right:2px solid currentColor;border-bottom:2px solid currentColor;transform:rotate(45deg) translateY(-2px)}
.chrome details[open] summary::after{transform:rotate(-135deg)}
.chrome ul{position:absolute;right:0;top:calc(100% + .35rem);margin:0;padding:.4rem;list-style:none;min-width:15rem;max-width:calc(100vw - 2rem);background:var(--bg);color:var(--fg);border:1px solid var(--ctl);border-radius:.6rem;box-shadow:0 .6rem 1.6rem rgba(0,0,0,.25)}
.chrome li a{display:block;padding:.55rem .7rem;border-radius:.4rem;color:var(--fg);text-decoration:none;font-size:.95rem}
.chrome li a:hover,.chrome li a:focus-visible{background:var(--hover)}
.chrome li a[aria-current]{font-weight:700;text-decoration:underline}
.chrome .gap{border-top:1px solid var(--ctl);margin-top:.3rem;padding-top:.3rem}
.chrome small{display:block;font-size:.85rem;color:var(--muted);font-weight:400}
.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.signin{display:grid;grid-template-columns:1fr auto auto;gap:.4rem .6rem;align-items:end;margin:1.25rem 0 .5rem}
.signin label{font-size:.9rem;color:var(--muted);grid-row:1}
.signin label[for=__none]{grid-column:2}
.signin input,.signin select,.signin button{font:inherit;font-size:1rem;padding:.55rem .7rem;border:1px solid var(--ctl);border-radius:6px;background:var(--field);color:var(--fg);min-height:44px}
.signin input{grid-column:1;grid-row:2}.signin select{grid-column:2;grid-row:2}
.signin button{grid-column:3;grid-row:2;background:var(--accent);color:var(--on-accent);border-color:var(--accent);font-weight:700;cursor:pointer}
@media (max-width:30rem){.signin{grid-template-columns:1fr auto}.signin button{grid-column:1/-1;grid-row:3}}
.status{font-weight:700;min-height:1.6em}
.note{font-size:.95rem;color:var(--muted)}
button.small,.out select{font:inherit;font-size:1rem;padding:.4rem .7rem;border:1px solid var(--ctl);border-radius:6px;background:var(--field);color:var(--link);font-weight:700;min-height:44px;cursor:pointer}
.out select{color:var(--fg);font-weight:400}
.out label{color:var(--muted)}
.actions{display:flex;flex-wrap:wrap;gap:.6rem;margin:1rem 0}
.actions button,.pub button{font:inherit;font-size:1rem;padding:.55rem 1rem;border-radius:6px;min-height:44px;cursor:pointer;border:1px solid var(--accent);font-weight:700}
#connect,.pub button{background:var(--accent);color:var(--on-accent)}#forget{background:var(--field);color:var(--link);border-color:var(--ctl)}
button:disabled{cursor:not-allowed}
.stats{display:flex;flex-wrap:wrap;gap:1rem 2.5rem;margin:1rem 0}.stats dt{font-size:.9rem;color:var(--muted)}.stats dd{margin:0;font-size:1.6rem;font-weight:700}
.pub{display:grid;gap:.35rem;max-width:36rem}.pub label{font-size:.95rem;color:var(--muted);margin-top:.4rem}
.pub input,.pub textarea,.pub select{font:inherit;font-size:1rem;padding:.5rem .7rem;border:1px solid var(--ctl);border-radius:6px;background:var(--field);color:var(--fg);min-height:44px}
.pub .check{display:flex;gap:.5rem;align-items:flex-start;color:var(--fg)}.pub .check input{min-height:auto;margin-top:.35rem}
.reels{list-style:none;padding:0;margin:1rem 0;display:grid;gap:1.25rem;grid-template-columns:repeat(auto-fill,minmax(min(100%,16rem),1fr))}
.reel{display:flex;gap:.9rem;align-items:flex-start;border-top:1px solid var(--line);padding-top:.9rem}
.reel img{width:90px;height:160px;object-fit:cover;border-radius:6px;background:var(--line);flex:none}
.reel h3{font-size:1rem;margin:0 0 .3rem;line-height:1.35}
.reel .note{margin:0 0 .3rem}
.reel .links{display:flex;flex-direction:column;gap:.2rem;margin:0}
#connect:disabled,.pub button:disabled{background:var(--field);color:var(--muted);border-color:var(--ctl);cursor:not-allowed}
.panel table{border-collapse:collapse;width:100%;font-size:.95rem}
.panel caption{text-align:left;font-weight:700;padding:.4rem 0}
.panel th,.panel td{text-align:left;vertical-align:top;padding:.45rem .6rem;border-bottom:1px solid var(--line);overflow-wrap:anywhere}
.panel thead th{color:var(--muted);font-size:.9rem}
#forget{margin:.3rem 0}
.out h3{font-size:1.1rem;margin:1rem 0 .3rem}
.out table{border-collapse:collapse;width:100%;font-size:.95rem}
.out caption{text-align:left;font-weight:700;padding:.4rem 0}
.out th,.out td{text-align:left;vertical-align:top;padding:.45rem .6rem;border-bottom:1px solid var(--line);overflow-wrap:anywhere}
.out thead th{color:var(--muted);font-size:.9rem}
.scroll{overflow-x:auto;margin:1rem 0}
.out table{border-collapse:collapse;width:100%;font-size:.95rem}
.out caption{text-align:left;font-weight:700;padding:.4rem 0}
.out th,.out td{text-align:left;vertical-align:top;padding:.45rem .6rem;border-bottom:1px solid var(--line)}
.out thead th{color:var(--muted);font-size:.9rem}
.out th .sub{display:block;font-weight:400;color:var(--muted);font-size:.875rem}
.out tr.group th{background:var(--hover);font-size:.875rem;letter-spacing:.06em;text-transform:uppercase}
.out td.vals{white-space:pre-wrap;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;overflow-wrap:anywhere}
.out td.ok{color:var(--ok);font-weight:700;white-space:nowrap}
.out td.bad{color:var(--bad);font-weight:700}
.out td.num{text-align:right;font-variant-numeric:tabular-nums}
.sent{font-size:.9rem;color:var(--muted)}
footer{padding:2rem 0 3rem;font-size:.95rem}
footer nav{display:flex;flex-wrap:wrap;gap:.25rem 1.25rem}
footer nav a{min-height:44px;display:inline-flex;align-items:center}
@media print{.chrome,.skip,.actions,#publishbox{display:none}}
"""


def head(n, css):
    name, idea = (DESIGNS[n - 1][1], DESIGNS[n - 1][2]) if n else ("", "")
    title = f"{name}, design {n} of YouTube" if n else "Five designs, YouTube"
    desc = (f"Design {n} of youtube.platform.sovereignweb.site, {name}: {idea}" if n else
            "Five designs of youtube.platform.sovereignweb.site, the same channel tools in five ideas, side by side.")
    url = f"{HOST}/designs/{n}/" if n else f"{HOST}/designs/"
    img = f"{HOST}/assets/share/card-1200x630.jpg"
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="YouTube">
<meta property="og:locale" content="en_GB">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="YouTube">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{img}">
<link rel="canonical" href="{url}">
<style>{BASE}{css}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def chrome(n):
    d = "".join(f'<li><a href="/designs/{i}/"{" aria-current=\"page\"" if i == n else ""}>{i}. {nm}<small>{idea}</small></a></li>' for i, nm, idea in DESIGNS)
    fam = "".join(f'<li><a href="{u}">{t}</a></li>' for u, t in FAMILY)
    return f"""<nav class="chrome" aria-label="Designs and the Sovereign Website family">
<details><summary>Choose a design</summary><ul>{d}<li class="gap"><a href="/designs/">All five, side by side</a></li><li><a href="/">The site as it is now</a></li></ul></details>
<details><summary>Sovereign Website</summary><ul><li><a href="/start/">Start here</a></li><li><a href="/agents/">Use with your AI</a></li><li><a href="/admin/">How this site was made</a></li><li class="gap"><a href="/policy/">How this site is governed</a></li>{fam}</ul></details>
</nav>"""


def own(cls="own"):
    return f'<nav class="{cls}" aria-label="This site"><a href="#monitor-h">Monitor</a><a href="#publish-h">Publish</a><a href="/start/">Start here</a><a href="/agents/">Use with your AI</a></nav>'


def connect():
    return f"""<div class="actions"><button id="connect" type="button">Connect with Google</button><button id="forget" type="button" hidden>Disconnect</button></div>
<p class="sent">{SENT}</p>
<p id="status" class="status" role="status" aria-live="polite"></p>"""


VID = ("What the agent is publishing: each video with its credits and sources, and links to YouTube and Instagram once posted. "
       "Posting runs under a written rule; the owner reviews what is published.")


def videos(h="h2"):
    return f'<section class="panel" aria-labelledby="videos-h"><{h} id="videos-h">Videos</{h}><p>{VID}</p><div id="videos"><p class="note">Loading the list of videos...</p></div></section>'


def monitor(h="h2"):
    return f'<section class="panel" aria-labelledby="monitor-h"><{h} id="monitor-h">Monitor</{h}><div id="monitor"><p class="note">{MON}</p></div></section>'


def understand(h="h2"):
    return f'<section class="panel" aria-labelledby="understand-h"><{h} id="understand-h">Understand</{h}><div id="understand"><p class="note">{UND}</p></div></section>'


def publish(h="h2"):
    return f"""<section class="panel" aria-labelledby="publish-h"><{h} id="publish-h">Publish</{h}>
<div id="publishbox" hidden>
<form id="publish" class="pub">
<label for="file">Video file</label>
<input id="file" type="file" accept="video/*" required>
<label for="title">Title</label>
<input id="title" type="text" maxlength="100" required>
<label for="desc">Description</label>
<textarea id="desc" rows="4" maxlength="5000"></textarea>
<label for="privacy">Visibility</label>
<select id="privacy"><option value="private" selected>Private</option><option value="unlisted">Unlisted</option><option value="public">Public</option></select>
<label class="check"><input id="confirm" type="checkbox"> <span>I want to upload this video to my channel now.</span></label>
<button type="submit">Publish</button>
</form>
<p id="pubstatus" class="status" role="status" aria-live="polite"></p>
</div>
<p class="note">{PUBNOTE}</p></section>"""


def ul(items, cls="plain"):
    return f'<ul class="{cls}">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def footer():
    return f"""<footer>
<nav aria-label="About this site"><a href="/start/">Start here</a> <a href="/agents/">Use with your AI</a> <a href="/admin/">How this site was made</a> <a href="/policy/">How this site is governed</a></nav>
<p>A sovereign website, made with the <a href="https://sovereignwebsite.org/">open pattern</a>. Source: <a href="https://github.com/SovereignWebsite/Site__Platform__YouTube">github.com/SovereignWebsite/Site__Platform__YouTube</a>.</p>
</footer>
<script src="/assets/yt.js" defer></script>
</body>
</html>
"""



HOWT = "How it works, and what stays with you"

# ---------------------------------------------------------------- 1. Control Room (dark first)
CSS1 = """
:root{--bg:#0d0d10;--fg:#f2f1ee;--muted:#b8b6b0;--link:#ff9d8a;--focus:#ff9d8a;--ctl:#85837d;--hover:#1c1c21;--field:#16161a;--accent:#ff9d8a;--on-accent:#1a0805;--line:#2c2c33;--ok:#86ddb3;--bad:#ff9b8a;--desk:#15151a}
@media (prefers-color-scheme:light){:root{--bg:#f1f0ed;--fg:#131316;--muted:#4d4c48;--link:#a1281b;--focus:#a1281b;--ctl:#77756f;--hover:#e3e2de;--field:#ffffff;--accent:#a1281b;--on-accent:#ffffff;--line:#d1cfc9;--ok:#1d6b45;--bad:#a13a2a;--desk:#ffffff}}
.wrap{max-width:84rem;margin:0 auto;padding:0 1rem}
.mast{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:.5rem 1rem;padding:.5rem 0}
.brand{font:800 1.1rem/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.2em;text-transform:uppercase;color:var(--fg);text-decoration:none;min-height:44px;display:inline-flex;align-items:center}
.own{display:flex;flex-wrap:wrap;gap:.25rem 1rem;font-size:.95rem}.own a{color:var(--fg);min-height:44px;display:inline-flex;align-items:center}
.top{display:grid;gap:1.5rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,26rem),1fr));padding:clamp(1.5rem,4vw,2.5rem) 0;align-items:end}
.k{font:700 .85rem ui-monospace,Menlo,Consolas,monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin:0}
h1{font-size:clamp(2.1rem,6vw,3.8rem);line-height:1.02;margin:.4rem 0 1rem;letter-spacing:-.02em}
.desks{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,22rem),1fr));margin:1rem 0 2rem}
.panel{background:var(--desk);border:1px solid var(--line);border-top:4px solid var(--accent);border-radius:.6rem;padding:1rem 1.2rem}
.panel h2{font:800 1rem ui-monospace,Menlo,Consolas,monospace;letter-spacing:.14em;text-transform:uppercase;margin:0 0 .5rem}
h2.plain-h{font-size:clamp(1.45rem,3.4vw,2rem);margin:1rem 0 .5rem}
.plain{padding-left:1.1rem;max-width:52rem}.plain li{margin:.5rem 0}
footer{border-top:1px solid var(--line)}
"""


def d1():
    return head(1, CSS1) + f"""<div class="wrap">{chrome(1)}
<header class="mast"><a class="brand" href="/">YouTube</a>{own()}</header>
<main id="main"><div class="top"><div><p class="k">{MARK}</p><h1>{H1}</h1><p>{INTRO}</p></div><div>{connect()}</div></div>
{videos()}<div class="desks">{monitor()}{understand()}{publish()}</div>
<h2 class="plain-h">{HOWT}</h2>{ul(HOW)}
</main>
""" + footer().replace("</body>", "</div></body>")


# ---------------------------------------------------------------- 2. Programme Guide
CSS2 = """
:root{--bg:#f7f3ea;--fg:#1c1914;--muted:#544c40;--link:#1f4f7a;--focus:#1f4f7a;--ctl:#7f7768;--hover:#ece6d8;--field:#ffffff;--accent:#1f4f7a;--on-accent:#ffffff;--line:#d8cfbd;--ok:#1d6b45;--bad:#a13a2a;--slot:#1c1914;--on-slot:#f7f3ea}
@media (prefers-color-scheme:dark){:root{--bg:#15130f;--fg:#efe9dc;--muted:#c2b9a7;--link:#9cc8f0;--focus:#9cc8f0;--ctl:#8c8473;--hover:#24201a;--field:#1d1a15;--accent:#9cc8f0;--on-accent:#0b1420;--line:#3b352b;--ok:#86ddb3;--bad:#ff9b8a;--slot:#efe9dc;--on-slot:#15130f}}
.wrap{max-width:66rem;margin:0 auto;padding:0 1rem}
.mast{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:.5rem 1rem;padding:.5rem 0;border-bottom:3px solid var(--fg)}
.brand{font:900 1.3rem Georgia,"Times New Roman",serif;color:var(--fg);text-decoration:none;min-height:44px;display:inline-flex;align-items:center}
.own{display:flex;flex-wrap:wrap;gap:.25rem 1rem;font-size:.95rem}.own a{color:var(--fg);min-height:44px;display:inline-flex;align-items:center}
h1,h2{font-family:Georgia,"Times New Roman",serif}
.k{font:700 .85rem ui-monospace,Menlo,Consolas,monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:1.5rem 0 .3rem}
h1{font-size:clamp(2.1rem,6vw,3.4rem);line-height:1.05;margin:0 0 1rem}
.guide{list-style:none;margin:1.5rem 0;padding:0;border-top:1px solid var(--fg)}
.guide>li{display:grid;grid-template-columns:7rem 1fr;gap:1rem;padding:1rem 0;border-bottom:1px solid var(--line)}
.slot{align-self:start;background:var(--slot);color:var(--on-slot);font:800 .9rem ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;text-align:center;padding:.4rem .3rem}
@media (max-width:34rem){.guide>li{grid-template-columns:1fr}.slot{justify-self:start}}
.panel h2,.guide h2{font-size:1.4rem;margin:0 0 .3rem}
.plain{padding-left:1.1rem}.plain li{margin:.5rem 0}
footer{border-top:3px solid var(--fg)}
"""


def d2():
    return head(2, CSS2) + f"""<div class="wrap">{chrome(2)}
<header class="mast"><a class="brand" href="/">YouTube</a>{own()}</header>
<main id="main"><p class="k">Today's guide · {MARK}</p><h1>{H1}</h1><p>{INTRO}</p>
<ol class="guide">
<li><span class="slot">First</span><div><h2>Connect</h2>{connect()}</div></li>
<li><span class="slot">Showing</span>{videos()}</li>
<li><span class="slot">Then</span>{monitor()}</li>
<li><span class="slot">28 days</span>{understand()}</li>
<li><span class="slot">Your call</span>{publish()}</li>
<li><span class="slot">Small print</span><div><h2>{HOWT}</h2>{ul(HOW)}</div></li>
</ol>
</main>
""" + footer().replace("</body>", "</div></body>")


# ---------------------------------------------------------------- 3. Dispatch
CSS3 = """
:root{--bg:#eef3f6;--fg:#0f1b24;--muted:#45525d;--link:#0b5394;--focus:#0b5394;--ctl:#6b7884;--hover:#dfe7ed;--field:#ffffff;--accent:#0b5394;--on-accent:#ffffff;--line:#c9d4dd;--ok:#1d6b45;--bad:#a13a2a;--slip:#ffffff;--guard:#7a4e00}
@media (prefers-color-scheme:dark){:root{--bg:#0c141b;--fg:#e8eff4;--muted:#adbac5;--link:#8cc4ff;--focus:#8cc4ff;--ctl:#788694;--hover:#172330;--field:#111c26;--accent:#8cc4ff;--on-accent:#06121c;--line:#25333f;--ok:#86ddb3;--bad:#ff9b8a;--slip:#111c26;--guard:#ffcf6e}}
.wrap{max-width:72rem;margin:0 auto;padding:0 1rem}
.mast{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:.5rem 1rem;padding:.5rem 0}
.brand{font-weight:800;font-size:1.2rem;color:var(--fg);text-decoration:none;min-height:44px;display:inline-flex;align-items:center}
.own{display:flex;flex-wrap:wrap;gap:.25rem 1rem;font-size:.95rem}.own a{color:var(--fg);min-height:44px;display:inline-flex;align-items:center}
.k{font-size:.85rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:1.5rem 0 .3rem}
h1{font-size:clamp(2.1rem,6vw,3.4rem);line-height:1.05;margin:0 0 1rem;letter-spacing:-.02em}
.desk{display:grid;gap:1.5rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,24rem),1fr));margin:1.5rem 0;align-items:start}
.slip{background:var(--slip);border:2px dashed var(--ctl);border-radius:.6rem;padding:1.2rem}
.slip .panel h2{font-size:1.5rem;margin:0 0 .5rem}
.guards{border-left:6px solid var(--guard);padding:.25rem 0 .25rem 1rem}
.guards h2{font-size:1.25rem;margin:0 0 .4rem}
.figures{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,22rem),1fr));margin:1.5rem 0 2rem}
.figures .panel{background:var(--slip);border:1px solid var(--line);border-radius:.6rem;padding:1rem 1.2rem}
.figures h2{font-size:1.25rem;margin:0 0 .3rem}
.plain{padding-left:1.1rem}.plain li{margin:.5rem 0}
footer{border-top:1px solid var(--line)}
"""


def d3():
    return head(3, CSS3) + f"""<div class="wrap">{chrome(3)}
<header class="mast"><a class="brand" href="/">YouTube</a>{own()}</header>
<main id="main"><p class="k">Dispatch · {MARK}</p><h1>{H1}</h1><p>{INTRO}</p>{connect()}
<div class="desk"><div class="slip">{publish()}</div>
<div class="guards"><h2>{HOWT}</h2>{ul(HOW)}</div></div>
<div class="figures">{videos()}{monitor()}{understand()}</div>
</main>
""" + footer().replace("</body>", "</div></body>")


# ---------------------------------------------------------------- 4. Channel Report
CSS4 = """
:root{--bg:#fbfaf7;--fg:#171614;--muted:#55524c;--link:#6b2a7a;--focus:#6b2a7a;--ctl:#7c7972;--hover:#efede7;--field:#ffffff;--accent:#6b2a7a;--on-accent:#ffffff;--line:#dcd9d1;--ok:#1d6b45;--bad:#a13a2a;--lead:#f2ecf4}
@media (prefers-color-scheme:dark){:root{--bg:#141215;--fg:#efebf0;--muted:#bdb6c0;--link:#d7a6e6;--focus:#d7a6e6;--ctl:#8a838d;--hover:#221e24;--field:#1c181e;--accent:#d7a6e6;--on-accent:#1a0d1f;--line:#352f38;--ok:#86ddb3;--bad:#ff9b8a;--lead:#211b24}}
.wrap{max-width:70rem;margin:0 auto;padding:0 1rem}
.mast{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:.5rem 1rem;padding:.5rem 0;border-bottom:1px solid var(--fg)}
.brand{font:italic 700 1.3rem Georgia,"Iowan Old Style","Times New Roman",serif;color:var(--fg);text-decoration:none;min-height:44px;display:inline-flex;align-items:center}
.own{display:flex;flex-wrap:wrap;gap:.25rem 1rem;font-size:.95rem}.own a{color:var(--fg);min-height:44px;display:inline-flex;align-items:center}
h1,h2{font-family:Georgia,"Iowan Old Style","Times New Roman",serif}
.masthead{text-align:center;padding:clamp(1.5rem,5vw,3rem) 0 1rem}
.k{font:600 .85rem ui-monospace,Menlo,Consolas,monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:0}
h1{font-size:clamp(2.2rem,6.4vw,4rem);line-height:1.02;margin:.5rem auto 1rem;max-width:18ch}
.masthead p{max-width:42rem;margin:0 auto}
.masthead .actions{justify-content:center}
.lead{background:var(--lead);border-radius:1rem;padding:clamp(1rem,3vw,2rem);margin:1rem 0}
.lead .panel h2{font-size:clamp(1.6rem,4vw,2.4rem);margin:0 0 .5rem}
.cols{display:grid;gap:2rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,20rem),1fr));margin:2rem 0;border-top:1px solid var(--line);padding-top:1.5rem}
.cols h2{font-size:1.4rem;margin:0 0 .4rem}
.plain{padding-left:1.1rem}.plain li{margin:.5rem 0}
footer{border-top:1px solid var(--fg)}
"""


def d4():
    return head(4, CSS4) + f"""<div class="wrap">{chrome(4)}
<header class="mast"><a class="brand" href="/">YouTube</a>{own()}</header>
<main id="main"><div class="masthead"><p class="k">Channel report · {MARK}</p><h1>{H1}</h1><p>{INTRO}</p>{connect()}</div>
<div class="lead">{understand()}</div>
{videos()}
<div class="cols">{monitor()}{publish()}<div><h2>{HOWT}</h2>{ul(HOW)}</div></div>
</main>
""" + footer().replace("</body>", "</div></body>")


# ---------------------------------------------------------------- 5. Brief
CSS5 = """
:root{--bg:#ffffff;--fg:#111111;--muted:#4a4a4a;--link:#0b4f8a;--focus:#0b4f8a;--ctl:#767676;--hover:#f0f0f0;--field:#ffffff;--accent:#0b4f8a;--on-accent:#ffffff;--line:#d6d6d6;--ok:#1d6b45;--bad:#a13a2a}
@media (prefers-color-scheme:dark){:root{--bg:#121212;--fg:#f1f1f1;--muted:#bdbdbd;--link:#8cc4ff;--focus:#8cc4ff;--ctl:#8a8a8a;--hover:#222;--field:#1a1a1a;--accent:#8cc4ff;--on-accent:#0b0b0b;--line:#333;--ok:#86ddb3;--bad:#ff9b8a}}
.wrap{max-width:42rem;margin:0 auto;padding:0 1rem}
.brand{font:700 1.1rem Georgia,"Times New Roman",serif;color:var(--fg);text-decoration:none;min-height:44px;display:inline-flex;align-items:center}
.own{display:flex;flex-wrap:wrap;gap:0 1rem;font-size:.95rem}.own a{min-height:44px;display:inline-flex;align-items:center}
h1{font:700 clamp(2rem,6vw,2.6rem)/1.15 Georgia,serif;margin:1.25rem 0 .75rem}
h2{font:700 1.45rem Georgia,serif;margin:2rem 0 .4rem;padding-top:1rem;border-top:1px solid var(--line)}
.plain{padding-left:1.2rem}.plain li{margin:.4rem 0}
footer{border-top:1px solid var(--line);margin-top:2rem}
"""


def d5():
    return head(5, CSS5) + f"""<div class="wrap">{chrome(5)}
<header><a class="brand" href="/">YouTube</a>{own()}</header>
<main id="main"><p>{MARK}</p><h1>{H1}</h1><p>{INTRO}</p>{connect()}
{videos()}{monitor()}{understand()}{publish()}
<h2>{HOWT}</h2>{ul(HOW)}</main>
""" + footer().replace("</body>", "</div></body>")


CSSI = """
:root{--bg:#f6f5f2;--fg:#151515;--muted:#4f4c47;--link:#a1281b;--focus:#a1281b;--ctl:#77736c;--hover:#e9e6df;--card:#fff;--line:#dcd8cf;--field:#fff;--accent:#a1281b;--on-accent:#fff;--ok:#1d6b45;--bad:#a13a2a}
@media (prefers-color-scheme:dark){:root{--bg:#121212;--fg:#efede8;--muted:#bdb9b1;--link:#ff9d8a;--focus:#ff9d8a;--ctl:#85817a;--hover:#222;--card:#1c1c1c;--line:#333;--field:#1a1a1a;--accent:#ff9d8a;--on-accent:#1a0805;--ok:#86ddb3;--bad:#ff9b8a}}
.wrap{max-width:76rem;margin:0 auto;padding:0 1rem}
.brand{font-weight:800;color:var(--fg);text-decoration:none;min-height:44px;display:inline-flex;align-items:center}
h1{font:700 clamp(2rem,5.5vw,3rem)/1.1 Georgia,serif;margin:1rem 0 .75rem}
.cards{list-style:none;margin:1.5rem 0 3rem;padding:0;display:grid;gap:1.25rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,20rem),1fr))}
.cards li{background:var(--card);border:1px solid var(--line);border-radius:.6rem;overflow:hidden}
.cards img{display:block;max-width:100%;height:auto;aspect-ratio:16/10;object-fit:cover;object-position:top;width:100%;border-bottom:1px solid var(--line)}
.cards .b{padding:1rem}.cards h2{font-size:1.2rem;margin:0 0 .3rem}.cards p{margin:.3rem 0}
footer{border-top:1px solid var(--line)}
"""


def index(rec):
    cards = "".join(f'<li><img src="/designs/{i}/shot-1366.webp" alt="Design {i}, {nm}, at desktop width" width="1366" height="854" loading="lazy"><div class="b"><h2><a href="/designs/{i}/">{i}. {nm}</a></h2><p>{idea}</p>{"<p><strong>Recommended by the designer.</strong></p>" if i == rec else ""}</div></li>' for i, nm, idea in DESIGNS)
    f = footer().replace('<script src="/assets/yt.js" defer></script>\n', "")
    return head(0, CSSI) + f"""<div class="wrap">{chrome(0)}
<header><a class="brand" href="/">YouTube</a></header>
<main id="main"><h1>Five designs of this site</h1>
<p>The same tools and the same words, in five ideas. Each one keeps the page's own script, so Connect, Monitor, Understand and Publish behave the same in all five. The owner picks one; the keeper makes it the site.</p>
<ul class="cards">{cards}</ul></main>
""" + f.replace("</body>", "</div></body>")


if __name__ == "__main__":
    for i, f in {1: d1, 2: d2, 3: d3, 4: d4, 5: d5}.items():
        os.makedirs(f"{OUT}/{i}", exist_ok=True)
        open(f"{OUT}/{i}/index.html", "w").write(f())
    open(f"{OUT}/index.html", "w").write(index(int(os.environ.get("RECOMMEND", "1"))))
    print("built", OUT)
