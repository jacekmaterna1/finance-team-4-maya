# Decisions

## D1 — Build team runs in Claude Code, not Cowork scheduled tasks (pre-start)
- Options: Cowork scheduled tasks; Claude Code with subagents.
- Choice: Claude Code. Subagents with scoped tools (test-steward, data-analyst, builder, qa-evaluator) running in parallel.
- Why: the hand-in is a working tool plus a repo plus the full AI working. Claude Code runs code, keeps a git history,
  deploys (Render/GitHub connectors) and stores every session transcript for the "your working" submission.
  Scheduled tasks suit recurring knowledge work, not a one-day build.
- Note: the *product's* agents (Cash App, Context, Collections, Controller) run on the Claude API inside the app on
  Render. That is separate from the build team.

## D2 — One process, many agents (pre-start, LOCKED by Jacek 2026-11-20)
- Options: (a) a broad "AI finance department" touching FIN-1..7; (b) one process end to end.
- Jacek first wanted (a), "solve all the finance problems under 1 team". After re-reading the brief he switched to (b).
  Maya's answers in hour 2 can change the scope or the guardrails, but not the process unless she gives strong evidence against it.
- Choice: (b) **Collections (FIN-1) with Cash Application (FIN-2) as the feeder**, run by a 4-agent team.
- Why: the brief says "Pick one", "one thing working well than five things sketched". Dana's quote and the board's
  concern point at cash. The two processes are causally linked: customers get chased for invoices already paid,
  or chased during open complaints.
- Rejected for now: FIN-3/4/7. They are valuable, but they are reporting outputs that a person still has to interpret,
  so the "changes the job" story is weaker. They go in "with more time" as the next agents to add.

## D3 — Nothing built before the timer (pre-start)
- Pre-start work is limited to reading the public brief, planning and setting up the team. We disclose this session in the submission.

## D4 — Design changes from Maya's first answer (T+0:05)
- Paidly failure → cash application is a hard gate before any chase. Test case #1 is "customer already paid by wire".
- Primary user is **Priya Nair (AR Specialist)**, not Dana. Every hold or draft explains itself, and Priya can edit rules and thresholds in the UI.
- Autonomy is limited to exact amount + invoice-reference matches. Write-off threshold is $0 until Dana sets it.
- No threatening language. The 45-day suspension template is retired, and the Controller blocks suspension/legal words without VP Finance sign-off.

## D5 — Stack (T+0:05)
- Python FastAPI + Jinja server-rendered pages. Deterministic engine in plain Python; Claude API for reading memos and ticket text and for drafting emails, with results cached so the demo is fast and repeatable. Falls back to templates if no API key is set.
- Google SSO restricted to the scaleworks.com domain plus Jacek's emails. Render web service. The data room CSVs ship in the repo (all fictional).

## D6 — Ticket status is not trusted; the agent reads the text (T+0:06 to T+0:11)
- Options: (a) take Zendesk status at face value (only open tickets block a chase); (b) read the text of every recent ticket for the customer, whatever its status.
- Choice: (b). The Account Context agent reads ticket text. Heuristic rules (refusal, legal, cancellation phrases plus invoice references) run now. Claude reads the text when ANTHROPIC_API_KEY is present. Claude's answers are cached to disk (`app/engine/llm_cache.json`), so the demo gives the same result on every run and the deployed app doesn't call the API on each page load.
- Why: at T+0:06 we found disputes sitting in tickets marked "solved" where the customer still refuses to pay (Riverside Partners $60.6k, Westbrook $47.9k, Okafor & Nakamura $46.8k), plus a cancellation notice (Mercer & Banerjee) and a chargeback/consumer-affairs threat (Eastman Engineering). Many tickets are also about invoices customers send *their own* clients in Ledgerline, which must not block a chase. Telling those apart is a reading job: it suits the LLM, not exact matching.
- Evidence: $263,964 of the $633,245 overdue is disputed in support (T+0:12 run). Code: `app/engine/context.py` (`heuristic_read`, `claude_read`), `app/engine/llm.py`.
- Risk, stated honestly: the regex rules are a fallback and will miss disputes that are phrased differently. Accuracy of rules vs. Claude still has to be measured by qa-evaluator.

