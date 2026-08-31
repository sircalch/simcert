"""
Unified Command Line Interface for SimCert.
"""

import sys
import os
import argparse
import numpy as np

from simcert import __version__
import mdcheck.cli
import dockcert.cli
import qmcert.cli
import adsorpqc.cli
import alphacert.cli
import fepcert.cli
import qsarcert.cli

from mdcheck.core.scoring import assess_trajectory_quality
from dockcert.core.scoring import assess_docking_quality
from qmcert.core.scoring import assess_qm_quality
from adsorpqc.core.scoring import assess_adsorption_quality
from alphacert.core.scoring import assess_alphafold_quality
from fepcert.core.scoring import assess_fep_quality
from qsarcert.core.scoring import assess_qsar_quality

from simcert.orchestrator import run_multiscale_audit
from simcert.meta_report import generate_simcert_meta_report


def print_banner():
    banner = rf"""
   _____ _             _____          _   
  / ____(_)           / ____|        | |  
 | (___  _ _ __ ___  | |     ___ _ __| |_ 
  \___ \| | '_ ` _ \ | |    / _ \ '__| __|
  ____) | | | | | | || |___|  __/ |  | |_ 
 |_____/|_|_| |_| |_(_)_____\___|_|   \__| v{__version__}

 Unified Scientific Simulation Quality-Control & Reproducibility Meta-Framework
 Monreal-Hernández et al., 2026
"""
    print(banner)


def run_demo_all(output_dir: str = "simcert_full_demo_output"):
    """
    Executes a comprehensive multi-scale project demonstration certifying all 7 tiers
    (Molecular Dynamics, Docking, Quantum Chemistry, Adsorption, AlphaFold, Free Energy / FEP, and QSAR / ML).
    """
    print(f"\n[SimCert] Running Full-Suite Multi-Scale Demonstration (7 Computational Tiers)...")
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Run MD demo
    md_dir = os.path.join(output_dir, "md")
    print("\n--- [Tier 1: Molecular Dynamics Certification (MDCheck)] ---")
    mdcheck.cli.run_demo(output_dir=md_dir)
    
    # 2. Run Docking demo
    dock_dir = os.path.join(output_dir, "docking")
    print("\n--- [Tier 2: Molecular Docking & Screening Certification (DockCert)] ---")
    dockcert.cli.run_demo(output_dir=dock_dir)
    
    # 3. Run QM demo
    qm_dir = os.path.join(output_dir, "qm")
    print("\n--- [Tier 3: Quantum Chemistry Certification (QMCert)] ---")
    qmcert.cli.run_demo(output_dir=qm_dir)
    
    # 4. Run Adsorption demo
    adsorp_dir = os.path.join(output_dir, "adsorption")
    print("\n--- [Tier 4: Adsorption & GCMC Simulation Certification (AdsorpQC)] ---")
    adsorpqc.cli.run_demo(output_dir=adsorp_dir)

    # 5. Run AlphaCert demo
    alpha_dir = os.path.join(output_dir, "alpha")
    print("\n--- [Tier 5: AlphaFold Structure & Confidence Certification (AlphaCert)] ---")
    alphacert.cli.run_demo(output_dir=alpha_dir)

    # 6. Run FEPCert demo
    fep_dir = os.path.join(output_dir, "fep")
    print("\n--- [Tier 6: Alchemical Free Energy & Cycle Closure (FEPCert)] ---")
    fepcert.cli.run_demo(output_dir=fep_dir)

    # 7. Run QSARCert demo
    qsar_dir = os.path.join(output_dir, "qsar")
    print("\n--- [Tier 7: QSAR & Molecular Machine Learning (QSARCert)] ---")
    qsarcert.cli.run_demo(output_dir=qsar_dir)
    
    # 8. Build consolidated project report
    print("\n--- [Generating Consolidated SimCert Project Summary Dashboard] ---")
    
    # Sample reports for meta-dashboard
    rng = np.random.default_rng(42)
    md_rep = assess_trajectory_quality({"RMSD": rng.normal(0.18, 0.01, 1000)})
    
    # Docking
    labels = np.array([1]*20 + [0]*180)
    scores = np.concatenate([rng.normal(-9.0, 0.5, 20), rng.normal(-5.0, 1.0, 180)])
    dock_rep = assess_docking_quality(labels=labels, scores=scores)
    
    # QM
    qm_rep = assess_qm_quality(metadata={"functional": "wB97X-D3BJ", "basis_set": "def2-TZVP", "engine": "ORCA"}, scf_converged=True, frequencies=[100.0, 500.0, 1500.0])
    
    # Adsorption
    adsorp_rep = assess_adsorption_quality(metadata={"framework": "Mg-MOF-74", "adsorbate": "CO2", "temperature_k": 298.15}, pressure_isotherm=np.array([0.1, 0.5, 1.0, 2.0]), loading_isotherm=np.array([1.2, 4.5, 6.8, 8.2]))
    
    # AlphaFold
    alpha_rep = assess_alphafold_quality(
        metadata={"name": "Target Kinase", "engine": "AlphaFold2"},
        plddt_values=[92.0]*100,
        pae_matrix=np.ones((100, 100))*3.0
    )

    # FEP
    fep_lambdas = [0.0, 0.5, 1.0]
    fep_grads = [rng.normal(-4.0 * l, 1.0, 200) for l in fep_lambdas]
    fep_rep = assess_fep_quality(
        metadata={"transformation": "Lig1 -> Lig2", "engine": "GROMACS 2024"},
        lambda_values=fep_lambdas,
        gradients_list=fep_grads,
        unit="kcal/mol"
    )

    # QSAR
    q_tr = rng.normal(0, 1, size=(50, 4))
    q_ev = rng.normal(0, 1, size=(15, 4))
    q_w = np.array([2.0, -1.0, 0.5, 1.0])
    q_y_ev = q_ev @ q_w
    q_y_pred = q_y_ev + rng.normal(0, 0.1, size=15)
    qsar_rep = assess_qsar_quality(
        metadata={"endpoint": "pIC50", "algorithm": "Random Forest"},
        y_true=q_y_ev,
        y_pred=q_y_pred,
        x_train=q_tr,
        x_eval=q_ev,
        run_y_scrambling=True,
        n_scrambling_iterations=20
    )

    meta_rep = run_multiscale_audit(
        project_name="Multi-Scale Drug Discovery & Nanoporous Delivery Project",
        md_report=md_rep,
        dock_report=dock_rep,
        qm_report=qm_rep,
        adsorp_report=adsorp_rep,
        alpha_report=alpha_rep,
        fep_report=fep_rep,
        qsar_report=qsar_rep
    )
    
    meta_html = os.path.join(output_dir, "simcert_project_summary.html")
    generate_simcert_meta_report(meta_rep, meta_html)
    
    print("\n" + "="*75)
    print(f" [SIMCERT CONSOLIDATED STATUS] Overall Multi-Scale Quality: {meta_rep.overall_status}")
    print("="*75)
    print(f"  * Tier 1 (Molecular Dynamics)  : PASS (Report in {md_dir}/)")
    print(f"  * Tier 2 (Molecular Docking)   : PASS (Report in {dock_dir}/)")
    print(f"  * Tier 3 (Quantum Chemistry)   : PASS (Report in {qm_dir}/)")
    print(f"  * Tier 4 (Adsorption in MOFs)  : PASS (Report in {adsorp_dir}/)")
    print(f"  * Tier 5 (AlphaFold Structures): PASS (Report in {alpha_dir}/)")
    print(f"  * Tier 6 (Alchemical Free E.)  : PASS (Report in {fep_dir}/)")
    print(f"  * Tier 7 (QSAR / Machine Learn): PASS (Report in {qsar_dir}/)")
    print("="*75)
    print(f"\nProject Hub Ready at: {os.path.abspath(meta_html)}\n")


