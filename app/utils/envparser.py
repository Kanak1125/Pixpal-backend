from pathlib import Path
import os

def parse_env(path: Path= Path("app/.env")):

    with open(path, "r") as f:
        for line in f.readlines():
            ###A=B\n
            if len(line) <= 1:
                continue
            if line[0] == "#":
                continue
            var, val = line.split("=", maxsplit=1)
            os.environ[var] = val.strip()
