"""Check a project folder against the standard. Usage: python check_folder.py [folder]"""
import json, sys, pathlib

REQUIRED = ["README.md", "spec.md", "features.json", "progress.md", "rubric.md", "run.md"]

def main(root="."):
    root = pathlib.Path(root)
    problems = []
    for name in REQUIRED:
        if not (root / name).is_file():
            problems.append(f"missing {name}")
    fpath = root / "features.json"
    if fpath.is_file():
        try:
            data = json.loads(fpath.read_text(encoding="utf-8"))
            feats = data.get("features")
            if not isinstance(feats, list) or not feats:
                problems.append("features.json: no features")
            else:
                seen = set()
                for f in feats:
                    fid = f.get("id", "?")
                    for key in ("id", "priority", "description", "check", "passes", "evidence"):
                        if key not in f:
                            problems.append(f"{fid}: missing {key}")
                    if fid in seen:
                        problems.append(f"{fid}: duplicate id")
                    seen.add(fid)
                    if f.get("passes") is True and not str(f.get("evidence", "")).strip():
                        problems.append(f"{fid}: passes without evidence")
        except json.JSONDecodeError as e:
            problems.append(f"features.json: not valid JSON ({e})")
    spec = root / "spec.md"
    if spec.is_file() and "{" in spec.read_text(encoding="utf-8").split("## Ask", 1)[-1].split("##", 1)[0]:
        problems.append("spec.md: Ask still a placeholder")
    for p in problems:
        print("FAIL", p)
    if not problems:
        print("OK", root)
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
