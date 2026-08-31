"""
Multi-scale simulation project orchestrator for SimCert.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import os

from mdcheck.core.scoring import SimulationQualityReport
from dockcert.core.scoring import DockingValidationReport
from qmcert.core.scoring import QMCertValidationReport
from adsorpqc.core.scoring import AdsorptionValidationReport
from alphacert.core.scoring import AlphaFoldValidationReport
from fepcert.core.scoring import FEPValidationReport
from qsarcert.core.scoring import QSARValidationReport
from catcert.core.scoring import SlabQualityReport
from nebcert.core.scoring import ReactionPathwayReport


@dataclass
class SimCertProjectReport:
    project_name: str
    overall_status: str  # 'PASS', 'WARNING', 'FAIL'
    md_report: Optional[SimulationQualityReport]
    dock_report: Optional[DockingValidationReport]
    qm_report: Optional[QMCertValidationReport]
    adsorp_report: Optional[AdsorptionValidationReport]
    alpha_report: Optional[AlphaFoldValidationReport]
    fep_report: Optional[FEPValidationReport]
    qsar_report: Optional[QSARValidationReport]
    cat_report: Optional[SlabQualityReport]
    neb_report: Optional[ReactionPathwayReport]
    consolidated_methods: str
    consolidated_bibtex: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def run_multiscale_audit(
    project_name: str = "Multi-Scale Computational Investigation",
    md_report: Optional[SimulationQualityReport] = None,
    dock_report: Optional[DockingValidationReport] = None,
    qm_report: Optional[QMCertValidationReport] = None,
    adsorp_report: Optional[AdsorptionValidationReport] = None,
    alpha_report: Optional[AlphaFoldValidationReport] = None,
    fep_report: Optional[FEPValidationReport] = None,
    qsar_report: Optional[QSARValidationReport] = None,
    cat_report: Optional[SlabQualityReport] = None,
    neb_report: Optional[ReactionPathwayReport] = None
) -> SimCertProjectReport:
    """
    Consolidates validation metrics across 9 computational tiers into a single executive report.
    """
    statuses = []
    methods_parts = []
    bib_parts = []

    if md_report:
        statuses.append(md_report.overall_status)
        methods_parts.append(
            f"Molecular dynamics trajectories were validated for statistical equilibration and convergence using MDCheck v1.0.0 (Monreal-Hernández, 2026). Status: {md_report.overall_status}."
        )
        bib_parts.append("""@software{monreal2026mdcheck,
  author = {Monreal-Hern\\'andez, Andre},
  title = {{MDCheck: Automated Statistical Convergence, Equilibration Detection, and Multi-Replica Reproducibility Assessment for Molecular Dynamics Simulations}},
  year = {2026},
  version = {1.0.0},
  publisher = {Zenodo},
  url = {https://github.com/amonreal/mdcheck}
}""")

    if dock_report:
        statuses.append(dock_report.overall_status)
        methods_parts.append(
            f"Molecular docking pose fidelity and screening early enrichment were certified using DockCert v1.0.0 (Monreal-Hernández, 2026). Status: {dock_report.overall_status}."
        )
        bib_parts.append("""@software{monreal2026dockcert,
  author = {Monreal-Hern\\'andez, Andre},
  title = {{DockCert: Automated Quality-Control, Early Enrichment Metrics, Symmetry-Corrected RMSD, and Reproducibility Assessment for Molecular Docking}},
  year = {2026},
  version = {1.0.0},
  publisher = {Zenodo},
  url = {https://github.com/amonreal/dockcert}
}""")

    if qm_report:
        statuses.append(qm_report.overall_status)
        methods_parts.append(
            f"Quantum-chemical electronic structures, stationary points, and spin contamination were certified using QMCert v1.0.0 (Monreal-Hernández, 2026). Status: {qm_report.overall_status}."
        )
        bib_parts.append("""@software{monreal2026qmcert,
  author = {Monreal-Hern\\'andez, Andre},
  title = {{QMCert: Automated Quality-Control, Stationary Point Certification, and Reproducibility Assessment for Quantum-Chemical Calculations}},
  year = {2026},
  version = {1.0.0},
  publisher = {Zenodo},
  url = {https://github.com/amonreal/qmcert}
}""")

    if adsorp_report:
        statuses.append(adsorp_report.overall_status)
        methods_parts.append(
            f"Nanoporous adsorption equilibria, GCMC burn-in, and isotherm model fits were validated using AdsorpQC v1.0.0 (Monreal-Hernández, 2026). Status: {adsorp_report.overall_status}."
        )
        bib_parts.append("""@software{monreal2026adsorpqc,
  author = {Monreal-Hern\\'andez, Andre},
  title = {{AdsorpQC: An Open-Source Toolkit for Quality-Control, GCMC Burn-in Detection, Isotherm Fitting, and Reproducibility Assessment of Adsorption Simulations}},
  year = {2026},
  version = {1.0.0},
  publisher = {Zenodo},
  url = {https://github.com/amonreal/adsorpqc}
}""")

    if alpha_report:
        statuses.append(alpha_report.overall_status)
        methods_parts.append(
            f"Predicted 3D protein structures, pLDDT per-residue confidence, and 2D PAE error matrices were certified using AlphaCert v1.0.0 (Monreal-Hernández, 2026). Status: {alpha_report.overall_status}."
        )
        bib_parts.append("""@software{monreal2026alphacert,
  author = {Monreal-Hern\\'andez, Andre},
  title = {{AlphaCert: An Open-Source Toolkit for Quality-Control, pLDDT/PAE Assessment, and Stereochemical Certification of Predicted Protein Structures}},
  year = {2026},
  version = {1.0.0},
  publisher = {Zenodo},
  url = {https://github.com/amonreal/alphacert}
}""")

    if fep_report:
        statuses.append(fep_report.overall_status)
        methods_parts.append(
            f"Alchemical free energy calculations, phase space overlap matrices, and thermodynamic cycle closures were certified using FEPCert v1.0.0 (Monreal-Hernández, 2026). Status: {fep_report.overall_status}."
        )
        bib_parts.append("""@software{monreal2026fepcert,
  author = {Monreal-Hern\\'andez, Andre},
  title = {{FEPCert: An Open-Source Toolkit for Quality-Control, Phase Space Overlap, and Thermodynamic Cycle Closure Certification of Alchemical Free Energy Simulations}},
  year = {2026},
  version = {1.0.0},
  publisher = {Zenodo},
  url = {https://github.com/amonreal/fepcert}
}""")

    if qsar_report:
        statuses.append(qsar_report.overall_status)
        methods_parts.append(
            f"Quantitative Structure-Activity Relationship (QSAR) and molecular machine learning models were audited for OECD Validation Principles, Applicability Domain (Williams Plot), and Y-Randomization using QSARCert v1.0.0 (Monreal-Hernández, 2026). Status: {qsar_report.overall_status}."
        )
        bib_parts.append("""@software{monreal2026qsarcert,
  author = {Monreal-Hern\\'andez, Andre},
  title = {{QSARCert: An Open-Source Toolkit for OECD Validation Principles, Applicability Domain Assessment, Y-Randomization, and Reproducibility Certification of QSAR and Molecular Machine Learning Models}},
  year = {2026},
  version = {1.0.0},
  publisher = {Zenodo},
  url = {https://github.com/amonreal/qsarcert}
}""")

    if cat_report:
        statuses.append(cat_report.overall_status)
        methods_parts.append(
            f"Heterogeneous catalysis surface slab models, vacuum potential flatness, work functions, and surface energy layer convergence were certified using CatCert v1.0.0 (Monreal-Hernández, 2026). Status: {cat_report.overall_status}."
        )
        bib_parts.append("""@software{monreal2026catcert,
  author = {Monreal-Hern\\'andez, Andre},
  title = {{CatCert: Automated Quality-Control, Vacuum Thickness, Dipole Correction, and Surface Energy Convergence Certification for Heterogeneous Catalysis & DFT Surface Slabs}},
  year = {2026},
  version = {1.0.0},
  publisher = {Zenodo},
  url = {https://github.com/amonreal/catcert}
}""")

    if neb_report:
        statuses.append(neb_report.overall_status)
        methods_parts.append(
            f"Nudged elastic band reaction pathways, transition states, Eyring rate constants, and quantum tunneling corrections were certified using NEBCert v1.0.0 (Monreal-Hernández, 2026). Status: {neb_report.overall_status}."
        )
        bib_parts.append("""@software{monreal2026nebcert,
  author = {Monreal-Hern\\'andez, Andre},
  title = {{NEBCert: Automated Quality-Control, Transition State Verification, Nudged Elastic Band (NEB), Quantum Tunneling, and Reaction Kinetics Certification}},
  year = {2026},
  version = {1.0.0},
  publisher = {Zenodo},
  url = {https://github.com/amonreal/nebcert}
}""")

    # Umbrella SimCert citation
    bib_parts.append("""@software{monreal2026simcert,
  author = {Monreal-Hern\\'andez, Andre},
  title = {{SimCert: A Unified Scientific Simulation Quality-Control and Reproducibility Meta-Framework}},
  year = {2026},
  version = {1.5.0},
  publisher = {Zenodo},
  url = {https://github.com/amonreal/simcert}
}""")

    if "FAIL" in statuses:
        overall = "FAIL"
    elif "WARNING" in statuses:
        overall = "WARNING"
    else:
        overall = "PASS"

    consolidated_methods = " ".join(methods_parts)
    consolidated_bibtex = "\n\n".join(bib_parts)

    return SimCertProjectReport(
        project_name=project_name,
        overall_status=overall,
        md_report=md_report,
        dock_report=dock_report,
        qm_report=qm_report,
        adsorp_report=adsorp_report,
        alpha_report=alpha_report,
        fep_report=fep_report,
        qsar_report=qsar_report,
        cat_report=cat_report,
        neb_report=neb_report,
        consolidated_methods=consolidated_methods,
        consolidated_bibtex=consolidated_bibtex
    )
