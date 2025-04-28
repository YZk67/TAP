#!/usr/bin/env python3 
"""Batch-run main_TAP.py with goals and target strings from a CSV.

Usage:
    python batch_run_TAP.py --csv advbench_behaviors.csv \
                            --attack-model gpt-3.5-turbo \
                            --target-model gpt-4o \
                            --evaluator-model gpt-4o \
                            --store-folder result \
                            --branching-factor 4 \
                            --width 10 \
                            --depth 10 \
                            --n-streams 30 \
                            --start-from 5

The script writes combined stdout/stderr for each run into 'batch_results.txt'.
"""

import argparse
import csv
import subprocess
from pathlib import Path
import sys

def parse_args():
    p = argparse.ArgumentParser(description="Batch-run main_TAP.py on a CSV dataset.")
    p.add_argument("--csv", required=True,
                   help="Path to the input CSV with columns: goal,target")
    p.add_argument("--attack-model", required=True,
                   help="Name of the attack model")
    p.add_argument("--target-model", required=True,
                   help="Name of the target model")
    p.add_argument("--evaluator-model", required=True,
                   help="Name of the evaluator model")
    p.add_argument("--store-folder", default="result",
                   help="Folder to store attack results")
    p.add_argument("--branching-factor", type=int, default=4,
                   help="Branching factor for TAP search")
    p.add_argument("--width", type=int, default=10,
                   help="Width for TAP search")
    p.add_argument("--depth", type=int, default=10,
                   help="Depth for TAP search")
    p.add_argument("--n-streams", type=int, default=30,
                   help="Number of parallel streams (for main_TAP.py)")
    p.add_argument("--start-from", type=int, default=1,
                   help="Which data row to start from (1-based index, default=1)")
    p.add_argument("--output", default="batch_results.txt",
                   help="File to collect all run outputs")
    return p.parse_args()

def main():
    args = parse_args()
    csv_path = Path(args.csv)
    if not csv_path.exists():
        raise FileNotFoundError(csv_path)
    
    python_exec = sys.executable

    with csv_path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if "goal" not in reader.fieldnames or "target" not in reader.fieldnames:
            raise ValueError("CSV must contain 'goal' and 'target' columns")

        with open(args.output, "w", encoding="utf-8") as out:
            for idx, row in enumerate(reader, start=1):
                if idx < args.start_from:
                    continue  # skip rows before start_from

                goal = (row.get("goal") or "").strip()
                target_str = (row.get("target") or "").strip()

                if not goal or not target_str:
                    print(f"Skipping empty goal/target at row {idx}")
                    continue

                cmd = [
                    python_exec, "main_TAP.py",
                    "--attack-model", args.attack_model,
                    "--target-model", args.target_model,
                    "--evaluator-model", args.evaluator_model,
                    "--goal", goal,
                    "--target-str", target_str,
                    "--store-folder", args.store_folder,
                    "--branching-factor", str(args.branching_factor),
                    "--width", str(args.width),
                    "--depth", str(args.depth),
                    "--n-streams", str(args.n_streams)
                ]

                out.write(f"### Run {idx}:\n{' '.join(cmd)}\n")
                out.flush()
                print(f"[{idx}] Running command...")

                completed = subprocess.run(cmd, text=True, capture_output=True, check=False)
                out.write(completed.stdout)
                if completed.stderr:
                    out.write("\n[stderr]\n" + completed.stderr)
                out.write(f"\n=== End of Run {idx} ===\n\n")
                out.flush()

    print(f"All runs complete. Results saved to {args.output}")

if __name__ == "__main__":
    main()