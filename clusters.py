#!/usr/bin/env python3
"""Cluster definitions (tight regexes) + counting. Amazon subs are excluded by request.

    python3 clusters.py counts
    python3 clusters.py show <cluster> [n]     # top posts w/ verified <25-word quotes
"""
import json, re, sys, collections
import analyze_posts as A

EXCLUDE_SUBS = {"amazonseller", "fulfillmentbyamazon"}

# name -> (regex, industries note)
CLUSTERS = {
 "AR-late-payment": (r"(customer|client|gc|contractor|company|account)s?\b.{0,40}(owes? me|not paying|won'?t pay|refus\w+ to pay|stopped (replying|responding|answering)|ghost\w*)|unpaid invoices?|chasing (payment|invoices?|clients? for)|(45|60|90) days? (late|past due|overdue)|past due invoices?", "any B2B/service"),
 "chargebacks-disputes": (r"chargebacks?|payment dispute|disputed (the )?charge|stripe (held|holding|froze|frozen)|paypal (held|holding|froze|limited)|merchant account (closed|terminated|frozen)|reserve held", "ecommerce, services, restaurants"),
 "processing-fees": (r"processing fees?|\binterchange\b|merchant (services|statement)|credit card fees?|surcharg\w+.{0,20}(card|credit)|\\bsquare fees?\\b|\\btoast fees?\\b|\\bclover fees?\\b", "restaurants, retail, services"),
 "lost-billable-time": (r"(lost|missed|forgot|forget|slip|unbilled|un-billed|write[- ]?offs?).{0,60}(billable|billing|hours|time entries|time)|can'?t prove (how long|the time|hours)|timekeeping|time tracking.{0,30}(forget|miss)", "law, consulting, agencies, trades"),
 "vendor-COI-compliance-tracking": (r"\bcois?\b|certificate of insurance|insurance expir|license expir|track(ing)? (vendor|sub|subcontractor)s?.{0,30}(insurance|licen)|prequal\w*|isnetworld|avetta|safety (paperwork|documentation|program)", "contractors, property mgmt"),
 "insurance-claims-denials": (r"claims? (denied|denial|rejected|was denied)|denied claims?|downcod\w+|underpa(id|yment|y)|eob\b|prior auth\w*|credentialing|clearinghouse|billing (backlog|company)|ar days|accounts receivable.{0,20}(aging|old|90)", "dental, medical, chiropractic, vet"),
 "missed-calls-intake-leakage": (r"missed calls?|voicemail|answering service|receptionist|no[- ]?shows?|intake.{0,30}(lost|missing|phone|calls?)|leads? (go|going|goes) cold|never (call|called|got back)", "law, medical, trades, home services"),
 "permits-inspection-delays": (r"permit.{0,50}(delay|weeks|months|nightmare|backlog|waiting|stuck)|inspection.{0,30}(delay|backlog|reschedul)|waiting on (the )?(city|county|permit)", "contractors, electricians, plumbers"),
 "tax-payroll-notices-penalties": (r"irs (notice|letter|penalt\w+)|payroll tax(es)?.{0,20}(penalt|notice|behind|owed)|sales tax.{0,30}(nexus|audit|penalt|notice)|penalt(y|ies).{0,30}(late|filing|1099|941)|state (tax )?notice", "any small business"),
 "vendor-price-creep-invoice-errors": (r"invoice (error|discrepanc\w+|mistake)|shorted|credit memo|price (creep|gouging)|overcharg\w+|billed (twice|incorrectly|wrong)|double[- ]?billed|duplicate (charge|payment|invoice)", "restaurants, retail, MSP, contractors"),
 "warranty-claims": (r"warranty (claim|labor|reimburse\w*|pay(ment|s|ing)?)|claim.{0,20}warranty|manufacturer.{0,40}(won'?t|not|refus\w+).{0,20}(pay|cover|reimburse)", "HVAC, plumbing, auto repair, appliances"),
 "delivery-app-disputes": (r"(doordash|uber ?eats|grubhub).{0,80}(refund|dispute|charge|missing|error|chargeback|fee)", "restaurants"),
 "carrier-refunds-shipping-claims": (r"(ups|fedex|usps|dhl).{0,60}(refund|claim|late|guarantee|adjustment|audit|overcharg)|late delivery refund|parcel audit|dimensional weight|shipping insurance claim", "ecommerce, small shippers"),
 "coop-funds-mdf": (r"co-?op (funds?|advertising|marketing|dollars)|market development funds?|manufacturer.{0,20}rebates?.{0,20}(dealer|claim)", "dealers, distributors"),
 "utility-bills": (r"utility bill|electric bill.{0,30}(high|error|wrong|overcharg)|demand charges?|water bill.{0,20}(error|wrong|high)|energy audit", "restaurants, retail, facilities"),
 "software-license-vendor-billing": (r"license (true[- ]?up|audit)|microsoft.{0,30}(bill|license|csp).{0,30}(wrong|error|overcharg)|vendor billing|reconcil\w+.{0,20}(distributor|vendor) invoices?", "MSPs"),
 "customer-refund-abuse-fraud": (r"refund abuse|return fraud|fraudulent (returns?|refunds?)|friendly fraud|empty box|item not received.{0,20}(claim|scam)", "ecommerce, retail"),
 "rent-collection-evictions": (r"late rent|evict\w+|delinquent tenants?|security deposit disput\w+|not paying rent", "property management"),
 "trucking-detention-broker-pay": (r"detention (pay|time|charge)|broker.{0,30}(short|not pay|won'?t pay|slow)|quick ?pay|factoring (fee|company)|lumper", "trucking"),
 "government-contract-bid-paperwork": (r"certified payroll|prevailing wage|\brfp\b|bid (docs|package)|sam\.gov|sbir|8\(a\)|minority[- ]owned certification", "contractors, small vendors"),
}
RX = {k: re.compile(v[0], re.I) for k, v in CLUSTERS.items()}


