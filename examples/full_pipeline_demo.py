"""
Full pipeline multi-scale demonstration for SimCert.
"""

import os
from simcert.cli import run_demo_all


def main():
    print("Executing full multi-scale pipeline demo for SimCert...")
    out_dir = "full_pipeline_output"
    run_demo_all(output_dir=out_dir)
    print(f"\nAll tiers certified! Open {os.path.abspath(os.path.join(out_dir, 'simcert_project_summary.html'))}")


if __name__ == "__main__":
    main()
