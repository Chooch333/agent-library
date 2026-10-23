"""Unit fixtures for templates/project-folder/check_folder.py (Build 45, checker rule).

Run: python tests/project-folder/test_check_folder.py   (from the agent-library root)
Each case builds a throwaway project folder and checks check_folder's verdict.
"""
import io, json, pathlib, sys, tempfile, contextlib, importlib.util

HERE = pathlib.Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "check_folder", HERE.parent.parent / "templates" / "project-folder" / "check_folder.py")
cf = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cf)


def make(tmp, *, checker=True, passes=True, evidence="checks/F01-1.md", checks=None, status="building"):
    root = pathlib.Path(tmp)
    (root / "README.md").write_text(f"# t\n**Status:** {status}\n", encoding="utf-8")
    (root / "spec.md").write_text("# s\n## Ask\nmake a thing\n## Works means\n", encoding="utf-8")
    for n in ("progress.md", "rubric.md", "run.md"):
        (root / n).write_text("x\n", encoding="utf-8")
    data = {"project": "t", "features": [{"id": "F01", "priority": 1, "description": "d", "check": ["c"],
                                          "passes": passes, "evidence": evidence}]}
    if checker is not None:
        data["checker"] = checker
    (root / "features.json").write_text(json.dumps(data), encoding="utf-8")
    if checks:
        (root / "checks").mkdir()
        for name, body in checks.items():
            (root / "checks" / name).write_text(body, encoding="utf-8")
    return root


def run(root):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = cf.main(str(root))
    return rc, buf.getvalue()


CASES = [
    # (name, kwargs, expect_ok, text that must appear in output when failing)
    ("rejects pass with no verdict", dict(), False, "without a checker verdict"),
    ("accepts pass with PASS verdict", dict(checks={"F01-1.md": "PASS — loop closed\n"}), True, None),
    ("rejects pass when newest verdict is FAIL",
     dict(checks={"F01-1.md": "PASS — ok\n", "F01-2.md": "FAIL — gap 6 in\n"}), False, "is FAIL"),
    ("CAN'T CHECK is not a pass",
     dict(checks={"F01-1.md": "CAN'T CHECK — no model file\n"}), False, "is CAN'T CHECK"),
    ("CAN'T CHECK with passes false is fine",
     dict(passes=False, evidence="", checks={"F01-1.md": "CAN'T CHECK — no model file\n"}), True, None),
    ("rejects pass whose evidence does not point at checks/",
     dict(evidence="builder says ok", checks={"F01-1.md": "PASS — ok\n"}), False, "does not point"),
    ("three FAILs without stopped status is rejected",
     dict(passes=False, evidence="", checks={f"F01-{n}.md": "FAIL — still broken\n" for n in (1, 2, 3)}),
     False, "three-strikes"),
    ("three FAILs with stopped status is fine",
     dict(passes=False, evidence="", status="stopped: F01 failed 3 checks",
          checks={f"F01-{n}.md": "FAIL — still broken\n" for n in (1, 2, 3)}), True, None),
    ("attempt 10 is newer than attempt 9",
     dict(checks={"F01-9.md": "FAIL — x\n", "F01-10.md": "PASS — fixed\n"}), True, None),
    ("old folders without checker flag keep the old rule", dict(checker=None, evidence="test result"), True, None),
]


def main():
    bad = 0
    for name, kw, expect_ok, needle in CASES:
        with tempfile.TemporaryDirectory() as tmp:
            rc, out = run(make(tmp, **kw))
        ok = (rc == 0) == expect_ok and (needle is None or needle in out)
        bad += not ok
        print(("ok  " if ok else "BAD ") + name + ("" if ok else f"  -> rc={rc} out={out!r}"))
    print(f"{len(CASES) - bad}/{len(CASES)} fixtures passed")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
