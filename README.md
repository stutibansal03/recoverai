# RecoverAI — Agentic Failed-Subscription Recovery

Built for the **Razorpay AI Buildathon — Track 3: AI Revenue Recovery**

## Problem

Subscription businesses lose real revenue every time a recurring payment fails — insufficient funds, an expired card, a bank decline, or a network error. Most systems handle this badly: they either retry blindly on a fixed schedule regardless of *why* it failed, or give up and let the customer churn silently.

**RecoverAI** closes this loop: it diagnoses *why* a payment failed, decides the right recovery action for that specific situation, executes it (simulated), and reports exactly how much revenue was recovered — with every decision logged and explainable.

## Architecture


## Why this design

- **Deterministic rules handle safety-critical logic** (e.g., `retry_count >= 3 → escalate to human`) — this stopping rule is never overridden by the AI layer, by design.
- **AI judgment is used only where it adds real value** — genuinely ambiguous bank-decline cases, where multiple signals (customer tenure, retry history, payment amount) need to be weighed together rather than following one rigid rule.
- **Every decision carries its reasoning** — not bolted on after the fact, but built into the decision object from the moment it's created, satisfying the audit-trail requirement.
- **Results are never inflated** — unresolved and escalated cases are reported honestly alongside recovered ones.

## How to run

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # if applicable
python3 data/run_all.py
```

This runs the full pipeline: generates the synthetic dataset, runs diagnosis + decision logic (rule-based + AI judgment layer), simulates execution, and prints the final revenue recovery report.

## Example output


## AI vs. deterministic baseline

Of the 17 genuinely ambiguous cases (bank declines), the AI judgment layer's decision differed from the deterministic default in 10 cases — weighing signals like customer tenure and prior retry history rather than defaulting to blanket escalation. Example:

> **CUST_0000** — bank decline, 16 months tenure, 0 prior failures
> Baseline default: `escalate_to_human`
> AI judgment: `cautious_retry_7_days` — *"16 months tenure with no prior failures - likely a temporary bank-side flag rather than real risk, worth one cautious retry before escalating."*
> Outcome: not recovered this time — an honest example of a reasonable, explainable judgment call that didn't pay off.

## Data

70 synthetic failed-payment records, with failure-type distribution grounded in published subscription-payments industry data (insufficient funds and generic bank declines as the leading causes, expired cards separately accounting for 10-15%). Generated with a fixed random seed for full reproducibility.

## Limitations / next steps

- The AI judgment layer currently runs in a reproducible simulation mode rather than a live LLM API call, designed to be swapped in with minimal changes.
- Success-rate assumptions per action are estimates; a production version would calibrate these against real historical recovery data.
- Simulated results only — this project does not process real payments or claim real-world recovered revenue.
