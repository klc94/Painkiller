# Painkiller report: which business problem to build a service around

## 0. Read this first: what this evidence is and is not

**Where the data came from.** Reddit blocks this server (403 on `www.reddit.com`, `old.reddit.com`, `api.reddit.com` and the OAuth host), so I could not use the Reddit JSON endpoints you specified. I pulled the same subreddits from the **Arctic Shift public Reddit archive** instead. Every post keeps its real ID and Reddit link, and every quote below was checked as an exact substring of the pulled text. But it is not a direct Reddit scrape, and two differences matter:

- The archive stores scores and comment counts as of about when each post was ingested, not final values. Ranking by "top of the year" is approximate.
- It cannot sort by top or run your 15 phrase searches reliably (server-side keyword search timed out). I pulled **every post from the past year** per subreddit and matched phrases locally.

**What was pulled:** about 384,000 posts across 24 subreddits that returned data. Skipped or incomplete:
- **Not pulled:** r/Construction, r/realtors, r/propertymanagement.
- **Partial:** r/landscaping.
- **Returned zero posts:** r/trucking, r/veterinaryprofessionals.
- **Excluded at your request:** r/AmazonSeller and r/FulfillmentByAmazon (pulled, then not analysed).
- **Added at your request** (law and medical offices): r/LawFirm, r/Lawyertalk, r/physicaltherapy, r/Chiropractic, r/optometry and r/MedicalCoding (the last two were pulled but not analysed in depth). r/PrivatePractice turned out to be a TV-show subreddit full of IPTV spam, and r/medicalbilling was empty, so both were dropped.

**Comment threads:** you asked for every thread with 20+ comments. I pulled **46 hand-picked threads** (the evidence posts for the finalist clusters), not all of them. You told me not to let this take forever.

**How I found the evidence.** Keyword counts were badly polluted. For example, "interchange" matched "interchangeable", "square fees" matched "square feet", "mdf" matched wood, and "underpaid" matched salary threads. So **the counts in the ranking are not trusted measurements**. The evidence is the set of posts I actually read and judged relevant (`pain_points.csv`, 59 rows). Keyword matches I did not read are not in it.

**Evidence versus assumptions.** Every number in this report is labelled:
- **REDDIT** means a real post or comment.
- **WEB** means a web-search snippet I have not verified beyond the snippet.
- **ASSUMPTION** means my estimate. Scores are my judgment on a 1 to 5 scale, not measurements.

**Reddit complaints do not prove willingness to pay or profitability.** Where I found actual payment signals (people paying billing companies or collection agencies), I say so. Where I found none, I say that too.

**The article you shared.** Its revenue claims are unverified, so I did not use them. I used its process: real complaints, a recurring expensive problem, work done for the customer, and finding customers where the problem is discussed.

**Nobody was contacted.** Everything about outreach below is a design, not an action.

---

## 1. Ranking of every cluster

Totals are out of 100 (19 criteria, with outreach counted double). **Gate** means the hard requirements you set, which override the score.

<<RANKING>>

**Only four clusters both pass the gates and have at least five real evidence quotes: A, C, B and G.** A fifth would be padding. F (vendor insurance certificates) is the next-best and has three quotes. It is on a watchlist at the end.

---

## 2. The top four

### A. Small-dollar payer denials and underpayments for independent clinics (score <<SCORE_A>>/100)

**The problem, in one sentence:** independent clinics let small or repeat insurance denials and underpayments go unchased because the biller's time costs more than the claim.

**Who has it:** independent physical therapy, chiropractic, dental and small medical or ortho practices, roughly $0.5M to $2M in collections (ASSUMPTION).

**Evidence (REDDIT):**

<<EVID A>>

**What this proves and does not prove.**
- **Proves:** clinic owners describe denial pain in detail. The only written cost math is one poster's ($65 claim, 45 to 60 minutes of a $28/hour biller). Owners already pay third parties for billing: about $1,000 a month in one post, and a commenter cites a vendor at $300 base plus 4% of collections. A commenter raised HIPAA fear ("a small fine will easily wipe out a few thousand in reimbursements").
- **Does not prove:** that clinics will pay a third party for the small-claim tail. It does not prove recovery rates. **The poster with the best cost math is also selling a competing tool and offers free audits, and claims to have recovered $4,200 for a clinic. That claim is unverified and self-interested.** The post scored 72 with 8 comments, so it is thin support.
- **WEB (unverified snippets):** industry denial rates of roughly 5% to 11%, "up to 65% of denied claims not resubmitted", and about $25 to rework one claim (a MGMA estimate cited in the results). The sources were medical-billing trade blogs, some selling denial-management services.

