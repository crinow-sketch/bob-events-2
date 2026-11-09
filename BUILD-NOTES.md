# BUILD-NOTES — BOB Events 2

Built 2026-11-08 by Crowbar (subagent) from the parent orchestrator's task.
Local tree only — **nothing was pushed to GitHub and nothing is live**.
Destination: `~/workspace/overnight-apps-2026-11-08/bob-events-2/`

## Starting points (all read first)

- **Base file:** `~/workspace/your_files/Logan Nine Fingers dissertation/bob-events-my-iteration-2026-11-05.html` (1,283 lines, the unified iteration: Trivia support + full BEO form + Inventory link, loading/error states with retry, explicit event-type field with legacy substring fallback, dynamic month range, CONFIG block, working toast).
- **Background:** `survey-inventory-report-2026-11-05.md`, §4a (BOB Events review) — the 9 verified weaknesses and what the iteration fixed.
- **Original repo (public, read-only):** https://github.com/crinow-sketch/bob-events, branch `master`, fetched via `curl` tarball (`https://codeload.github.com/crinow-sketch/bob-events/tar.gz/refs/heads/master`). The v1 repo and live site were **not touched** in any way (tarball extracted to `/tmp` only).

## Files included

| File | Source / change |
|---|---|
| `index.html` (81,077 bytes) | Iteration file, rebranded to "BOB Events 2" + 2 small fixes (below) |
| `app-manifest.json` | v1 manifest, rebranded: name "BOB Events 2", short_name "BOB 2", description "…(v2)", `start_url` `/bob-events/` → `/bob-events-2/` |
| `icon-192.png`, `icon-512.png`, `icon.svg` | Byte-identical copies from the v1 repo (`cmp` verified) |
| `publish.bat` | v1 script, repointed: title "BOB Events 2", live URL `https://crinow-sketch.github.io/bob-events-2/` |
| `_seed_bills.py` | Byte-identical copy from the v1 repo (`diff` verified). One-off seeder that POSTs 17 Bills games into `music_events` using the same public anon key. Unchanged because it targets the same table v2 uses. |
| `README.md` | New: what the app is, changes vs v1, GitHub Pages deploy steps, Supabase/EmailJS notes, honest security note |
| `BUILD-NOTES.md` | This file |

**Not included, deliberately:** `inventory.html` (separate Firebase/QR inventory app — never in the v1 repo; the nav link to it survives from the Drive copy and will 404 until that app is added), `sw.js` (no service worker in v1 either, despite the PWA manifest), `_seed_music.py` / `_seed_sabres.py` (exist in Drive, not in the v1 repo — not copied).

## What changed vs the v1 repo

v1 repo contents were: `index.html` (61,027 bytes, 1,151 lines), `app-manifest.json`, `icon-192.png`, `icon-512.png`, `icon.svg`, `publish.bat`, `_seed_bills.py`. Diffing that against the iteration file confirmed the iteration already covered the survey §4a fixes (unified copies, error states, explicit `type`, dynamic months, escaping, working toast, CONFIG block). The v2 build adds, on top of the iteration:

1. **Rebrand to "BOB Events 2"** — `<title>`, nav brand ("Events Hub 2"), site bar ("BOB Events 2"), `apple-mobile-web-app-title` ("BOB 2"), manifest name/short_name/start_url, header comment, export filename (`bob-events-2-export-…`), localStorage draft key (`bob-events-2-beo-draft`, so v1 and v2 never share drafts on one device), notification email body, `publish.bat` URL.
2. **Fix 1 — missing `EMAILJS_SERVICE_ID`.** The iteration's `sendEventNotification` reads `CONFIG.EMAILJS_SERVICE_ID`, but the iteration's `CONFIG` never defines it (only `EMAILJS_TEMPLATE_ID` and `EMAILJS_PUBLIC_KEY`). Added `EMAILJS_SERVICE_ID: "default_service"` and restored v1's template value (`"template_event_notify"`). Behavior is unchanged — the public key stays empty, so notifications still degrade to `mailto:` — but if Cjr ever fills in a public key, the EmailJS branch will actually work instead of failing on an undefined service ID.
3. **Fix 2 — `loadBEODraft()` never called.** The iteration defines it (offer a saved BEO draft back on load) but nothing invokes it, so the Drive copy's draft-restore was dead code. It is now called on init (`loadData(); loadBEODraft();`). It only prompts if a draft exists on that device.
4. **Kept exactly as the owner decided:** `ADMIN_PIN = "1234"`; same Supabase project URL + public anon key as v1 (works against `music_events` / `beos` / `staff_contacts` out of the box); EmailJS public key stays empty (mailto fallback); **no Supabase Auth, no staff sign-in, no RLS SQL run or applied** — the RLS policies remain documentation-only in the `index.html` header comment, exactly as the task required. No money spent, nobody contacted, nothing pushed.

