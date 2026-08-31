# SimCert

[![CI](https://github.com/amonreal/simcert/actions/workflows/test.yml/badge.svg)](https://github.com/amonreal/simcert/actions)
[![PyPI version](https://img.shields.io/pypi/v/simcert.svg?color=blue)](https://pypi.org/project/simcert/)
[![Python versions](https://img.shields.io/pypi/pyversions/simcert.svg)](https://pypi.org/project/simcert/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1234567.svg)](https://doi.org/10.5281/zenodo.1234567)

> **A Unified Scientific Simulation Quality-Control, Stationary Point Certification, and AI Structure Validation Meta-Framework.**

---

## The SimCert Scientific Suite

**SimCert** is an integrated umbrella framework unifying automated quality assurance, statistical convergence diagnostics, stationary point certification, and manuscript-ready reporting across multiple computational domains:

| Tier | Engine / Module | Focus Area | Package |
| :--- | :--- | :--- | :--- |
| **Tier 1 (MD)** | [`MDCheck`](https://github.com/amonreal/mdcheck) | Molecular Dynamics: Automated $t_{\text{eq}}$, $\tau_{\text{int}}$, $N_{\text{eff}}$, drift, and multi-replica consistency ($R_1, R_2, R_3$). | `mdcheck` |
| **Tier 2 (Docking)** | [`DockCert`](https://github.com/amonreal/dockcert) | Molecular Docking: Early enrichment (BEDROC, RIE, EF1%), symmetry-corrected RMSD, decoy bias audit. | `dockcert` |
| **Tier 3 (QM/DFT)** | [`QMCert`](https://github.com/amonreal/qmcert) | Quantum Chemistry: Stationary point certification (0 imag freqs for min / 1 for TS), $\langle S^2 \rangle$ spin purity, Grimme quasi-RRHO. | `qmcert` |
| **Tier 4 (Adsorption)** | [`AdsorpQC`](https://github.com/amonreal/adsorpqc) | Porous Materials / GCMC: Burn-in detection, non-linear isotherm fits (Langmuir, Sips, Toth), $K_H$, $q_{\text{st}}$, IAST selectivity. | `adsorpqc` |
| **Tier 5 (AlphaFold)** | [`AlphaCert`](https://github.com/amonreal/alphacert) | AI Protein Structures: Per-residue pLDDT band categorization, 2D PAE error domain decomposition, steric clashes, Ramachandran check, and docking readiness. | `alphacert` |

```
                           ┌──────────────────┐
                           │     SimCert      │
                           │  Meta-Framework  │
                           └─────────┬────────┘
                                     │
         ┌──────────────┬────────────┼────────────┬──────────────┐
         ▼              ▼            ▼            ▼              ▼
    ┌─────────┐    ┌─────────┐  ┌─────────┐  ┌─────────┐    ┌─────────┐
    │ MDCheck │    │DockCert │  │ QMCert  │  │AdsorpQC │    │AlphaCert│
    │  (MD)   │    │(Docking)│  │(QM/DFT) │  │ (GCMC)  │    │(AF/ESM) │
    └─────────┘    └─────────┘  └─────────┘  └─────────┘    └─────────┘
         │              │            │            │              │
         └──────────────┴────────────┼────────────┴──────────────┘
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
# 1. Run all 5 domain benchmarks in one command
simcert demo-all -o full_project_audit/

# 2. Molecular Dynamics (MDCheck)
simcert md assess -i rmsd.xvg rg.xvg -o md_report/

# 3. Molecular Docking (DockCert)
simcert dock assess -i screening_scores.csv -o dock_report/

# 4. Quantum Chemistry (QMCert)
simcert qm assess -i dft_opt_freq.out -o qm_report/

# 5. Adsorption / MOFs (AdsorpQC)
simcert adsorp assess -i isotherm.csv --framework "Mg-MOF-74" -o adsorp_report/

# 6. AlphaFold / ESMFold Structures (AlphaCert)
simcert alpha assess -i model.pdb --pae model_pae.json -o alpha_report/
```

---

## Citation

If you use the SimCert framework in your research, please cite:

```bibtex
@software{monreal2026simcert,
  author = {Monreal-Hern{\'a}ndez, Andre},
  title = {{SimCert: A Unified Scientific Simulation Quality-Control and Reproducibility Meta-Framework}},
  year = {2026},
  version = {1.1.0},
  publisher = {Zenodo},
  url = {https://github.com/amonreal/simcert}
}
```

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
