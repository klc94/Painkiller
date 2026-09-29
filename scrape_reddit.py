#!/usr/bin/env python3
"""Scrape Reddit pain-point data into ./reddit_raw/ (raw JSON, resumable).

Standard library only (Python 3.8+). Run:

    python3 scrape_reddit.py                 # everything
    python3 scrape_reddit.py --subs HVAC msp # subset
    python3 scrape_reddit.py --no-comments   # listings/search only
    python3 scrape_reddit.py --min-comments 20 --delay 2

Layout written under reddit_raw/:
    <sub>/top_year.json                 top posts, past year (limit 100)
    <sub>/search__<term>__<sort>.json   search (past year), sort = top | comments
    <sub>/comments/<post_id>.json       full comment thread for posts w/ >= N comments
    _errors.log                         every failed request

Every file already on disk is skipped, so re-running resumes where it stopped
and nothing is ever re-fetched. Delete a file to force a re-fetch.

Strategy per request: try www.reddit.com/*.json first; on 403/blocked/non-JSON
fall back to old.reddit.com HTML (parsed into the same {"data": {"children": ...}}
shape, flagged with "_source": "old.reddit.com-html"). 429s back off and retry.

NOTE: the HTML fallback parser is best-effort and was written without live
access to Reddit; check a few output files after the first run.
"""
import argparse
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

SUBREDDITS = [
    "smallbusiness", "Entrepreneur", "sweatystartup", "Contractor", "HVAC",
    "electricians", "Plumbing", "restaurateur", "KitchenConfidential",
    "ecommerce", "FulfillmentByAmazon", "AmazonSeller", "landscaping",
    "Construction", "msp", "dentistry", "realtors", "propertymanagement",
    "trucking", "autorepair", "Accounting", "Bookkeeping",
]

SEARCH_TERMS = [
    "biggest headache", "losing money", "I hate dealing with", "waste of time",
    "nightmare", "would pay someone", "owed money", "chasing", "overcharged",
    "deadline", "paperwork", "claim denied", "refund", "reimbursement",
    "compliance",
]
SEARCH_SORTS = ["top", "comments"]

OUT = "reddit_raw"
DELAY = 2.0
_last_request = 0.0


def log_error(msg):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "_errors.log"), "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
    print("  !", msg, file=sys.stderr)


def slug(s):
    return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_").lower()


