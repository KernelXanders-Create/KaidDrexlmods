"""Write RETURN_MANIFEST.md: every file in RETURN/, its sha256, and what it is."""
import hashlib
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DESC = {
    "SUMMARY.md": "1-page summary for Miran: pick one per map",
    "QUESTIONS.md": "Design forks with recommended defaults",
    "REFERENCES.md": "Canon settings + real-world landform teachers, with links",
    "RISKS.md": "Engine risks per concept + proposed tests",
    "README.md": "How to rerun the tools",
}


def describe(rel):
    b = os.path.basename(rel)
    if b in DESC:
        return DESC[b]
    if b.startswith("concept_"):
        return f"Concept {b[8]} write-up (PROPOSED)"
    if b.startswith("plan_"):
        return f"Plan-view sketch, concept {b[5]} (PROPOSED, for choosing)"
    if b.startswith("objectives_"):
        return "Objective network JSON (schema per 05_RETURN_FORMAT)"
    if b.startswith("stats_"):
        return "MEASURED sketch stats (areas, gaps, depths)"
    if b.startswith("validation"):
        return "MEASURED house-rule checks per op"
    if b.endswith(".py"):
        return "Python used to make the sketches"
    return ""


rows = []
for dp, dn, fn in os.walk(ROOT):
    dn[:] = sorted(d for d in dn if d != "__pycache__")
    for f in sorted(fn):
        rel = os.path.relpath(os.path.join(dp, f), ROOT)
        if rel == "RETURN_MANIFEST.md":
            continue
        h = hashlib.sha256(open(os.path.join(dp, f), "rb").read()).hexdigest()
        rows.append(f"| `{rel}` | `{h}` | {describe(rel)} |")
with open(os.path.join(ROOT, "RETURN_MANIFEST.md"), "w") as fh:
    fh.write("# RETURN manifest (Kernel Stage A)\n\nsha256 of every file in RETURN/ "
             "(this manifest excluded). Regenerate with `python3 tools/make_manifest.py`.\n\n"
             "| File | sha256 | What it is |\n|---|---|---|\n" + "\n".join(rows) + "\n")
print(len(rows), "files")
