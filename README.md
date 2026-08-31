# SimCert

[![CI](https://github.com/amonreal/simcert/actions/workflows/test.yml/badge.svg)](https://github.com/amonreal/simcert/actions)
[![PyPI version](https://img.shields.io/pypi/v/simcert.svg?color=blue)](https://pypi.org/project/simcert/)
[![Python versions](https://img.shields.io/pypi/pyversions/simcert.svg)](https://pypi.org/project/simcert/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1234570.svg)](https://doi.org/10.5281/zenodo.1234570)

> **Unified Quality-Control, Structure Validation, and Reproducibility Meta-Framework for Molecular Simulations & AI Models (MD, Docking, QM, Adsorption, AlphaFold, FEP).**

---

## Overview

**SimCert** is a high-level scientific umbrella meta-framework that connects, standardizes, and unifies automated quality control, convergence certification, and reproducibility reporting across **six distinct computational simulation and structural modeling domains**:

```
                                    ┌─────────────────────────────────────────┐
                                    │                 SimCert                 │
                                    │    (Umbrella Project Meta-Dashboard)    │
                                    └─────────────────────────────────────────┘
                                                         │
         ┌───────────────────┬───────────────────┬───────┴───────────┬───────────────────┬───────────────────┐
         │                   │                   │                   │                   │                   │
         ▼                   ▼                   ▼                   ▼                   ▼                   ▼
   ┌───────────┐       ┌───────────┐       ┌───────────┐       ┌───────────┐       ┌───────────┐       ┌───────────┐
   │  MDCheck  │       │ DockCert  │       │  QMCert   │       │ AdsorpQC  │       │ AlphaCert │       │  FEPCert  │
   │  Tier 1   │       │  Tier 2   │       │  Tier 3   │       │  Tier 4   │       │  Tier 5   │       │  Tier 6   │
   │    MD     │       │  Docking  │       │    DFT    │       │   GCMC    │       │ AlphaFold │       │ FEP / TI  │
   └───────────┘       └───────────┘       └───────────┘       └───────────┘       └───────────┘       └───────────┘
```

---

## The 6 Computational Tiers

1. **Tier 1: Molecular Dynamics (`mdcheck`)**
   - Autocorrelation time ($\tau_{\text{int}}$), effective sample size ($N_{\text{eff}}$), Chodera automated equilibration ($t_{\text{eq}}$), Geweke diagnostic, linear drift, multi-replica consistency ($R_1, R_2, R_3$).
2. **Tier 2: Molecular Docking & Screening (`dockcert`)**
   - Exact analytical BEDROC ($\alpha=20.0, 80.5, 160.9$), RIE, EF1%, EF5%, EF10%, ROC-AUC, PR-AUC, optimal MCC, Hungarian algorithm symmetry-corrected heavy-atom RMSD, decoy property matching KS-tests.
3. **Tier 3: Quantum Chemistry & DFT (`qmcert`)**
   - Stationary point certification (0 imaginary frequencies for minima, exactly 1 for transition states), spin contamination $\langle S^2 \rangle$, Grimme quasi-RRHO harmonic entropy correction for low modes ($\nu < 100\text{ cm}^{-1}$), simulated IR spectra.
4. **Tier 4: Adsorption in Nanoporous MOFs & GCMC (`adsorpqc`)**
   - GCMC equilibration burn-in detection, loading drift lock, non-linear isotherm model fitting (Langmuir, Dual-site, Sips, Toth, Freundlich, BET), Henry constant $K_H$, isosteric heat $q_{\text{st}}$, IAST binary selectivity with bootstrap confidence intervals.
5. **Tier 5: AlphaFold / ESMFold Structure Confidence (`alphacert`)**
   - Per-residue pLDDT categorization across 4 canonical bands ($>90, 70-90, 50-70, <50$), 2D Predicted Aligned Error (PAE) matrix domain decomposition, steric clashscore, Ramachandran dihedral distribution ($\phi, \psi$), certifications `DOCKING_READY` and `MD_READY`.
6. **Tier 6: Alchemical Free Energy & FEP (`fepcert`)**
   - Phase space overlap matrix ($\Pi_{ij} \ge 3\%$), Thermodynamic Integration (TI), Bennett Acceptance Ratio (BAR), forward/reverse time convergence and dissipated work $W_{\text{diss}}$, thermodynamic cycle closure audit ($\oint \Delta\Delta G \approx 0$).

---

## Installation

```bash
pip install simcert
```

---

## Quickstart (CLI)

```bash
# 1. Run full 6-tier multi-scale benchmark demonstration
simcert demo-all -o full_project_audit/

# 2. Delegate to any individual tier
simcert md assess -i trajectory.csv -o md_report/
simcert dock assess -i scores.csv -o dock_report/
simcert qm assess -i opt_freq.out -o qm_report/
simcert adsorp assess -i isotherm.csv -o adsorp_report/
simcert alpha assess -i model.pdb --pae model_pae.json -o alpha_report/
simcert fep assess -d gromacs_fep/ -o fep_report/

# 3. View consolidated citations
simcert cite
```

---

## Citation

```bibtex
@software{monreal2026simcert,
  author = {Monreal-Hern{\'a}ndez, Andre},
  title = {{SimCert: A Unified Scientific Simulation Quality-Control and Reproducibility Meta-Framework}},
  year = {2026},
  version = {1.2.0},
  publisher = {Zenodo},
  url = {https://github.com/amonreal/simcert}
}
```

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
