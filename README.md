# Esperanza Program Pricing (prototype)

A calculator for pricing group trips in Egypt for Esperanza Travel. It replaces the paper costing sheet: number of people → transport, guides, tickets, meals, hotels and cruises → price per person in a double room, in a triple room, the single supplement, and children's prices, for each group size.

This is a **prototype for testing with the client**. It is one HTML file with no server, no build step and no dependencies. Data is saved in the browser (localStorage) on the device that uses it.

## Files

| File | What it is |
|---|---|
| `tour-costing.html` | The whole app (English by default, switchable to Arabic). **Edit this one.** |
| `tour-costing-ar.html` | Arabic-default copy. Generated: don't edit by hand. |
| `scripts/build-ar.py` | Regenerates the Arabic copy from the English file. |
| `.claude/launch.json` | Local preview server config for Claude Code. |

## Run it locally

```bash
python3 -m http.server 8765
```

Then open http://localhost:8765/tour-costing.html (or `tour-costing-ar.html`).

## After every change

```bash
python3 scripts/build-ar.py
```

Commit both HTML files together.

## How the code is organized (inside `tour-costing.html`)

- **Data:** `CITIES`, `VEH` (vehicle types and seats), `RATES` (transport sheet), `LISTS` (price list definitions), `seedLists()` (sample prices), `TEMPLATES` (3 ready programs), `defaults()` (settings).
- **Pricing:** `calcTier(pax)` works out one group size; `compute()` runs all sizes and `warnings()`; `totals()` gives revenue, cost, profit and deposit.
- **Screens:** `renderShell()` and `renderView()` (by URL hash: `#program`, `#files`, `#lists`, `#settings`), the 7-step wizard, `renderPanel()` (live price), `clientView()` and `internalView()`.
- **Text:** every label is `T(english, arabic)`. RTL layout uses logical CSS properties.
- **Events:** one delegated `input`/`change` handler (`onInput`, `data-*` attributes) and one `click` handler (`data-act`).

## Price data

Only the transport sheet, three tickets (GEM, Pyramids, Islamic Cairo) and the lunch price are the client's real numbers. Everything else is sample data until the real price sheets arrive.

## Not in the prototype (needs the real app)

User logins and roles, shared price lists across the team, change log, backups, PDF output, the service order for guides and reps, Italian and Spanish documents.
