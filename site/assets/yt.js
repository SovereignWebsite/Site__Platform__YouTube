// YouTube from your own browser: connect, monitor, understand, publish.
// No server, no cookies, no tracking. Google's sign-in script (accounts.google.com/gsi/client)
// loads only when you press Connect. The access token is kept in this tab's memory only and is
// sent only to Google's APIs. Nothing is uploaded until you press Publish and confirm.
const READ = ['https://www.googleapis.com/auth/youtube.readonly', 'https://www.googleapis.com/auth/yt-analytics.readonly'];
const UPLOAD = 'https://www.googleapis.com/auth/youtube.upload';
const API = 'https://www.googleapis.com/youtube/v3';
let clientId = '', token = '', granted = new Set(), tokenClient = null;

const $ = s => document.querySelector(s);
const el = (tag, text, cls) => { const e = document.createElement(tag); if (text != null) e.textContent = text; if (cls) e.className = cls; return e; };
const num = n => (n == null ? '-' : Number(n).toLocaleString('en-GB'));
const say = t => { $('#status').textContent = t; };

function loadGsi() {
  return new Promise((ok, fail) => {
    if (window.google && google.accounts) return ok();
    const s = document.createElement('script');
    s.src = 'https://accounts.google.com/gsi/client';
    s.onload = ok; s.onerror = () => fail(new Error('Could not load Google sign-in'));
    document.head.append(s);
  });
}

async function connect(scopes) {
  await loadGsi();
  return new Promise(ok => {
    tokenClient = google.accounts.oauth2.initTokenClient({
      client_id: clientId,
      scope: scopes.join(' '),
      include_granted_scopes: true,
      callback: r => {
        if (r.error) { say(`Google did not connect: ${r.error}.`); return ok(false); }
        token = r.access_token;
        (r.scope || '').split(' ').forEach(s => granted.add(s));
        ok(true);
      },
    });
    tokenClient.requestAccessToken();
  });
}

async function get(url) {
  const r = await fetch(url, { headers: { authorization: 'Bearer ' + token }, credentials: 'omit', referrerPolicy: 'no-referrer' });
  if (!r.ok) { let m = `HTTP ${r.status}`; try { m = (await r.json()).error.message || m; } catch {} return { error: m }; }
  return { data: await r.json() };
}

function table(caption, head, rows) {
  const wrap = el('div', null, 'scroll');
  wrap.tabIndex = 0; wrap.setAttribute('role', 'region'); wrap.setAttribute('aria-label', caption);
  const t = el('table'); t.append(el('caption', caption));
  const tr = el('tr'); head.forEach(h => { const th = el('th', h); th.scope = 'col'; tr.append(th); });
  const thead = el('thead'); thead.append(tr); t.append(thead);
  const tb = el('tbody');
  rows.forEach(cells => { const r = el('tr'); cells.forEach(c => { const td = el('td'); if (c instanceof Node) td.append(c); else td.textContent = String(c); r.append(td); }); tb.append(r); });
  if (!rows.length) { const r = el('tr'), td = el('td', 'None yet'); td.colSpan = head.length; r.append(td); tb.append(r); }
  t.append(tb); wrap.append(t); return wrap;
}

