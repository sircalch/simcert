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


@dataclass
class SimCertProjectReport:
    project_name: str
    overall_status: str  # 'PASS', 'WARNING', 'FAIL'
    md_report: Optional[SimulationQualityReport]
    dock_report: Optional[DockingValidationReport]
    qm_report: Optional[QMCertValidationReport]
    adsorp_report: Optional[AdsorptionValidationReport]
    consolidated_methods: str
    consolidated_bibtex: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def run_multiscale_audit(
    project_name: str = "Multi-Scale Computational Investigation",
    md_report: Optional[SimulationQualityReport] = None,
    dock_report: Optional[DockingValidationReport] = None,
    qm_report: Optional[QMCertValidationReport] = None,
    adsorp_report: Optional[AdsorptionValidationReport] = None
) -> SimCertProjectReport:
    """
    Consolidates validation metrics across computational tiers into a single executive report.

    Parameters
    ----------
    project_name : str
        Title of the manuscript or project.
    md_report : SimulationQualityReport, optional
    dock_report : DockingValidationReport, optional
    qm_report : QMCertValidationReport, optional
    adsorp_report : AdsorptionValidationReport, optional

    Returns
    -------
    report : SimCertProjectReport
        Consolidated multi-scale report.
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

    # Umbrella SimCert citation
    bib_parts.append("""@software{monreal2026simcert,
  author = {Monreal-Hern\\'andez, Andre},
  title = {{SimCert: A Unified Scientific Simulation Quality-Control and Reproducibility Meta-Framework}},
  year = {2026},
  version = {1.0.0},
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
        consolidated_methods=consolidated_methods,
        consolidated_bibtex=consolidated_bibtex
    )
