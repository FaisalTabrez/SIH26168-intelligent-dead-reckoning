#!/usr/bin/env python3
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
output=ROOT/"docs/bootstrap/repository_manifest.json"
targets=[]
targets.extend(sorted((ROOT/"docs/bootstrap").glob("*")))
targets.extend(sorted((ROOT/"docs/architecture").rglob("*")))
files=[]
for p in targets:
    if p.is_file() and p != output:
        files.append({"path":p.relative_to(ROOT).as_posix(),"size_bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()})
doc={"schema_version":1,"scope":"Bootstrap and immutable Architecture Revision 3 artifacts; manifest excludes itself.","files":files}
output.write_text(json.dumps(doc,indent=2)+"\n",encoding="utf-8",newline="\n")
print(hashlib.sha256(output.read_bytes()).hexdigest())
