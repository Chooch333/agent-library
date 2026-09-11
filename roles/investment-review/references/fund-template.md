# Fund Template

Reference for `roles/investment-review/SKILL.md` — used when the output type is **Fund**: one 13F filer, current quarter vs prior quarter (or two quarters Charles names).

| § | Section | Content rule |
|---|---|---|
| F0 | Header | Filer · CIK · Before quarter → After quarter · filed dates · source ladder used |
| F1 | Bottom line | One paragraph: what the manager did and the read-through for Charles |
| F2 | Summary strip | Before vs After: reported value · position count · top-10 concentration. Counts: New · Exited · Increased · Decreased · Unchanged. Verified from SEC cover pages |
| F3 | Before / After comparison | The centerpiece table — spec below |
| F4 | Portfolio shape | Theme concentration before vs after; turnover estimate |
| F5 | Read-through | Themes leaning in/out; named confirmations or conflicts with Charles's theses |
| F6 | Book overlap | Shared names and their sleeves |
| F7 | Study candidates | Names worth a Study — no verdicts |
| F8 | 13F limits applied | Days of lag; long-only US; options shown as underlying; no cash, shorts, non-US, or directly held crypto |
| F9 | Checkpoints | Next filing due date; any 13D/G to watch |
| F10 | Sources + completeness | |

## F3 spec — Before / After comparison table

**Columns:** Ticker · Before shares · Before value · Before % of portfolio · After shares · After value · After % of portfolio · Share change · Signal

**Grouped by status, in this order, each with a subtotal row:**
1. **New** — zero shares before, shares after
2. **Exited** — shares before, zero after
3. **Increased** — more shares after
4. **Decreased** — fewer shares after
5. **Unchanged** — identical share count (value change is price-only). For filers with 50+ positions, show only unchanged positions in the After top 20 by value, plus a "+N other unchanged" line.

Within each group, sort by After value (Exited: by Before value).

**Rules**
- Status comes from share count only. Dollar value never sets status.
- Split-adjust Before shares when a split happened between quarters; note it in the Signal column.
- Options (PUT/CALL) get their own rows, labeled, never merged with common stock.
- Signal values: *Real capital* (share count moved) · *Price-only* (unchanged shares) · *Disclosure artifact* (position newly reportable — shown under New but flagged).
- If one large New position distorts After weights, flag "denominator distortion" on the summary strip and don't read weight changes as conviction changes.

**Illustrative layout (placeholder tickers, not real data)**

| Ticker | Before sh | Before $ | Before % | After sh | After $ | After % | Δ shares | Signal |
|---|---|---|---|---|---|---|---|---|
| **New** | | | | | | | | |
| AAA | — | — | — | 1.2M | $190M | 4.1% | new | Real capital |
| **Exited** | | | | | | | | |
| BBB | 800K | $95M | 2.3% | — | — | — | exited | Real capital |
| **Increased** | | | | | | | | |
| CCC | 500K | $60M | 1.5% | 900K | $120M | 2.6% | +80% | Real capital |
| **Decreased** | | | | | | | | |
| DDD | 3.0M | $410M | 10.0% | 1.1M | $170M | 3.7% | −63% | Real capital |
| **Unchanged** | | | | | | | | |
| EEE | 2.0M | $300M | 7.3% | 2.0M | $360M | 7.8% | 0% | Price-only |