## Diff findings — what the iteration missed (carried over, documented, not silently fixed)

- **Band-contact display lost.** v1's music detail modal showed band contact info (contact name, email via `mailto:`, phone via `tel:`) looked up from a hardcoded `BAND_CONTACTS` map of ~26 real bands, and the music form used it too. The iteration replaced that map with placeholder emails (e.g. `joeyrox@email.com`) and **never uses it anywhere** — no lookup code at all — so v2's music detail modal shows no band contact info. The iteration header's claim that it "tries a `band_contacts` Supabase table first" is aspirational: no such query exists in the code. The header comment in v2's `index.html` now says this plainly instead of repeating the claim. The real v1 contact details were deliberately **not** restored (survey §4a weakness #6: personal contact data should not live in a public repo). To restore the feature properly: create a `band_contacts` table (`name`, `email`, `phone`) in Supabase and wire a lookup into `showEventDetail`.
- **v1 detail-modal Edit/Remove buttons were gated on `isUnlocked`.** v2's modals show Edit unconditionally (same as the iteration). Minor; the PIN gate still guards the Manage section itself.
- **`inventory.html` link is a dead link in this repo** (see "Not included" above). It came from the Drive working copy, which the iteration merged in. If the inventory app is ever added to this repo, the link will work as-is.
- **No service worker.** The PWA manifest exists but, as in v1, there is no `sw.js`, so there is no offline support — installability only.

## What was verified (tests run 2026-11-08)

1. **JS syntax:** all `<script>` blocks extracted to a temp file; `node --check` → **passed** (no syntax errors). Note: the page has multiple `<script>` blocks (main app, detail modals, forms, notifications, init); all were concatenated in document order for the check.
2. **HTML parses:** `python3` `html.parser` feed of the full file → **passed** (no parse errors; balanced tags as far as the parser checks).
3. **Rebrand grep:** user-visible titles/manifest read "BOB Events 2" (`<title>`, brand, site bar, manifest `name`/`short_name`, `start_url` `/bob-events-2/`). Remaining `bob-events` strings are intentional references to the **v1** repo/site (`github.com/crinow-sketch/bob-events`, `crinow-sketch.github.io/bob-events/` labeled "v1") plus the nav link `inventory.html` (no repo name in it).
4. **PIN:** `ADMIN_PIN: "1234"` confirmed present exactly once in `CONFIG`; no other PIN value anywhere.
5. **No Supabase Auth added:** grep for `createClient`, `signIn`, `signUp`, `supabase.auth`, `getSession`, `onAuthStateChange` → **no matches** in code. The only `auth.` occurrences are inside the RLS SQL **comment block** in the file header (`auth.role() = 'authenticated'`), which is documentation only and is not executed. No RLS SQL was run or applied.
6. **Supabase config preserved:** `SB_URL` and `SB_ANON_KEY` byte-identical to v1's values (same project `cbdjoydzoiysvcleybpq`, same public anon key).
7. **EmailJS behavior preserved:** `EMAILJS_PUBLIC_KEY` is still `""`, so `sendEventNotification` still takes the `mailto:` branch; the EmailJS branch is now reachable if a key is ever set (fix 1 above).
8. **Icons + seed script:** `cmp`/`diff` against the v1 tarball → byte-identical.
9. **file:// static check:** the file is self-contained HTML/CSS/JS with CDN dependencies (Google Fonts, EmailJS browser SDK) and Supabase `fetch` calls, exactly like v1. It will load from `file://` and render its static shell; live data requires network access to Supabase, and `localStorage` draft save/load works from `file://` in most browsers. No live Supabase call was made during testing (not needed, and no write test was run against the live tables).

## What could NOT be verified

- **Live behavior against Supabase** (loading real events, saving a BEO, PIN unlock flow in a browser) — no live browser test was run in this subagent session; the checks above are static/syntax only. A quick open of the file in a browser pointed at the live tables would confirm end-to-end function. The parent agent can arrange that.
- **GitHub Pages deployment** — nothing was pushed (no auth here, and the task forbids it). The deploy steps in `README.md` are the standard Pages flow from the v1 repo's own setup; the `start_url` and manifest assume the repo is named `bob-events-2` under `crinow-sketch`.
- **Whether the v1 repo has changed since the tarball fetch** — fetched 2026-11-08 from `master`; if v1 gets new commits, this snapshot comparison goes stale (does not affect v2's function).

## 2026-11-09 visual redesign (Crowbar — own vision, not Claude's)

Presentation-only restyle of `index.html`. No JS, data flow, Supabase call,
PIN, or feature behavior changed — both `<script>` blocks are byte-identical
to the 2026-11-08 file (verified by diff), and the two v2 fixes are intact
(`CONFIG.EMAILJS_SERVICE_ID` defined; `loadBEODraft()` called on init).

**Design:** warm brewery identity — charcoal `#211D18` + amber `#E8A317` /
gold `#D49A1F` + cream `#F7F1E5`. Type: Oswald (taproom-sign caps for
headings, nav, numbers), Inter (body), Fraunces italic (hero kicker).
Replaces the old look entirely (Playfair Display / Source Sans 3,
terracotta `#C2654A` / navy `#1B2A4A` / sage are gone from the file).

**What changed, file by file:**
- `index.html` — whole `<style>` block rewritten; the double header
  (dark site-bar + white nav) replaced by one sticky charcoal masthead
  carrying the real faceted-buffalo logo (`bob-logo-white.png`, white
  artwork generated from the black original by inverting RGB with alpha
  preserved); hero gains a Fraunces italic kicker ("Buffalo Olde Brewery ·
  1223 Lovejoy St"); stats become a charcoal band with amber numbers;
  event cards are ticket-style (paper card, gold spine, dashed
  perforation between date block and details); the month calendar is
  card-based (gapped cream day cards, amber ring on today, tinted type
  chips with a colored left edge — Sabres/Bills/Trivia keep solid team
  colors); BEO status chips are explicit (Confirmed = green,
  Tentative = amber, Draft = gray); modal and BEO-form headers are
  charcoal with a gold rule; buttons are amber-primary / charcoal /
  outline; PIN gate shows the black logo (`bob-logo.png`); a charcoal
  footer with the logo and the Lovejoy address was added. Old CSS variable
  names are kept as aliases with new values, so every inline style and
  JS-generated string still renders. Mobile: masthead stacks, nav becomes
  a horizontal scroll row, calendar cells shrink.
- `bob-logo.png` (new) — the real black faceted-buffalo logo, copied from
  `~/workspace/documents/Buffalo Olde Brewery Logo.png`.
- `bob-logo-white.png` (new) — same logo with artwork inverted to white
  for the charcoal masthead/footer. Note: the source file
  "Buffalo Olde Brewery Logo - white.png" is actually black artwork on a
  solid white box (fully opaque), so it was NOT used; the white version
  was generated from the transparent black original instead.
- `icon.svg`, `icon-192.png`, `icon-512.png` — redrawn in the new palette
  (charcoal tile, gold frame, amber BOB, cream subline). The old navy /
  terracotta beer-mug icon is gone.
- `app-manifest.json` — `theme_color` / `background_color` `#1B2A4A` →
  `#211D18`.
- The `inventory.html` nav link is kept (still a dead link in this repo,
  as before — behavior unchanged).

**Verified 2026-11-09 (this session):** `node --check` passed on both
inline `<script>` blocks; `html.parser` feed clean (no errors, no
unclosed tags); all 37 ids referenced by JS exist; every `var(--…)` used
is defined; CSS braces balanced (206 rules); no Playfair / Source Sans /
old navy-terracotta hex left; all locally referenced assets exist and
serve HTTP 200 from a local `python3 -m http.server` (index, both logos,
manifest, svg + both png icons). Not verified: a live browser render or
screenshot (no headless browser on this machine) and no live Supabase
calls were made — the parent should open the page once before pushing.
