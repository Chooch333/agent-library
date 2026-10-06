# Stack Advisor — email format

Read at DELIVER (step 6c). Moved here unchanged from SKILL.md v1.8.1 by
BB-2026-10-05-advisor-reads-smarter (Build 28). Build 28.1 added the two
honest lines and the FRONTIER tag. Once the critic is live, the Advisor
Critic sends this email, not the Advisor.

The email is a quick hit. Charles reads the full idea on the Stack
screen; the email tells him what's there in under a minute. It is built
from the same ideas as the ADV file, cut down — never new content. Send
it with both `htmlBody` (the formatted version) and `body` (the same text
as a plain-text fallback). Subject: "Stack Advisor brief ADV-YYYY-MM-DD".

**Per idea, in this order:**
1. Heading line: `ADV-NNN · {title, rule 6}` plus ` · HIGH CONVICTION`
   or ` · FRONTIER` when it applies.
2. One short source line: who or what it came from, in a few words,
   with the source link on the name. Own-records ideas say "From your
   own records — {what they are}" with no link.
3. Six sections, **one sentence each** (about 25 words max):
   "What they found" (or "What your records show"), "What you have
   today", "What's wrong today", "Why it matters", "What you'd gain",
   "Why this might be wrong". No "In plain terms" — the title does that
   job in the email.
4. One small line: `Effort: {small|medium|large} · Checked: {what was
   verified, a few words} · Assumed: {what wasn't, a few words}` (drop
   the Assumed part if nothing was assumed).
5. If resurfaced: one small line `Raised again because: {one clause}`.
6. Link: `Open the full idea on the Stack screen →` pointing to
   `{STACK_URL}?sel=advisor:ADV-NNN`.

**Whole email:** title line "Stack Advisor — {Mon D}", then the opening
(rule 7, at most three sentences), then the ideas. If there are
"Questions for Charles", they follow the ideas as one short numbered
list. **No "How this run worked" section and no git path** — those stay
in the ADV file. A zero-idea run sends just the title line and the
opening.

**STACK_URL** (one place to change at go-live):
`https://cbrain-ui-git-review-chooch333s-projects.vercel.app/stack`

**HTML template** (`htmlBody`; inline styles only — Gmail strips
`<style>` blocks). Repeat the idea rows per idea; escape `&`, `<`, `>`,
and quotes in all inserted text:

```html
<html><body style="margin:0;padding:0;background:#ffffff;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" style="padding:24px 12px;">
<table role="presentation" width="640" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:640px;font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.55;color:#222222;">
<tr><td style="padding:0 0 18px 0;font-size:22px;font-weight:bold;">Stack Advisor — {Mon D}</td></tr>
<tr><td style="padding:0 0 24px 0;">{opening}</td></tr>
<!-- per idea: -->
<tr><td style="padding:0 0 6px 0;font-size:20px;font-weight:bold;text-decoration:underline;">ADV-NNN · {title}{ · HIGH CONVICTION}</td></tr>
<tr><td style="padding:0 0 16px 0;font-size:13px;color:#666666;">{source line, link on the name}</td></tr>
<tr><td style="padding:0 0 2px 0;font-size:16px;font-weight:bold;text-decoration:underline;">What they found</td></tr>
<tr><td style="padding:0 0 14px 0;">{one sentence}</td></tr>
<tr><td style="padding:0 0 2px 0;font-size:16px;font-weight:bold;text-decoration:underline;">What you have today</td></tr>
<tr><td style="padding:0 0 14px 0;">{one sentence}</td></tr>
<tr><td style="padding:0 0 2px 0;font-size:16px;font-weight:bold;text-decoration:underline;">What's wrong today</td></tr>
<tr><td style="padding:0 0 14px 0;">{one sentence}</td></tr>
<tr><td style="padding:0 0 2px 0;font-size:16px;font-weight:bold;text-decoration:underline;">Why it matters</td></tr>
<tr><td style="padding:0 0 14px 0;">{one sentence}</td></tr>
<tr><td style="padding:0 0 2px 0;font-size:16px;font-weight:bold;text-decoration:underline;">What you'd gain</td></tr>
<tr><td style="padding:0 0 14px 0;">{one sentence}</td></tr>
<tr><td style="padding:0 0 6px 0;font-size:13px;color:#555555;"><b>Effort:</b> {size} · <b>Checked:</b> {…} · <b>Assumed:</b> {…}</td></tr>
<tr><td style="padding:0 0 10px 0;font-size:13px;color:#555555;"><b>Raised again because:</b> {…}</td></tr><!-- only if resurfaced -->
<tr><td style="padding:0 0 28px 0;"><a href="{STACK_URL}?sel=advisor:ADV-NNN" style="color:#1a5fb4;font-weight:bold;">Open the full idea on the Stack screen →</a></td></tr>
<!-- end per idea -->
</table>
</td></tr></table>
</body></html>
```

The plain-text `body` carries the same words in the same order, with
blank lines between sections and the Stack screen URL written out.