**Hard requirements:**
- **License:** none for provider-side appeals. Avoid collecting patient balances, which could trigger collection-agency licensing. HIPAA business associate agreements and security controls are required (a compliance cost, not a license).
- **Margin:** about 60 to 65% (ASSUMPTION), with a real risk of falling below 60% in year one.
- **Obsolescence:** medium risk. Payers and providers are both adopting AI, which raises the volume of denials.

**Scores (1 to 5):** painkiller <<S A 1>>, frequency <<S A 2>>, willingness to pay <<S A 3>>, AI resistance <<S A 4>>, delivery automation <<S A 5>>, outreach automation <<S A 6>> (double), massive pain <<S A 7>>, purchasing power <<S A 8>>, easy to target <<S A 9>>, growing <<S A 10>>, dream outcome <<S A 11>>, provable upfront <<S A 12>>, speed <<S A 13>>, low client effort <<S A 14>>, Grand Slam potential <<S A 15>>, recurring <<S A 16>>, LTV:CAC <<S A 17>>, margin <<S A 18>>, ads and mail reach <<S A 19>>.

**$1M math:**
- **Revenue per client:** ASSUMPTION $3,600 a year ($1.2M in collections, 1.5% additionally recovered, 20% fee). The 1.5% is the weakest number in this report; test 0.5% to 3%.
- **Clients needed:** about 278.
- **Reachable market (WEB):** about 33,000 independent PT clinics and about 80,000 independent dental practices, so about 113,000. Chiropractic (about 66,000 businesses) and small medical practices are extra, not counted.
- **Share needed:** about 0.25%, well under the 2 to 3% risk line.
- **If recovery is only 0.5%:** revenue per client falls to $1,200, so 833 clients (0.74%). Still feasible, but the cost of winning each client would have to be low.
- **Scaling without you:** yes if appeals are mostly automated and a few reviewers handle exceptions. Payer phone calls are the main labor risk.

**How delivery works:**
- **Trigger:** a weekly pull of remittance data or the 90+ day aging report from the clinic's practice-management system.
- **Access needed:** a read-only export or clearinghouse access, a signed business associate agreement, and payer portal access. This is the hardest step, and it varies by clinic software.
- **Automatic:** classify denial reasons, compare payments to the payer contract to find underpayments, draft appeals or state prompt-pay demands, submit them, track deadlines, and send a weekly report.
- **Still needs a person:** medical-necessity denials, high-dollar appeals, payer phone calls, onboarding and data mapping, compliance, and client support.
- **Automation estimate:** about 65% at launch, 70 to 75% later (ASSUMPTION). Onboarding, integration breakage, exceptions and support are the reason I do not claim more.

**How you'd find and reach prospects automatically:**
- **Lists (public data, verify before use):** the federal NPI registry lists practice name, address, phone and provider type. State licensing boards and Google Maps add more.
- **Automation:** build the list by metro, find each practice's website and contact, and personalize with the state's prompt-pay law and the clinic's likely payer mix. Send print mail through a mail API and email from a separate domain, and run job-title-targeted ads. Follow email and phone rules (CAN-SPAM and phone-consent law).
- **Ads and mail:** this is the best fit of any cluster. The customer is a named owner at a physical address.

**Draft Grand Slam Offer:**
- **Offer:** "Free 7-day found-money audit of claims you've already written off or stopped chasing."
- **Price:** 20% of what is actually paid, dropping to 15% above $50,000 a year. No setup fee, no monthly fee.
- **Guarantee:** you pay nothing unless we recover money, and you can cancel any time.
- **Bonuses:** a report of denials by payer and code, a front-desk checklist for the five most common denial reasons, and a monthly payer scorecard.

**Why they'd pay even though billing software and billing companies exist.** ASSUMPTION, to test in interviews: existing tools and companies handle first-pass claims and the biggest denials. The tail is too small for a per-hour biller, and a billing company paid a percentage of collections may not chase claims of $60. Contingency pricing removes the cost risk.

**Competitors (WEB and REDDIT):** medical billing companies (about 4% of collections in one comment), revenue-cycle software, and denial-management vendors. The Reddit poster above is one small competitor. Whether small practices are underserved in the tail is plausible and **unproven**.

**Biggest risk:** trust and compliance. Clinics must hand over patient-related data to a new vendor, the top reply on the one relevant post is a HIPAA objection, and real recovery may be much smaller than assumed.

---

### C. Chargeback and processor-hold dispute packaging (score <<SCORE_C>>/100)

**The problem, in one sentence:** small merchants lose sales to chargebacks and frozen processor accounts and lack the time or evidence to win disputes.

