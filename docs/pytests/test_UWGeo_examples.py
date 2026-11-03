import subprocess
import pytest
import glob
import ntpath
import importlib.util
from inspect import getsourcefile

wdir = ntpath.dirname(getsourcefile(lambda:0))+"/../UWGeodynamics/examples/"

# badlands pins numpy<2, so numpy 2 environments run without it
no_badlands = pytest.mark.skipif(importlib.util.find_spec("badlands") is None, reason="badlands not installed")

def _marks(path):
    with open(path) as f:
        return [no_badlands] if "Badlands(" in f.read() else []

# get ipynb scripts to test
scripts = [pytest.param(path, id=ntpath.basename(path), marks=_marks(path)) for path in sorted(glob.glob(wdir+"/*.ipynb"))]

@pytest.mark.parametrize('script', scripts)
def test_script_execution(script):
    subprocess.run(["pytest", "--nbmake", script], check=True)
