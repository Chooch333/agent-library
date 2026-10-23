"""Check a project folder against the standard. Usage: python check_folder.py [folder]"""
import json, re, sys, pathlib

REQUIRED = ["README.md", "spec.md", "features.json", "progress.md", "rubric.md", "run.md"]
VERDICTS = ("PASS", "FAIL", "CAN'T CHECK")


def verdicts(root, fid):
    """Checker verdict files for one feature, oldest attempt first: [(n, verdict, path)]."""
    out = []
    for p in (root / "checks").glob(f"{fid}-*.md"):
        m = re.fullmatch(re.escape(fid) + r"-(\d+)\.md", p.name)
        if not m:
            continue
        first = p.read_text(encoding="utf-8").lstrip().splitlines()[:1]
        first = first[0].strip().upper() if first else ""
        v = next((x for x in VERDICTS if first.startswith(x)), "?")
        out.append((int(m.group(1)), v, p))
    return sorted(out)


def checker_rules(root, feats, problems):
    """On when features.json has "checker": true. Only a checker verdict can mark a feature passed."""
    readme = root / "README.md"
    stopped = readme.is_file() and re.search(r"Status:\**\s*stopped:", readme.read_text(encoding="utf-8"))
    for f in feats:
        fid = f.get("id", "?")
        vs = verdicts(root, fid)
        newest = vs[-1] if vs else None
        if f.get("passes") is True:
            if not newest:
                problems.append(f"{fid}: passes without a checker verdict (no checks/{fid}-<n>.md)")
            elif newest[1] != "PASS":
                problems.append(f"{fid}: passes but newest verdict {newest[2].name} is {newest[1]}, not PASS")
            elif f"checks/{fid}-" not in str(f.get("evidence", "")):
                problems.append(f"{fid}: passes but evidence does not point at its checks/ file")
        fails = sum(1 for v in vs if v[1] == "FAIL")
        if fails >= 3 and newest and newest[1] != "PASS" and not stopped:
            problems.append(f"{fid}: {fails} FAIL verdicts but README Status is not 'stopped:' (three-strikes rule)")


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
                if data.get("checker") is True:
                    checker_rules(root, feats, problems)
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
