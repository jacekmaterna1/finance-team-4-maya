# FAILURES: where the system is wrong, unsure, or could be gamed

QA Evaluator. **Updated 2026-11-20 at 12:20 CST (QA pass 2).** Every case can be reproduced with
`analysis/scripts/eval_*.py`. The numbers are in `analysis/EVAL.md`; the web-app checks are in
`analysis/QA_PASS_2.md`.

**REAL** means it happens on today's records. **REAL + MUTATION** means a real record changed in memory in a way the
data shows is common. **SYNTHETIC** means injected text or amounts, labelled as such.

**Status** is FIXED (re-tested on current code), OPEN, or BY DESIGN. The fixed cases are kept, because the
before/after is part of the evidence.

---

## Open: what a person still has to watch

### A. "Override hold" lifts a dispute hold without the account manager (REAL UI path). OPEN, sev-2
- **What happened.** On Riverside's disputed INV-25787, "Release hold" correctly refuses without the "AM confirmed"
  box and the AM's name. But the **"Override hold"** button right next to it (`_invoice.html:50-51`) lifts the same
  DISPUTE hold with any 5-character reason. We did this on Okafor & Nakamura INV-25765 with "QA: just chase them":
  HTTP 200, and the invoice moved to "Hold lifted: write or approve the message".
- **Why.** `views.py:535-536` checks the AM requirement only when `kind == "release_hold"`.
- **Impact.** $312,922 of disputed invoices can be released by one click. That defeats Maya's condition: "the hold
  should only be released once the AM agrees the dispute is settled".
- **What a person should do.** Never use Override on a dispute or cancellation. Use Release with the AM's name.
- **Fix idea.** Apply the AM check to both kinds, or hide Override when a DISPUTE or CANCELLATION hold is present.

### B. The send endpoint trusts the browser (REAL UI/API path). OPEN, sev-2
- **What happened.**
  - (1) A POST to `/collections/INV-25784/send` (Jessop, money received, HOLD, no override) was accepted and logged as
    **sent**. That is a Paidly chase recorded by the system.
  - (2) Typing `ap@okaforlegal-billing.example`, a look-alike not in contacts.csv, into the editable "To" field of
    INV-25848 was accepted.
- **Why.** `views.py:493-515` checks only the banned wording. It does not check the invoice's action or hold state,
  or whether recipients are verified. The UI hides the form for held invoices, but nothing on the server enforces it.
- **Impact.** In this demo, sends are simulated. Once sending is wired, both are wrong-chase or wrong-recipient
  incidents.
- **Fix idea.** Allow a send only for DRAFT_REMINDER or HUMAN_WRITES invoices, or after a logged override or release.
  Restrict "To" to `collections.recipients(ctx)` addresses.

### C. A partial rules save switches guardrails off (REAL API path). OPEN, sev-2
- **What happened.** A POST to `/rules` with only `fee_tolerance=25` set `top50_human_only`,
  `auto_apply_exact_ref_match` and `notify_am_before_contact` to false, and **emptied the banned-phrase list (13 → 0)**.
- **Why.** `views.py:276-300` treats a missing checkbox as False and a missing textarea as an empty list. The full
  browser form is fine. A script, an old tab or a future "quick edit" is not.
- **Also.** Priya can untick "top-50: a person writes" on her own. Policy makes that Dana's call, or the CEO's.
- **Fix idea.** Only update keys present in the form. Refuse an empty banned list. Require Dana's approval to switch
  off top-50, the banned list or the AM cc.

### D. No courtesy note before the due date (REAL). OPEN, sev-2 (policy gap; no harm done)
- **What happened.** Policy says to send a courtesy note 5 days before the due date. **16 invoices, $219,071, are due
  on 1–5 Nov and none gets one.** They show as "Next reminder at day 7". Examples: INV-25933 Whitlock (due 11-01) and
  INV-25950 Achebe + Pemberton (due 11-04, $67,968).
- **Why.** `pipeline.py:74` uses `ar_aging.days_past_due`, which the QuickBooks export floors at 0 (FACTS §1). So
  `stage_for()` never sees a negative number.
- **Impact.** The friendliest step of the policy is skipped. Late payment could follow, as could complaints from
  customers who wanted a heads-up.
- **Fix idea.** Compute days past due from `due_date` and AS_OF, and floor it only for display.

