#!/usr/bin/env python3
"""Pull past-year Reddit posts (and later comment trees) from the Arctic Shift
public archive, because reddit.com blocks this environment. Resumable.

    python3 pull_archive.py posts              # all posts, past 365 days, per sub
    python3 pull_archive.py comments [N]       # comment trees for selected threads

Output (reddit_raw/):
    <sub>/posts_year.jsonl        one post per line
    <sub>/comments/<post_id>.json comment tree for selected posts
    _thread_selection.json        written by analyze step (post ids to fetch)
"""
import json, os, sys, time, urllib.parse, urllib.request, urllib.error

BASE = "https://arctic-shift.photon-reddit.com"
OUT = "reddit_raw"
SUBS = ["LawFirm", "Lawyertalk", "medicalbilling", "PracticeManagement", "privatepractice", "smallbusiness", "Entrepreneur", "sweatystartup", "Contractor", "HVAC",
        "electricians", "Plumbing", "restaurateur", "KitchenConfidential",
        "ecommerce", "FulfillmentByAmazon", "AmazonSeller", "landscaping",
        "Construction", "msp", "dentistry", "realtors", "propertymanagement",
        "trucking", "autorepair", "Accounting", "Bookkeeping"]
FIELDS = "id,subreddit,author,created_utc,title,selftext,score,num_comments,url,link_flair_text"
DELAY = 1.0


def get(path, params):
    url = f"{BASE}{path}?{urllib.parse.urlencode(params)}"
    for attempt in range(6):
        time.sleep(DELAY)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36", "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (400, 404):
                print(f"  HTTP {e.code}: {url[:150]}", file=sys.stderr)
                return None
            wait = 10 * (attempt + 1)
        except Exception:
            wait = 10 * (attempt + 1)
        print(f"  retry in {wait}s: {url[:120]}", file=sys.stderr)
        time.sleep(wait)
    return None


def pull_posts(subs=None):
    since = int(time.time()) - 365 * 86400
    for sub in (subs or SUBS):
        d = os.path.join(OUT, sub)
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, "posts_year.jsonl")
        done = os.path.join(d, "posts_year.done")
        if os.path.exists(done):
            continue
        seen, cursor = set(), since
        if os.path.exists(path):  # resume
            with open(path) as f:
                for line in f:
                    p = json.loads(line)
                    seen.add(p["id"])
                    cursor = max(cursor, p["created_utc"])
        n = len(seen)
        with open(path, "a") as f:
            while True:
                r = get("/api/posts/search", {"subreddit": sub, "after": cursor, "limit": 100,
                                              "sort": "asc", "fields": FIELDS})
                if r is None:
                    raise SystemExit(f"request failed for r/{sub} at cursor {cursor}; not marking done")
                rows = r.get("data") or []
                new = [p for p in rows if p["id"] not in seen]
                for p in new:
                    p["permalink"] = f"https://www.reddit.com/r/{p['subreddit']}/comments/{p['id']}/"
                    seen.add(p["id"])
                    f.write(json.dumps(p) + "\n")
                f.flush()
                n += len(new)
                if not rows:
                    break
                nxt = max(p["created_utc"] for p in rows)
                if nxt == cursor and not new:
                    cursor += 1
                else:
                    cursor = nxt
                if len(rows) < 100 and not new:
                    break
        open(done, "w").close()
        print(f"r/{sub}: {n} posts", flush=True)


def pull_comments(limit_note=None):
    sel = json.load(open(os.path.join(OUT, "_thread_selection.json")))
    total = sum(len(v) for v in sel.values())
    i = 0
    for sub, ids in sel.items():
        os.makedirs(os.path.join(OUT, sub, "comments"), exist_ok=True)
        for pid in ids:
            i += 1
            path = os.path.join(OUT, sub, "comments", f"{pid}.json")
            if os.path.exists(path):
                continue
            r = get("/api/comments/tree", {"link_id": f"t3_{pid}", "limit": 9999})
            if r is not None:
                with open(path, "w") as f:
                    json.dump(r, f)
            if i % 25 == 0:
                print(f"comments {i}/{total}", flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "posts":
        pull_posts(sys.argv[2:] or None)
    else:
        pull_comments()
