import subprocess
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
scripts = [
    "01_financial_model_advanced.py",
    "02_scenario_and_sensitivity.py",
    "03_generate_advanced_figures.py",
    "04_v2_risk_carbon_benchmark.py",
]

for script in scripts:
    print(f"\nRunning {script}...")
    subprocess.run([sys.executable, str(ROOT / "src" / script)], check=True)

print("\nAll ORC V2 outputs generated.")