### E. Live state disappears on restart, including the demo video link (REAL, live). BY DESIGN on the free plan, but must be disclosed
- **What happened.**
  - The live audit log currently shows 0 human actions.
  - On every deploy (autoDeploy on each push) or idle spin-down, everything Priya, Dana or a reviewer did is lost:
    approvals, sends, overrides, AM releases, rules changes, chat history and the Loom link saved on /demo.
  - Instructions accepted in Direct are appended to the agent manual inside the container, then revert to the repo
    version.
- **Why.** SQLite, rules.json and the manuals live on the container's disk. `render.yaml` asks for a paid plan with a
  disk, but the live service is on the free plan.
- **Impact.** The "append-only audit log" isn't durable on live. A reviewer who approves something and returns
  later sees nothing.
- **What to do now.** Set `DEMO_VIDEO_URL` in the Render env. Commit accepted instructions. Show "demo state resets on
  restart" on the RIG.
- **For go-live.** A paid instance with a disk, or Postgres.

### F. Kingsway: one $5,100 payment, two $5,100 invoices (REAL). OPEN (the system is unsure, correctly)
- **What happened.**
  - PAY-65805 ($5,100, no memo) from Kingsway. Two overdue $5,100 invoices exist: INV-25469 (111 dpd) and INV-25852
    (19 dpd).
  - The agent proposes the oldest, the house convention (91% historically), and holds both. That is right.
  - "Already received" now counts the money once: **$78,348 (was $83,448)**. FIXED.
  - **Still open:** "Approve" on the Cash page records INV-25469 without asking Priya to choose. Approving twice
    writes two `apply` rows (`views.py:443-450`).
- **What a person should do.** Ask Kingsway which invoice the payment covers before approving. Their renewal is
  close, so tell the AM.

### G. Ticket marked "solved" while the dispute is unresolved (REAL). OPEN (by data; handled)
- **What happened.** 11 of the 14 disputed invoices ($309,000) sit on tickets marked solved, for example Riverside
  Partners INV-25787 ($60,576, "We've paused payment pending a corrected invoice").
  - The system catches all of them from the ticket text. Each hold says "marked solved but the customer said they
    won't pay", and the new contract check states whether the invoice matches the contract.
- **Residual risk.** No status field ever records "settled". Dispute holds still depend on
  `dispute_lookback_days` = 120 (`controller.py:62`). They will start dropping off silently from about late November
  unless an AM releases them first.
- **Fix idea.** Make the hold sticky until an AM releases it, with the release written to the audit log.

### H. Ambrose & Lowell held for an open high-priority PRODUCT bug (REAL). OPEN: policy-correct, arguably over-cautious
- **What happened.** Both $658 invoices are held under OPEN_ESCALATION because of T880474 (Bug, high, pending since
  08-24): "Card payments are going through ... invoices stay marked unpaid in Ledgerline". That is a bug in the
  customer's own invoicing.
  - `hold_on_open_ticket_days` is now wired in (`controller.py:68-71`), but its default was raised to 120, so a
    68-day-old ticket still holds.
  - The hold's subject renders as `'???'`, which is the real ticket subject.
- **Impact.** $1,316 not chased. Defensible, but it is the AM's call.
- **Fix idea.** Treat a product-bug escalation as a soft flag for the AM to confirm. Keep the hard hold for billing
  escalations.

### I. The keyword complaint counter said 14; the agent's read says 2 (REAL). FIXED (before/after kept for the video)
- **Before.** `COMPLAINT_RX` (`pipeline.py:13`) counted 14 "collections complaints" in 120 days.
- **Hand check of the 14:**
  - 12 are about the customers' own reminder emails, notices or invoice runs to *their* clients. Examples: T880733
    "Where do I edit the subject line on reminder emails?"; T880608 "client paid on time and still got a 'final
    notice'".
  - 1 (T880373 Highmoor) is a question about a Ledgerline charge.
  - 1 is real (T880519 Eastman).
- **After.** The agent's read gives **2**: T880519 Eastman (consumer affairs, contest the charge) and T880019 Drummond
  (chargeback for double billing). Drummond's ticket is now read regardless of age.
- **Why it matters.** Ledgerline sells invoicing software, so "reminder" and "final notice" are product words. A
  naive veto metric would have read 7x worse than reality.
- **Residual risk.** The read is still rules-based (see J). Treat 2 as a floor.

### J. Ticket reading still misses soft complaints and mis-reads some legal words (REAL). OPEN, low impact today
- **Misses.**
  - T880966 Quill & Corbin: "invoice still bills us for the full seat count ... seems one-sided". This is a soft
    dispute with no INV id and no refusal words.
  - T880624 and T880625 are borderline.
  - The estimated false-negative rate is 3% to 10% of the 498 unflagged money-related tickets.
