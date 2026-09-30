import csv, re
import build_outputs as B
rows = list(csv.DictReader(open("pain_points.csv")))
letter = lambda c: c.split()[0]
def evid(L):
    out = []
    for r in rows:
        if letter(r["cluster"]) != L: continue
        q = r["quote_under_25_words"].replace('"', '“', 1) if False else r["quote_under_25_words"]
        out.append(f'- "{q}" (r/{r["subreddit"]}, {r["source"]}, score {r["score"]}; {r["industry"]}) [link]({r["url"]})')
    return "\n".join(out)
GATE = {"M": "pass, with retaliation/verification caveats", "N": "**FAIL: obsolescence**", "A": "pass, with HIPAA/collections conditions", "C": "pass", "B": "**conditional**: fails if it collects debts",
        "G": "pass (avoid processor residuals)", "L": "pass, but no Reddit voice", "J": "pass, thin evidence",
        "F": "pass, thin evidence", "K": "pass, thin evidence", "H": "pass, no evidence", "I": "pass, no evidence",
        "D": "**FAIL: obsolescence**", "E": "**FAIL: crowded/AI-native, and the category you asked me not to anchor on**"}
tot = lambda n: B.total(B.CL[n][0])
names = sorted(B.CL, key=lambda n: -tot(n))
tbl = ["| Rank | Cluster | Score | Gate | Clients for $1M | Share of reachable market |", "|---|---|---|---|---|---|"]
for i, n in enumerate(names, 1):
    m = B.MATH[n[0]]; c = round(1e6 / m[0])
    tbl.append(f"| {i} | {n} | {tot(n)} | {GATE[n[0]]} | {c:,} | {100*c/m[2]:.2f}% |")
s = open("report_template.md").read().replace("<<NROWS>>", str(len(rows)))
s = s.replace("<<RANKING>>", "\n".join(tbl))
for n in names:
    L = n[0]
    s = s.replace(f"<<SCORE_{L}>>", str(tot(n)))
    for k, v in enumerate(B.CL[n][0], 1):
        s = s.replace(f"<<S {L} {k}>>", str(v))
    s = s.replace(f"<<EVID {L}>>", evid(L))
assert "<<" not in s, re.findall(r"<<[^>]+>>", s)[:5]
open("painkiller_report.md", "w").write(s)
print("ok", len(s.split()), "words")
