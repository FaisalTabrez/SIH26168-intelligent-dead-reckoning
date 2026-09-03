#!/usr/bin/env python3
import argparse, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/"contracts/generated/contract_version.json"
expected=json.dumps({"contract_version":"1.0.0-bootstrap","generated_from":["contracts/VERSION","contracts/enums/navigation_states_v1.json"]},indent=2)+"\n"
parser=argparse.ArgumentParser(); parser.add_argument("--check",action="store_true"); args=parser.parse_args()
if args.check:
    if not OUTPUT.exists() or OUTPUT.read_text()!=expected: raise SystemExit("generated contract drift")
    print("PASS: generated contract bindings")
else: OUTPUT.write_text(expected,encoding="utf-8",newline="\n")