## D7 — An ambiguous payment holds every candidate invoice, not just the proposed one (T+0:11)
- Options: (a) hold only the invoice the agent proposes (oldest first, the house convention); (b) hold every open invoice the payment could cover.
- Choice: (b). Kingsway Engineering Group paid $5,100 on 29 Oct (PAY-65805) with no reference, and two $5,100 invoices are open (INV-25469, 111 days overdue, and INV-25852). The agent proposes the oldest and lists the other as an alternative, and the Controller holds both until Priya confirms.
- Why: whichever invoice it is, the customer has paid one of them. Chasing the "other" one is the Paidly failure that got the last tool switched off. Holding a second invoice for a day costs little; chasing a paid invoice costs trust.
- Evidence: `app/engine/cash_app.py` (alternatives list), `app/engine/pipeline.py` (candidate and alternative invoices both feed the money-received hold); `analysis/FACTS.md` (PAY-65805 labelled ambiguous; oldest-first is the convention 91% of the time).

## D8 — Failed-card re-runs: the system proposes, Priya approves each one (T+0:17)
- Options: (a) re-run a failed charge automatically when the same customer's later card charges went through; (b) propose the re-run and have Priya approve each one; (c) leave failed cards out of scope.
- Choice: (b). The Collections agent proposes a re-run, with the evidence that the card now works, and Priya approves or rejects each one. Making it automatic is Dana's call, not ours.
- Why: Maya (Exchange 2): "Charging a customer's card without a person looking is exactly the kind of thing that ends up in the CEO's inbox, and Dana owns the call on whether that ever changes." Charging money is customer-facing and hard to undo, so it stays with a person.
- Evidence: 10 of the 16 failed-card invoices belong to customers whose later card charges succeeded (engine run, T+0:15). Northgate's $799 is written off automatically by policy at 150 days, tomorrow. That goes to Dana as a decision today, as Maya asked.
- Status at 11:30: **decided, not built.** No re-run proposal exists in `app/` yet. The current build drafts a card-failed reminder and warns at 140 days (`card_writeoff_warning_days`).
- Update, later at 11:30 (JOURNAL): the main thread built 10 card re-run proposals that Priya approves one at a time, and 2 "decisions for Dana today" (Northgate $799, Hollis Nair $517). At 11:40 we stopped proposing a re-run when a chargeback is threatened (Drummond, D14).

## D9 — Priya gets a short Slack-style morning digest that links to the queue (T+0:17)
- Options: (a) Priya logs into the tool's morning queue; (b) a Slack or email digest that links to the queue.
- Choice: (b), with the queue staying the place where she approves. The digest says how many drafts, holds, card re-runs and decisions are waiting, and links to each.
- Why: Maya: "I believe Priya lives in Slack and would rather get a short morning digest that links to the queue than log into another tool." Maya's own success test is whether Priya is still using it in a month (Exchange 1), so we go to where Priya already works.
- Open: Maya told us to ask Priya directly. Not yet asked. For the demo, the digest is a generated message (shown in the app or posted to a test webhook). No real Slack workspace is connected.
- Status at 11:30: **decided, not built.** Update, later at 11:30 (JOURNAL): the main thread built a Slack-style morning digest. Priya has still not been asked. Maya's Exchange 4 asks for a 30-minute walkthrough with her before Monday, which is the moment to ask.

