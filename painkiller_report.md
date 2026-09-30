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

| Rank | Cluster | Score | Gate | Clients for $1M | Share of reachable market |
|---|---|---|---|---|---|
| 1 | A Small-dollar payer denials and underpayments (independent clinics) | 77 | pass, with HIPAA/collections conditions | 278 | 0.25% |
| 2 | E Missed calls / intake / no-show follow-up | 75 | **FAIL: crowded/AI-native, and the category you asked me not to anchor on** | 419 | 0.04% |
| 3 | C Chargeback / processor-hold dispute packaging | 73 | pass | 667 | 0.44% |
| 4 | D Lost billable time capture (small law/consulting) | 73 | **FAIL: obsolescence** | 842 | 0.47% |
| 5 | B Overdue-invoice follow-up + lien/notice deadlines (owner-name, not collections) | 69 | **conditional**: fails if it collects debts | 559 | 0.05% |
| 6 | G Card processing fee audit | 69 | pass (avoid processor residuals) | 1,333 | 0.03% |
| 7 | L UPS/FedEx late-delivery refunds | 69 | pass, but no Reddit voice | 667 | 0.22% |
| 8 | J HVAC manufacturer warranty claim recovery | 62 | pass, thin evidence | 400 | 0.36% |
| 9 | F Vendor COI / prequal compliance tracking | 61 | pass, thin evidence | 842 | 0.14% |
| 10 | K Delivery-app dispute recovery | 60 | pass, thin evidence | 1,333 | 0.31% |
| 11 | H Utility bill audit (audit only) | 58 | pass, no evidence | 2,222 | 0.11% |
| 12 | I Manufacturer co-op fund recovery | 53 | pass, no evidence | 800 | 0.40% |

**Only four clusters both pass the gates and have at least five real evidence quotes: A, C, B and G.** A fifth would be padding. F (vendor insurance certificates) is the next-best and has three quotes. It is on a watchlist at the end.

---

## 2. The top four

### A. Small-dollar payer denials and underpayments for independent clinics (score 77/100)

**The problem, in one sentence:** independent clinics let small or repeat insurance denials and underpayments go unchased because the biller's time costs more than the claim.

**Who has it:** independent physical therapy, chiropractic, dental and small medical or ortho practices, roughly $0.5M to $2M in collections (ASSUMPTION).

**Evidence (REDDIT):**

