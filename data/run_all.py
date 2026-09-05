import subprocess

print("Running RecoverAI pipeline...\n")
subprocess.run(["python3", "data/generate_data.py"])
subprocess.run(["python3", "data/llm_decision_layer.py"])
subprocess.run(["python3", "data/report.py"])
print("\nPipeline complete.")