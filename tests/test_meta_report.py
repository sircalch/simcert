"""
Tests for multi-scale meta-report orchestration in SimCert.
"""

import os
import tempfile
import numpy as np
import pytest

from mdcheck.core.scoring import assess_trajectory_quality
from dockcert.core.scoring import assess_docking_quality
from qmcert.core.scoring import assess_qm_quality
from adsorpqc.core.scoring import assess_adsorption_quality
from alphacert.core.scoring import assess_alphafold_quality
from fepcert.core.scoring import assess_fep_quality
from qsarcert.core.scoring import assess_qsar_quality
from catcert.core.scoring import assess_slab_quality
from catcert.core.surface_energy import calculate_surface_energy_convergence
from nebcert.core.scoring import assess_reaction_pathway_quality
from nebcert.core.neb_profile import calculate_neb_profile_analysis
from nebcert.core.ts_frequency import verify_ts_frequency_and_irc
from nebcert.core.tst_kinetics import calculate_eyring_tst_rates
from nebcert.core.tunneling import calculate_quantum_tunneling_corrections

from simcert.orchestrator import run_multiscale_audit
from simcert.meta_report import generate_simcert_meta_report


def test_multiscale_orchestrator():
    rng = np.random.default_rng(42)

    # 1. MD
    md_rep = assess_trajectory_quality({"RMSD": rng.normal(0.18, 0.01, 1000)})
    
    # 2. Docking
    labels = np.array([1]*10 + [0]*90)
    scores = np.concatenate([rng.normal(-9.0, 0.5, 10), rng.normal(-5.0, 1.0, 90)])
    dock_rep = assess_docking_quality(labels=labels, scores=scores)
    
    # 3. QM
    qm_rep = assess_qm_quality(
        metadata={"engine": "ORCA", "functional": "B3LYP"},
        scf_converged=True,
        frequencies=[200.0, 800.0, 1600.0]
    )
    
    # 4. Adsorption
    adsorp_rep = assess_adsorption_quality(
        metadata={"framework": "HKUST-1", "adsorbate": "CH4"},
        pressure_isotherm=np.array([0.1, 0.5, 1.0, 2.0]),
        loading_isotherm=np.array([1.0, 3.5, 5.0, 6.2])
    )

    # 5. AlphaFold
    alpha_rep = assess_alphafold_quality(
        metadata={"name": "Protein", "engine": "AlphaFold2"},
        plddt_values=[85.0]*50,
        pae_matrix=np.ones((50, 50))*2.5
    )

    # 6. FEP
    fep_rep = assess_fep_quality(
        metadata={"transformation": "Lig1 -> Lig2", "engine": "GROMACS"},
        lambda_values=[0.0, 0.5, 1.0],
        gradients_list=[rng.normal(-3.0*l, 1.0, 200) for l in [0.0, 0.5, 1.0]],
        unit="kcal/mol"
    )

    # 7. QSAR
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

    # 8. Catalysis
    cat_se = calculate_surface_energy_convergence(
        slab_energies_ev=[-72.22, -96.42, -120.61],
        n_atoms_list=[12, 16, 20],
        layer_counts=[3, 4, 5],
        surface_area_ang2=27.60,
        bulk_energy_per_atom_ev=-6.045
    )
    cat_rep = assess_slab_quality(
        metadata={"surface": "Pt(111)", "functional": "PBE-D3", "software": "VASP"},
        surface_energy_res=cat_se
    )

    # 9. NEB / Kinetics
    neb_calc = calculate_neb_profile_analysis(
        energies_ev=[0.0, 0.05, 0.15, 0.23, 0.10, -0.25, -0.62],
        coordinates_s_ang=[0.0, 0.4, 0.8, 1.2, 1.6, 2.0, 2.4]
    )
    neb_ts = verify_ts_frequency_and_irc([-1250.0, 120.0, 300.0], irc_confirmed=True)
    neb_tst = calculate_eyring_tst_rates(neb_calc.e_forward_barrier_ev)
    neb_tun = calculate_quantum_tunneling_corrections(1250.0, neb_calc.e_forward_barrier_ev, neb_calc.e_reverse_barrier_ev)
    neb_rep = assess_reaction_pathway_quality(
        metadata={"reaction": "CH4 + OH -> CH3 + H2O", "functional": "wB97X-D3", "software": "ORCA"},
        neb_res=neb_calc,
        ts_freq_res=neb_ts,
        tst_res=neb_tst,
        tunneling_res=neb_tun
    )

    meta_rep = run_multiscale_audit(
        project_name="Complete 9-Tier Molecular Investigation",
        md_report=md_rep,
        dock_report=dock_rep,
        qm_report=qm_rep,
        adsorp_report=adsorp_rep,
        alpha_report=alpha_rep,
        fep_report=fep_rep,
        qsar_report=qsar_rep,
        cat_report=cat_rep,
        neb_report=neb_rep
    )

    assert meta_rep.overall_status in ["PASS", "WARNING"]
    assert "MDCheck" in meta_rep.consolidated_methods
    assert "DockCert" in meta_rep.consolidated_methods
    assert "QMCert" in meta_rep.consolidated_methods
    assert "AdsorpQC" in meta_rep.consolidated_methods
    assert "AlphaCert" in meta_rep.consolidated_methods
    assert "FEPCert" in meta_rep.consolidated_methods
    assert "QSARCert" in meta_rep.consolidated_methods
    assert "CatCert" in meta_rep.consolidated_methods
    assert "NEBCert" in meta_rep.consolidated_methods

    with tempfile.TemporaryDirectory() as tmpdir:
        out_html = os.path.join(tmpdir, "simcert_project_summary.html")
        generate_simcert_meta_report(meta_rep, out_html)
        assert os.path.exists(out_html)
        assert os.path.getsize(out_html) > 1000
