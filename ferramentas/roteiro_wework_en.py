"""Builds projetos/wework-en/projeto.json (WeWork, Hidden Cost channel, English)."""
import json, os

G, W, R, M = "gold", "white", "red", "muted"


def big(*lines):
    return {"type": "bigtext", "stagger": 0.25, "lines": [list(l) for l in lines]}


def img(media, wiki, lower, fb):
    return {"type": "image", "media": media, "wiki": wiki, "lower": lower, "dim": 0.4, "fallback": fb}


def prt(media, url, source, fb):
    return {"type": "print", "media": media, "url": url, "source": source, "rotate": -1.0, "fallback": fb}


def vid(media, q, lower, fb):
    return {"type": "video", "media": media, "search": q, "search_en": q, "start": 0.0, "dim": 0.4, "lower": lower, "fallback": fb}


S = lambda text, scene: {"text": text, "scene": scene}
FOTO_WW = ["WeWork office", "WeWork coworking space", "WeWork"]
FOTO_NEUMANN = ["Adam Neumann", "Adam Neumann WeWork"]
LOGOS = {"logo_wework": ["File:WeWork logo.svg", "File:WeWork Logo.svg", "WeWork logo"]}

U_PAYOUT = "https://techcrunch.com/2019/10/22/softbank-reportedly-ends-wework-ownership-debacle-with-a-1-7-billion-payout-to-adam-neumann"
U_S1 = "https://www.fool.com/investing/2019/08/14/wework-files-updated-ipo-massive-losses.aspx"
U_WE = "https://foxbusiness.com/business-leaders/wework-ceo-adam-neumann-returns-trademark-money"
U_EXIT = "https://www.newser.com/story/351625/wework-emerges-from-bankruptcy.html"
U_FLOW = "https://techcrunch.com/2022/08/15/a16z-andreessen-horowitz-backs-adam-neumann-wework-new-venture-flow-real-estate/"
U_SPAC = "https://rebusinessonline.com/bowx-acquisition-corp-agree-to-buy-wework-plans-to-take-company-public-at-9b-valuation/"


def capa(faixa, linhas, recorte):
    return {"type": "capa", "foto": "wework", "wiki": FOTO_WW, "seta": False, "recorte": recorte,
            "faixa": faixa, "linhas": linhas, "logo": "logo_wework"}