- **False positives.** "attorney" (Studio Finch) and "solicitor" (Studio Achebe) are read as legal threats, so
  precision is 19 of 21. None of these customers has open AR today.
- **Fix idea.** Use the Claude read once Legal approves the Bedrock DPA. Only count legal words next to a threat
  verb.

### K. Same customer, two failed cards, two treatments (REAL). OPEN
- **What happened.** Quill, Mott & Co has two failed $1,632 card invoices. INV-25708 gets a card re-run; INV-25975
  gets a "your card didn't go through" email. The "card works" test runs per invoice (`pipeline.py:89-98`).
- **What a person should do.** Re-run the older invoice first. Email only if that fails.
- **Fix idea.** Decide per customer.

### L. Cash application blind spots on SYNTHETIC traps, plus a test-set defect. OPEN, low impact (traps absent from real data)
- **What happened.**
  - Bank-fee deductions and 10% short payments **with no memo ref** always end as exceptions (8 of 20 synthetic rows).
    `fee_tolerance` only applies on the reference path (`cash_app.py:111`).
  - The labels mislead: +$0.02 reads "partial or combined payment", and -$0.01 reads "looks like a bank fee".
  - For SYN-040, the matcher proposes the first pair of invoices adding up to the amount, without saying that other
    pairs fit too.
- **Test-set defect (data-analyst).** 7 of 10 synthetic "combined" rows include an invoice that had already been
  paid before the receipt date.

### M. A look-alike domain is blocked but mislabelled (SYNTHETIC). OPEN, sev-3
- **What happened.** A contact at `thornfleldconsultinggr.example` is never used, but the hold says "Billing contact
  has left". That hides a possible spoofing signal.
- **Fix idea.** Use a SUSPICIOUS_DOMAIN code routed to Dana.

### N. A banned-language block also cancels card re-runs (SYNTHETIC template injection). OPEN, sev-3
- **What happened.** When a template contains banned wording, the invoice becomes HOLD before the card re-run check
  runs. The 9 legitimate re-run proposals vanish, although no email would have gone out for them
  (`pipeline.py:80-93`).
- **Also.** "court" is now banned as a plain substring (`rules.py`, `controller.py:127-128`). No draft is affected
  today, but "courtesy" or "courteous" would be blocked. Match on word boundaries.

---

## Fixed since pass 1 (re-tested on current code)

| # | case | before | after |
|---|---|---|---|
| 1 | **Paidly with a shortened payer** (REAL + MUTATION) | `BRANDT` led to a DRAFT_REMINDER for a paid $6,324. `JESSOP` was tagged to the wrong customer (Jessop Legal), and the $62,688 top-50 invoice got a chase draft | All held: "possible payment from an unidentified payer" (`controller.py:36-43`). The fuzzy match needs ≥0.75 and a clear lead (`cash_app.py:50`) |
| 2 | **Drummond chargeback one day outside the lookback** (REAL) | A card re-run was proposed for a customer charging us back | HUMAN_WRITES with LEGAL_RISK. Card re-runs are blocked on legal threats (`pipeline.py:92-93`) |
| 3 | **"Jessop payment" memo fits 8 customers** (REAL) | Safe only because the payer name matched exactly | Shortened names now return candidates. A unique exact open amount among them is proposed at 0.6 (`cash_app.py:89-94`) |
| 4 | **Complaint wording outside the lists** (SYNTHETIC) | "will not pay", "refuse to pay", a How-to tag and a polite overcharge were all drafted | All held (strong refusals in any category, `context.py`) |
| 5 | **Reyes $51,072 held as a "dispute"** (REAL) | A "void it" question about their own client invoice | No longer flagged. Reyes's not-yet-due top-50 invoice is NO_ACTION |
| 6 | **Narrow banned list** (SYNTHETIC) | "debt collector", "legal proceedings" and "cut off" passed | Blocked, both in drafts and on the human send path |
| 7 | **Kingsway double count** (REAL) | $83,448 already received | $78,348 |
| 8 | **`hold_on_open_ticket_days` ignored** (REAL) | Not read by the engine | Wired in (`controller.py:68`). The default of 120 keeps Ambrose held (see H) |

**Strongest demo cases now:**
- **I** (14 → 2, real).
- **Fixed #1** (the BRANDT/JESSOP before/after on the Paidly guardrail).
- **A** (a dispute released with one click). Only use A once it is fixed, as a "found by QA, closed" story.
