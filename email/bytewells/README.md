# Bytewells email templates

Branded HTML + plain-text emails for Bytewells by ThoughtPivot outreach and replies. Layout: ThoughtPivot/Bytewells logo header, body, CTA button, Detroit footer with unsubscribe line.

## Files

| File | Use |
| --- | --- |
| `email1.html` / `email1.txt` | Outreach email 1 (rental pricing, Nov 2 launch) |
| `email2.html` / `email2.txt` | Follow-up |
| `email3.html` / `email3.txt` | Last note |
| `reply_waitlist.html` / `.txt` | Reply to a developer waitlist signup. Greeting is always "Hi there,", and there is no sign-off. Primary button is "Join us on Discord" (24px Discord logo, link from the `DISCORD` constant in `build.py`); the waitlist link sits in the body sentence |
| `build.py` | Source of truth for email1-3 and the waitlist reply (`R`); regenerates all `.html` and `.txt` files |
| `assets/*.svg` | Source logos (Bytewells, ThoughtPivot, Discord). The PNGs used in emails are rendered from these and hosted at `email/bytewells-logo.png`, `email/tp-logo.png` and `email/discord-logo.png` in the repo root (48px, transparent, white Discord glyph for the blurple button) |

Do not move or rename `email/bytewells-logo.png`, `email/tp-logo.png` or `email/discord-logo.png`; the templates load them from
`https://thoughtpivot.github.io/assets/email/` (GitHub Pages).

## Rendering

`build.py` holds the copy (`E1`, `E2`, `E3`, `R`) and the HTML/text templates. Edit the copy there, then run `python3 build.py` from any directory; it rewrites the `.html` and `.txt` files next to it. Constants at the top (`DISCORD`, `WL`, logo URLs, address) are one-line changes.

Optional flags need Python 3 and Playwright (`pip install playwright && playwright install chromium`): `--logos` re-renders the PNG logos from `assets/*.svg` into `email/`, and `--previews` writes preview screenshots to a temp directory (never committed).

## Placeholders

Mustache-style, filled by the sender:

- `{{first_name}}` (outreach emails 1-3 only). If the first name is empty or unknown, the sender must substitute `there` so the greeting reads "Hi there,". Never send "Hi ,".
- `{{apify_username}}` (waitlist reply only): the Apify username from the signup. The waitlist reply greeting is a fixed "Hi there," and has no name placeholder
- `{{store_actor_count}}`
- `{{sample_actor_url}}`
- `{{unsubscribe_url}}`
- `{{#had_rentals}}...{{/had_rentals}}`: block shown only if the developer had rental Actors before Oct 1

## Sending rules

- Send via Resend from `bytewells@thoughtpivot.com` (From name "Dan at Bytewells", Reply-To the same address, include a `List-Unsubscribe` header).
- Always send the HTML and plain-text parts together.
- Footer is required: ThoughtPivot, Inc., 2937 East Grand Boulevard, Detroit, MI 48202, plus the unsubscribe link.
- EU recipients get the GDPR legitimate-interest line (already in the outreach footer).
- Write "Bytewells by ThoughtPivot". English only, factual, not pitchy. No AEC words.
- Don't claim Bytewells runs on Flight, Scribe or Silc. Don't make unverified claims about how source code is stored or protected.
- Anyone who asks to be removed is removed from every list and is never replied to.
- Nothing goes out until Dan has reviewed it.