long_parts = [
    {"chapter": "", "sentences": [
        dict(S("Hey everyone, Vinícius here, and this is Hidden Cost.",
               capa("Never made a profit", [["$47", G, 270], ["BILLION", W, 200], ["BANKRUPT", R, 210]], "WeWork · 2019")), abertura=True),
        S("In January twenty nineteen, a company that rents out office space was valued at forty seven billion dollars.",
          {"type": "counter", "value": 47, "prefix": "$", "suffix": "B", "over": "JANUARY 2019", "label": "WEWORK'S VALUATION", "color": G, "size": 240}),
        S("Nine months later, it couldn't even go public.", {"type": "stamp", "org": "WEWORK · 2019", "title": "THE IPO", "stamp": "PULLED", "stamp_at": 0.9}),
        S("Four years after that, it filed for bankruptcy.", big(("2023", R, 220), ("BANKRUPT", W, 160))),
        S("And the man who built it walked away with a deal reported at up to one point seven billion dollars.",
          {"type": "counter", "value": 1.7, "prefix": "$", "suffix": "B", "over": "THE FOUNDER'S DEAL", "label": "AS REPORTED IN 2019", "color": G, "size": 230}),
        S("So who paid the hidden cost? Let's find out.", {"type": "bullets", "items": ["THE PITCH", "THE $47 BILLION", "THE IPO", "WHO PAID"], "size": 85, "last_gold": True}),
    ]},
    {"chapter": "THE PITCH", "sentences": [
        S("WeWork was founded in twenty ten, in New York, by Adam Neumann and Miguel McKelvey.", big(("2010", G, 230), ("NEW YORK", W, 140))),
        S("The idea was simple. Lease big office floors, split them into desks and small rooms, and rent them out by the month.",
          {"type": "flow", "a": "BIG FLOORS", "a_sub": "leased for years", "b": "SMALL DESKS", "b_sub": "rented monthly", "caption": "THE MODEL"}),
        S("Free coffee, beer on tap, glass walls, and a promise: this isn't an office. It's a community.",
          img("ww_space", FOTO_WW, "A WeWork space", big(("NOT AN OFFICE", W, 130), ("A COMMUNITY", G, 150)))),
        S("But there was a catch. WeWork signed leases that lasted many years. Its members could leave with a month's notice.",
          {"type": "compare", "title": "THE MISMATCH", "items": [["YEARS", "WEWORK'S LEASES", R], ["1 MONTH", "MEMBERS' NOTICE", W]], "size": 160, "stagger": 1.2, "vs": True}),
        S("If the economy slowed down, the customers could walk away. The rent bills would stay.", big(("CUSTOMERS LEAVE", W, 120), ("RENT STAYS", R, 170))),
        S("Neumann didn't sell WeWork as a real estate company. He sold it as a tech company.",
          img("neumann", FOTO_NEUMANN, "Adam Neumann, WeWork co-founder", big(("NOT REAL ESTATE", W, 120), ("TECH", G, 230)))),
        S("And that matters, because investors pay a lot more for tech companies.", big(("TECH", G, 200), ("= HIGHER PRICE", W, 130))),
    ]},
    {"chapter": "THE $47 BILLION", "sentences": [
        S("In twenty seventeen, the Japanese giant SoftBank and its CEO, Masayoshi Son, started pouring billions into WeWork.",
          big(("2017", G, 220), ("SOFTBANK", W, 160), ("BILLIONS IN", M, 100))),
        S("By January twenty nineteen, WeWork was valued at forty seven billion dollars.",
          {"type": "counter", "value": 47, "prefix": "$", "suffix": "B", "over": "JANUARY 2019", "label": "ON PAPER", "color": G, "size": 240}),
        S("The company was growing fast. In twenty eighteen, revenue hit about one point eight billion dollars.",
          {"type": "counter", "value": 1.8, "prefix": "$", "suffix": "B", "over": "2018", "label": "REVENUE", "color": G, "size": 230}),
        S("But that same year, it lost about one point six billion.",
          prt("print_s1", U_S1, "The Motley Fool · Aug 14, 2019",
              {"type": "compare", "title": "WEWORK · 2018", "items": [["$1.8B", "REVENUE", G], ["-$1.6B", "NET LOSS", R]], "size": 160, "stagger": 1.2, "vs": False})),
        S("For every dollar it brought in, it lost almost ninety cents.", big(("EVERY $1 IN", W, 140), ("~90¢ LOST", R, 170))),
        S("And its future lease payments added up to around eighteen billion dollars.",
          {"type": "counter", "value": 17.9, "prefix": "$", "suffix": "B", "over": "LEASE OBLIGATIONS", "label": "PER THE IPO FILING", "color": R, "size": 220}),
        S("Still, the plan was to go public, and cash in on that forty seven billion.", big(("NEXT STOP", W, 140), ("WALL STREET", G, 160))),
    ]},
    {"chapter": "THE IPO", "sentences": [
        S("In August twenty nineteen, WeWork filed its paperwork to go public. And investors finally got to read the details.",
          {"type": "date", "month": "AUGUST", "day": "14", "year": "2019", "tag": "THE IPO FILING"}),
        S("Neumann's special shares had twenty votes each. Public investors would get one.",
          {"type": "compare", "title": "VOTES PER SHARE", "items": [["20", "NEUMANN'S SHARES", G], ["1", "PUBLIC INVESTORS", W]], "size": 200, "stagger": 1.2, "vs": True}),
        S("The filing also showed that WeWork had paid Neumann five point nine million dollars for the trademark to the word, We.",
          prt("print_we", U_WE, "Fox Business · 2019",
              {"type": "stamp", "org": "TRADEMARK DEAL", "title": "THE WORD \"WE\"", "stamp": "$5.9M", "stamp_at": 0.9})),
        S("After the backlash, he gave the money back.", big(("THE $5.9M", W, 150), ("RETURNED", G, 170))),
        S("And it showed that WeWork leased space in buildings that Neumann had a stake in.", big(("THE LANDLORD", W, 140), ("WAS THE CEO", R, 150))),
        S("Investors did the math. Reports said the expected valuation dropped to around ten billion dollars.",
          {"type": "compare", "title": "THE VALUATION", "items": [["$47B", "JANUARY 2019", G], ["~$10B", "SEPTEMBER 2019", R]], "size": 160, "stagger": 1.2, "vs": False}),
        S("On September twenty fourth, twenty nineteen, Neumann stepped down as CEO.", {"type": "stamp", "org": "WEWORK · SEP 24, 2019", "title": "ADAM NEUMANN, CEO", "stamp": "OUT", "stamp_at": 0.9}),
        S("Six days later, the IPO was officially pulled.", {"type": "stamp", "org": "WEWORK · SEP 30, 2019", "title": "THE IPO", "stamp": "WITHDRAWN", "stamp_at": 0.9}),
    ]},
    {"chapter": "WHO PAID", "sentences": [
        S("In October, SoftBank took control of WeWork, now valued at around eight billion dollars.",
          {"type": "compare", "title": "NINE MONTHS LATER", "items": [["$47B", "JANUARY", G], ["~$8B", "OCTOBER", R]], "size": 170, "stagger": 1.2, "vs": False}),
        S("And the rescue came with a deal for Neumann, reported at up to one point seven billion dollars.",
          prt("print_payout", U_PAYOUT, "TechCrunch · Oct 22, 2019",
              {"type": "counter", "value": 1.7, "prefix": "$", "suffix": "B", "over": "THE EXIT DEAL", "label": "AS REPORTED", "color": G, "size": 230})),
        S("That included nearly a billion dollars to buy his shares, a five hundred million dollar credit line, and a hundred and eighty five million in consulting fees.",
          {"type": "bullets", "title": "THE DEAL", "items": ["~$1B FOR HIS SHARES", "$500M CREDIT LINE", "$185M CONSULTING"], "size": 85, "last_gold": True}),
        S("Weeks later, WeWork announced thousands of layoffs.", vid("office_empty", "empty office desks", "Layoffs", big(("THOUSANDS", W, 160), ("LAID OFF", R, 170)))),
        S("Here's the hidden cost.", {"type": "flash", "text": "THE HIDDEN\nCOST", "tint": "red", "size": 150}),
        S("The founder walked away a billionaire. Thousands of employees walked away without a job. And many of them held stock that was now worth a fraction of what they had been told.",
          {"type": "compare", "title": "WHO PAID", "items": [["BILLIONAIRE", "THE FOUNDER", G], ["NO JOB", "THOUSANDS OF EMPLOYEES", R]], "size": 140, "stagger": 1.2, "vs": True}),
    ]},
    {"chapter": "THE FALL", "sentences": [
        S("Then, in twenty twenty, the pandemic emptied offices around the world.", vid("empty_city", "empty city office building", "2020", big(("2020", R, 220), ("EMPTY OFFICES", W, 130)))),
        S("In October twenty twenty one, WeWork finally went public, through a merger with a blank check company, at a value of about nine billion dollars.",
          prt("print_spac", U_SPAC, "REBusiness · 2021",
              {"type": "counter", "value": 9, "prefix": "$", "suffix": "B", "over": "OCTOBER 2021", "label": "FINALLY PUBLIC", "color": G, "size": 230})),
        S("It never turned a profit.", big(("PROFIT", W, 170), ("NEVER", R, 220))),
        S("In November twenty twenty three, WeWork filed for bankruptcy.", {"type": "stamp", "org": "WEWORK · NOV 2023", "title": "CHAPTER 11", "stamp": "FILED", "stamp_at": 0.9}),
        S("By the end of that year, the company once valued at forty seven billion was worth less than a hundred million on the stock market.",
          {"type": "compare", "title": "WEWORK", "items": [["$47B", "2019", G], ["<$100M", "END OF 2023", R]], "size": 160, "stagger": 1.2, "vs": False}),
        S("It came out of bankruptcy in June twenty twenty four. Smaller, with a new majority owner, the software company Yardi Systems.",
          prt("print_exit", U_EXIT, "Newser · Jun 13, 2024", big(("JUNE 2024", G, 170), ("NEW OWNER", W, 140)))),
        S("It cut more than four billion dollars in debt and closed about a hundred and seventy locations.",
          {"type": "bullets", "title": "THE RESTART", "items": ["$4B+ DEBT CUT", "~170 LOCATIONS CLOSED"], "size": 90, "last_gold": True}),
        S("And Adam Neumann? In twenty twenty two, the venture firm Andreessen Horowitz backed his new real estate startup, Flow, with three hundred and fifty million dollars.",
          prt("print_flow", U_FLOW, "TechCrunch · Aug 15, 2022",
              {"type": "counter", "value": 350, "prefix": "$", "suffix": "M", "over": "FLOW · 2022", "label": "NEUMANN'S NEXT STARTUP", "color": G, "size": 220})),
        S("According to TechCrunch, it was the firm's biggest single check ever.", big(("THEIR BIGGEST", W, 140), ("CHECK EVER", G, 170))),
        S("The hidden lesson? A great story can be worth more than a business. Until someone reads the numbers.",
          {"type": "flash", "text": "READ THE\nNUMBERS", "tint": "red", "size": 150}),
        S("Which company do you think is the next WeWork? Tell me in the comments, and follow Hidden Cost for a new case every week.",
          {"type": "endcard", "sub": "THE WEWORK CASE"}),
    ]},
]

