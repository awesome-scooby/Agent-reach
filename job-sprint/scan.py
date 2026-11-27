#!/usr/bin/env python3
"""Job Sprint scanner.

Pulls jobs from employer career feeds (Greenhouse + Workday public JSON, the
same endpoints the employers' own careers pages load), keeps Melbourne and
Perth roles, scores each against profile.json, and writes:

  out/jobs.json        every kept job, scored, newest first
  out/docs/<id>.json   one file per NEW job, shaped for the Job Sprint db
  out/writes.json      ArtifactData batch entries (<=50 per chunk) for new jobs

Usage:
  python3 scan.py                       # scan everything
  python3 scan.py --known known.json    # skip ids already in the db (JSON list)
  python3 scan.py --probe               # just test every feed answers

Uses Scrapling's Fetcher (curl_cffi browser impersonation) for HTTP.
"""
import argparse, datetime as dt, hashlib, html, json, re, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from scrapling.fetchers import Fetcher

HERE = Path(__file__).resolve().parent
FEEDS = json.loads((HERE / "feeds.json").read_text())
P = json.loads((HERE / "profile.json").read_text())
TODAY = dt.date.today().isoformat()


# ---------------------------------------------------------------- fetching
def get_json(url, method="GET", body=None):
    for attempt in range(2):
        try:
            r = (Fetcher.post(url, json=body, timeout=30, retries=1) if method == "POST"
                 else Fetcher.get(url, timeout=30, retries=1))
            if r.status == 200:
                return json.loads(r.body)
            return None
        except Exception:
            time.sleep(1.5)
    return None


