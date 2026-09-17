import os
import subprocess
import sys

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def in_fresh_worker():
    """Evaluate an expression in a brand new interpreter, the way the platform starts a worker.

    Returns a callable ``(expression) -> str``.  Each call is an independent process, which is
    the point: workers are started separately on different machines and have to agree.
    """

    def run(expression: str) -> str:
        env = dict(os.environ, PYTHONPATH=REPO_ROOT)
        code = f"import json,sys; sys.stdout.write(str({expression}))"
        out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env=env, cwd=REPO_ROOT)
        assert out.returncode == 0, out.stderr
        return out.stdout

    return run
