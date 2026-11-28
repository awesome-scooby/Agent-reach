# Stage 5 launch checklist (only on the owner's instruction)

## Before launch: must be confirmed by the practitioner
- [ ] Public business name, and title exactly as on the Ahpra register
- [ ] Services, client ages, languages, scope ("when I might not be the right fit")
- [ ] Fees, durations, cancellation terms
- [ ] Medicare rebate wording, amounts and eligibility (or remove the section)
- [ ] Referral route (secure messaging ID or fax) and provider number
- [ ] Urgent-help wording and numbers for the live state
- [ ] Complaints bodies for the live state
- [ ] Privacy policy matches what the practice actually does
- [ ] No draft markers left: search the site for "practice-draft" and "["

## Technical
- [ ] Domain registered to the practice; HTTPS on
- [ ] Booking link points to the real provider and has been tested end to end
- [ ] Settings › Reading: tick off "Discourage search engines"
- [ ] SEO plugin: titles and meta descriptions written; sitemap on; draft pages excluded
- [ ] Redirect plugin installed (needed for room moves)
- [ ] Backups confirmed; first restore drill done
- [ ] All accounts are individual and have MFA
- [ ] Re-run `tests/site_checks.py` and `tests/editing_contract.py` against staging
- [ ] Lighthouse mobile ≥ 90 on Home and Fees, run on the real host

## After launch
- [ ] Smoke check on a phone: Home, Fees, booking link, For GPs, Contact, a 404 URL
- [ ] Record: open issues, responsible person, review date
