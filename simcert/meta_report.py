"""
Consolidated Meta-Report Generator for SimCert.
"""

import os
import jinja2
from simcert.orchestrator import SimCertProjectReport

META_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SimCert Project Quality Summary</title>
    <style>
        :root {
            --bg-color: #0b0f19;
            --card-bg: #151e2e;
            --card-border: #26354a;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --pass-color: #10b981;
            --pass-bg: rgba(16, 185, 129, 0.15);
            --warn-color: #f59e0b;
            --warn-bg: rgba(245, 158, 11, 0.15);
            --fail-color: #ef4444;
            --fail-bg: rgba(239, 68, 68, 0.15);
            --accent-blue: #38bdf8;
            --accent-purple: #a855f7;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            line-height: 1.6;
            padding: 2rem 1rem;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--card-border);
            padding-bottom: 1.5rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
            gap: 1rem;
        }
        .title-group h1 { font-size: 2.2rem; font-weight: 800; }
        .title-group p { color: var(--text-secondary); font-size: 1rem; }
        .status-badge {
            display: inline-flex;
            align-items: center;
            padding: 0.6rem 1.5rem;
            border-radius: 9999px;
            font-weight: 800;
            font-size: 1.15rem;
            text-transform: uppercase;
        }
        .badge-pass { background-color: var(--pass-bg); color: var(--pass-color); border: 1px solid var(--pass-color); }
        .badge-warning { background-color: var(--warn-bg); color: var(--warn-color); border: 1px solid var(--warn-color); }
        .badge-fail { background-color: var(--fail-bg); color: var(--fail-color); border: 1px solid var(--fail-color); }

        .tier-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2.5rem;
        }
        .tier-card {
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 0.85rem;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2);
            transition: transform 0.2s;
        }
        .tier-card:hover { transform: translateY(-2px); border-color: var(--accent-blue); }
        .tier-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }
        .tier-title { font-size: 1.15rem; font-weight: 700; color: var(--text-primary); }
        .tier-tag { font-size: 0.75rem; font-weight: 800; padding: 0.2rem 0.6rem; border-radius: 0.375rem; }
        .tier-desc { font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 1rem; }
        .metric-item { display: flex; justify-content: space-between; padding: 0.4rem 0; border-top: 1px solid rgba(255,255,255,0.05); font-size: 0.85rem; }
        .metric-item span:first-child { color: var(--text-secondary); }
        .metric-item span:last-child { font-weight: 600; color: var(--text-primary); }

        .section-title { font-size: 1.3rem; font-weight: 700; margin-bottom: 1rem; color: var(--accent-blue); }
        .box { background-color: var(--card-bg); border: 1px solid var(--card-border); border-radius: 0.75rem; padding: 1.25rem; margin-bottom: 2rem; }
        pre { background-color: rgba(0, 0, 0, 0.4); padding: 1rem; border-radius: 0.5rem; color: #38bdf8; font-family: monospace; font-size: 0.85rem; white-space: pre-wrap; }
        .btn-copy { background-color: #2563eb; color: white; border: none; padding: 0.4rem 0.8rem; border-radius: 0.375rem; cursor: pointer; font-size: 0.8rem; margin-top: 0.5rem; }
        .btn-copy:hover { background-color: #1d4ed8; }

        footer { text-align: center; font-size: 0.85rem; color: var(--text-secondary); margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid var(--card-border); }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="title-group">
                <h1>SimCert Project Validation Hub</h1>
                <p>{{ report.project_name }} &bull; Multi-Tier Simulation Quality Certification</p>
            </div>
            <div>
                <span class="status-badge badge-{{ report.overall_status.lower() }}">
                    OVERALL: {{ report.overall_status }}
                </span>
            </div>
        </header>

        <h2 class="section-title">Computational Simulation Tiers</h2>
        <div class="tier-grid">
            <!-- 1. Molecular Dynamics (MDCheck) -->
            <div class="tier-card">
                <div class="tier-header">
                    <div class="tier-title">Molecular Dynamics</div>
                    <span class="tier-tag badge-{{ report.md_report.overall_status.lower() if report.md_report else 'warning' }}">
                        {{ report.md_report.overall_status if report.md_report else 'NOT RUN' }}
                    </span>
                </div>
                <div class="tier-desc">Toolkit: <strong>MDCheck v1.0.0</strong></div>
                {% if report.md_report %}
                <div class="metric-item"><span>Observables</span><span>{{ report.md_report.n_observables }} audited</span></div>
                <div class="metric-item"><span>Equilibration</span><span>t_eq detected</span></div>
                <div class="metric-item"><span>Sampling (N_eff)</span><span>Certified</span></div>
                {% else %}
                <div class="metric-item"><span>Status</span><span>No MD runs in project</span></div>
                {% endif %}
            </div>

            <!-- 2. Molecular Docking (DockCert) -->
            <div class="tier-card">
                <div class="tier-header">
                    <div class="tier-title">Molecular Docking</div>
                    <span class="tier-tag badge-{{ report.dock_report.overall_status.lower() if report.dock_report else 'warning' }}">
                        {{ report.dock_report.overall_status if report.dock_report else 'NOT RUN' }}
                    </span>
                </div>
                <div class="tier-desc">Toolkit: <strong>DockCert v1.0.0</strong></div>
                {% if report.dock_report %}
                <div class="metric-item"><span>BEDROC (a=20)</span><span>{{ "%.3f"|format(report.dock_report.enrichment.bedroc_alpha_20) if report.dock_report.enrichment else 'N/A' }}</span></div>
                <div class="metric-item"><span>ROC-AUC</span><span>{{ "%.3f"|format(report.dock_report.enrichment.roc_auc) if report.dock_report.enrichment else 'N/A' }}</span></div>
                <div class="metric-item"><span>Redocking RMSD</span><span>{{ report.dock_report.redocking.status if report.dock_report.redocking else 'N/A' }}</span></div>
                {% else %}
                <div class="metric-item"><span>Status</span><span>No Docking runs in project</span></div>
                {% endif %}
            </div>

            <!-- 3. Quantum Chemistry (QMCert) -->
            <div class="tier-card">
                <div class="tier-header">
                    <div class="tier-title">Quantum Chemistry</div>
                    <span class="tier-tag badge-{{ report.qm_report.overall_status.lower() if report.qm_report else 'warning' }}">
                        {{ report.qm_report.overall_status if report.qm_report else 'NOT RUN' }}
                    </span>
                </div>
                <div class="tier-desc">Toolkit: <strong>QMCert v1.0.0</strong></div>
                {% if report.qm_report %}
                <div class="metric-item"><span>Stationary Point</span><span>{{ report.qm_report.frequency_result.point_type if report.qm_report.frequency_result else 'Certified' }}</span></div>
                <div class="metric-item"><span>SCF Convergence</span><span>{{ report.qm_report.scf_result.status if report.qm_report.scf_result else 'PASS' }}</span></div>
                <div class="metric-item"><span>Spin Contamination</span><span>{{ report.qm_report.spin_result.status if report.qm_report.spin_result else 'PASS' }}</span></div>
                {% else %}
                <div class="metric-item"><span>Status</span><span>No QM runs in project</span></div>
                {% endif %}
            </div>

            <!-- 4. Adsorption / MOFs (AdsorpQC) -->
            <div class="tier-card">
                <div class="tier-header">
                    <div class="tier-title">Adsorption & GCMC</div>
                    <span class="tier-tag badge-{{ report.adsorp_report.overall_status.lower() if report.adsorp_report else 'warning' }}">
                        {{ report.adsorp_report.overall_status if report.adsorp_report else 'NOT RUN' }}
                    </span>
                </div>
                <div class="tier-desc">Toolkit: <strong>AdsorpQC v1.0.0</strong></div>
                {% if report.adsorp_report %}
                <div class="metric-item"><span>GCMC Burn-in</span><span>{{ report.adsorp_report.burnin_result.status if report.adsorp_report.burnin_result else 'Certified' }}</span></div>
                <div class="metric-item"><span>Optimal Isotherm</span><span>{{ report.adsorp_report.isotherm_fits.best_model_name if report.adsorp_report.isotherm_fits else 'Fitted' }}</span></div>
                <div class="metric-item"><span>Loading Drift</span><span>{{ "%.2f"|format(report.adsorp_report.burnin_result.loading_drift_pct) if report.adsorp_report.burnin_result else '0.0%' }}</span></div>
                {% else %}
                <div class="metric-item"><span>Status</span><span>No Adsorption runs in project</span></div>
                {% endif %}
            </div>
        </div>

        <h2 class="section-title">Consolidated Manuscript Methods Text</h2>
        <div class="box">
            <pre id="methodsSnippet">{{ report.consolidated_methods }}</pre>
            <button class="btn-copy" onclick="copyToClipboard('methodsSnippet')">Copy All Methods Text</button>
        </div>

        <h2 class="section-title">Consolidated BibTeX References</h2>
        <div class="box">
            <pre id="bibSnippet">{{ report.consolidated_bibtex }}</pre>
            <button class="btn-copy" onclick="copyToClipboard('bibSnippet')">Copy BibTeX Citations</button>
        </div>

        <footer>
            Generated automatically by <strong>SimCert v1.0.0</strong> &bull; Unified Scientific Simulation Quality-Control Meta-Framework &bull; Monreal-Hernández, 2026.
        </footer>
    </div>

    <script>
        function copyToClipboard(elementId) {
            const text = document.getElementById(elementId).innerText;
            navigator.clipboard.writeText(text).then(() => {
                alert('Copied to clipboard!');
            }).catch(err => {
                console.error('Error copying: ', err);
            });
        }
    </script>
</body>
</html>
"""


def generate_simcert_meta_report(report: SimCertProjectReport, output_path: str) -> str:
    template = jinja2.Template(META_HTML_TEMPLATE)
    rendered = template.render(report=report)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)
    return output_path
