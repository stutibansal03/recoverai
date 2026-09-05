import csv

with open("data/failed_payments.csv", "r") as f:
    reader = csv.DictReader(f)
    records = list(reader)

def diagnose(record):
    reason = record["failure_reason"]
    if reason == "insufficient_funds":
        return "high recovery chance - retry later"
    elif reason == "network_error":
        return "high recovery chance - retry now"
    elif reason == "expired_card":
        return "recoverable - needs customer action"
    else:
        return "uncertain - proceed cautiously"

for record in records:
    record["diagnosis"] = diagnose(record)

print("Loaded", len(records), "diagnosed records.")
print(records[0])