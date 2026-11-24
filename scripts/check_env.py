"""Reject local environment files in staged paths."""

import sys
from pathlib import Path

private = [name for name in sys.argv[1:] if Path(name).name != ".env.example"]
if private:
    sys.exit("Commit only .env.example. Remove local environment files from the index.")
