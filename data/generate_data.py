import csv
import random

random.seed(42)

failure_types = ["insufficient_funds", "expired_card", "bank_decline", "network_error"]
weights = [0.35, 0.20, 0.30, 0.15]

records = []

for i in range(70):
    record = {
        "customer_id": f"CUST_{i:04d}",
        "failure_reason": random.choices(failure_types, weights=weights)[0],
        "amount": random.choice([199, 499, 999, 1999]),
        "retry_count": random.choice([0, 0, 0, 1, 2]),
        "customer_tenure_months": random.randint(1, 36),
    }
    records.append(record)

with open("data/failed_payments.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)

print("Done! Created", len(records), "records.")