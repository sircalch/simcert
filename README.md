# SimCert

[![CI](https://github.com/amonreal/simcert/actions/workflows/test.yml/badge.svg)](https://github.com/amonreal/simcert/actions)
[![PyPI version](https://img.shields.io/pypi/v/simcert.svg?color=blue)](https://pypi.org/project/simcert/)
[![Python versions](https://img.shields.io/pypi/pyversions/simcert.svg)](https://pypi.org/project/simcert/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1234567.svg)](https://doi.org/10.5281/zenodo.1234567)

> **A Unified Scientific Simulation Quality-Control, Stationary Point Certification, and Reproducibility Meta-Framework.**

---

## The SimCert Scientific Suite

**SimCert** is an integrated umbrella framework unifying automated quality assurance, statistical convergence diagnostics, stationary point certification, and manuscript-ready reporting across multiple scales of molecular modeling:

| Tier | Engine / Module | Focus Area | Package |
| :--- | :--- | :--- | :--- |
| **MD** | [`MDCheck`](https://github.com/amonreal/mdcheck) | Molecular Dynamics: Automated $t_{\text{eq}}$, $\tau_{\text{int}}$, $N_{\text{eff}}$, drift, and multi-replica consistency ($R_1, R_2, R_3$). | `mdcheck` |
| **Docking** | [`DockCert`](https://github.com/amonreal/dockcert) | Molecular Docking: Early enrichment (BEDROC, RIE, EF1%), symmetry-corrected RMSD, decoy bias audit. | `dockcert` |
| **QM / DFT** | [`QMCert`](https://github.com/amonreal/qmcert) | Quantum Chemistry: Stationary point certification (0 imag freqs for min / 1 for TS), $\langle S^2 \rangle$ spin purity, Grimme quasi-RRHO. | `qmcert` |
| **Adsorption** | [`AdsorpQC`](https://github.com/amonreal/adsorpqc) | Porous Materials / GCMC: Burn-in detection, non-linear isotherm fits (Langmuir, Sips, Toth), $K_H$, $q_{\text{st}}$, IAST selectivity. | `adsorpqc` |

```
                           ┌──────────────────┐
                           │     SimCert      │
                           │  Meta-Framework  │
                           └─────────┬────────┘
                                     │
         ┌───────────────────┬───────┴───────────┬───────────────────┐
         ▼                   ▼                   ▼                   ▼
    ┌─────────┐         ┌─────────┐         ┌─────────┐         ┌─────────┐
    │ MDCheck │         │DockCert │         │ QMCert  │         │AdsorpQC │
    │  (MD)   │         │(Docking)│         │(QM/DFT) │         │ (GCMC)  │
    └─────────┘         └─────────┘         └─────────┘         └─────────┘
         │                   │                   │                   │
         └───────────────────┴───────┬───────────┴───────────────────┘
                                     ▼
                    ┌──────────────────────────────────┐
                    │  simcert_project_summary.html    │
                    │  Unified Manuscript Methods      │
                    │  Consolidated BibTeX Citations   │
                    └──────────────────────────────────┘
```

---

## Installation

Install the entire suite in a single command:

```bash
pip install simcert
```

---

## CLI Usage

Run any module directly from the unified `simcert` CLI:

```bash
# 1. Run all 4 domain benchmarks in one command
simcert demo-all -o full_project_audit/

# 2. Molecular Dynamics (MDCheck)
simcert md assess -i rmsd.xvg rg.xvg -o md_report/

# 3. Molecular Docking (DockCert)
simcert dock assess -i screening_scores.csv -o dock_report/

# 4. Quantum Chemistry (QMCert)
simcert qm assess -i dft_opt_freq.out -o qm_report/

# 5. Adsorption / MOFs (AdsorpQC)
simcert adsorp assess -i isotherm.csv --framework "Mg-MOF-74" -o adsorp_report/
```

---

## Python API Usage

```python
from simcert.orchestrator import run_multiscale_audit
from simcert.meta_report import generate_simcert_meta_report

import mdcheck
import dockcert
import qmcert
import adsorpqc

# Generate individual tier reports ...
# Consolidate into a multi-scale executive report
meta_report = run_multiscale_audit(
    project_name="Target Kinase Drug Discovery Campaign",
    md_report=md_rep,
    dock_report=dock_rep,
    qm_report=qm_rep,
    adsorp_report=adsorp_rep
)

generate_simcert_meta_report(meta_report, "simcert_project_summary.html")
```

---

## Citation

If you use the SimCert framework in your research, please cite:

```bibtex
@software{monreal2026simcert,
  author = {Monreal-Hern{\'a}ndez, Andre},
  title = {{SimCert: A Unified Scientific Simulation Quality-Control and Reproducibility Meta-Framework}},
  year = {2026},
  version = {1.0.0},
  publisher = {Zenodo},
  url = {https://github.com/amonreal/simcert}
}
```

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
