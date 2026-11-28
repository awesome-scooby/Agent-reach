# Operations and handover

Fill this in at handover. Every account belongs to the practice, with one named person per login.

## Accounts and ownership

| Service | Account owner | Login holders | MFA | Renewal date | Cost (est.) |
|---|---|---|---|---|---|
| Domain (.com.au) | [Practice entity] | [Owner] | [ ] | [date] | ~$20–40/yr |
| Hosting (managed WordPress) | [Practice entity] | [Owner] | [ ] | [date] | ~$20–60/mo |
| WordPress admin | — | Owner (Administrator), Practitioner (Editor or approver) | [ ] | — | — |
| GitHub repository | [Practice organisation] | [Owner] | [ ] | — | Free |
| Booking system | [Practice] | [ ] | [ ] | [date] | [ ] |
| Email | [Practice] | [ ] | [ ] | [date] | [ ] |

## What lives where

- **Theme code (GitHub):** layout, styles, patterns. Deploying code changes these and nothing else.
- **Database:** pages, fees, intake status, contact details, menus, any Site Editor edits.
- **Media library:** photos and their descriptions.

## Backups and restore
- Host backups: daily, kept [30] days. Confirm this with the host.
- Before any code update, take a manual backup (host dashboard › Backups › Create).
- **To restore together:** 1) restore the database and media from the same backup point on staging, 2) deploy the theme version that was live at that date (git tag), 3) check on staging, 4) push staging to production *only* if nothing has been edited on production since.
- Run a restore drill once on staging at handover, then every 6 months. [Record the date and result here.]

## Updating code without overwriting content
1. Make and test the change on staging.
2. Deploy **only the theme folder** to production (via Git deploy or SFTP). Never copy the staging database over production, or newer edits will be lost.
3. If a changed template doesn't appear, it was edited in the Site Editor. Reset that template, or redo the edit.

## Maintenance
- Monthly (about 30 min): apply WordPress and plugin updates on staging, check, then apply on production. Check that the booking link works.
- Quarterly: review fees, policies (owner and review date), urgent-help numbers and practitioner details.
- If the booking link breaks or something urgent needs correcting: [named person], phone [ ]. As a fallback, switch the Booking action to "Enquiries only", which points people to phone and email.

## Change request (copy for each change)
- **Goal:**
- **Pages affected:**
- **Shared items touched** (fees / booking action / contact / urgent help):
- **Effect on phone layout:**
- **Cost:**
- **How we'll know it worked:**
- **How to undo it:**
