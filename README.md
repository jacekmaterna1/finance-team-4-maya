# Ledgerline AR Operator

An AI order-to-cash team for Ledgerline's finance function. Four scoped agents run in a fixed order on every cycle:
**Cash Application** matches unapplied bank receipts to open invoices, **Account Context** builds a 360 of each
customer (tickets, NPS, usage, contract, renewal, contacts), the **Controller** holds anything that must not go out
(money already received, an open complaint, a billing-rewrite dispute, a renewal in flight, an unverified contact,
threatening wording), and **Collections** ranks overdue AR, picks the stage and tone under the collections policy and
drafts the reminder. Cash Application runs first, so a receipt that plausibly pays an invoice blocks any chase on it.

It is built for Priya, the AR specialist who runs it every morning. Every decision carries a confidence and a
plain-English reason, every human action is logged next to the agent decisions in an append-only audit trail, and
Priya can change the thresholds herself on the Rules page. Agents propose; a person approves anything that touches a
customer or the ledger. The only thing an agent does alone is apply a receipt whose amount and invoice reference both
match exactly, and Priya can undo that.

## Run locally (3 commands)

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload        # open http://127.0.0.1:8000
```

With no `GOOGLE_CLIENT_ID` set the app runs in **dev mode**: you are signed in as `dev@localhost` and a yellow
"DEV MODE: auth off" banner is shown on every page. Runs on Python 3.9+ (Render uses 3.11.9).

## Pages

| Page | What it is for |
|---|---|
| RIG `/`, `/team`, `/architecture`, `/activity`, `/maya`, `/direct`, `/buildlog`, `/agents/{slug}` | The command center: KPIs, the agent roster and humans in the loop, architecture diagram, live activity feed, the Maya thread, standing instructions and manual editing, and the paper trail. "Talk to the team" chat (bottom right) answers from the live records using rules; rule changes need an Apply click. |
| Today `/today` | Overdue balance, cash found, chases prevented, drafts awaiting approval, holds, and the collections-complaints veto counter. "Needs you today" list, largest first. |
| Cash application `/cash` | Receipts with the agent's decision (auto-applied / proposed / exception), matched invoices, difference, confidence and reasons. Approve or reject proposals; undo an auto-application. |
| Collections `/collections` | Open invoices grouped by Held / Person writes / Draft / No action. Expand a row for holds, reasons and the editable draft. Approve & send (simulated), reject, or release/override a hold with a typed reason. |
| Customers `/customers`, `/customers/{id}` | Searchable list of customers with open AR and the per-customer 360. |
| Audit trail `/audit` | Agent decisions and human actions merged, filterable by agent, CSV download. |
| Rules `/rules` | Edit thresholds (auto-apply, write-off threshold, tolerances, reminder schedule, top-50 rule, banned phrases...). Saving re-runs the agents and shows what changed. |
| About `/about` | The one-pager (`submission/ONE_PAGER.md`) and the demo video if `DEMO_VIDEO_URL` is set. |
| `/healthz` | Health check, returns `ok`. |

## Environment variables

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `GOOGLE_CLIENT_ID` | prod | unset = dev mode | Google OAuth client id. |
| `GOOGLE_CLIENT_SECRET` | prod | | Google OAuth client secret. |
| `SESSION_SECRET` | prod | random per process | Signs the session cookie. Render generates one. |
| `BASE_URL` | prod | derived from request | Public URL, e.g. `https://ledgerline-ar-operator.onrender.com`. Redirect URI is `<BASE_URL>/auth/callback`. |
| `ALLOWED_DOMAINS` | | `scaleworks.com` | Comma list. Sign-in needs Google `hd` claim = domain, email domain = domain, and a verified email. |
| `ALLOWED_EMAILS` | | | Comma list of individual addresses always allowed (still need a verified email). |
| `ANTHROPIC_API_KEY` | optional | | Enables Claude for fuzzy matching and draft text. Without it the engine uses deterministic templates. |
| `DB_PATH` | | `./ledgerline.db` | SQLite file for human actions. |
| `RULES_PATH` | | `./rules.json` | JSON file holding the rules Priya edits. |
| `DATA_DIR` | | `./data` | Data-room CSVs. |
| `MANUALS_DIR` | | `app/engine/manuals` | Agent operating manuals (edited on Direct the team). |
| `RIG_CHAT_AI` | | off | `on` lets Claude rephrase chat answers (also needs `ANTHROPIC_API_KEY` and `use_claude`). |
| `DEMO_VIDEO_URL` | | | Loom, YouTube or Google Drive link; embedded on `/about`. |

## Deploy to Render

1. Push the repo to GitHub (the `data/` folder must be included; the engine reads it at start-up).
2. Render dashboard → **New → Blueprint** → pick the repo. `render.yaml` creates one Python web service
   (Python 3.11.9, `pip install -r requirements.txt`, `uvicorn app.main:app`, health check `/healthz`).
3. Fill in the `sync: false` variables: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `BASE_URL`, `ALLOWED_EMAILS`,
   `ANTHROPIC_API_KEY`, optionally `DEMO_VIDEO_URL`.
4. The blueprint mounts a 1 GB disk at `/var/data` (`DB_PATH=/var/data/ledgerline.db`,
   `RULES_PATH=/var/data/rules.json`). **Persistent disks need a paid instance.** On the free plan, delete the
   `disk:` block: the app still works, but human actions and rule edits reset on each deploy or restart. That is
   acceptable for a demo.

## Google OAuth client

1. Google Cloud Console → APIs & Services → **OAuth consent screen**: choose *External* (so allow-listed personal
   accounts can sign in) or *Internal* if every user is in one Workspace. Scopes: `openid`, `email`, `profile`.
2. **Credentials → Create credentials → OAuth client ID → Web application.**
3. Authorized JavaScript origin: `<BASE_URL>`. Authorized redirect URI: **`<BASE_URL>/auth/callback`**
   (add `http://localhost:8000/auth/callback` too if you want to test real sign-in locally).
4. Put the client id and secret in Render's environment, never in the repo.

## Known limitation

During the challenge, Maya only exists in the Scaleworks web chat, so an operator (Jacek's Claude Code session driving
his browser) carries approved questions to her and posts her replies back to the RIG (via `/api/maya/*`). When the
challenge closes, the Maya desk keeps working for proposing and approving questions, but nothing reaches Maya without
that operator. **Recommendation to Scaleworks:** expose Maya as an MCP server (or webhook) so the RIG can connect to
her directly, with no operator.

## Simulated vs real

| Real | Simulated |
|---|---|
| The data-room records (invoices, payments, AR aging, customers, contacts, contracts, tickets, NPS, usage, policy). | **No email is ever sent.** "Approve & send" records the approved text and marks it sent in the audit trail. |
| Every agent decision, confidence and reason, computed from those records. | **No ledger is written.** Approving a cash application or undoing an auto-application is recorded as an action only. |
| Human actions, rule changes and the audit trail (stored in SQLite). | Anything the data room lacks and the engine had to generate is labelled SYNTHETIC where it appears. |
