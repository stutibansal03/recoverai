import json
import random

random.seed(42)

with open("data/decided_records.json", "r") as f:
    records = json.load(f)

def simulate_outcome(record):
    action = record["final_action"]
    amount = int(record["amount"])

    if action == "retry_immediately":
        success = random.random() < 0.80
    elif action == "schedule_retry_3_days":
        success = random.random() < 0.65
    elif action == "cautious_retry_7_days":
        success = random.random() < 0.55
    elif action == "send_card_update_email":
        success = random.random() < 0.55
    else:
        success = False

    if action == "escalate_to_human":
        return "escalated"
    elif action == "send_card_update_email":
        return "recovered" if success else "requires_customer_action"
    elif success:
        return "recovered"
    else:
        return "not_recovered"

total_at_risk = 0
total_recovered = 0
action_counts = {}
outcome_counts = {}

for record in records:
    amount = int(record["amount"])
    total_at_risk += amount
    outcome = simulate_outcome(record)
    record["outcome"] = outcome

    if outcome == "recovered":
        total_recovered += amount

    action = record["final_action"]
    action_counts[action] = action_counts.get(action, 0) + 1
    outcome_counts[outcome] = outcome_counts.get(outcome, 0) + 1

recovery_rate = (total_recovered / total_at_risk) * 100

with open("data/audit_trail.json", "w") as f:
    json.dump(records, f, indent=2)

print("=" * 50)
print("RECOVERAI - REVENUE RECOVERY REPORT (SIMULATED)")
print("=" * 50)
print(f"Payments processed:     {len(records)}")
print(f"Revenue at risk:        Rs {total_at_risk}")
print(f"Revenue recovered:      Rs {total_recovered}")
print(f"Recovery rate:          {recovery_rate:.1f}%")
print()
print("Actions taken:")
for action, count in action_counts.items():
    print(f"  {action}: {count}")
print()
print("Outcomes:")
for outcome, count in outcome_counts.items():
    print(f"  {outcome}: {count}")
print("=" * 50)
print("Full audit trail saved to data/audit_trail.json")