def strip_html(s):
    s = html.unescape(s or "")
    s = re.sub(r"<(br|/p|/li|/h\d)[^>]*>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"[ \t\r\f\v]+", " ", s).strip()


def from_greenhouse(f):
    d = get_json(f"https://boards-api.greenhouse.io/v1/boards/{f['board']}/jobs?content=true")
    if d is None:
        return None
    out = []
    for j in d.get("jobs", []):
        out.append(dict(
            source="greenhouse:" + f["board"], company=f["company"], sector=f.get("sector", ""),
            title=j.get("title", "").strip(), location=(j.get("location") or {}).get("name", ""),
            url=j.get("absolute_url", ""), posted=(j.get("first_published") or j.get("updated_at") or "")[:10],
            text=strip_html(j.get("content", ""))[:6000], ext_id=str(j.get("id"))))
    return out


def from_workday(f):
    base = f"https://{f['host']}/wday/cxs/{f['tenant']}/{f['site']}"
    seen, rows, answered = set(), [], False
    for term in FEEDS.get("workday_terms", ["electrical"]):
        for offset in (0, 20, 40):
            d = get_json(base + "/jobs", "POST", {"appliedFacets": {}, "limit": 20, "offset": offset, "searchText": term + " Australia"})
            if d is None:
                break
            answered = True
            posts = d.get("jobPostings", [])
            for p in posts:
                path = p.get("externalPath")
                if path and path not in seen:
                    seen.add(path)
                    rows.append(p)
            if len(posts) < 20:
                break
    if not answered:
        return None
    out = []
    for p in rows:
        loc = p.get("locationsText", "")
        title = p.get("title", "").strip()
        # cheap pre-filter before fetching the detail page
        if city_of(loc + " " + p.get("externalPath", "").replace("-", " ")) is None and "locations" not in loc.lower():
            continue
        if role_tier(title)[0] == 0:
            continue
        det = get_json(base + p["externalPath"]) or {}
        info = det.get("jobPostingInfo", {})
        out.append(dict(
            source="workday:" + f["tenant"], company=f["company"], sector=f.get("sector", ""),
            title=title, location=info.get("location") or loc,
            url=info.get("externalUrl") or f"https://{f['host']}/{f['site']}{p['externalPath']}",
            posted=(info.get("startDate") or "")[:10],
            text=(strip_html(info.get("jobDescription", "")) + " " + (info.get("timeType") or ""))[:6000],
            ext_id=info.get("jobReqId") or p["externalPath"].rsplit("_", 1)[-1]))
    return out


def get_text(url):
    for attempt in range(2):
        try:
            r = Fetcher.get(url, timeout=30, retries=1)
            if r.status == 200:
                return r.body.decode("utf-8", "ignore") if isinstance(r.body, bytes) else str(r.body)
            return None
        except Exception:
            time.sleep(1.5)
    return None


def keep_early(title, loc):
    """Cheap filter before fetching a detail page: Australian city we score, and a role we score."""
    return city_of(loc) is not None and role_tier(title)[0] > 0


def from_oracle(f):
    """Oracle Recruiting Cloud public candidate-experience API (Downer, GHD, Honeywell)."""
    base = f"https://{f['host']}/hcmRestApi/resources/latest"
    seen, rows, answered = set(), [], False
    for term in FEEDS.get("oracle_terms", ["electrical"]):
        for offset in (0, 25, 50, 75):
            d = get_json(f"{base}/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList&finder=findReqs;"
                         f"siteNumber={f['site']},facetsList=NONE,limit=25,offset={offset},keyword={term.replace(' ', '%20')},location=Australia")
            if not d or not d.get("items"):
                break
            answered = True
            reqs = d["items"][0].get("requisitionList", [])
            for r in reqs:
                if r["Id"] not in seen:
                    seen.add(r["Id"]); rows.append(r)
            if len(reqs) < 25:
                break
    if not answered:
        return None
    out = []
    for r in rows:
        title, loc = r.get("Title", ""), r.get("PrimaryLocation", "")
        if not keep_early(title, loc):
            continue
        det = get_json(f"{base}/recruitingCEJobRequisitionDetails?expand=all&onlyData=true&finder=ById;Id=%22{r['Id']}%22,siteNumber={f['site']}") or {}
        di = (det.get("items") or [{}])[0]
        text = " ".join(strip_html(di.get(k) or "") for k in ("ExternalDescriptionStr", "ExternalResponsibilitiesStr", "ExternalQualificationsStr"))
        out.append(dict(source="oracle:" + f["site"], company=f["company"], sector=f.get("sector", ""), title=title,
                        location=loc, url=f"https://{f['host']}/hcmUI/CandidateExperience/en/sites/{f['site']}/job/{r['Id']}",
                        posted=r.get("PostedDate") or "", text=((r.get("ShortDescriptionStr") or "") + " " + text)[:6000], ext_id=r["Id"]))
    return out


def from_amazon(f):
    seen, out, answered = set(), [], False
    for term in f.get("terms", ["data center"]):
        d = get_json("https://www.amazon.jobs/en/search.json?base_query=" + term.replace(" ", "%20") +
                     "&normalized_country_code%5B%5D=AUS&result_limit=100")
        if d is None:
            continue
        answered = True
        for j in d.get("jobs", []):
            if j["id_icims"] in seen:
                continue
            seen.add(j["id_icims"])
            text = strip_html(" ".join(j.get(k) or "" for k in ("description_short", "basic_qualifications", "preferred_qualifications")))
            out.append(dict(source="amazon", company="Amazon / AWS", sector=f.get("sector", ""), title=j["title"],
                            location=j.get("normalized_location", ""), url="https://www.amazon.jobs" + j["job_path"],
                            posted=j.get("posted_date", ""), text=text[:6000], ext_id=j["id_icims"]))
    return out if answered else None


def from_smartrecruiters(f):
    d = get_json(f"https://api.smartrecruiters.com/v1/companies/{f['id']}/postings?country=au&limit=100")
    if d is None:
        return None
    out = []
    for j in d.get("content", []):
        loc = ", ".join(x for x in (j["location"].get("city"), j["location"].get("region"), "Australia") if x)
        if not keep_early(j["name"], loc):
            continue
        det = get_json(f"https://api.smartrecruiters.com/v1/companies/{f['id']}/postings/{j['id']}") or {}
        secs = (det.get("jobAd") or {}).get("sections") or {}
        text = " ".join(strip_html((secs.get(k) or {}).get("text", "")) for k in ("jobDescription", "qualifications"))
        out.append(dict(source="smartrecruiters:" + f["id"], company=f["company"], sector=f.get("sector", ""), title=j["name"],
                        location=loc, url=f"https://jobs.smartrecruiters.com/{f['id']}/{j['id']}",
                        posted=(j.get("releasedDate") or "")[:10], text=text[:6000], ext_id=j["id"]))
    return out


def from_pageup(f):
    page = get_text(f"https://careers.pageuppeople.com/{f['id']}/{f['site']}/en/listing/")
    if page is None:
        return None
    out = []
    for blk in page.split('class="job-listing-title"')[1:]:
        m = re.search(r'href="([^"]+)">([^<]+)</a>', blk)
        if not m:
            continue
        loc = re.search(r'class="location">([^<]*)<', blk)
        desc = re.search(r"<p>(.*?)</p>", blk, re.S)
        out.append(dict(source="pageup:" + f["id"], company=f["company"], sector=f.get("sector", ""), title=html.unescape(m.group(2)).strip(),
                        location=(loc.group(1) if loc else "").replace("Aus - ", "") + ", Australia",
                        url="https://careers.pageuppeople.com" + m.group(1), posted="",
                        text=strip_html(desc.group(1) if desc else ""), ext_id=m.group(1).split("/job/")[-1].split("/")[0]))
    return out


# ---------------------------------------------------------------- scoring
def has(text, terms):
    return [t for t in terms if t in text]


def city_of(loc):
    l = " " + loc.lower() + " "
    for city, terms in P["cities"].items():
        if any(t in l for t in terms):
            return city
    return None


def role_tier(title):
    t = title.lower()
    for tier in P["role_tiers"]:
        if any(p in t for p in tier["patterns"]):
            return tier["pts"], tier["label"]
    return 0, ""


MONEY = re.compile(r"\$\s?(\d{2,3}(?:[,.]\d{3})?)\s?(k|K|,000)?(?:\s?(?:-|–|to)\s?\$?\s?(\d{2,3}(?:[,.]\d{3})?)\s?(k|K|,000)?)?")


def parse_salary(text):
    """Return (low, high, is_package, raw) in dollars per year, or None."""
    best = None
    for m in MONEY.finditer(text):
        def num(v, k):
            if not v:
                return None
            n = float(v.replace(",", "").replace(".", "")) if ("," in v or "." in v) and len(v) > 4 else float(v.replace(",", ""))
            if k or n < 1000:
                n *= 1000
            return n
        lo, hi = num(m.group(1), m.group(2)), num(m.group(3), m.group(4) or m.group(2))
        hi = hi or lo
        if not lo or lo < 60000 or hi > 450000:
            continue  # hourly rates, allowances, project values
        ctx = text[max(0, m.start() - 60): m.end() + 80].lower()
        pkg = any(w in ctx for w in ("package", "incl", "inclusive", "total", "tfr", "trp", "including super"))
        best = (lo, hi, pkg, text[m.start(): m.end()].strip())
        break
    return best


def score(job):
    title, text = job["title"], job.get("text", "")
    blob = (title + " " + text).lower()
    reasons, flags = [], []
    pts, label = role_tier(title)
    if pts == 0:
        return None
    reasons.append(f"{label} (+{pts})")

    sec = [t for t in P["sector_terms"] if re.search(r"(?<![a-z])" + re.escape(t.strip()) + r"(?![a-z])", blob)]
    s_pts = min(20, 5 * len(set(sec)))
    if job.get("sector") in ("data centre", "HV / grid", "BESS"):
        s_pts = max(s_pts, 12)
    if s_pts:
        reasons.append(f"Sector: {', '.join(sorted(set(s.strip() for s in sec))[:4]) or job['sector']} (+{s_pts})")
    pts += s_pts

    city = city_of(job["location"]) or city_of(title)
    if city is None:
        return None
    l_pts = P.get("city_points", {}).get(city, 8)
    reasons.append(f"{city} (+{l_pts})")
    pts += l_pts

    t = title.lower()
    if has(t, P["junior_terms"]) or has(" " + t + " ", P.get("exclude_terms", [])):
        return None
    if has(t + " ", P.get("off_discipline_terms", [])):
        pts -= 25; flags.append("Different discipline (not electrical)")
    if has(t, P["too_senior_terms"]):
        pts += 2; flags.append("Very senior: stretch")
    elif has(t, P["senior_terms"]):
        pts += 10; reasons.append("Senior level (+10)")
    else:
        pts += 6

    sal = parse_salary(title + " " + text)
    if sal:
        lo, hi, pkg, raw = sal
        hi_pkg = hi if pkg else hi * (1 + P["super_rate"])
        job["salary"] = raw + (" (package)" if pkg else " (+ super)")
        job["salary_pkg_high"] = round(hi_pkg)
        if hi_pkg >= P["floor_package"]:
            pts += 15; reasons.append(f"Pay clears ${P['floor_package']//1000}k pkg floor (+15)")
        else:
            flags.append(f"Pay cut risk: tops out ~${round(hi_pkg/1000)}k pkg")
    else:
        pts += 7; reasons.append("Pay not stated (+7)")

    if has(blob, P["contract_terms"]):
        pts -= 5; flags.append("Contract / fixed-term")
    if has(blob, P["fifo_terms"]):
        flags.append("FIFO / roster")

    pts = max(0, min(100, pts))
    job.update(city=city, score=pts, reasons=reasons, flags=flags,
               grade="A" if pts >= 80 else "B" if pts >= 65 else "C" if pts >= 50 else "D")
    return job


def job_id(job):
    key = job["source"] + "|" + (job.get("ext_id") or job["url"])
    return "j" + hashlib.sha1(key.encode()).hexdigest()[:12]


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--known", help="JSON list of job ids already in the db")
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--min-score", type=int, default=45)
    a = ap.parse_args()

    fn = {"greenhouse": from_greenhouse, "workday": from_workday, "oracle": from_oracle, "amazon": from_amazon,
          "smartrecruiters": from_smartrecruiters, "pageup": from_pageup}
    tasks = [(k, f) for k in fn for f in FEEDS.get(k, [])]
    with ThreadPoolExecutor(8) as ex:
        results = list(ex.map(lambda t: (t, fn[t[0]](t[1])), tasks))

    sources, raw = {}, []
    for (kind, f), rows in results:
        sources[f["company"]] = "down" if rows is None else len(rows)
        raw += rows or []
    if a.probe:
        print(json.dumps(sources, indent=1)); return

    kept, seen = [], set()
    for j in raw:
        s = score(dict(j))
        if not s or s["score"] < a.min_score:
            continue
        s["id"] = job_id(s)
        if s["id"] in seen:
            continue
        seen.add(s["id"])
        kept.append(s)
    kept.sort(key=lambda j: (-j["score"], j["title"]))

    known = set(json.loads(Path(a.known).read_text())) if a.known else set()
    out = HERE / "out"; (out / "docs").mkdir(parents=True, exist_ok=True)
    for old in (out / "docs").glob("*.json"):
        old.unlink()
    (out / "jobs.json").write_text(json.dumps(kept, indent=1))

    writes = []
    for j in kept:
        if j["id"] in known:
            continue
        doc = {k: j.get(k) for k in ("title", "company", "location", "city", "url", "source", "sector", "posted",
                                     "score", "grade", "reasons", "flags", "salary", "salary_pkg_high")}
        doc["summary"] = j.get("text", "")[:900]
        doc["firstSeen"] = TODAY
        p = out / "docs" / f"{j['id']}.json"
        p.write_text(json.dumps(doc))
        writes.append({"op": "set", "collection": "jobs", "doc_id": j["id"], "file_path": str(p)})
    chunks = [writes[i:i + 50] for i in range(0, len(writes), 50)]
    (out / "writes.json").write_text(json.dumps(chunks, indent=1))
    meta = {"lastRun": dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes"), "sources": sources,
            "kept": len(kept), "new": len(writes), "topNew": [
                {"title": j["title"], "company": j["company"], "score": j["score"]} for j in kept
                if j["id"] not in known and j["score"] >= 75][:5]}
    (out / "meta.json").write_text(json.dumps(meta, indent=1))
    print(json.dumps(meta, indent=1))


if __name__ == "__main__":
    sys.exit(main())