def posts():
    for p in A.load():
        if p["subreddit"].lower() in EXCLUDE_SUBS:
            continue
        yield p


def quote(p, rx, maxw=24):
    """Return a <=24-word sentence-ish window around the match, verbatim from the post text."""
    t = " ".join(A.text(p).split())
    m = rx.search(t)
    if not m:
        return None
    start = max(t.rfind(". ", 0, m.start()), t.rfind("? ", 0, m.start()), t.rfind("! ", 0, m.start()))
    start = 0 if start < 0 else start + 2
    words = t[start:].split()
    pre = len(t[start:m.start()].split())
    if pre > maxw - 6:
        words = words[pre - 8:]
    q = " ".join(words[:maxw])
    assert q in t
    return q


if __name__ == "__main__":
    if sys.argv[1] == "counts":
        stat = collections.defaultdict(lambda: {"n": 0, "subs": collections.Counter(), "big": 0, "cm": 0})
        for p in posts():
            t = A.text(p)
            for k, rx in RX.items():
                if rx.search(t):
                    s = stat[k]; s["n"] += 1; s["subs"][p["subreddit"]] += 1
                    s["big"] += p.get("num_comments", 0) >= 20; s["cm"] += p.get("num_comments", 0)
        for k, s in sorted(stat.items(), key=lambda x: -x[1]["n"]):
            top = ",".join(f"{a}:{b}" for a, b in s["subs"].most_common(4))
            print(f"{k:38s} posts={s['n']:5d} subs={len(s['subs']):2d} >=20c={s['big']:4d}  {top}")
    elif sys.argv[1] == "show":
        k, n = sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 12
        rx = RX[k]
        hits = [p for p in posts() if rx.search(A.text(p))]
        hits.sort(key=lambda p: -(p.get("num_comments", 0) * 2 + p.get("score", 0)))
        print(f"## {k}: {len(hits)} posts")
        for p in hits[:n]:
            print(f"- r/{p['subreddit']} {p['permalink']} sc={p.get('score')} c={p.get('num_comments')}\n  T: {p['title'][:120]}\n  Q: {quote(p, rx)}")
