# Esperanza Program Pricing — project context for Claude

## Who and why
- **Client:** Reem, Esperanza Travel (Egypt). She prices group trips (mostly Italian, Spanish and other European groups) on paper. This app replaces her paper costing sheet.
- **Owner of this repo:** Ahmed (builds the app for her). Talk to him in plain language; he is not reviewing code line by line.
- **Stage:** working prototype, validated step by step with Reem. Live at https://reem.wheretospot.com (Nov 2026). Next: collect her real prices.

## What the client asked for (spec PDF, Nov 2026, "مواصفات تطبيق تسعير البرامج")
The PDF is not in the repo (client document; `*.pdf` is gitignored). Summary:
- **Phase 1 (done):** price lists, day-by-day program builder, price per person in double / triple / single supplement.
- **Phase 2 quick wins (done):** free places (FOC, e.g. 20+1), children priced as % of adult by age band, high-season dates with +% per price row, Gala Dinner on 31 Dec, categories A/B (two hotel levels side by side), several group sizes compared, Esperanza branding.
- **Phase 3 (not started):** service order for guides and reps; client documents in Italian and Spanish (program language already exists as a field: ar/it/es/en).
- **Phase 4 (not started):** statuses and reports across files, users and roles (admin / pricing / view), change log, backups, PDF output, mobile.
- Phase 3–4 items that need a server (logins, shared price lists across the team, audit log, backups) are out of scope for the single-file prototype.

## Still waiting on from Reem (spec section 8)
Real price sheets for every list (hotels, cruises, flights, train, guides, reps, restaurants, activities, optional tours, tips/visa by nationality), default profit %, child age bands and %s, season dates, her 3 standard programs, logo PNG, a sample program PDF and a service order, user names and roles.
**Real data today:** only the transport sheet (`RATES`), three tickets (GEM 1600, Pyramids 1000, Islamic Cairo 750 EGP) and lunch (1500, flagged `paper:true`). Everything else in `seedLists()` is sample data and is labelled "sample" in the UI.

## Files
- `tour-costing.html` — the whole app, vanilla JS, no build, no dependencies (Google Fonts only). **Edit only this file.**
- `tour-costing-ar.html` — generated Arabic-default copy. After every change run `python3 scripts/build-ar.py` and commit both.
- `index.html` — start page for the hosted site: links to the English and Arabic app.
- `robots.txt` — keeps the site out of search engines (internal tool).
- `.cpanel.yml` — cPanel Git deployment: copies only `index.html`, the two app pages and `robots.txt` to the web folder. Add any new web file to its `cp` line.

## How the app works
- 7-step wizard: 🧾 Client → 👥 People & rooms → 📅 Dates → 🗓️ Days → 🏨 Hotels & cruise → ✅ Included → 💾 Review & save. Live price panel beside it. Other views by hash: `#files`, `#lists`, `#settings`.
- Pricing per person = (shared costs ÷ paying people) + individual costs + room ÷ occupancy + misc % → profit (% or fixed) → round up. FOC: `floor(pax/focEvery)` free people; their costs and a single room go into shared costs. Transport VAT 14%. Vehicles chosen automatically (fewest or cheapest).
- Key functions: `calcTier(pax)`, `compute()` (sets `RES`), `totals()`, `warnings()`, `inclItems()/exclItems()`, `clientView()`, `internalView()`, `renderPanel()`, `waText()`.
- Text: every label is `T(english, arabic)`. RTL uses logical CSS properties. Numbers inside Arabic text use `.num`/`<bdi>`; group sizes like `20+1` go through `pl()` so they don't flip.
- Events: one delegated `input`/`change` handler (`onInput`, `data-*` attributes) and one `click` handler (`data-act`).
- Storage: browser `localStorage`, one key `esperanza-pricing.v4` shared by the English and Arabic pages (data stays in each browser/device; not shared between team members).
  - First load merges the old per-page keys `esperanza-pricing.v4.en` / `.v4.ar` (`mergeOld()`): files, custom list rows and transport rows from both; an unsaved program from the other page becomes a draft in Files. Old keys are left as a backup; `esperanza-pricing.migrated` stops Reset from re-importing them.
  - Display language is per page: `esperanza-pricing.lang.<en|ar>` (`pageLang()`).
  - A `storage` event listener reloads `S` when the other page/tab saves, so two open tabs don't overwrite each other.
- Debug handle: `window.__app = {S, compute, calcTier, totals, RES}`.

## Testing
- Run locally: `python3 -m http.server 8765`, open `/tour-costing.html` and `/tour-costing-ar.html`.
- Check after changes: the cost breakdown adds up to total cost; prices change when a ticket is toggled; no console errors; no horizontal scroll at 375px width in both languages (Arabic is RTL).
- Reference check from Reem's paper example: about $328 / $311 / $305 per person for her three group sizes (her paper says 328 / 311 / 306; the gap is her per-line rounding).

## Hosting (live)
- **URL:** https://reem.wheretospot.com — Namecheap shared hosting (cPanel, LiteSpeed). Domain registered at Namecheap; the main `wheretospot.com` site is on Wix, so don't touch the domain's other DNS records.
- **Deploy:** cPanel → Git Version Control clones the repo over HTTPS into `~/repositories/esperanza-pricing`; `.cpanel.yml` copies the site files to `~/reem.wheretospot.com/`. Not automatic: after merging to `main`, Ahmed clicks Manage → Pull or Deploy → **Update from Remote**, then **Deploy HEAD Commit**.
- **SSL:** cPanel AutoSSL certificate for `reem.wheretospot.com`.
- **Access control:** cPanel Directory Privacy (password per team member) on the `reem.wheretospot.com` folder. Check it is on before sharing the link.
- **The GitHub repo is public** (made public so cPanel can clone without SSH keys). Anything committed is visible to anyone, including Reem's real transport sheet in `RATES`. Never commit passwords, keys, client documents, customer names or more of her real prices without asking Ahmed; if real prices must stay private, keep them in the in-app price lists (browser only) or make the repo private again and set up a deploy key.
- The old claude.ai artifact links belong to Ahmed's personal Claude account; the hosted domain replaces them.

## Working rules
- Pull before starting, commit and push when done (Ahmed works from two Claude accounts). Changes reach the live site only after merge to `main` and a cPanel deploy; remind Ahmed.
- Ask Ahmed before anything that costs money or changes DNS.
- Keep it one HTML file unless the move to a real backend is decided.
- Don't commit client documents, logos received by email, or real customer names beyond the sample.