## D10 — Disputes go to the account manager; a dispute hold is released only on AM confirmation (T+0:17)
- Options: (a) route disputed invoices to the AM automatically with the ticket summary; (b) finance owns the fix with support and the AM is just informed.
- Choice: (a) for ownership of the customer conversation. Finance and support still fix the billing error together. A DISPUTE hold can only be released once the AM confirms it is settled, and the release records who confirmed.
- Why: Maya: "the AMs own the relationship and are walking into renewal calls blind." $312k of overdue is disputed, mostly in tickets marked "solved", so the AM is the one person who can confirm the customer actually agrees it is fixed.
- Evidence: 14 disputed invoices / $309k, where engine and analyst agree exactly (T+0:14), plus Eastman Engineering's chargeback threat. 11 of the 14 have a "solved" ticket and an uncorrected invoice (`analysis/FACTS.md`).
- Status at 11:30: **decided, not built.** Today any signed-in user can release a hold by typing a reason (`app/web/templates/_invoice.html`, `app/store.py`). The gate needs an "AM confirmed" field, or AM-only release for DISPUTE holds.
- Update, later at 11:30 (JOURNAL): the main thread built dispute routing to the AM, with release only on AM confirmation. The test-steward has not yet checked this against the deployed build.

## D11 — AI is off by default until Legal signs a DPA; Bedrock preferred; only ticket text and invoice facts sent (T+0:18)
- Options: (a) call the Anthropic API directly now; (b) Anthropic API under Anthropic's commercial terms plus DPA, after Legal review; (c) Claude via Amazon Bedrock under Ledgerline's existing AWS agreement, after Legal sign-off; (d) no LLM at all.
- Choice: (c) preferred, (b) as the alternative. Until Legal signs off, the AI is off: `use_claude` defaults to False. Holds and matching run on rules, and drafts come from the policy templates.
- Why: Maya (Exchange 2): "Legal won't let customer ticket content or financial data go to a new vendor without a data processing agreement." Ledgerline already hosts on AWS, so Bedrock adds no new vendor. Under Anthropic's commercial terms API data is not used for training, and Bedrock does not share data with the model provider. Both claims are as stated in Exchange 3; Legal still has to review.
- What it costs: with the AI off, the ticket reading falls back to rules. That works on this data because the engine now matches the analyst's 14 disputes exactly, but phrasing the rules don't know will be missed. The "reading" job that justified the LLM (D6) only switches on after Legal approves. The demo must say this plainly.
- Evidence: `app/engine/rules.py` (`"use_claude": False`), `app/engine/llm.py` (`LLM_PROVIDER=bedrock` uses `anthropic.AnthropicBedrock()`). The cache in D6 means demo runs with the AI on make no live calls.
- Gap found at 11:30: the promise is "only ticket text and invoice facts, never bank details". No bank fields are sent. But the drafting prompt (`app/engine/collections.py`) also sends customer name, plan, last NPS, usage trend, renewal date and the contact's first name. Either trim it or describe the scope to Maya accurately. Small inconsistency too: `context.py` and `collections.py` still use `rules.get("use_claude", True)` as a fallback. That is harmless while `load_rules()` merges the defaults, but should be `False`.
- Resolved at 11:31 (JOURNAL): the drafting prompt now sends only invoice facts, with names masked, and emails and phone numbers are removed from ticket text. `submission/LEGAL_NOTE.md` describes exactly that, and Exchange 4 told Maya the same.

## D12 — GitHub through the connector, plus a browser upload for the data zip (T+0:29)
- Options: (a) push over SSH from the terminal; (b) the GitHub connector; (c) the connector for code, plus GitHub's web upload for files it can't carry.
- Choice: (c). Repo `jacekmaterna1/finance-team-4-maya`, created through the GitHub connector. The 6MB data-room zip went up through GitHub's web upload in Jacek's Chrome, and the app unpacks it at start-up.
- Why: Jacek preferred the connector to setting up SSH keys. The connector can't carry a 6MB file.
- Cost: the repo's history is connector commits plus one browser upload, not a normal local `git push` history. The README must say how the data gets unpacked, so that "runs in minutes" holds for a reviewer.

