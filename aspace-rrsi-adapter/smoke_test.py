"""Smoke test de l'adapter A'Space pour rrsi (contrat seul).

Hors-ligne : modules purs du cœur de la méthode + --help de la CLI.
Aucun appel modèle, aucun appel réseau, aucun domaine invoqué.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
GEL = "be50316"


def _git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args],
                          capture_output=True, text=True,
                          check=True).stdout.strip()


def test_gel_is_ancestor():
    assert _git("merge-base", "HEAD", GEL) == _git("rev-parse", GEL)


def test_only_adapter_changed():
    out = _git("diff", "--name-only", GEL, "HEAD")
    assert out, "aucun fichier changé depuis le gel"
    assert all(p.startswith("aspace-rrsi-adapter/")
               for p in out.splitlines())


def test_contract():
    c = json.loads((HERE / "contract.json").read_text())
    assert c["upstream"]["frozen_commit"] == GEL
    assert c["version"] == "0.1.0"


def test_pure_core_offline():
    sys.path.insert(0, str(ROOT))
    from rrsi.config import RRSIConfig
    from rrsi.schedule import budget_table, edit_budget
    from rrsi.selection import select_round
    cfg = RRSIConfig()
    assert cfg.T == 20 and cfg.b_min == 1 and cfg.b_max == 4
    table = budget_table(20, 1, 4)
    assert len(table) == 20
    assert all(isinstance(b, int) and 1 <= b <= 4 for b in table)
    assert edit_budget(0, 20, 1, 4) == table[0]
    assert callable(select_round)


def test_cli_help():
    p = subprocess.run([sys.executable, str(ROOT / "rrsi.py"), "--help"],
                       capture_output=True, text=True, timeout=60)
    assert p.returncode == 0
    assert "RRSI command line" in p.stdout
