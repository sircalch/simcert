"""
Tests for SimCert CLI.
"""

import os
import tempfile
import pytest
from simcert.cli import run_demo_all


def test_cli_demo_all():
    with tempfile.TemporaryDirectory() as tmpdir:
        run_demo_all(output_dir=tmpdir)
        assert os.path.exists(os.path.join(tmpdir, "simcert_project_summary.html"))
        assert os.path.exists(os.path.join(tmpdir, "md", "report.html"))
        assert os.path.exists(os.path.join(tmpdir, "docking", "report.html"))
        assert os.path.exists(os.path.join(tmpdir, "qm", "report.html"))
        assert os.path.exists(os.path.join(tmpdir, "adsorption", "report.html"))