async function monitor() {
  const out = $('#monitor'); out.textContent = '';
  say('Reading your channel...');
  const ch = await get(`${API}/channels?part=snippet,statistics,contentDetails&mine=true`);
  if (ch.error) { say(`Could not read your channel: ${ch.error}`); return; }
  const c = (ch.data.items || [])[0];
  if (!c) { say('This Google account has no YouTube channel.'); return; }
  const s = c.statistics;
  say(`Connected: ${c.snippet.title}.`);
  const dl = el('dl', null, 'stats');
  [['Subscribers', s.hiddenSubscriberCount ? 'hidden' : num(s.subscriberCount)], ['Views', num(s.viewCount)], ['Videos', num(s.videoCount)]]
    .forEach(([k, v]) => { const d = el('div'); d.append(el('dt', k), el('dd', v)); dl.append(d); });
  out.append(dl);
  const up = c.contentDetails.relatedPlaylists.uploads;
  const pl = await get(`${API}/playlistItems?part=contentDetails&maxResults=25&playlistId=${encodeURIComponent(up)}`);
  if (pl.error) { out.append(el('p', `Uploads: ${pl.error}`, 'note')); return; }
  const ids = (pl.data.items || []).map(i => i.contentDetails.videoId);
  if (!ids.length) { out.append(table('Latest uploads', ['Video'], [])); return understand(); }
  const v = await get(`${API}/videos?part=snippet,statistics,status&id=${ids.join(',')}`);
  if (v.error) { out.append(el('p', `Videos: ${v.error}`, 'note')); return; }
  out.append(table('Latest uploads', ['Video', 'Published', 'Visibility', 'Views', 'Likes', 'Comments'],
    v.data.items.map(x => {
      const a = el('a', x.snippet.title); a.href = `https://www.youtube.com/watch?v=${x.id}`; a.rel = 'noopener noreferrer';
      return [a, x.snippet.publishedAt.slice(0, 10), x.status.privacyStatus, num(x.statistics.viewCount), num(x.statistics.likeCount), num(x.statistics.commentCount)];
    })));
  understand();
}

async function understand() {
  const out = $('#understand'); out.textContent = '';
  const end = new Date(), start = new Date(Date.now() - 28 * 864e5);
  const d = x => x.toISOString().slice(0, 10);
  const r = await get(`https://youtubeanalytics.googleapis.com/v2/reports?ids=channel==MINE&startDate=${d(start)}&endDate=${d(end)}&metrics=views,estimatedMinutesWatched,averageViewDuration,subscribersGained,subscribersLost&dimensions=day&sort=day`);
  if (r.error) { out.append(el('p', `Analytics: ${r.error}`, 'note')); return; }
  const rows = r.data.rows || [];
  const sum = i => rows.reduce((a, x) => a + (x[i] || 0), 0);
  out.append(el('p', `Last 28 days: ${num(sum(1))} views, ${num(sum(2))} minutes watched, ${num(sum(4) - sum(5))} net subscribers.`, 'note'));
  out.append(table('Day by day, last 28 days', ['Day', 'Views', 'Minutes watched', 'Average view (s)', 'Subscribers gained', 'Lost'],
    rows.slice().reverse().map(x => [x[0], num(x[1]), num(x[2]), num(x[3]), num(x[4]), num(x[5])])));
}

async function publish(e) {
  e.preventDefault();
  const f = $('#file').files[0];
  const msg = $('#pubstatus');
  if (!f) { msg.textContent = 'Choose a video file first.'; return; }
  if (!$('#confirm').checked) { msg.textContent = 'Tick the confirmation to publish.'; return; }
  if (!granted.has(UPLOAD)) {
    msg.textContent = 'Asking Google for permission to upload...';
    if (!(await connect([...READ, UPLOAD])) || !granted.has(UPLOAD)) { msg.textContent = 'Upload permission was not given. Nothing was uploaded.'; return; }
  }
  const meta = {
    snippet: { title: $('#title').value.trim().slice(0, 100), description: $('#desc').value.slice(0, 5000) },
    status: { privacyStatus: $('#privacy').value, selfDeclaredMadeForKids: false },
  };
  const boundary = 'sws' + Math.random().toString(36).slice(2);
  const body = new Blob([
    `--${boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n${JSON.stringify(meta)}\r\n`,
    `--${boundary}\r\nContent-Type: ${f.type || 'video/*'}\r\n\r\n`, f, `\r\n--${boundary}--`,
  ]);
  const xhr = new XMLHttpRequest();
  xhr.open('POST', 'https://www.googleapis.com/upload/youtube/v3/videos?uploadType=multipart&part=snippet,status');
  xhr.setRequestHeader('authorization', 'Bearer ' + token);
  xhr.setRequestHeader('content-type', `multipart/related; boundary=${boundary}`);
  xhr.upload.onprogress = p => { if (p.lengthComputable) msg.textContent = `Uploading: ${Math.round(100 * p.loaded / p.total)}%`; };
  xhr.onload = () => {
    if (xhr.status >= 200 && xhr.status < 300) {
      const v = JSON.parse(xhr.responseText);
      msg.textContent = `Uploaded as ${v.status.privacyStatus}: https://www.youtube.com/watch?v=${v.id}`;
      $('#publish').reset();
      monitor();
    } else {
      let m = `HTTP ${xhr.status}`; try { m = JSON.parse(xhr.responseText).error.message || m; } catch {}
      msg.textContent = `YouTube refused the upload: ${m}`;
    }
  };
  xhr.onerror = () => { msg.textContent = 'The upload failed to reach YouTube.'; };
  xhr.send(body);
}

