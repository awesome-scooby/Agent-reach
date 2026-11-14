"""Run: cd property-research && python3 -m pytest perth/tests -q"""
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PERTH = HERE.parent
PR = PERTH.parent
REPO = PR.parent
sys.path.insert(0, str(PERTH))
sys.path.insert(0, str(PR))
import model_perth as mp  # noqa: E402


def uni():
    return json.loads((PERTH / "data" / "universe.json").read_text())


def test_universe_rule_is_applied():
    d = uni()
    for r in d["rows"]:
        if r["included"]:
            assert r["south"] and r["km"] <= 35.0, r
    names = {r["suburb"] for r in d["rows"] if r["included"]}
    for must in ("Armadale", "Gosnells", "Kelmscott", "Canning Vale", "Cannington", "Cockburn Central", "Success",
                 "Medina", "Bertram", "Wellard", "South Perth", "Como", "Victoria Park", "Byford"):
        assert must in names, must
    for out in ("Rockingham", "Baldivis", "Warnbro", "Nedlands", "Cottesloe", "North Fremantle"):
        assert out not in names, out
    assert d["meta"]["projected_crs"].startswith("GDA2020 / MGA zone 50")


def test_required_lgas_covered():
    lgas = {r["lga"] for r in uni()["rows"] if r["included"]}
    for l in ("Canning, City Of", "Gosnells, City Of", "Armadale, City Of", "Cockburn, City Of", "Kwinana, City Of", "South Perth, City Of"):
        assert l in lgas


def test_duty_python_matches_js():
    js = "const PF=require('./finance.js');console.log(JSON.stringify([550000,600000,650050,700000,800000,800001,950000].map(v=>PF.dutyFirstHome(v,'2026-11-14'))))"
    out = json.loads(subprocess.check_output(["node", "-e", js], cwd=PERTH))
    py = [round(mp.duty_fhor(v), 2) for v in (550000, 600000, 650050, 700000, 800000, 800001, 950000)]
    assert out == py


def test_ar1_reproducible_and_ordered():
    s = json.loads((PERTH / "data" / "abs_rppi_perth.json").read_text())["series"]
    x = [math.log(s[i][1] / s[i - 1][1]) for i in range(1, len(s))]
    f = mp.fit_ar1(x)
    a, b = mp.city_scenarios(f, math.log(0.943)), mp.city_scenarios(f, math.log(0.943))
    assert a == b
    for i in range(len(mp.POINTS)):
        assert a["bear"][i] <= a["base"][i] <= a["bull"][i]


def test_backtest_has_no_lookahead():
    """Fitting with data up to t must not change when later data changes."""
    s = json.loads((PERTH / "data" / "abs_rppi_perth.json").read_text())["series"]
    x = [math.log(s[i][1] / s[i - 1][1]) for i in range(1, len(s))]
    f1 = mp.fit_ar1(x[:30])
    x2 = x[:30] + [v * 3 for v in x[30:]]
    f2 = mp.fit_ar1(x2[:30])
    assert f1["phi"] == f2["phi"] and f1["drift"] == f2["drift"]


def test_model_output_invariants():
    m = json.loads((PERTH / "data" / "model.json").read_text())
    assert m["points"][-1] == "2036-10" and len(m["points"]) == 16
    for s in m["suburbs"]:
        if s["conf"] == "Insufficient":
            assert s["paths"] is None and s["comp"] is None, s["suburb"]
        if s["paths"]:
            for i in range(16):
                assert s["paths"]["bear"][i] <= s["paths"]["base"][i] <= s["paths"]["bull"][i], s["suburb"]
            assert 0.7 <= s["beta"] <= 1.5
        if s["h3"] is None:
            assert s["group_house"] == "Insufficient data"
    c = m["counts"]
    assert c["listings_verified"] is None and c["individual_sales_verified"] is None


def test_melbourne_page_rebuild_is_unchanged(tmp_path):
    """Regression: the existing shortlist page must rebuild byte-identical from its own data."""
    work = tmp_path / "repo"
    (work / "property-research").mkdir(parents=True)
    shutil.copy(PR / "build.py", work / "property-research" / "build.py")
    shutil.copy(PR / "template.html", work / "property-research" / "template.html")
    shutil.copytree(PR / "data", work / "property-research" / "data")
    subprocess.check_call([sys.executable, str(work / "property-research" / "build.py")], stdout=subprocess.DEVNULL)
    assert (work / "melbourne-perth-600k-shortlist.html").read_bytes() == (REPO / "melbourne-perth-600k-shortlist.html").read_bytes()


def test_perth_pipeline_does_not_touch_shared_files():
    out = subprocess.check_output(["git", "status", "--porcelain", "--", "property-research/data", "property-research/template.html",
                                   "property-research/build.py", "property-research/model.py", "property-research/collect.py",
                                   "property-research/hazards.py", "property-research/daily.py", "melbourne-perth-600k-shortlist.html"],
                                  cwd=REPO, text=True)
    assert out.strip() == "", out