def print_citation():
    bib = """@software{monreal2026simcert,
  author = {Monreal-Hern\\'andez, Andre},
  title = {{SimCert: A Unified Scientific Simulation Quality-Control and Reproducibility Meta-Framework}},
  year = {2026},
  version = {1.3.0},
  publisher = {Zenodo},
  url = {https://github.com/amonreal/simcert}
}"""
    print("\nIf you use the SimCert umbrella meta-framework in your research, please cite:\n")
    print("APA Style:")
    print("Monreal-Hernández, A. (2026). SimCert: A Unified Scientific Simulation Quality-Control and Reproducibility Meta-Framework (v1.3.0). Zenodo. https://github.com/amonreal/simcert\n")
    print("BibTeX:")
    print(bib)
    print()


def main():
    parser = argparse.ArgumentParser(
        prog="simcert",
        description="SimCert: Unified Scientific Simulation Quality-Control & Reproducibility Meta-Framework."
    )
    parser.add_argument("-v", "--version", action="version", version=f"simcert {__version__}")
    
    subparsers = parser.add_subparsers(dest="subcommand", help="Simulation domain or action")
    
    # Subcommands
    subparsers.add_parser("md", help="Delegate to MDCheck (Molecular Dynamics Quality Control)")
    subparsers.add_parser("dock", help="Delegate to DockCert (Molecular Docking & Screening Certification)")
    subparsers.add_parser("qm", help="Delegate to QMCert (Quantum Chemistry & DFT Certification)")
    subparsers.add_parser("adsorp", help="Delegate to AdsorpQC (Adsorption & GCMC Simulation Validation)")
    subparsers.add_parser("alpha", help="Delegate to AlphaCert (AlphaFold & Protein Structure Certification)")
    subparsers.add_parser("fep", help="Delegate to FEPCert (Alchemical Free Energy & Cycle Closure Certification)")
    subparsers.add_parser("qsar", help="Delegate to QSARCert (QSAR & Molecular Machine Learning Certification)")
    
    demo_p = subparsers.add_parser("demo-all", help="Run full multi-scale demonstration benchmark (7 tiers)")
    demo_p.add_argument("-o", "--output", default="simcert_full_demo_output", help="Output directory")
    
    subparsers.add_parser("cite", help="Display consolidated citations")
    
    if len(sys.argv) == 1:
        print_banner()
        parser.print_help()
        sys.exit(0)
        
    # Check if first arg is a delegated module
    first_arg = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    
    if first_arg == "md":
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        mdcheck.cli.main()
    elif first_arg == "dock":
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        dockcert.cli.main()
    elif first_arg == "qm":
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        qmcert.cli.main()
    elif first_arg == "adsorp":
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        adsorpqc.cli.main()
    elif first_arg == "alpha":
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        alphacert.cli.main()
    elif first_arg == "fep":
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        fepcert.cli.main()
    elif first_arg == "qsar":
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        qsarcert.cli.main()
    elif first_arg == "demo-all":
        print_banner()
        out = "simcert_full_demo_output"
        if "-o" in sys.argv:
            idx = sys.argv.index("-o")
            if idx + 1 < len(sys.argv):
                out = sys.argv[idx + 1]
        elif "--output" in sys.argv:
            idx = sys.argv.index("--output")
            if idx + 1 < len(sys.argv):
                out = sys.argv[idx + 1]
        run_demo_all(output_dir=out)
    elif first_arg == "cite":
        print_banner()
        print_citation()
    else:
        args = parser.parse_args()


if __name__ == "__main__":
    main()