async function init() {
  try { clientId = ((await (await fetch('/data/youtube.json')).json()).client_id || '').trim(); } catch {}
  if (!clientId) {
    $('#connect').disabled = true;
    say('Not connected yet: the owner adds the Google OAuth client ID to data/youtube.json.');
    return;
  }
  $('#connect').addEventListener('click', async () => { if (await connect(READ)) { $('#forget').hidden = false; $('#publishbox').hidden = false; monitor(); } });
}
$('#forget').addEventListener('click', () => {
  if (token && window.google) google.accounts.oauth2.revoke(token, () => {});
  token = ''; granted = new Set();
  ['#monitor', '#understand', '#pubstatus'].forEach(s => { $(s).textContent = ''; });
  $('#publishbox').hidden = true; $('#forget').hidden = true;
  say('Disconnected. The access token was revoked and nothing was stored.');
});
$('#publish').addEventListener('submit', publish);
init();

// Videos: the agent's Reels and Shorts, from the Instagram site's public feed (no token, no login).
const FEED = 'https://instagram.platform.sovereignweb.site/data/reels.json';
const STATE = { sent: 'Published', waiting: 'Waiting to post', 'deleted, to be reposted': 'Being re-made' };
async function videos() {
  const box = $('#videos');
  let d;
  try { const r = await fetch(FEED, { credentials: 'omit', referrerPolicy: 'no-referrer' }); if (!r.ok) throw 0; d = await r.json(); }
  catch { box.textContent = ''; box.append(el('p', 'The list of videos could not be loaded just now.', 'note')); return; }
  box.textContent = '';
  const list = el('ul', null, 'reels');
  for (const v of d.reels || []) {
    const li = el('li', null, 'reel');
    if (v.poster) { const img = el('img'); img.src = v.poster; img.alt = ''; img.loading = 'lazy'; img.width = 180; img.height = 320; li.append(img); }
    const body = el('div');
    body.append(el('h3', v.title));
    const meta = [STATE[v.state] || v.state, v.duration_s ? `${v.duration_s} s` : '', v.published_at ? String(v.published_at).slice(0, 16).replace('T', ' ') + ' UTC' : ''].filter(Boolean).join(' · ');
    body.append(el('p', meta, 'note'));
    const links = el('p', null, 'links');
    const add = (href, text) => { if (!href) return; const a = el('a', text); a.href = href; a.rel = 'noopener noreferrer'; links.append(a); };
    add(v.page, 'Watch, with credits and sources');
    add(v.channels && v.channels.youtube, 'On YouTube');
    add(v.channels && v.channels.instagram, 'On Instagram');
    body.append(links);
    li.append(body);
    list.append(li);
  }
  if (!list.children.length) box.append(el('p', 'No videos yet.', 'note')); else box.append(list);
  box.append(el('p', `List updated ${String(d.updated || '').replace('T', ' ')}, from the agent's Instagram site.`, 'note'));
}
videos();
