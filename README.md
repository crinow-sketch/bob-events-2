# BOB Events 2

Events & calendar app for **Buffalo Olde Brewery** (1223 Lovejoy St, Buffalo, NY) — live music schedule, monthly calendar, private events / Banquet Event Orders (BEOs), and a staff notification list.

Owner: Cory "Cjr" Rinow, Carousel Development.

This is **version 2**: a new repo built from the 2026-11-05 unified iteration of the original app. The v1 repo (`crinow-sketch/bob-events`) and its live site are untouched — v2 is a separate repo that talks to the **same Supabase project and tables**, so it works against the same live data out of the box with no migration.

- v1 repo (read-only): https://github.com/crinow-sketch/bob-events
- v1 live site: https://crinow-sketch.github.io/bob-events/
- **v2 live site (once published): https://crinow-sketch.github.io/bob-events-2/**

## What it does

- **Dashboard** — stats (live music / private events / BMC concerts) + "Coming Up Next" cards.
- **Monthly calendar** — color-coded by event type (Live Music, Private Event, BMC Concert, Sabres, Bills, Trivia). The month range is dynamic: 2 months back through the current month + 18 months, so it never runs out.
- **All Events** — filterable list (music / private / BMC / Sabres / Bills / Trivia).
- **Manage Events** (behind a PIN gate) — add/edit/delete music events and full BEOs (guests, menu, staffing, pricing, timeline, contacts), save BEO drafts on the device, print BEOs, export all data as JSON, and manage the staff email notification list.
- **Notifications** — EmailJS if configured (it isn't — see below), otherwise falls back to opening the user's mail app (`mailto:`) with the checked staff in the To line.
- **PWA** — installable via `app-manifest.json` (`BOB Events 2`); icons included.

## What changed vs v1

Taken from the 2026-11-05 iteration (see `BUILD-NOTES.md` for the full diff):

1. **Unified the two divergent copies.** v1's repo had Trivia support; the Drive working copy had the full BEO form, the Inventory link, and "Private Events / BEOs". The live site only ever had the repo version. v2 has both.
2. **Loading + error states.** v1 failed silently (console only) when Supabase was unreachable — empty sections, no message. v2 shows a loading spinner, an error banner with a **Retry** button, and a "last updated" stamp.
3. **Explicit event-type field.** v1 inferred type by substring-matching names/notes ("sabres", "bills", "trivia", "bmc"). v2 reads an explicit `type` column when present and only falls back to substring detection for legacy rows.
4. **No hardcoded end date.** v1's month nav ran through December 2027. v2 builds months dynamically (see above).
5. **HTML escaping.** v1 interpolated event names/notes straight into `innerHTML`. v2 escapes every interpolated string via `esc()`.
6. **Working toast.** v1's `sendEventNotification` called `toast(...)`, but `toast` was never defined (latent ReferenceError). v2 defines it.
7. **CONFIG block.** Supabase URL/key, PIN, and EmailJS settings live in one `CONFIG` object at the top of the script instead of being scattered through the file.
8. **Band contacts no longer publish real personal data.** v1 hardcoded ~26 bands' personal emails/phones in a public repo. v2 uses a placeholder seed map. Known gap: the band-contact display in the music detail modal was lost in the merge — see `BUILD-NOTES.md`.
9. **"2" branding** — page title, header, PWA manifest name, export filenames, and the localStorage draft key are all namespaced to v2 so v1 and v2 never collide on the same device.

Two small fixes made while building v2 (not in the iteration file):

- `CONFIG` referenced `EMAILJS_SERVICE_ID` but never defined it — added it, with v1's service/template values. Behavior is unchanged (public key is still empty, so notifications still degrade to `mailto:`).
- `loadBEODraft()` was defined but never called — it is now called on init, so a saved BEO draft is actually offered back.

## Deploy to GitHub Pages (free)

1. Create a new public repo named **`bob-events-2`** under `crinow-sketch` and upload this whole folder (or `git init` here, add the remote, and push).
2. In the repo: **Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: `master` (or `main`) / `/ (root)` → Save.**
3. Wait about a minute. The site will be live at **https://crinow-sketch.github.io/bob-events-2/**.
4. On Windows, `publish.bat` does the git add / commit / push in one double-click (update the branch name in it if you use `main` instead of `master`).

No build step, no server, no cost. The app is a static single file plus manifest/icons.

## Supabase config

- Project: `https://cbdjoydzoiysvcleybpq.supabase.co`
- Tables: `music_events`, `beos`, `staff_contacts` (same as v1 — no migration).
- The anon key in `CONFIG.SB_ANON_KEY` is the **public anon key**, identical to the one v1 already publishes in its page source. An anon key is not a password and was never secret. If you ever rotate it in Supabase, update it here too.
- Optional: a `band_contacts` table (`name`, `email`, `phone`) is the intended home for band contact details — see `BUILD-NOTES.md`. The app works without it.
- Optional: add a `type` column to `music_events` / `beos` to use the explicit event type; legacy rows without it still work via the substring fallback.

## EmailJS

`CONFIG.EMAILJS_PUBLIC_KEY` is intentionally empty, exactly as in v1 and in the iteration: with no key, notifications degrade to opening the user's mail app (`mailto:`) with all checked staff in the To line. To use EmailJS instead, create an EmailJS account, set `EMAILJS_PUBLIC_KEY` (and service/template IDs if they differ from the v1 values already in `CONFIG`), and redeploy. Note the `mailto:` fallback exposes all staff addresses to each other.

## Security — read this

**The Manage PIN (`ADMIN_PIN = "1234"`) only hides buttons. It does not protect data.** This is an explicit owner decision (Nov 6, 2026: Cjr chose the easy PIN over real staff sign-in). There is deliberately **no Supabase Auth and no staff sign-in** in this app, and no Row Level Security (RLS) SQL has been applied.

Because the Supabase anon key is public and RLS is disabled (v1's state, unchanged), **anyone who reads the page source can read, write, and delete every row in `music_events`, `beos`, and `staff_contacts` with a single request** — the PIN cannot stop that. The RLS SQL that would actually protect the tables is documented as a comment at the top of `index.html` only. Do **not** run it with this version of the app: enabling RLS while the app still uses only the anon key would lock the app itself out of writing. Real protection requires a staff sign-in (Supabase Auth) in the app first — that was built and reverted at Cjr's request, so it is intentionally not here.

Treat the PIN as a UI convenience for keeping casual visitors out of the Manage forms, nothing more.

## Files

| File | What it is |
|---|---|
| `index.html` | The whole app (single file, ~81 KB) |
| `app-manifest.json` | PWA manifest ("BOB Events 2") |
| `icon-192.png`, `icon-512.png`, `icon.svg` | PWA icons (unchanged from v1) |
| `publish.bat` | Windows one-click git add/commit/push |
| `_seed_bills.py` | One-off script that seeds Bills games into `music_events` (unchanged from v1; uses the same public anon key) |
| `README.md` | This file |
| `BUILD-NOTES.md` | What was built, what changed vs v1, what was verified, what wasn't |

Not included: `inventory.html` (a separate Firebase/QR-code inventory app — it was never in the v1 repo; the nav link to it in `index.html` comes from the Drive working copy and will 404 until that app is added to this repo) and `sw.js` (no service worker in v1 either, despite the PWA manifest).
