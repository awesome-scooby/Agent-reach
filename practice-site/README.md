# Practice website (private staging build)

Block theme plus setup scripts for the psychology practice website. Every public fact is a **placeholder** until the practitioner approves it. No real fees, names, credentials, referrals or clinical information go in this repository.

## Five stages

| Stage | Deliverable | Status |
|---|---|---|
| 1. Agree the brief | `docs/decision-sheet.md` (with assumptions), `docs/persuasion-principles.md`, costed plan | Done, with assumptions marked |
| 2. Prove the design and editor | Clarity style (Apple-like, default), plus Eucalypt and Dusk variations; editing test | Done |
| 3. Build the launch site | All pages, service/profile/room/policy starter patterns, draft Perth and Melbourne rooms, referral route | Done on local staging, with placeholders |
| 4. Test and hand over | `tests/site_checks.py` (38 checks), `tests/editing_contract.py` (17), Lighthouse, `docs/editor-guide.md`, `docs/operations.md` | Automated tests pass. Owner exercise and restore drill need a real host |
| 5. Launch | `docs/launch-checklist.md` | Waiting for your instruction, a host and approved content |

## Where business content lives

- `theme/practice/`: presentation only (layout, colours, fonts, patterns). Safe to redesign.
- The database: fees, intake status, contact details and urgent help as **synced patterns**, plus all pages. A theme update never overwrites them.
- `setup/`: creates the shared blocks and pages with placeholder data on a fresh site.

Note: once someone edits a template in the Site Editor, that edited copy is saved in the database and overrides the theme file. A later theme update won't show on that template until it's reset (Site Editor › Templates › Reset).

## Run locally

Needs Node 22.20 or newer.

```bash
npx @wp-playground/cli@3.1.66 server --port 9400 \
  --mount=$PWD/theme/practice:/wordpress/wp-content/themes/practice \
  --mount=$PWD/setup:/wordpress/practice-setup \
  --blueprint=$PWD/setup/blueprint.json --login
```

Then open http://127.0.0.1:9400. Each run starts from a fresh site.

## Draft preview (static, for review only)

```bash
# start the site with setup/blueprint-visitor.json (logged out), then:
python3 -I tools/export_preview.py OUT_DIR
python3 -I tests/preview_checks.py OUT_DIR
```

The export is a snapshot for sharing a draft. The real site stays in WordPress.

## Tests

```bash
python3 -I tests/editing_contract.py   # fee changed once, intake paused, both restored
python3 -I tests/site_checks.py axe.min.js   # accessibility, reflow, keyboard, journeys, drafts, noindex
python3 -I tests/screens.py OUT_DIR a  # phone and desktop screenshots
```
