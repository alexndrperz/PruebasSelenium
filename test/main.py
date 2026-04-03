import sys
import subprocess
from pathlib import Path


subprocess.run(
    [sys.executable, "-m", "pytest", "src", "-o", "python_files=*_test.py",
     "--html=reports/report.html", "--self-contained-html"],
    cwd=Path(__file__).parent
)