**Who has it:** small ecommerce stores, event organizers, and service businesses that take cards online.

**Evidence (REDDIT):**

<<EVID C>>

**What this proves and does not prove.**
- **Proves:** vivid, frequent pain, high engagement (a Stripe-hold post scored 949), and dollar amounts from $3,400 to $1.2M.
- **Does not prove:** willingness to pay. One event organizer says their tool "fights the chargeback" but doubts it does. That is a sign of paid tools and distrust, not of demand for a new one.
- **WEB (unverified):** Stripe charges $15 per dispute regardless of the outcome, and there are 2.5M to 3.5M live Shopify stores.

**Hard requirements:**
- **License:** none.
- **Margin:** about 70% (ASSUMPTION).
- **Obsolescence:** medium. Stripe and Shopify keep improving their own dispute tools.
- **Purchasing power:** weak. Small merchants pay little.

**Scores (1 to 5):** painkiller <<S C 1>>, frequency <<S C 2>>, willingness to pay <<S C 3>>, AI resistance <<S C 4>>, delivery automation <<S C 5>>, outreach automation <<S C 6>> (double), massive pain <<S C 7>>, purchasing power <<S C 8>>, easy to target <<S C 9>>, growing <<S C 10>>, dream outcome <<S C 11>>, provable upfront <<S C 12>>, speed <<S C 13>>, low client effort <<S C 14>>, Grand Slam potential <<S C 15>>, recurring <<S C 16>>, LTV:CAC <<S C 17>>, margin <<S C 18>>, ads and mail reach <<S C 19>>.

**$1M math:**
- **Revenue per client:** ASSUMPTION $1,500 a year.
- **Clients needed:** about 667.
- **Reachable market:** WEB says 2.5M to 3.5M live Shopify stores; ASSUMPTION that only about 5% (150,000) are big enough to matter.
- **Share needed:** about 0.44%.
- **Concern:** the fee per client is small, so acquisition cost has to be very low. Churn among tiny merchants will be high.

**How delivery works:**
- **Trigger:** a dispute-created notice from the payment processor.
- **Access needed:** read access to the processor and store (order, shipping, customer messages) and permission to submit evidence.
- **Automatic:** assemble the evidence packet, draft the rebuttal, submit before the deadline, and track outcomes.
- **Still needs a person:** high-value disputes, fraud patterns, and processor-hold appeals.
- **Automation estimate:** about 75% (ASSUMPTION).

**Outreach:** find stores from public store directories and app-store data, and reach owners by email and targeted ads. Direct mail is weaker here because online stores rarely publish street addresses.

**Draft offer:** free audit of your last 90 days of disputes ("here is what we'd have won"). You pay 25% of disputed money recovered, with no monthly fee and nothing if we lose.

**Why they'd pay even though the processor offers tools.** ASSUMPTION: built-in tools are generic, and merchants in the thread don't trust them.

**Competitors (WEB):** dedicated chargeback services already exist (Chargeflow and Chargebacks911 appeared in the search results). Small merchants may be underserved on price, but that is unverified.

**Biggest risk:** low revenue per client and platforms absorbing the feature.

---

### B. Overdue-invoice follow-up and pre-lien notices (score <<SCORE_B>>/100, passes only if we never collect debts)

**The problem, in one sentence:** owners of service businesses and contractors don't reliably chase late payers, so money sits unpaid for months.

**Who has it:** contractors, small law firms, wholesalers and service businesses.

**Evidence (REDDIT):**

<<EVID B>>

**What this proves and does not prove.**
- **Proves:** the most frequent and specific money-owed pain in the dataset, with concrete amounts: $14k, $25k, $40k, $162k and $180k.
- **Willingness to pay:** owners use collection agencies at a negotiated percentage, and commenters suggest factoring. That is paid help, but it is licensed collection work, not reminder software.
- **Weak spot:** the top law-firm advice is a process fix (advance retainers, withdraw for nonpayment), not a purchase.

**Hard requirements:**
- **License:** **fails** if we collect debts on behalf of the owner. Passes only as reminders sent in the owner's name.
- **Legal practice:** computing lien or notice deadlines drifts toward legal advice. Avoid or keep to calendar reminders.
- **Obsolescence:** high. Accounting and invoicing software already sends reminders.