- "for $65 is denied, it takes a biller (paid \~$28/hr) about 45 minutes to an hour to research the denial, wait on hold with" (r/physicaltherapy, post, score 72; physical therapy) [link](https://www.reddit.com/r/physicaltherapy/comments/1tbdqtt/)
- "They bank on "Administrative Exhaustion." They deny small-balance claims for nonsense reasons, knowing your staff will never chase them. I'm a developer, so I" (r/physicaltherapy, post, score 72; physical therapy (author also sells a tool: self-interested)) [link](https://www.reddit.com/r/physicaltherapy/comments/1tbdqtt/)
- "Insurance denied my patient's 7th visit even though she still can't climb stairs Just got off the phone with UnitedHealthcare. They're cutting off a" (r/physicaltherapy, post, score 68; physical therapy) [link](https://www.reddit.com/r/physicaltherapy/comments/1r6fht0/)
- "A ridiculous workers comp denial Sometimes I cant stand the stupidity that comes with dealing with workers comp or any insurance for that matter." (r/physicaltherapy, post, score 75; physical therapy) [link](https://www.reddit.com/r/physicaltherapy/comments/1turokv/)
- "Bringing billing in-house…is it really that hard? I pay a billing company $1,000 month but really don't want to anymore if it's something I" (r/Chiropractic, post, score 2; chiropractic (WTP signal)) [link](https://www.reddit.com/r/Chiropractic/comments/1w7etcs/)
- "No it's not that bad… then again, I pay for a billing company to do everything… if I could have all BCBS PPO plans" (r/Chiropractic, comment, score 2; chiropractic (WTP signal)) [link](https://www.reddit.com/r/Chiropractic/comments/1sy2avs/_/oir0wft/)
- "Olympus billing is good and they only do $300 base pay with 4% collections and they can do all verifications" (r/Chiropractic, comment, score 2; chiropractic (competitor price point)) [link](https://www.reddit.com/r/Chiropractic/comments/1w7etcs/_/p7w5t5y/)
- "How HIPAA compliant is it? As it how securely is patient data processed and stored? A small fine will easily wipe out a few" (r/physicaltherapy, comment, score 11; physical therapy (objection: HIPAA)) [link](https://www.reddit.com/r/physicaltherapy/comments/1tbdqtt/_/olgdgva/)
- "are we not all oon. Ada doesn't care or do anything, get lowballed for any services we do and it's just untenable at this" (r/Dentistry, post, score 64; dental (fee schedules: structural, not recoverable)) [link](https://www.reddit.com/r/Dentistry/comments/1pvkex8/)
- "3 months consecutively but still after insurance reimbursement the total net collections was just at about break even (35k) on one of the months." (r/Dentistry, post, score 48; dental) [link](https://www.reddit.com/r/Dentistry/comments/1wo9oi7/)

**What this proves and does not prove.**
- **Proves:** clinic owners describe denial pain in detail. The only written cost math is one poster's ($65 claim, 45 to 60 minutes of a $28/hour biller). Owners already pay third parties for billing: about $1,000 a month in one post, and a commenter cites a vendor at $300 base plus 4% of collections. A commenter raised HIPAA fear ("a small fine will easily wipe out a few thousand in reimbursements").
- **Does not prove:** that clinics will pay a third party for the small-claim tail. It does not prove recovery rates. **The poster with the best cost math is also selling a competing tool and offers free audits, and claims to have recovered $4,200 for a clinic. That claim is unverified and self-interested.** The post scored 72 with 8 comments, so it is thin support.
- **WEB (unverified snippets):** industry denial rates of roughly 5% to 11%, "up to 65% of denied claims not resubmitted", and about $25 to rework one claim (a MGMA estimate cited in the results). The sources were medical-billing trade blogs, some selling denial-management services.

**Hard requirements:**
- **License:** none for provider-side appeals. Avoid collecting patient balances, which could trigger collection-agency licensing. HIPAA business associate agreements and security controls are required (a compliance cost, not a license).
- **Margin:** about 60 to 65% (ASSUMPTION), with a real risk of falling below 60% in year one.
- **Obsolescence:** medium risk. Payers and providers are both adopting AI, which raises the volume of denials.

**Scores (1 to 5):** painkiller 4, frequency 3, willingness to pay 4, AI resistance 4, delivery automation 3, outreach automation 4 (double), massive pain 3, purchasing power 3, easy to target 5, growing 4, dream outcome 4, provable upfront 5, speed 3, low client effort 3, Grand Slam potential 5, recurring 4, LTV:CAC 4, margin 3, ads and mail reach 5.

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

### C. Chargeback and processor-hold dispute packaging (score 73/100)

**The problem, in one sentence:** small merchants lose sales to chargebacks and frozen processor accounts and lack the time or evidence to win disputes.

**Who has it:** small ecommerce stores, event organizers, and service businesses that take cards online.

**Evidence (REDDIT):**

- "Stripe is holding $8,000 of my money indefinitely. My post on r/stripe hit 16k views and was removed. Here are the receipts. I run" (r/smallbusiness, post, score 949; small merchant) [link](https://www.reddit.com/r/smallbusiness/comments/1phlsw0/)
- "Stripe holding $1.2M of our operating funds for 6+ weeks with No Real Support My company has $1.2 M in operating funds being held" (r/smallbusiness, post, score 159; merchant) [link](https://www.reddit.com/r/smallbusiness/comments/1ruedgx/)
- "at my stripe dashboard watching my money disappear. Woke up this morning to seven chargebacks. seven. all from orders I shipped last month. all" (r/ecommerce, post, score 284; ecommerce) [link](https://www.reddit.com/r/ecommerce/comments/1qci3a4/)
- "Just got charged back $3,400 in one day and I literally want to throw my laptop out the window. Not even joking rn I'm" (r/ecommerce, post, score 284; ecommerce) [link](https://www.reddit.com/r/ecommerce/comments/1qci3a4/)
- "Chargebacks are basically legalized theft and no one talks about it I am really convinced that chargebacks are one of the most broken systems" (r/ecommerce, post, score 245; ecommerce) [link](https://www.reddit.com/r/ecommerce/comments/1rjivlb/)
- "Chargebacks for festival Man I'm so tired of chargebacks. I run a festival with about 15,000 attendees. My org is a nonprofit and we" (r/smallbusiness, post, score 365; events (15,000 attendees)) [link](https://www.reddit.com/r/smallbusiness/comments/1tnt780/)
- "shopify $3k a month. they locked my store for 48 hrs becz of a chargeback on a $47 order it wasn't a ban. It" (r/Entrepreneur, post, score 435; ecommerce) [link](https://www.reddit.com/r/Entrepreneur/comments/1qlt8xl/)
- "Chargebacks about to sink my whole side hustle, need chargeback prevention fast, pregnant wife counting on this Started flipping electronics couple months back, making" (r/smallbusiness, post, score 178; ecommerce) [link](https://www.reddit.com/r/smallbusiness/comments/1rppa5u/)
- "Being scammed with online orders Hi guys, I was curious if anyone else was facing this issue? We are seeing a lot of scams" (r/restaurateur, post, score 0; restaurant (delivery apps)) [link](https://www.reddit.com/r/restaurateur/comments/1smq52b/)
- "eat that fee regardless. They say they fight the chargeback on our behalf but who knows if they do. It's probably not even in" (r/smallbusiness, comment, score 15; events (WTP signal: relies on paid tool, distrusts it)) [link](https://www.reddit.com/r/smallbusiness/comments/1tnt780/_/onwo02o/)

**What this proves and does not prove.**
- **Proves:** vivid, frequent pain, high engagement (a Stripe-hold post scored 949), and dollar amounts from $3,400 to $1.2M.
- **Does not prove:** willingness to pay. One event organizer says their tool "fights the chargeback" but doubts it does. That is a sign of paid tools and distrust, not of demand for a new one.
- **WEB (unverified):** Stripe charges $15 per dispute regardless of the outcome, and there are 2.5M to 3.5M live Shopify stores.

**Hard requirements:**
- **License:** none.
- **Margin:** about 70% (ASSUMPTION).
- **Obsolescence:** medium. Stripe and Shopify keep improving their own dispute tools.
- **Purchasing power:** weak. Small merchants pay little.

**Scores (1 to 5):** painkiller 4, frequency 4, willingness to pay 3, AI resistance 3, delivery automation 4, outreach automation 4 (double), massive pain 4, purchasing power 2, easy to target 3, growing 4, dream outcome 3, provable upfront 4, speed 3, low client effort 4, Grand Slam potential 5, recurring 4, LTV:CAC 3, margin 4, ads and mail reach 4.

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

### B. Overdue-invoice follow-up and pre-lien notices (score 69/100, passes only if we never collect debts)

**The problem, in one sentence:** owners of service businesses and contractors don't reliably chase late payers, so money sits unpaid for months.

**Who has it:** contractors, small law firms, wholesalers and service businesses.

**Evidence (REDDIT):**

- "customer owes me $14k and has stopped replying, and everyone keeps saying "just take them to court" like that's a thing that happens Small" (r/smallbusiness, post, score 564; services/contracting) [link](https://www.reddit.com/r/smallbusiness/comments/1uw84p0/)
- "get so crazy. The client basically ghosted me and have stopped trying to pay anything at all after I stopped service. I don't have" (r/smallbusiness, post, score 230; services) [link](https://www.reddit.com/r/smallbusiness/comments/1ovpacl/)
- "Worth it to sue a customer for $14,000 in unpaid invoices? It would be my first time suing someone, so I don't know the" (r/smallbusiness, post, score 233; services) [link](https://www.reddit.com/r/smallbusiness/comments/1o8efjo/)
- "and the one thing I still can't get comfortable with is chasing payments. It's not that I don't know how, it's that every reminder" (r/smallbusiness, post, score 54; services) [link](https://www.reddit.com/r/smallbusiness/comments/1sh4b89/)
- "me $3k and is 45 days late. How much time do you guys waste chasing unpaid invoices? It feels like i'm spending my entire" (r/smallbusiness, post, score 65; services) [link](https://www.reddit.com/r/smallbusiness/comments/1t4hryr/)
- "Need advice: Wholesale account owes me $25K and keeps ghosting me I run a small clothing brand and have been selling wholesale for a" (r/smallbusiness, post, score 76; wholesale/apparel) [link](https://www.reddit.com/r/smallbusiness/comments/1p0zi4o/)
- "Commercial client not paying :( My construction business that I started last year is owes $40k by a client who has been promising to" (r/smallbusiness, post, score 142; construction) [link](https://www.reddit.com/r/smallbusiness/comments/1qzkjmj/)
- "paid on receipt. right now i ve got somewhere around 180k sitting in unpaid invoices. that's real money we earned. but i can't use" (r/smallbusiness, post, score 38; B2B services) [link](https://www.reddit.com/r/smallbusiness/comments/1sl6m0a/)
- "a lien and was in litigation for two years. Racked up $70K of legal fees. Finally got to the point of going to trial" (r/Contractor, post, score 217; contracting) [link](https://www.reddit.com/r/Contractor/comments/1pufmg5/)
- "goes dark like that, what's your actual line? How many follow-ups before you give up or fi⁤e in small claims co⁤urt ??" (r/Contractor, post, score 74; contracting) [link](https://www.reddit.com/r/Contractor/comments/1q068o1/)
- "business and my family side. I'm good at pulling wire but I'm terrible at chasing invoices at 9pm. Anyone here running their own shop" (r/electricians, post, score 154; electrical) [link](https://www.reddit.com/r/electricians/comments/1s87s5s/)
- "sales rep told customer they could have net 75 now customer won't pay at net 30 Got a call from a customer yesterday saying" (r/Accounting, post, score 188; B2B (accounting view)) [link](https://www.reddit.com/r/Accounting/comments/1s51cf8/)
- "Finally got paid $15k from a GC who ghosted me for 4 months. Here is what worked. Long story short: Did a commercial electrical" (r/smallbusiness, post, score 312; electrical contracting) [link](https://www.reddit.com/r/smallbusiness/comments/1ppx9pp/)
- "no payment (and with a warning), but I still have thousands of dollars of unpaid invoices. Any advice is appreciated!" (r/LawFirm, post, score 7; law) [link](https://www.reddit.com/r/LawFirm/comments/1qtc2o6/)
- "per month, about a 9% increase in profitability. My unpaid balances are up slightly to $35,000 from the non paying clients I've had to" (r/LawFirm, post, score 42; law) [link](https://www.reddit.com/r/LawFirm/comments/1pp11hg/)
- "We're a small firm in commercial litigation. We're getting very tired of people not paying their retainers. When a collection call is made, we" (r/Lawyertalk, post, score 48; law) [link](https://www.reddit.com/r/Lawyertalk/comments/1uyg6kr/)
- "try and talk my client into settling. Probably going to just write off this $16k bill as well. Not like he is going to" (r/Lawyertalk, post, score 256; law) [link](https://www.reddit.com/r/Lawyertalk/comments/1owd6da/)
- "I use a collection agency. They are ruthless and you can negotiate their percentage. I use Tucker Albin services. You lose some money, but" (r/smallbusiness, comment, score 35; services (WTP signal: pays % to collector)) [link](https://www.reddit.com/r/smallbusiness/comments/1uw84p0/_/oxh6zvz/)
- "There's a thing called "factoring", where you can sell your receivables to companies that collect debts for a living. You will not get the" (r/smallbusiness, comment, score 36; services (alternative to service)) [link](https://www.reddit.com/r/smallbusiness/comments/1o8efjo/_/njua7p7/)

**What this proves and does not prove.**
- **Proves:** the most frequent and specific money-owed pain in the dataset, with concrete amounts: $14k, $25k, $40k, $162k and $180k.
- **Willingness to pay:** owners use collection agencies at a negotiated percentage, and commenters suggest factoring. That is paid help, but it is licensed collection work, not reminder software.
- **Weak spot:** the top law-firm advice is a process fix (advance retainers, withdraw for nonpayment), not a purchase.

**Hard requirements:**
- **License:** **fails** if we collect debts on behalf of the owner. Passes only as reminders sent in the owner's name.
- **Legal practice:** computing lien or notice deadlines drifts toward legal advice. Avoid or keep to calendar reminders.
- **Obsolescence:** high. Accounting and invoicing software already sends reminders.

**Scores (1 to 5):** painkiller 4, frequency 5, willingness to pay 2, AI resistance 2, delivery automation 4, outreach automation 4 (double), massive pain 4, purchasing power 3, easy to target 4, growing 3, dream outcome 3, provable upfront 3, speed 4, low client effort 3, Grand Slam potential 3, recurring 4, LTV:CAC 2, margin 4, ads and mail reach 4.

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

### G. Card processing fee audit (existing candidate #1) (score 69/100)

**The problem, in one sentence:** businesses overpay processing and bank fees and rarely audit them.

**Evidence (REDDIT):**

- "be feeling my pain here. Just ran the numbers on what payment processing fees actually cost us last year now that my accountant brought" (r/smallbusiness, post, score 399; small business) [link](https://www.reddit.com/r/smallbusiness/comments/1ol8edm/)
- "bought by global Payments. My processing fees have always been around 4%. In 2025 the fees were around 9%. We also switched to their" (r/smallbusiness, post, score 16; small business) [link](https://www.reddit.com/r/smallbusiness/comments/1qfuedn/)
- "has been worthwhile). My biggest surprise expense, which I was aware of but just didnt fully grasp, is credit card fees. I chose to" (r/Lawyertalk, post, score 42; law (solo)) [link](https://www.reddit.com/r/Lawyertalk/comments/1rathu6/)
- "way, of all the problems with your business model, payment processing is the smallest. Before getting pissed off at everyone else, get your shit" (r/smallbusiness, comment, score 12; counter-evidence: commenter says fees are ~2.5% of gross) [link](https://www.reddit.com/r/smallbusiness/comments/1ol8edm/_/nmgclee/)
- "of paying by credit card. I owned a restaurant for 10 years. It was my second highest expense." (r/smallbusiness, comment, score 16; restaurant) [link](https://www.reddit.com/r/smallbusiness/comments/1ol8edm/_/nmgdsgg/)

**What this proves and does not prove.**
- **Proves:** one construction owner paid **$70K in fees on $2.8M revenue, including about $23K in ACH fees**, and commenters said ACH should cost a small flat fee. Another owner's fees went from about 4% to about 9%. That is exactly what an audit finds.
- **Counter-evidence:** commenters said fees are only about 2.5% of gross and "the smallest" problem, and many said they pay $15 to $40 a month for ACH. Owners also treat surcharging as normal.
- **Only about 3 to 5 genuine posts** out of 342 keyword matches.

**Hard requirements:**
- **License:** none for audit only. **Taking residuals from a processor is ISO or sales-agent territory. Avoid it.**
- **Margin:** about 70% (ASSUMPTION).
- **Obsolescence:** low, since processors must be negotiated with.

**Scores (1 to 5):** painkiller 3, frequency 3, willingness to pay 2, AI resistance 4, delivery automation 4, outreach automation 4 (double), massive pain 2, purchasing power 3, easy to target 4, growing 3, dream outcome 3, provable upfront 5, speed 3, low client effort 4, Grand Slam potential 4, recurring 3, LTV:CAC 3, margin 4, ads and mail reach 4.

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
| Merchant/credit card fee audits | 3 to 5 real posts (one big thread), plus real counter-evidence | 69 | **Supports weakly.** One strong example, but crowded and beaten by A and C. |
| Utility bill audits (audit only) | No business-owner complaints found; only consumer leak and billing posts | 58 | **Weakens.** Nothing on Reddit, and many established auditors exist. |
| Manufacturer co-op advertising funds | Effectively none (one removed MSP post) | 53 | **Weakens.** No demand signal. Unknown leaks are hard to see on Reddit, but I can't claim demand. |
| HVAC manufacturer warranty claim recovery | About 10 relevant posts; one tech vents about free warranty labor | 62 | **Weakens.** Real but thin, and manufacturer portals vary. |
| Delivery app dispute recovery | 2 relevant posts | 60 | **Weakens.** Platforms auto-refund customers and allow about 10 days to dispute (WEB). |
| UPS/FedEx late refund recovery | 1 real post (surcharges) | 69 | **Neutral.** Real money, but a crowded contingency market (25 to 50% fees per WEB) and no Reddit voice. |

**Beaten by:** A and C outscore all six. Note that the six candidates are "money you're owed but don't know about" problems, which are structurally hard to see in complaints. Absence on Reddit does not prove no demand, but it means I cannot support these with your standard of evidence.

---

## 4. Rejected clusters

| Cluster | Why rejected |
|---|---|
| D. Lost billable time (small law/consulting) | Scores well (73) but **fails obsolescence.** A commenter already uses an AI tool that logs calls into practice software. |
| E. Missed calls, intake, no-shows | Highest raw volume (75), but it is the AI receptionist and follow-up space you told me not to anchor on, and it is the most crowded. |
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

**F. Vendor insurance certificate and prequalification tracking** (61/100). Three real quotes, low willingness to pay, and a small market signal.

- "and I swear I spend half my Mondays just staring at a spreadsheet trying to figure out whose COI is about to expire. We" (r/smallbusiness, post, score 0; landscaping/property services) [link](https://www.reddit.com/r/smallbusiness/comments/1sh61hu/)
- "lost a 100k contract because my safety paperwork wasn't up to their standard a small landscaping and civil crew in SEQ, 8 guys doing" (r/smallbusiness, post, score 16; landscaping/civil) [link](https://www.reddit.com/r/smallbusiness/comments/1tdbch2/)
- "obtain or that would significantly increase my premiums. Custom COI requests with multiple additional insureds. And then 45,60 day payment terms that start on" (r/smallbusiness, post, score 16; services to enterprise) [link](https://www.reddit.com/r/smallbusiness/comments/1wellfk/)