## D13 — Render free plan to start (T+0:29)
- Options: free plan; Starter (paid, always on).
- Choice: free plan (ledgerline-finance-rig, Virginia): https://ledgerline-finance-rig.onrender.com.
- Why: no charge without Jacek's OK.
- Risk: free services sleep when idle and take a while to wake, which a reviewer may read as "broken". **We recommend Starter before reviewers use the link.** That is Jacek's call, and it costs money. Also check that the SQLite audit log is still there after a restart: free instances have no persistent disk.

## D14 — Fix the severity-1 failure by over-holding, not by guessing harder (T+0:30, confirmed by Maya T+0:32)
- Problem: when a bank shortened the payer name ("BRANDT" for Brandt & Lowell CPAs, "JESSOP"), a weak fuzzy match failed to tie the payment to a customer, and the tool would have chased Brandt for $6,324 they had already paid. That is the Paidly failure, and 416 past receipts arrived with names shortened like that.
- Options: (a) better fuzzy name matching, so it assigns the customer more often; (b) when the payer can't be identified, hold every overdue invoice of the same amount until Priya names the payer; (c) both.
- Choice: (b) now. A single weak fuzzy match no longer assigns a customer.
- Why: a wrong match puts money on the wrong account, and a missed match chases a paid customer. Both are worse than an unnecessary hold, which costs Priya a minute. Maya (Exchange 4): "Over-holding is the right way to be wrong. Reyes costs Priya a minute, but a BRANDT-style chase would cost us a customer."
- Evidence: `analysis/EVAL.md` and `analysis/FAILURES.md` (severity-1 finding, 11:36). Replaying BRANDT, JESSOP and KINGSWAY after the fix drafts no chase (11:40).
- Cost and how we watch it: more holds, including false ones such as Reyes Consulting asking about their own client's invoice. **Hold-override rate** (how often Priya overrides a hold) is now a RIG metric, and Maya wants that number in a month. If it is high, (a) is the next step.

## D15 — Write to Maya only for a Confirmation or Intel (Jacek, T+0:25)
- Options: (a) keep Maya updated at each milestone; (b) write only when we need a decision she or Dana owns (Confirmation) or facts the data room can't give (Intel).
- Choice: (b). Every draft starts with `Purpose: Confirmation` or `Purpose: Intel`, and adds only as much context as the ask needs.
- Why: Maya has 60 messages for the day and acts as a real COO. Status updates use up her attention and give the reviewers nothing. What we ask her is part of what gets graded.
- Effect: Draft 4 (an "app is live" update) was put on hold at T+0:32. Exchange 4 was a pure Confirmation and got the go-live decision. Messages used: 5 of 60, target 12 or fewer.

## D16 — Stay on Render's free plan (Jacek, T+1:18)
- Options: Starter + 1 GB disk (~$7.25/month, state persists) vs free (state wiped on restart or after 15 idle minutes).
- Choice: free.
- Mitigation: the courier writes every message sent to Maya and her verbatim reply into trail/MAYA_QA.md and pushes, so the RIG's Maya thread (rendered from the trail) stays durable. Desk approvals are ephemeral, so Jacek approves right before the courier collects the queue, and nothing is deployed between approval and send.

## D17 — Upgraded Render to a paid instance with a 1 GB disk (Jacek, ~T+2:15; supersedes D16)
- Why: the free plan slept after 15 idle minutes ("the app is down"), and every deploy wiped the Maya desk's state.
- Done: Jacek upgraded the instance and added the disk at /var/data. Claude Code set DB_PATH=/var/data/ledgerline.db and RULES_PATH=/var/data/rules.json.
- Verified: wrote a test chat entry, restarted the service, and the entry was still in Activity afterwards. The Maya desk showed 6 proposed questions at 4 of 60 used.
- The courier still mirrors every Maya exchange into trail/MAYA_QA.md for the paper trail.