**Scores (1 to 5):** painkiller <<S B 1>>, frequency <<S B 2>>, willingness to pay <<S B 3>>, AI resistance <<S B 4>>, delivery automation <<S B 5>>, outreach automation <<S B 6>> (double), massive pain <<S B 7>>, purchasing power <<S B 8>>, easy to target <<S B 9>>, growing <<S B 10>>, dream outcome <<S B 11>>, provable upfront <<S B 12>>, speed <<S B 13>>, low client effort <<S B 14>>, Grand Slam potential <<S B 15>>, recurring <<S B 16>>, LTV:CAC <<S B 17>>, margin <<S B 18>>, ads and mail reach <<S B 19>>.

**$1M math:**
- **Revenue per client:** ASSUMPTION $1,788 a year ($149 a month).
- **Clients needed:** about 559.
- **Reachable market (WEB):** about 598,000 trade contractor establishments plus about 450,000 law firms, so about 1.05M.
- **Share needed:** about 0.05%.
- **Concern:** the price ceiling and churn, not market size.

**How delivery works:**
- **Trigger:** an invoice reaches N days past due in the owner's accounting or job software.
- **Access needed:** read invoices and contacts, plus permission to send from the owner's email.
- **Automatic:** escalating reminders in the owner's voice, payment links, payment-plan offers, and alerts to the owner.
- **Still needs a person:** disputes, and anything legal.

**Outreach:** contractor license boards, permit records and directories give named owners and addresses. Ads by job title also work.

**Draft offer:** "We chase your late invoices in your name, for a flat $149 a month." No collections and no legal threats, with a 30-day money-back guarantee.

**Why they'd pay even though invoicing software has reminders.** The Reddit evidence is that owners avoid following up because it feels personal ("chasing payments"). The problem is doing it, not the tool. But **no post shows anyone paying for reminders**. This is the weakest part of B.

**Competitors:** I did not search this cluster. Assume built-in reminders in accounting and invoicing tools.

**Biggest risk:** it is a commodity and easily copied, and the willingness to pay is for licensed collection, which you cannot do.

---

### G. Card processing fee audit (existing candidate #1) (score <<SCORE_G>>/100)

**The problem, in one sentence:** businesses overpay processing and bank fees and rarely audit them.

**Evidence (REDDIT):**

<<EVID G>>

**What this proves and does not prove.**
- **Proves:** one construction owner paid **$70K in fees on $2.8M revenue, including about $23K in ACH fees**, and commenters said ACH should cost a small flat fee. Another owner's fees went from about 4% to about 9%. That is exactly what an audit finds.
- **Counter-evidence:** commenters said fees are only about 2.5% of gross and "the smallest" problem, and many said they pay $15 to $40 a month for ACH. Owners also treat surcharging as normal.
- **Only about 3 to 5 genuine posts** out of 342 keyword matches.

**Hard requirements:**
- **License:** none for audit only. **Taking residuals from a processor is ISO or sales-agent territory. Avoid it.**
- **Margin:** about 70% (ASSUMPTION).
- **Obsolescence:** low, since processors must be negotiated with.

**Scores (1 to 5):** painkiller <<S G 1>>, frequency <<S G 2>>, willingness to pay <<S G 3>>, AI resistance <<S G 4>>, delivery automation <<S G 5>>, outreach automation <<S G 6>> (double), massive pain <<S G 7>>, purchasing power <<S G 8>>, easy to target <<S G 9>>, growing <<S G 10>>, dream outcome <<S G 11>>, provable upfront <<S G 12>>, speed <<S G 13>>, low client effort <<S G 14>>, Grand Slam potential <<S G 15>>, recurring <<S G 16>>, LTV:CAC <<S G 17>>, margin <<S G 18>>, ads and mail reach <<S G 19>>.

**$1M math:**
- **Revenue per client:** ASSUMPTION $750 a year.
- **Clients needed:** about 1,333.
- **Reachable market (WEB, SBA):** 6.4M employer firms; ASSUMPTION about 70% take cards.
- **Share needed:** about 0.03%.
- **Concern:** at this price, acquisition cost decides everything.

**How delivery works:**
- **Trigger:** the monthly processor statement.
- **Access needed:** a statement PDF or export. No system access.
- **Automatic:** parse fees, compare to benchmarks, flag markups and junk fees, and draft the renegotiation letter.
- **Still needs a person:** negotiating with the processor, switching processors, and exceptions.

**Competitors (WEB):** many. A free statement analyzer, several consulting audit firms, and at least one flat-fee auditor appeared in the results.

**Biggest risk:** crowded, free alternatives, and savings that are small compared with other costs.

---

## 3. Comparison against your six existing candidates