FIM = "The full story is on the channel. Search WeWork on Hidden Cost."
CTA = big(("FULL STORY", W, 120), ("SEARCH WEWORK", G, 130), ("ON HIDDEN COST", W, 110))
shorts = [
    {"title": "From $47 Billion to Bankrupt in 4 Years: WeWork", "sentences": [
        S("WeWork was valued at forty seven billion dollars. Four years later, it was bankrupt.", capa("In 4 years", [["$47B", G, 270], ["TO", W, 170], ["BANKRUPT", R, 220]], "WeWork · 2019")),
        S("It rented out office space, but it was sold to investors as a tech company.", big(("OFFICE SPACE", W, 140), ("SOLD AS TECH", G, 150))),
        S("In twenty eighteen, it made about one point eight billion dollars, and lost about one point six billion.",
          {"type": "compare", "title": "WEWORK · 2018", "items": [["$1.8B", "REVENUE", G], ["-$1.6B", "NET LOSS", R]], "size": 160, "stagger": 1.2, "vs": False}),
        S("When it tried to go public in twenty nineteen, investors read the numbers. And the IPO was pulled.", {"type": "stamp", "org": "WEWORK · 2019", "title": "THE IPO", "stamp": "PULLED", "stamp_at": 0.9}),
        S("In twenty twenty three, it filed for bankruptcy.", big(("2023", R, 220), ("BANKRUPT", W, 160))),
        S(FIM, CTA)]},
    {"title": "WeWork Paid Its Own CEO $5.9 Million for the Word \"We\"", "sentences": [
        S("WeWork paid its own founder five point nine million dollars for the word, We.", capa("For one word", [["$5.9M", G, 250], ["FOR THE WORD", W, 160], ["\"WE\"", R, 260]], "WeWork · 2019")),
        S("Adam Neumann owned the trademark, and the company paid him for it.", img("neumann", FOTO_NEUMANN, "Adam Neumann, WeWork co-founder", big(("THE FOUNDER", W, 140), ("OWNED \"WE\"", G, 160)))),
        S("It came out in twenty nineteen, when WeWork filed to go public.", big(("2019", G, 220), ("THE IPO FILING", W, 120))),
        S("After the backlash, he gave the money back.", big(("THE $5.9M", W, 150), ("RETURNED", G, 170))),
        S("But it was too late. The IPO was pulled a few weeks later.", {"type": "stamp", "org": "WEWORK · 2019", "title": "THE IPO", "stamp": "PULLED", "stamp_at": 0.9}),
        S(FIM, CTA)]},
    {"title": "The IPO Collapsed. The CEO Got a $1.7 Billion Deal", "sentences": [
        S("WeWork's founder got a deal reported at up to one point seven billion dollars to step away.", capa("The IPO collapsed", [["THE CEO", W, 200], ["GOT", W, 170], ["$1.7B", G, 270]], "WeWork · 2019")),
        S("In twenty nineteen, the IPO failed and Adam Neumann stepped down as CEO.", {"type": "stamp", "org": "WEWORK · SEP 2019", "title": "ADAM NEUMANN, CEO", "stamp": "OUT", "stamp_at": 0.9}),
        S("SoftBank took control, at a valuation of around eight billion. Down from forty seven.",
          {"type": "compare", "title": "WEWORK · 2019", "items": [["$47B", "JANUARY", G], ["~$8B", "OCTOBER", R]], "size": 170, "stagger": 1.2, "vs": False}),
        S("The deal included about a billion dollars for his shares and a hundred and eighty five million in consulting fees.",
          {"type": "bullets", "title": "THE DEAL", "items": ["~$1B FOR HIS SHARES", "$185M CONSULTING"], "size": 90, "last_gold": True}),
        S("Weeks later, thousands of employees were laid off.", big(("THOUSANDS", W, 160), ("LAID OFF", R, 170))),
        S(FIM, CTA)]},
    {"title": "This $47 Billion Startup Lost 90¢ on Every Dollar", "sentences": [
        S("For every dollar WeWork brought in, it lost almost ninety cents.", capa("Valued at $47 billion", [["LOST 90¢", R, 230], ["ON EVERY", W, 180], ["$1", G, 280]], "WeWork · 2018")),
        S("In twenty eighteen, revenue was about one point eight billion dollars. The loss, about one point six billion.",
          {"type": "compare", "title": "WEWORK · 2018", "items": [["$1.8B", "REVENUE", G], ["-$1.6B", "NET LOSS", R]], "size": 160, "stagger": 1.2, "vs": False}),
        S("It signed leases for years, but its members could leave with a month's notice.",
          {"type": "compare", "title": "THE MISMATCH", "items": [["YEARS", "WEWORK'S LEASES", R], ["1 MONTH", "MEMBERS' NOTICE", W]], "size": 160, "stagger": 1.2, "vs": True}),
        S("And still, investors valued it at forty seven billion dollars.", {"type": "counter", "value": 47, "prefix": "$", "suffix": "B", "over": "JANUARY 2019", "label": "ON PAPER", "color": G, "size": 240}),
        S(FIM, CTA)]},
]

