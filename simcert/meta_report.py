"""
Consolidated Project Executive Dashboard HTML Generator for SimCert.
"""

import os
import jinja2
from simcert.orchestrator import SimCertProjectReport

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SimCert Project Summary Dashboard</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --card-border: #334155;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --pass-color: #10b981;
            --pass-bg: rgba(16, 185, 129, 0.15);
            --warn-color: #f59e0b;
            --warn-bg: rgba(245, 158, 11, 0.15);
            --fail-color: #ef4444;
            --fail-bg: rgba(239, 68, 68, 0.15);
            --accent-blue: #38bdf8;
            --accent-purple: #c084fc;
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
            padding: 0.5rem 1.5rem;
            border-radius: 9999px;
            font-weight: 800;
            font-size: 1.2rem;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }
        .badge-pass { background-color: var(--pass-bg); color: var(--pass-color); border: 1px solid var(--pass-color); }
        .badge-warning { background-color: var(--warn-bg); color: var(--warn-color); border: 1px solid var(--warn-color); }
        .badge-fail { background-color: var(--fail-bg); color: var(--fail-color); border: 1px solid var(--fail-color); }

        .grid-tiers {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2.5rem;
        }
        .tier-card {
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 0.75rem;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
            position: relative;
        }
        .tier-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            padding-bottom: 0.5rem;
        }
        .tier-title { font-size: 1.15rem; font-weight: 700; color: var(--accent-blue); }
        .tag { display: inline-block; padding: 0.2rem 0.6rem; border-radius: 0.375rem; font-size: 0.75rem; font-weight: 700; }
        .tag-pass { background-color: var(--pass-bg); color: var(--pass-color); }
        .tag-warning { background-color: var(--warn-bg); color: var(--warn-color); }
        .tag-fail { background-color: var(--fail-bg); color: var(--fail-color); }

        .tier-body { font-size: 0.9rem; color: var(--text-secondary); }
        .tier-body p { margin-bottom: 0.4rem; }
        .tier-body strong { color: var(--text-primary); }

        .section-title { font-size: 1.4rem; font-weight: 700; margin-bottom: 1rem; color: var(--accent-purple); }
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
                <h1>SimCert Multi-Scale Quality Hub</h1>
                <p>{{ report.project_name }} &bull; Comprehensive In Silico Quality Certification</p>
            </div>
            <div>
                <span class="status-badge badge-{{ report.overall_status.lower() }}">
                    {{ report.overall_status }}
                </span>
            </div>
        </header>

        <h2 class="section-title">Computational Tiers Certification Summary</h2>
        <div class="grid-tiers">
            <!-- Tier 1: MD -->
            <div class="tier-card">
                <div class="tier-header">
                    <div class="tier-title">Molecular Dynamics (MDCheck)</div>
                    {% if report.md_report %}
                    <span class="tag tag-{{ report.md_report.overall_status.lower() }}">{{ report.md_report.overall_status }}</span>
                    {% else %}
                    <span class="tag" style="background-color: #334155; color: #94a3b8;">SKIPPED</span>
                    {% endif %}
                </div>
                <div class="tier-body">
                    {% if report.md_report %}
                    <p><strong>Observables Evaluated:</strong> {{ report.md_report.key_metrics.n_observables_evaluated }}</p>
                    <p><strong>Min Sample Size:</strong> {{ "%.1f"|format(report.md_report.key_metrics.min_effective_sample_size) }}</p>
                    <p><strong>Assessment:</strong> {{ report.md_report.score_summary }}</p>
                    <p><a href="md/report.html" style="color: var(--accent-blue); text-decoration: underline;">View Detailed MD Report &rarr;</a></p>
                    {% else %}
                    <p>No molecular dynamics trajectory evaluated.</p>
                    {% endif %}
                </div>
            </div>

            <!-- Tier 2: Docking -->
            <div class="tier-card">
                <div class="tier-header">
                    <div class="tier-title">Molecular Docking (DockCert)</div>
                    {% if report.dock_report %}
                    <span class="tag tag-{{ report.dock_report.overall_status.lower() }}">{{ report.dock_report.overall_status }}</span>
                    {% else %}
                    <span class="tag" style="background-color: #334155; color: #94a3b8;">SKIPPED</span>
                    {% endif %}
                </div>
                <div class="tier-body">
                    {% if report.dock_report and report.dock_report.enrichment_metrics %}
                    <p><strong>BEDROC (&alpha;=20.0):</strong> {{ "%.3f"|format(report.dock_report.enrichment_metrics['bedroc_20'].value if 'bedroc_20' in report.dock_report.enrichment_metrics else 0.0) }}</p>
                    <p><strong>ROC-AUC:</strong> {{ "%.3f"|format(report.dock_report.enrichment_metrics['roc_auc'].value if 'roc_auc' in report.dock_report.enrichment_metrics else 0.0) }}</p>
                    <p><strong>Assessment:</strong> {{ report.dock_report.validation_score }}</p>
                    <p><a href="docking/report.html" style="color: var(--accent-blue); text-decoration: underline;">View Detailed Docking Report &rarr;</a></p>
                    {% elif report.dock_report %}
                    <p><strong>Assessment:</strong> {{ report.dock_report.validation_score }}</p>
                    <p><a href="docking/report.html" style="color: var(--accent-blue); text-decoration: underline;">View Detailed Docking Report &rarr;</a></p>
                    {% else %}
                    <p>No docking or virtual screening benchmark evaluated.</p>
                    {% endif %}
                </div>
            </div>

            <!-- Tier 3: QM -->
            <div class="tier-card">
                <div class="tier-header">
                    <div class="tier-title">Quantum Chemistry (QMCert)</div>
                    {% if report.qm_report %}
                    <span class="tag tag-{{ report.qm_report.overall_status.lower() }}">{{ report.qm_report.overall_status }}</span>
                    {% else %}
                    <span class="tag" style="background-color: #334155; color: #94a3b8;">SKIPPED</span>
                    {% endif %}
                </div>
                <div class="tier-body">
                    {% if report.qm_report %}
                    <p><strong>Engine / Theory:</strong> {{ report.qm_report.metadata.get('engine', 'QM') }} / {{ report.qm_report.metadata.get('functional', 'DFT') }}</p>
                    {% if report.qm_report.frequency_result %}
                    <p><strong>Stationary Point:</strong> {{ report.qm_report.frequency_result.stationary_point_type }} ({{ report.qm_report.frequency_result.n_imaginary }} imag freqs)</p>
                    {% else %}
                    <p><strong>Stationary Point:</strong> Evaluated</p>
                    {% endif %}
                    <p><strong>Assessment:</strong> {{ report.qm_report.validation_score }}</p>
                    <p><a href="qm/report.html" style="color: var(--accent-blue); text-decoration: underline;">View Detailed QM Report &rarr;</a></p>
                    {% else %}
                    <p>No electronic structure or DFT calculation evaluated.</p>
                    {% endif %}
                </div>
            </div>

            <!-- Tier 4: Adsorption -->
            <div class="tier-card">
                <div class="tier-header">
                    <div class="tier-title">Adsorption & MOFs (AdsorpQC)</div>
                    {% if report.adsorp_report %}
                    <span class="tag tag-{{ report.adsorp_report.overall_status.lower() }}">{{ report.adsorp_report.overall_status }}</span>
                    {% else %}
                    <span class="tag" style="background-color: #334155; color: #94a3b8;">SKIPPED</span>
                    {% endif %}
                </div>
                <div class="tier-body">
                    {% if report.adsorp_report %}
                    <p><strong>Framework:</strong> {{ report.adsorp_report.metadata.get('framework', 'Porous Material') }}</p>
                    {% if report.adsorp_report.isotherm_fit %}
                    <p><strong>Best Isotherm:</strong> {{ report.adsorp_report.isotherm_fit.best_model_name }}</p>
                    {% endif %}
                    <p><strong>Assessment:</strong> {{ report.adsorp_report.validation_score }}</p>
                    <p><a href="adsorption/report.html" style="color: var(--accent-blue); text-decoration: underline;">View Detailed Adsorption Report &rarr;</a></p>
                    {% else %}
                    <p>No adsorption or GCMC simulation evaluated.</p>
                    {% endif %}
                </div>
            </div>

            <!-- Tier 5: AlphaFold / ESMFold -->
            <div class="tier-card">
                <div class="tier-header">
                    <div class="tier-title">AlphaFold / Structures (AlphaCert)</div>
                    {% if report.alpha_report %}
                    <span class="tag tag-{{ report.alpha_report.overall_status.lower() }}">{{ report.alpha_report.overall_status }}</span>
                    {% else %}
                    <span class="tag" style="background-color: #334155; color: #94a3b8;">SKIPPED</span>
                    {% endif %}
                </div>
                <div class="tier-body">
                    {% if report.alpha_report %}
                    <p><strong>Target & Engine:</strong> {{ report.alpha_report.metadata.get('name', 'Protein') }} ({{ report.alpha_report.metadata.get('engine', 'AlphaFold2') }})</p>
                    <p><strong>Mean pLDDT:</strong> {{ "%.1f"|format(report.alpha_report.plddt_result.mean_plddt) }} / 100</p>
                    <p><strong>Assessment:</strong> {{ report.alpha_report.validation_score }}</p>
                    <p><a href="alpha/report.html" style="color: var(--accent-blue); text-decoration: underline;">View Detailed Structure Report &rarr;</a></p>
                    {% else %}
                    <p>No predicted protein structure evaluated.</p>
                    {% endif %}
                </div>
            </div>
        </div>

        <h2 class="section-title">Consolidated Manuscript Methods Section</h2>
        <div class="box">
            <pre id="methodsSnippet">{{ report.consolidated_methods }}</pre>
            <button class="btn-copy" onclick="copyToClipboard('methodsSnippet')">Copy Consolidated Methods</button>
        </div>

        <h2 class="section-title">Consolidated BibTeX Citations</h2>
        <div class="box">
            <pre id="bibSnippet">{{ report.consolidated_bibtex }}</pre>
            <button class="btn-copy" onclick="copyToClipboard('bibSnippet')">Copy Consolidated BibTeX</button>
        </div>

        <footer>
            Generated automatically by <strong>SimCert v1.1.0</strong> &bull; Unified Scientific Simulation Quality Meta-Framework &bull; Monreal-Hernández, 2026.
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
    """
    Renders consolidated multi-scale project summary HTML.
    """
    template = jinja2.Template(HTML_TEMPLATE)
    rendered = template.render(report=report)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)
    return output_path
