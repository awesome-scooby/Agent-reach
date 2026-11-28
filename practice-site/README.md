# Practice website (private staging build)

Block theme plus setup scripts for the psychology practice website. Every public fact is a **placeholder** until the practitioner approves it. No real fees, names, credentials, referrals or clinical information go in this repository.

## Five stages

| Stage | Deliverable | Status |
|---|---|---|
| 1. Agree the brief | `docs/decision-sheet.md`, `docs/persuasion-principles.md`, costed plan | Draft, waiting on your answers |
| 2. Prove the design and editor | Theme with two style directions, Home and Fees pages, shared blocks, editing test | **Built, waiting on your feedback** |
| 3. Build the launch site | Remaining pages and templates, referral route, room template, policies | Starts after you approve stage 2 |
| 4. Test and hand over | Accessibility and browser tests, Lighthouse, editor guide, backup/restore drill, owner exercise | After stage 3 |
| 5. Launch | Domain, HTTPS, redirects, indexing | Only when you instruct |

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

## Tests

```bash
python3 -I tests/editing_contract.py   # fee changed once, intake paused, both restored
python3 -I tests/screens.py OUT_DIR a  # phone and desktop screenshots
```
