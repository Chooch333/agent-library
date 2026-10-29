# Stack Advisor — email format

Read at DELIVER (step 6c). Moved here unchanged from SKILL.md v1.8.1 by
BB-2026-10-05-advisor-reads-smarter (Build 28). Build 28.1 added the two
honest lines and the lane tag (NEW CAPABILITY since Build 41). Build 57
(BB-2026-10-28-advisor-done-for-you) split it into two groups — Done for
you first, Ideas for you second — and cut each idea to three lines. Once
the critic is live, the Advisor Critic sends this email, not the Advisor.

The email is a quick hit. Charles reads the full idea on the Stack
screen; the email tells him what's there in under a minute, in plain
words ("Writing for Charles", `brief-format.md`: 20 words or fewer per
sentence, what changes for him, not how it works). It is built from the
same ideas as the ADV file, cut down — never new content. Send it with
both `htmlBody` (the formatted version) and `body` (the same text as a
plain-text fallback). Subject: "Stack Advisor brief ADV-YYYY-MM-DD".

**Whole email, in this order:**
1. Title line "Stack Advisor — {Mon D}".
2. The opening: at most two sentences. Say what will build unless he
   says no, then how many ideas ("2 upgrades will build Wednesday night
   unless you say no. 3 ideas for you below."). Skipped or unmatched
   answers from step 1 get one short clause here, nothing more.
3. **Done for you** (only when step 4b shelved something). Group heading,
   then per item:
   - Heading: `ADV-NNN · {title, rule 6}`.
   - *What will change* — 1–2 plain sentences. No file, tool or code
     names.
   - *What you'll notice* — 1 sentence.
   - The stop line: "Click Declined on the Stack screen before 1 am on
     {day}, or tell any chat "don't build ADV-NNN"."
   - Link: `Open it on the Stack screen →` to
     `{STACK_URL}?sel=advisor:ADV-NNN`.
4. **Ideas for you** — every other idea. Group heading, then per idea:
   - Heading: `ADV-NNN · {title, rule 6}` plus ` · HIGH CONVICTION` or
     ` · NEW CAPABILITY` when it applies. The high-conviction idea goes
     first in this group.
   - Three one-sentence lines: *What it is*, *What you'd get*, *Why it
     might not be worth it*.
   - One small line: `Effort: {small|medium|large}`, then
     ` · Cost change: {one clause}` only if the idea has a Cost line,
     then ` · Raised again because: {one clause}` only if resurfaced.
   - Link: `Open the full idea on the Stack screen →` to
     `{STACK_URL}?sel=advisor:ADV-NNN`.
5. **Questions for Charles**, if any: one short numbered list, last.

Not in the email (they stay in the ADV file and on the Stack screen): the
six-section block, "What they found", the source line, the
Checked/Assumed line, the Lens line, "How this run worked" and any git
path. A zero-idea run with nothing done for you sends just the title line
and the opening. A group with nothing in it is left out entirely.

**STACK_URL** (one place to change at go-live):
`https://cbrain-ui-git-review-chooch333s-projects.vercel.app/stack`

**HTML template** (`htmlBody`; inline styles only — Gmail strips
`<style>` blocks). Repeat the item rows per item; escape `&`, `<`, `>`,
and quotes in all inserted text:

```html
<html><body style="margin:0;padding:0;background:#ffffff;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" style="padding:24px 12px;">
<table role="presentation" width="640" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:640px;font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.55;color:#222222;">
<tr><td style="padding:0 0 18px 0;font-size:22px;font-weight:bold;">Stack Advisor — {Mon D}</td></tr>
<tr><td style="padding:0 0 24px 0;">{opening}</td></tr>

<!-- Done for you group (only when something was shelved): -->
<tr><td style="padding:0 0 4px 0;font-size:13px;font-weight:bold;letter-spacing:1px;text-transform:uppercase;color:#1a5fb4;">Done for you</td></tr>
<tr><td style="padding:0 0 18px 0;font-size:13px;color:#555555;">These build on their own unless you say no.</td></tr>
<!-- per Done-for-you item: -->
<tr><td style="padding:0 0 10px 0;font-size:20px;font-weight:bold;text-decoration:underline;">ADV-NNN · {title}</td></tr>
<tr><td style="padding:0 0 2px 0;font-size:16px;font-weight:bold;text-decoration:underline;">What will change</td></tr>
<tr><td style="padding:0 0 14px 0;">{1–2 sentences}</td></tr>
<tr><td style="padding:0 0 2px 0;font-size:16px;font-weight:bold;text-decoration:underline;">What you'll notice</td></tr>
<tr><td style="padding:0 0 14px 0;">{one sentence}</td></tr>
<tr><td style="padding:10px 12px;background:#f3f6fb;border-left:3px solid #1a5fb4;">Click <b>Declined</b> on the Stack screen before 1 am on {day}, or tell any chat "don't build ADV-NNN".</td></tr>
<tr><td style="padding:10px 0 28px 0;"><a href="{STACK_URL}?sel=advisor:ADV-NNN" style="color:#1a5fb4;font-weight:bold;">Open it on the Stack screen →</a></td></tr>
<!-- end per Done-for-you item -->

<!-- Ideas for you group: -->
<tr><td style="padding:0 0 18px 0;font-size:13px;font-weight:bold;letter-spacing:1px;text-transform:uppercase;color:#1a5fb4;">Ideas for you</td></tr>
<!-- per idea: -->
<tr><td style="padding:0 0 10px 0;font-size:20px;font-weight:bold;text-decoration:underline;">ADV-NNN · {title}{ · HIGH CONVICTION | · NEW CAPABILITY}</td></tr>
<tr><td style="padding:0 0 2px 0;font-size:16px;font-weight:bold;text-decoration:underline;">What it is</td></tr>
<tr><td style="padding:0 0 14px 0;">{one sentence}</td></tr>
<tr><td style="padding:0 0 2px 0;font-size:16px;font-weight:bold;text-decoration:underline;">What you'd get</td></tr>
<tr><td style="padding:0 0 14px 0;">{one sentence}</td></tr>
<tr><td style="padding:0 0 2px 0;font-size:16px;font-weight:bold;text-decoration:underline;">Why it might not be worth it</td></tr>
<tr><td style="padding:0 0 14px 0;">{one sentence}</td></tr>
<tr><td style="padding:0 0 10px 0;font-size:13px;color:#555555;"><b>Effort:</b> {size}{ · <b>Cost change:</b> …}{ · <b>Raised again because:</b> …}</td></tr>
<tr><td style="padding:0 0 28px 0;"><a href="{STACK_URL}?sel=advisor:ADV-NNN" style="color:#1a5fb4;font-weight:bold;">Open the full idea on the Stack screen →</a></td></tr>
<!-- end per idea -->

<!-- Questions for Charles (only if any): -->
<tr><td style="padding:0 0 8px 0;font-size:16px;font-weight:bold;text-decoration:underline;">Questions for you</td></tr>
<tr><td style="padding:0 0 24px 0;"><ol style="margin:0;padding-left:20px;"><li>{question}</li></ol></td></tr>
</table>
</td></tr></table>
</body></html>
```

The plain-text `body` carries the same words in the same order, with
the group headings in capitals ("DONE FOR YOU", "IDEAS FOR YOU"), blank
lines between sections and the Stack screen URL written out.