projeto = {
    "title": "WeWork",
    "slug": "wework",
    "idioma": "en",
    "angle": "WeWork was valued at $47 billion, never made a profit, and went bankrupt. The founder walked away with a deal reported at up to $1.7 billion.",
    "voz": {"nome": "gravada", "motor": "eleven", "eleven_voz": "Vinícius Torales"},
    "logos": LOGOS,
    "script": {"long": {"parts": long_parts}, "shorts": shorts},
    "serie": [
        {"partes": [1, 2], "capa": capa("Part 1 of 4", [["$47B", G, 260], ["FOR RENTING", W, 170], ["DESKS", R, 230]], "WeWork · Part 1"),
         "caption": "WeWork, part 1: how a company that rents desks got sold as a tech startup. Follow for part 2.", "fim": ["CONTINUES IN", "PART 2"],
         "hashtags": ["#wework", "#business", "#startup", "#history", "#series"]},
        {"partes": [3, 4], "capa": capa("Part 2 of 4", [["THE FILING", W, 200], ["THAT KILLED", G, 180], ["THE IPO", R, 220]], "WeWork · Part 2"),
         "caption": "WeWork, part 2: the $47 billion valuation and the IPO filing investors finally read.", "fim": ["CONTINUES IN", "PART 3"],
         "hashtags": ["#wework", "#ipo", "#business", "#startup", "#series"]},
        {"partes": [5], "capa": capa("Part 3 of 4", [["COMPANY SANK", R, 190], ["FOUNDER GOT", W, 180], ["$1.7B", G, 270]], "WeWork · Part 3"),
         "caption": "WeWork, part 3: the founder's exit deal and who paid the hidden cost.", "fim": ["CONTINUES IN", "PART 4"],
         "hashtags": ["#wework", "#adamneumann", "#business", "#startup", "#series"]},
        {"partes": [6], "capa": capa("Part 4 of 4", [["BANKRUPT.", R, 230], ["THEN $350M", G, 200], ["FOR HIM", W, 190]], "WeWork · Final"),
         "caption": "WeWork, final part: the pandemic, the bankruptcy, and the founder's $350 million comeback.", "fim": ["END OF", "THE SERIES"],
         "hashtags": ["#wework", "#bankruptcy", "#business", "#startup", "#series"]},
    ],
    "meta": {
        "titles": [
            "WEWORK: The $47 Billion Startup That Never Made a Profit",
            "WeWork Collapsed. Its CEO Walked Away With $1.7 Billion",
        ],
        "description": "In January 2019, WeWork was valued at $47 billion. Nine months later, its IPO was pulled. In 2023, it filed for bankruptcy. Meanwhile, its founder walked away with a deal reported at up to $1.7 billion. In this video: the pitch, the $47 billion valuation, the IPO filing investors finally read, and who paid the hidden cost.\n\n[CAPÍTULOS]\n\nSources: WeWork IPO filing (S-1, Aug 2019) as reported by The Motley Fool; TechCrunch (Oct 22, 2019; Aug 15, 2022); Fox Business (2019); REBusiness (2021); Newser (Jun 13, 2024); Fox Business (Nov 2023).\n\n#WeWork #AdamNeumann #HiddenCost",
        "tags": ["wework", "adam neumann", "wework bankruptcy", "what happened to wework", "wework ipo", "softbank wework", "hidden cost"],
    },
    "thumbs_capa": [
        capa("Never made a profit", [["$47", G, 280], ["BILLION", W, 210], ["BANKRUPT", R, 220]], "WeWork · 2019"),
        capa("The company sank", [["THE CEO", W, 200], ["GOT", W, 170], ["$1.7B", G, 280]], "WeWork · 2019"),
    ],
    "thumbs": [
        {"glow": "red", "lines": [{"text": "$47 BILLION", "color": "gold", "size": 150}, {"text": "ZERO", "color": "white", "size": 150}, {"text": "PROFIT", "color": "red", "size": 150}]},
        {"glow": "gold", "lines": [{"text": "COMPANY SANK", "color": "red", "size": 130}, {"text": "CEO GOT", "color": "white", "size": 130}, {"text": "$1.7 BILLION", "color": "gold", "size": 140}]},
    ],
    "notes": "FACTS CHECKED (with source)\n"
             "- Founded 2010 (New York) by Adam Neumann and Miguel McKelvey; $47B valuation Jan 2019 (Wikipedia; Fox Business)\n"
             "- 2018: revenue $1.82B, net loss $1.6B; lease obligations $17.9B; Class B/C shares 20 votes vs 1 (The Motley Fool, S-1 coverage, Aug 14, 2019)\n"
             "- $5.9M paid to Neumann for the 'We' trademark, returned after backlash (Fox Business; Inc.)\n"
             "- Related-party leases in buildings Neumann had stakes in (disclosed in the S-1)\n"
             "- Neumann out as CEO Sep 24, 2019; IPO withdrawn Sep 30, 2019 (Wikipedia)\n"
             "- SoftBank takeover at ~$8B; Neumann deal up to $1.7B: ~$1B share purchase, $500M credit line, $185M consulting (TechCrunch, Oct 22, 2019, citing WSJ)\n"
             "- SPAC (BowX) listing Oct 2021 at ~$9B (REBusiness); never profitable (Fox Business)\n"
             "- Chapter 11 Nov 2023 (NJ); market cap ~$21M Dec 2023 (Wikipedia)\n"
             "- Exit from bankruptcy Jun 11, 2024; Yardi majority owner; $4B+ debt cut; ~170 locations exited (Newser, Jun 13, 2024)\n"
             "- a16z $350M into Flow, largest single check ever (TechCrunch, Aug 15, 2022)\n"
             "- ~2,400 layoffs announced Nov 21, 2019 (CNN); expected valuation reported at ~$10B in Sep 2019 (Wikipedia)\n"
             "- REVIEW: script pending Vinícius' approval",
}

d = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "projetos", "wework-en")
os.makedirs(os.path.join(d, "audio"), exist_ok=True)
json.dump(projeto, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
n = sum(len(s["text"].split()) for p in long_parts for s in p["sentences"])
print("long:", n, "words (~", round(n / 150, 1), "min);", "shorts:", [sum(len(s["text"].split()) for s in sh["sentences"]) for sh in shorts])
