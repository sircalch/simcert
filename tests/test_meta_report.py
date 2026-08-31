"""
Tests for SimCert multi-scale orchestration and meta-report generation.
"""

import os
import tempfile
import pytest
import numpy as np

from simcert.orchestrator import run_multiscale_audit
from simcert.meta_report import generate_simcert_meta_report
from mdcheck.core.scoring import assess_trajectory_quality
from dockcert.core.scoring import assess_docking_quality
from qmcert.core.scoring import assess_qm_quality
from adsorpqc.core.scoring import assess_adsorption_quality
from alphacert.core.scoring import assess_alphafold_quality


def test_multiscale_orchestrator():
    # 1. Mock components with stationary data
    rng = np.random.default_rng(42)
    md_stationary = 0.20 + rng.normal(0, 0.005, size=2000)
    md_rep = assess_trajectory_quality({"RMSD": md_stationary}, min_neff_pass=100.0)
    
    # Docking
    labels = np.array([1]*20 + [0]*180)
    scores = np.concatenate([rng.normal(-9.0, 0.5, 20), rng.normal(-5.0, 1.0, 180)])
    dock_rep = assess_docking_quality(labels=labels, scores=scores)
    
    # QM
    qm_rep = assess_qm_quality(metadata={"functional": "B3LYP", "basis_set": "def2-TZVP", "engine": "ORCA"}, scf_converged=True, frequencies=[100.0, 500.0])
    
    # Adsorption
    adsorp_rep = assess_adsorption_quality(metadata={"framework": "MOF-5", "adsorbate": "CH4", "temperature_k": 298.15}, pressure_isotherm=np.array([0.1, 0.5, 1.0]), loading_isotherm=np.array([1.0, 3.0, 5.0]))

    # AlphaFold
    alpha_rep = assess_alphafold_quality(metadata={"name": "Target", "engine": "AlphaFold2"}, plddt_values=[92.0]*50, pae_matrix=np.ones((50, 50))*3.0)

    # 2. Run multi-scale audit
    project_rep = run_multiscale_audit(
        project_name="Integrated In Silico Pipeline",
        md_report=md_rep,
        dock_report=dock_rep,
        qm_report=qm_rep,
        adsorp_report=adsorp_rep,
        alpha_report=alpha_rep
    )

    assert project_rep.overall_status in ["PASS", "WARNING", "FAIL"]
    assert "MDCheck" in project_rep.consolidated_methods
    assert "DockCert" in project_rep.consolidated_methods
    assert "QMCert" in project_rep.consolidated_methods
    assert "AdsorpQC" in project_rep.consolidated_methods
    assert "AlphaCert" in project_rep.consolidated_methods

    # 3. Test HTML rendering
    with tempfile.TemporaryDirectory() as tmpdir:
        html_out = os.path.join(tmpdir, "simcert_project_summary.html")
        generate_simcert_meta_report(project_rep, html_out)
        assert os.path.exists(html_out)
        assert os.path.getsize(html_out) > 1000
