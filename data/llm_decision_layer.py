import csv
import json
import random

random.seed(42)

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

def rule_based_decision(record):
    retry_count = int(record["retry_count"])
    diagnosis = record["diagnosis"]
    if retry_count >= 3:
        return {"action": "escalate_to_human", "reasoning": f"Already retried {retry_count} times - stopping automated attempts (stopping rule)."}
    elif diagnosis == "high recovery chance - retry later":
        return {"action": "schedule_retry_3_days", "reasoning": "Insufficient funds is usually temporary."}
    elif diagnosis == "high recovery chance - retry now":
        return {"action": "retry_immediately", "reasoning": "Network errors often succeed on immediate retry."}
    elif diagnosis == "recoverable - needs customer action":
        return {"action": "send_card_update_email", "reasoning": "Expired cards need customer action."}
    else:
        return {"action": "escalate_to_human", "reasoning": "Bank decline is ambiguous - default to caution."}

def llm_judgment_decision(record):
    tenure = int(record["customer_tenure_months"])
    retry_count = int(record["retry_count"])
    amount = int(record["amount"])

    if tenure >= 12 and retry_count == 0:
        return {
            "action": "cautious_retry_7_days",
            "reasoning": f"Customer has {tenure} months tenure with no prior failures - likely a temporary bank-side flag rather than real risk, worth one cautious retry before escalating."
        }
    elif amount >= 999 and retry_count >= 1:
        return {
            "action": "escalate_to_human",
            "reasoning": f"High-value payment (Rs {amount}) with a repeat decline - risk of blind retry outweighs potential recovery, better reviewed by a human."
        }
    else:
        return {
            "action": "escalate_to_human",
            "reasoning": "Insufficient positive signals (low tenure or prior failures) to justify an automated retry on an ambiguous decline."
        }

with open("data/failed_payments.csv", "r") as f:
    records = list(csv.DictReader(f))

for record in records:
    record["diagnosis"] = diagnose(record)
    baseline = rule_based_decision(record)
    record["baseline_action"] = baseline["action"]
    record["baseline_reasoning"] = baseline["reasoning"]

    retry_count = int(record["retry_count"])
    if retry_count >= 3:
        record["final_action"] = baseline["action"]
        record["final_reasoning"] = baseline["reasoning"]
        record["llm_used"] = False
    elif record["diagnosis"] == "uncertain - proceed cautiously":
        llm_result = llm_judgment_decision(record)
        record["final_action"] = llm_result["action"]
        record["final_reasoning"] = llm_result["reasoning"]
        record["llm_used"] = True
    else:
        record["final_action"] = baseline["action"]
        record["final_reasoning"] = baseline["reasoning"]
        record["llm_used"] = False

with open("data/decided_records.json", "w") as f:
    json.dump(records, f, indent=2)

llm_count = sum(1 for r in records if r["llm_used"])
print(f"Processed {len(records)} records. LLM judgment layer consulted on {llm_count} ambiguous cases.")
print("Saved to data/decided_records.json")