| Candidate | Reddit evidence | Score | Verdict |
|---|---|---|---|
| Merchant/credit card fee audits | 3 to 5 real posts (one big thread), plus real counter-evidence | <<SCORE_G>> | **Supports weakly.** One strong example, but crowded and beaten by A and C. |
| Utility bill audits (audit only) | No business-owner complaints found; only consumer leak and billing posts | <<SCORE_H>> | **Weakens.** Nothing on Reddit, and many established auditors exist. |
| Manufacturer co-op advertising funds | Effectively none (one removed MSP post) | <<SCORE_I>> | **Weakens.** No demand signal. Unknown leaks are hard to see on Reddit, but I can't claim demand. |
| HVAC manufacturer warranty claim recovery | About 10 relevant posts; one tech vents about free warranty labor | <<SCORE_J>> | **Weakens.** Real but thin, and manufacturer portals vary. |
| Delivery app dispute recovery | 2 relevant posts | <<SCORE_K>> | **Weakens.** Platforms auto-refund customers and allow about 10 days to dispute (WEB). |
| UPS/FedEx late refund recovery | 1 real post (surcharges) | <<SCORE_L>> | **Neutral.** Real money, but a crowded contingency market (25 to 50% fees per WEB) and no Reddit voice. |

**Beaten by:** A and C outscore all six. Note that the six candidates are "money you're owed but don't know about" problems, which are structurally hard to see in complaints. Absence on Reddit does not prove no demand, but it means I cannot support these with your standard of evidence.

---

## 4. Rejected clusters

| Cluster | Why rejected |
|---|---|
| D. Lost billable time (small law/consulting) | Scores well (<<SCORE_D>>) but **fails obsolescence.** A commenter already uses an AI tool that logs calls into practice software. |
| E. Missed calls, intake, no-shows | Highest raw volume (<<SCORE_E>>), but it is the AI receptionist and follow-up space you told me not to anchor on, and it is the most crowded. |
| Rent collection and evictions | Collecting or enforcing debts and evictions is legal or licensed work. |
| Tax and payroll notices | Representing clients before tax authorities needs a license. |
| Collections for late invoices | Debt collection licensing (the licensed version of B). |
| Vendor price creep and invoice errors | About 360 keyword matches, but the top posts were jokes, salaries and unrelated ("shorted out"). Not real evidence. |
| Permit delays | No relevant thread reached 20 comments, and rules are city-specific. |
| Government contract paperwork | Noisy and thin. |
| Dental insurance fee schedules | The anger is real but it is about low contracted rates, which are not recoverable money. |
| Trucking (detention, broker pay) | The archive returned no posts for r/trucking, so I could not assess it. |
| Amazon FBA and seller reimbursements | Excluded at your request. |

---

## 5. Recommendation

**Pursue A (small-dollar payer denial and underpayment recovery for independent clinics) as the first thing to validate.** It scores highest and passes the hard requirements. It has the best fit for ads and direct mail, contingency pricing that removes the client's risk, and a market where you need only about 0.25% of reachable practices. **But the Reddit evidence for it is moderate, not strong**: real denial pain and real payments to billing companies, with the key cost math coming from a competitor. Treat it as the best hypothesis, not a proven idea. If it fails the test below, move to C.

### First three things to do this week

1. **Run a manual found-money test.** Ask 5 to 10 independent PT, chiro or dental practices you can reach through your network for a de-identified 90+ day receivables aging report. Hand-review it and count small denials and underpayments. **Stop if fewer than about 1% of collections looks recoverable across at least five clinics.**
2. **Learn who you're competing with and what compliance costs.** Talk to 5 billing-company owners or clinic managers about what they don't chase and how they're paid. Get quotes for a HIPAA business associate agreement template, security tooling and cyber/E&O insurance. Check prompt-pay laws in your first two states.
3. **Test the offer with a small mail run.** Build the one-page sample found-money report and price test it with about 100 mailers to practices from the public NPI registry in one metro. Aim to learn the response rate. Sending is your decision; I have contacted no one.

---

## 6. Files

- `painkiller_report.md` (this report)
- `pain_points.csv`: 59 reviewed evidence rows. The dollar and time impact column is auto-extracted from nearby text and sometimes picks up unrelated numbers, so check it against the quote.
- `scores.csv`: all 12 clusters with 19 scores, $1M math and gate notes.
- `painkiller_workbook.xlsx`: scores (formulas recalculate), $1M math (editable assumptions) and pain points.
- `scrape_reddit.py`, `pull_archive.py`, `analyze_posts.py`, `clusters.py`, `build_outputs.py`: the data-gathering scripts. You said you don't need a tool, so these are just how the data was collected.

## 7. Watchlist

**F. Vendor insurance certificate and prequalification tracking** (<<SCORE_F>>/100). Three real quotes, low willingness to pay, and a small market signal.

<<EVID F>>