def http_get(url, accept="application/json"):
    """GET with rate limit + 429/5xx backoff. Returns (status, body_text)."""
    global _last_request
    for attempt in range(5):
        wait = DELAY - (time.time() - _last_request)
        if wait > 0:
            time.sleep(wait)
        _last_request = time.time()
        req = urllib.request.Request(url, headers={
            "User-Agent": UA, "Accept": accept, "Accept-Language": "en-US,en;q=0.9"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace") if e.fp else ""
            if e.code in (429, 500, 502, 503, 504):
                retry = e.headers.get("Retry-After")
                sleep = int(retry) if retry and retry.isdigit() else 10 * (2 ** attempt)
                print(f"  {e.code} on {url}; sleeping {sleep}s", file=sys.stderr)
                time.sleep(sleep)
                continue
            return e.code, body
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if attempt >= 1:  # blocked/unreachable: don't hang for minutes
                print(f"  network error {e!r}; giving up on {url}", file=sys.stderr)
                break
            sleep = 5
            print(f"  network error {e!r}; sleeping {sleep}s", file=sys.stderr)
            time.sleep(sleep)
    return 0, ""


def get_json(url):
    status, body = http_get(url)
    if status == 200:
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            pass
    return None


# ---------------------------------------------------------------- HTML fallback

def _attr(tag_html, name):
    m = re.search(r'\b%s="([^"]*)"' % re.escape(name), tag_html)
    return html.unescape(m.group(1)) if m else None


def parse_old_listing(page):
    """Parse an old.reddit.com listing/search page into Reddit-JSON-like children."""
    children = []
    for m in re.finditer(r'<div class="[^"]*\bthing\b[^"]*"[^>]*data-fullname="t3_[^"]*"[^>]*>', page):
        tag = m.group(0)
        chunk = page[m.end(): m.end() + 4000]
        title_m = re.search(r'<a class="title[^"]*"[^>]*>(.*?)</a>', chunk, re.S)
        perma = _attr(tag, "data-permalink")
        fullname = _attr(tag, "data-fullname") or ""
        children.append({"kind": "t3", "data": {
            "id": fullname.replace("t3_", ""),
            "subreddit": _attr(tag, "data-subreddit"),
            "author": _attr(tag, "data-author"),
            "permalink": perma,
            "url": _attr(tag, "data-url"),
            "score": int(_attr(tag, "data-score") or 0),
            "num_comments": int(_attr(tag, "data-comments-count") or 0),
            "created_utc": int(_attr(tag, "data-timestamp") or 0) // 1000,
            "title": html.unescape(re.sub(r"<[^>]+>", "", title_m.group(1))) if title_m else "",
            "selftext": "",  # only available on the thread page
        }})
    after = None
    nm = re.search(r'<span class="next-button"><a href="([^"]+)"', page)
    if nm:
        am = re.search(r"[?&]after=([^&\"]+)", html.unescape(nm.group(1)))
        after = am.group(1) if am else None
    return {"_source": "old.reddit.com-html",
            "data": {"children": children, "after": after}}


class _ThreadParser(HTMLParser):
    """Extract selftext + flat comment list from an old.reddit thread page."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.comments, self.selftext = [], []
        self._stack = []          # (tag, role)
        self._cur = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class", "") or ""
        role = None
        if tag == "div" and "thing" in cls.split() and "comment" in cls.split():
            self._cur = {"id": (a.get("data-fullname") or "").replace("t1_", ""),
                         "author": a.get("data-author"),
                         "permalink": a.get("data-permalink"),
                         "score": None, "body": []}
            self.comments.append(self._cur)
            role = "comment"
        elif tag == "div" and "md" in cls.split():
            role = "md_comment" if self._cur is not None and self._in("comment") else "md_post"
        self._stack.append((tag, role))

    def _in(self, role):
        return any(r == role for _, r in self._stack)

    def handle_endtag(self, tag):
        while self._stack:
            t, r = self._stack.pop()
            if t == tag:
                if r == "comment":
                    self._cur = None
                break

    def handle_data(self, data):
        if self._in("md_comment") and self._cur is not None:
            self._cur["body"].append(data)
        elif self._in("md_post") and not self._in("comment"):
            self.selftext.append(data)


def parse_old_thread(page, post_id):
    p = _ThreadParser()
    p.feed(page)
    comments = [{"kind": "t1", "data": {
        "id": c["id"], "author": c["author"], "permalink": c["permalink"],
        "body": " ".join("".join(c["body"]).split())}} for c in p.comments]
    post = {"kind": "t3", "data": {"id": post_id,
            "selftext": " ".join("".join(p.selftext[:200]).split())}}
    return {"_source": "old.reddit.com-html",
            "post": post, "comments_flat": comments}


# ---------------------------------------------------------------- fetch helpers

def fetch_listing(www_url, old_url):
    data = get_json(www_url)
    if data and "data" in data:
        return data
    status, body = http_get(old_url, accept="text/html")
    if status == 200 and "thing" in body:
        return parse_old_listing(body)
    log_error(f"listing failed: {www_url} (old status {status})")
    return None


def save(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f)
    os.replace(tmp, path)


def scrape_sub(sub, args):
    base = os.path.join(OUT, sub)
    print(f"\n=== r/{sub}")

    # 1. top of the past year
    path = os.path.join(base, "top_year.json")
    if not os.path.exists(path):
        q = "t=year&limit=100"
        d = fetch_listing(f"https://www.reddit.com/r/{sub}/top.json?{q}&raw_json=1",
                          f"https://old.reddit.com/r/{sub}/top/?t=year&limit=100")
        if d:
            save(path, d)

    # 2. searches
    for term in SEARCH_TERMS:
        for sort in SEARCH_SORTS:
            path = os.path.join(base, f"search__{slug(term)}__{sort}.json")
            if os.path.exists(path):
                continue
            qs = urllib.parse.urlencode({"q": f'"{term}"', "restrict_sr": 1, "t": "year",
                                         "sort": sort, "limit": 100, "raw_json": 1})
            old_qs = urllib.parse.urlencode({"q": f'"{term}"', "restrict_sr": "on", "t": "year",
                                             "sort": sort})
            d = fetch_listing(f"https://www.reddit.com/r/{sub}/search.json?{qs}",
                              f"https://old.reddit.com/r/{sub}/search/?{old_qs}")
            if d:
                save(path, d)
            print(f"  search {term!r} / {sort}")

    if args.no_comments:
        return

    # 3. comment threads for every post with >= min_comments
    posts = {}
    for fn in os.listdir(base):
        if fn.endswith(".json") and (fn.startswith("search__") or fn == "top_year.json"):
            with open(os.path.join(base, fn)) as f:
                try:
                    d = json.load(f)
                except json.JSONDecodeError:
                    continue
            for c in d.get("data", {}).get("children", []):
                pd = c.get("data", {})
                if pd.get("id") and pd.get("num_comments", 0) >= args.min_comments:
                    posts[pd["id"]] = pd
    todo = sorted(posts.values(), key=lambda p: -p["num_comments"])
    print(f"  {len(todo)} threads with >= {args.min_comments} comments")
    for i, pd in enumerate(todo, 1):
        path = os.path.join(base, "comments", f"{pd['id']}.json")
        if os.path.exists(path):
            continue
        d = get_json(f"https://www.reddit.com/r/{sub}/comments/{pd['id']}.json"
                     f"?limit=500&sort=top&raw_json=1")
        if not (isinstance(d, list) and len(d) == 2):
            status, body = http_get(
                f"https://old.reddit.com/r/{sub}/comments/{pd['id']}/?limit=500&sort=top",
                accept="text/html")
            if status == 200:
                d = parse_old_thread(body, pd["id"])
            else:
                log_error(f"thread failed: {pd['id']} ({pd.get('permalink')}) status {status}")
                continue
        save(path, d)
        if i % 10 == 0:
            print(f"  threads {i}/{len(todo)}")


def main():
    global OUT, DELAY
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--subs", nargs="+", default=SUBREDDITS)
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--delay", type=float, default=DELAY, help="seconds between requests")
    ap.add_argument("--min-comments", type=int, default=20)
    ap.add_argument("--no-comments", action="store_true")
    args = ap.parse_args()
    OUT, DELAY = args.out, args.delay

    # quick reachability check so a blocked network fails loudly, not silently
    status, _ = http_get("https://www.reddit.com/r/smallbusiness/top.json?limit=1")
    status_old, _ = http_get("https://old.reddit.com/r/smallbusiness/", accept="text/html")
    if status != 200 and status_old != 200:
        sys.exit(f"Reddit unreachable (www={status}, old={status_old}). "
                 "Check network/proxy policy before running.")

    for sub in args.subs:
        scrape_sub(sub, args)
    print("\nDone. Failures (if any) are in", os.path.join(OUT, "_errors.log"))


if __name__ == "__main__":
    main()
