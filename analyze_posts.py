#!/usr/bin/env python3
"""Load pulled posts, flag pain-related ones, and emit ranked candidates.

Usage:
    python3 analyze_posts.py stats
    python3 analyze_posts.py grep "regex" [--sub SUB] [--min-comments N] [--n 40]
    python3 analyze_posts.py select [N_PER_SUB]   # writes reddit_raw/_thread_selection.json
"""
import glob, json, os, re, sys, time

RAW = "reddit_raw"
PHRASES = ["biggest headache", "losing money", "lose money", "i hate dealing with", "waste of time",
           "nightmare", "would pay", "owed", "chasing", "chase", "overcharged", "overcharge",
           "deadline", "paperwork", "claim denied", "denied", "refund", "reimburse", "compliance",
           "chargeback", "dispute", "warranty", "unpaid", "not paid", "late payment", "invoice",
           "fees", "audit", "penalt", "fine ", "back office", "admin"]
PAIN_RE = re.compile("|".join(re.escape(p) for p in PHRASES), re.I)


def load(sub=None):
    for path in glob.glob(f"{RAW}/*/posts_year.jsonl"):
        s = os.path.basename(os.path.dirname(path))
        if sub and s.lower() != sub.lower():
            continue
        with open(path) as f:
            for line in f:
                try:
                    p = json.loads(line)
                except json.JSONDecodeError:
                    continue
                p["subreddit"] = p.get("subreddit") or s
                yield p


def text(p):
    return f"{p.get('title','')}\n{p.get('selftext','') or ''}"


def snippet(p, rx, width=110):
    t = " ".join(text(p).split())
    m = rx.search(t)
    if not m:
        return t[:2 * width]
    a = max(0, m.start() - width)
    return t[a:m.end() + width]


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "stats":
        per = {}
        for p in load():
            d = per.setdefault(p["subreddit"], [0, 0, 0])
            d[0] += 1
            d[1] += bool(PAIN_RE.search(text(p)))
            d[2] += p.get("num_comments", 0) >= 20
        for s, (n, pn, c) in sorted(per.items(), key=lambda x: -x[1][0]):
            print(f"{s:22s} posts={n:6d} pain_match={pn:6d} >=20cmts={c:5d}")
    elif cmd == "grep":
        rx = re.compile(sys.argv[2], re.I)
        args = sys.argv[3:]
        sub = args[args.index("--sub") + 1] if "--sub" in args else None
        minc = int(args[args.index("--min-comments") + 1]) if "--min-comments" in args else 0
        n = int(args[args.index("--n") + 1]) if "--n" in args else 40
        hits = [p for p in load(sub) if rx.search(text(p)) and p.get("num_comments", 0) >= minc]
        hits.sort(key=lambda p: -(p.get("num_comments", 0) * 2 + p.get("score", 0)))
        print(f"{len(hits)} hits")
        for p in hits[:n]:
            print(f"- r/{p['subreddit']} | {p['permalink']} | sc={p.get('score')} c={p.get('num_comments')}")
            print(f"  T: {p['title'][:140]}")
            print(f"  S: {snippet(p, rx)}")
    elif cmd == "select":
        k = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        sel = {}
        for path in glob.glob(f"{RAW}/*/posts_year.jsonl"):
            s = os.path.basename(os.path.dirname(path))
            ps = [p for p in load(s) if p.get("num_comments", 0) >= 20 and PAIN_RE.search(text(p))]
            ps.sort(key=lambda p: -p["num_comments"])
            sel[s] = [p["id"] for p in ps[:k]]
        json.dump(sel, open(f"{RAW}/_thread_selection.json", "w"))
        print({s: len(v) for s, v in sel.items()})
