#!/usr/bin/env python3
"""
Static site generator for chayananda.com (zero dependencies).

    python3 scripts/build.py

Writes plain HTML pages next to /assets. Vercel runs this on every deploy.
Edit content (CASES, EXPERIENCE, EDUCATION) below, then rebuild to preview.
"""
from __future__ import annotations

from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent.parent

SITE = {
    "name": "Chayananda Nagesh",
    "short": "Chaya",
    "role": "Senior Product Designer",
    "years": "8",
    "email": "nchayananda@gmail.com",
    "url": "https://chayananda.vercel.app",
    "dribbble": "https://dribbble.com/chayananda",
    "instagram": "https://www.instagram.com/chayananda.nagesh/",
    "goodreads": "https://www.goodreads.com/chayananda",
    "letterboxd": "https://letterboxd.com/chayananda/",
    "portrait": "https://framerusercontent.com/images/kZ0YMk93M25yCTgeSQVlRtni9KA.jpg?width=921&height=1247",
}

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    'family=Inter:wght@400;500;600&family=Inter+Tight:wght@500;600;700&'
    'family=JetBrains+Mono:wght@400;500&display=swap">'
)

# --------------------------------------------------------------------------
# Icons
# --------------------------------------------------------------------------
I = {
    "arrow": '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "back": '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13 8H3M7 4L3 8l4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "check": '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M4 10.5l4 4 8-9" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "menu": '<svg viewBox="0 0 20 20" width="18" height="18" fill="none" aria-hidden="true"><path d="M3 6h14M3 14h14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
    "copy": '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><rect x="5" y="5" width="8" height="8" rx="2" stroke="currentColor" stroke-width="1.4"/><path d="M3 10V4a1 1 0 011-1h6" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>',
    "eye": '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z" stroke="currentColor" stroke-width="1.5"/><circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="1.5"/></svg>',
    "cut": '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 6h16M7 12h10M10 18h4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
    "spark": '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
    "grid": '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3.5" y="3.5" width="7" height="7" rx="1.5" stroke="currentColor" stroke-width="1.5"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.5" stroke="currentColor" stroke-width="1.5"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.5" stroke="currentColor" stroke-width="1.5"/><path d="M14 17h6M17 14v6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
}

# --------------------------------------------------------------------------
# Image covers (files in assets/img/, 16:9, cropped to fit on smaller screens)
# --------------------------------------------------------------------------
def cover_image(src: str):
    def render() -> str:
        return f'<div class="cover cover--img" aria-hidden="true"><img src="/assets/img/{src}" alt="" decoding="async"></div>'
    return render


# --------------------------------------------------------------------------
# Code-drawn covers (no image requests, crisp at any size)
# --------------------------------------------------------------------------
def cover_iiq() -> str:
    rows = "".join(
        f'<div class="mk-row"><i></i><s></s><span style="--w:{w}%"></span><em></em></div>'
        for w in (92, 74, 58, 81, 36)
    )
    bars = "".join(f'<i style="height:{h}%"></i>' for h in (38, 52, 46, 64, 58, 72, 80, 76, 88))
    return f"""
<div class="cover cover--iiq" aria-hidden="true">
  <span class="cover__label">Impakt IQ · ESG audit workspace</span>
  <div class="mk-browser">
    <div class="mk-bar"><i></i><i></i><i></i><em></em></div>
    <div class="mk-app">
      <div class="mk-side"><b></b><span class="on"></span><span></span><span></span><span></span><span></span><span></span></div>
      <div class="mk-main">
        <div class="mk-tiles">
          <div class="mk-tile"><i></i><b>42</b><u>companies</u></div>
          <div class="mk-tile"><i></i><b>318</b><u>KPIs mapped</u></div>
          <div class="mk-tile"><i></i><b>86%</b><u>responses in</u></div>
          <div class="mk-tile"><i></i><b>4.1 d</b><u>to onboard</u></div>
        </div>
        <div class="mk-chart"><div class="mk-bars">{bars}</div><div class="mk-donut"><i></i></div></div>
        <div class="mk-rows">{rows}</div>
      </div>
    </div>
  </div>
</div>"""


def cover_ts() -> str:
    def week(on: int) -> str:
        return "".join(
            f'<i class="{"on" if d == on else ("ok" if d < on else "")}"></i>' for d in range(7)
        )

    def tasks(hours) -> str:
        return "".join(f'<div class="mk-task"><i></i><b>{h}</b><s></s></div>' for h in hours)

    return f"""
<div class="cover cover--ts" aria-hidden="true">
  <span class="cover__label">TCS Ultimatix · Timesheet</span>
  <div class="mk-phones">
    <div class="mk-phone"><div class="mk-ph-top"><b></b><i></i></div><div class="mk-week">{week(2)}</div><div class="mk-tasks">{tasks(("4h","3h","1h"))}</div><div class="mk-ph-cta"><i></i></div></div>
    <div class="mk-phone"><div class="mk-ph-top"><b></b><i></i></div><div class="mk-ring-wrap"><div class="mk-ring"></div><b>8:00</b></div><div class="mk-tasks">{tasks(("5h","3h"))}</div><div class="mk-ph-cta"><i></i></div></div>
    <div class="mk-phone"><div class="mk-ph-top"><b></b><i></i></div><div class="mk-week">{week(5)}</div><div class="mk-tasks">{tasks(("2h","6h","—"))}</div><div class="mk-ph-cta"><i></i></div></div>
  </div>
</div>"""


def cover_uls() -> str:
    sofa = (
        '<svg class="mk-sofa" viewBox="0 0 200 90" fill="none">'
        '<rect x="14" y="20" width="172" height="40" rx="12" fill="#8c6a52"/>'
        '<rect x="4" y="34" width="28" height="40" rx="10" fill="#7a5a45"/>'
        '<rect x="168" y="34" width="28" height="40" rx="10" fill="#7a5a45"/>'
        '<rect x="26" y="48" width="148" height="24" rx="8" fill="#a07b60"/>'
        '<line x1="100" y1="50" x2="100" y2="72" stroke="#7a5a45" stroke-width="2"/>'
        '<rect x="30" y="74" width="6" height="12" rx="2" fill="#2a211c"/>'
        '<rect x="164" y="74" width="6" height="12" rx="2" fill="#2a211c"/>'
        '<ellipse cx="100" cy="88" rx="96" ry="3" fill="rgba(0,0,0,.45)"/>'
        "</svg>"
    )
    return f"""
<div class="cover cover--uls" aria-hidden="true">
  <span class="cover__label">Urban Ladder · UL Studio for iPad</span>
  <div class="mk-tablet">
    <div class="mk-screen">
      <div class="mk-stage"><i class="mk-light l1"></i><i class="mk-light l2"></i><i class="mk-gizmo"></i>{sofa}</div>
      <div class="mk-panel">
        <b></b><div class="mk-slider" style="--v:68%"></div><div class="mk-slider" style="--v:32%"></div>
        <b></b><div class="mk-swatches"><i style="background:#a07b60"></i><i style="background:#4f5d52"></i><i style="background:#c9b9a3"></i><i style="background:#2f3a4a"></i></div>
        <b></b><div class="mk-slider" style="--v:50%"></div>
      </div>
      <div class="mk-tray"><i></i><i class="on"></i><i></i><i></i><i></i></div>
    </div>
  </div>
</div>"""


# --------------------------------------------------------------------------
# Content
# --------------------------------------------------------------------------
CASES = [
    {
        "slug": "impaktiq",
        "title": "Impakt IQ",
        "headline": "Turning a spreadsheet-and-email ESG audit into one platform, from zero to MVP in 16 weeks",
        "card_desc": "A 0→1 web platform that onboards companies, maps ESG KPIs and runs audit questionnaires in one place, replacing email threads and scattered workbooks.",
        "company": "Brillio for Impakt IQ",
        "platform": "Web · B2B SaaS",
        "timeline": "4 months (2024)",
        "role": "Lead product designer",
        "tags": ["0→1", "ESG", "B2B SaaS", "Design system"],
        "cover": cover_image("iiq.jpg"),
        "card_stats": [("−80%", "client onboarding time"), ("2.3×", "audits run per analyst"), ("16 wk", "kickoff to MVP")],
        "problem": (
            "Impakt IQ helps companies measure and report their sustainability impact. Every audit ran on email, "
            "spreadsheets and third-party forms. Onboarding a client took about three weeks, analysts chased KPI owners "
            "by hand, and nobody could see where an audit stood. The firm needed one product that could onboard companies, "
            "map ESG KPIs, collect answers and feed reports, and it needed an MVP inside a fixed four-month contract."
        ),
        "roles": [
            ("My role", "Sole designer. Led discovery, IA, interaction and visual design, and the design system through to dev handoff."),
            ("Team", "1 business analyst, 6 engineers across front end, back end and infra, client stakeholders from Impakt IQ."),
            ("Scope", "Onboarding, KPI mapping, questionnaires, audit tracking and role-based access for 5 user types."),
        ],
        "impact": [
            ("−80", "%", "Client onboarding time", "From ~15 working days to 3, measured on the first 12 companies onboarded.", 80),
            ("2.3", "×", "Audits per analyst per quarter", "Analysts moved from 3 to 7 concurrent audits without added headcount.", 70),
            ("−45", "%", "Questionnaire turnaround", "Median days to collect KPI responses, driven by owner assignment and reminders.", 45),
            ("6 → 1", "", "Tools replaced", "Email, 3 spreadsheets, a form tool and a file share consolidated into one workspace.", 100),
        ],
        "before": [
            "Client details, SOWs and contracts traded over email",
            "KPI mapping matrix rebuilt in Excel for every audit",
            "Account executives chased KPI owners one by one",
            "No shared view of audit progress",
        ],
        "after": [
            "Guided onboarding creates the company, divisions and CXO login in one flow",
            "Reusable KPI matrix by sector, industry and framework",
            "Owners assigned per KPI, with automatic reminders",
            "Live work plan with per-division progress",
        ],
        "decisions": [
            ("Designed around roles, not screens", "An RBAC exercise with the BA mapped <b>5 roles</b> and the permissions each needs. Because one person often holds two roles, I added a role switcher instead of separate logins, which removed an entire support category before launch."),
            ("Made the KPI matrix the product's spine", "Every later step, from assignment to scoring, reads from the matrix. Making it reusable by sector cut a typical setup from <b>2 days to under 3 hours</b>."),
            ("Shipped on Material, tuned to the brand", "I compared Material, Ant, Fluent, Carbon and Lightning against the engineers' component library. Material with a warm brand palette let the team ship <b>60+ dev-ready screens</b> without a single design-blocked sprint."),
            ("Re-scoped the work plan to what could ship", "The first concept paired a list with a Gantt chart that the front-end library couldn't support. I reworked it into a progress list with milestone chips, kept the information and saved an estimated <b>3 sprints</b>."),
        ],
        "shots": [
            ("https://framerusercontent.com/images/81jR64fvwHIvZj5mBw6hjdLDo.png?width=1200", "Final screens: companies, setup and work plan", True),
            ("https://framerusercontent.com/images/vGyM7wlc6KdGks0aeYHKhb1YG0w.png?width=1200", "Visual direction", False),
            ("https://framerusercontent.com/images/C2InrC7rKSzqGdcv6en5Jnw8WyA.png?width=1200", "Brand-tuned Material system", False),
        ],
        "reflection": "The fastest way through a 0→1 project with a fixed deadline was to agree early on what the MVP would leave out. Reports stayed outside the product for v1, which kept the team focused on the part of the workflow that cost the client the most time.",
    },
    {
        "slug": "timesheet",
        "title": "TCS Timesheet",
        "headline": "Taking timesheets for 600,000+ TCS employees from desktop-only to a one-minute mobile habit",
        "card_desc": "A hybrid mobile timesheet for Tata Consultancy Services that lets employees in 46 countries log, copy and submit their day from a phone.",
        "company": "Tata Consultancy Services",
        "platform": "Mobile · iOS & Android (Ionic)",
        "timeline": "6 months, 2 releases",
        "role": "UX designer & researcher",
        "tags": ["Enterprise mobile", "600K+ users", "Usability testing"],
        "cover": cover_image("timesheet.jpg"),
        "card_stats": [("600K+", "employees"), ("−76%", "time to log a day"), ("100%", "task success in testing")],
        "problem": (
            "Every TCS employee must log their hours before month-end to get paid. The timesheet lived in a dense web "
            "app built for desktops, so people working on client sites or travelling batched entries at the last minute. "
            "Late and corrected submissions created payroll rework. Overseas employees, who bill hourly and log breaks and "
            "overtime, had a separate and even heavier flow."
        ),
        "roles": [
            ("My role", "UX designer and researcher. Owned research, flows, prototyping, usability testing and the visual design for both releases."),
            ("Team", "Product owner, Ultimatix platform team and an Ionic development squad of 5."),
            ("Scope", "Release 1: regular timesheet for India. Release 2: overtime timesheet for overseas employees."),
        ],
        "impact": [
            ("−76", "%", "Time to log a workday", "From 3 min 40 s on the web flow to 52 s on mobile in moderated tests.", 76),
            ("41", "%", "Submissions made on mobile", "Share of monthly timesheets submitted from the app six months after launch.", 41),
            ("−28", "%", "Late submissions", "Month-end late or corrected timesheets in the two quarters after rollout.", 28),
            ("100", "%", "Task completion", "All 5 test tasks completed with no abandonment across test sessions.", 100),
        ],
        "before": [
            "Web-only timesheet with a full-month grid",
            "All 7 charge types shown on every task",
            "Copying effort meant re-entering it day by day",
            "Overtime users mixed breaks and billable time by hand",
        ],
        "after": [
            "Week view by default, expanding to month on demand",
            "The 1–2 charge types people actually use come first",
            "Copy a day's effort to a day, week or month with a preview",
            "Break logging with automatic billable vs working hours",
        ],
        "decisions": [
            ("Defaulted to what 70% of people do", "Usage data showed about <b>70% of employees use one or two charge types</b> and most work on assigned tasks. Assigned tasks became the landing tab and rare charge types moved behind a single tap."),
            ("Copy with a preview", "Recorded Webex sessions showed people filling identical days over and over. Copy-effort lets them repeat a day across a week or month, and a calendar preview shows exactly which days will change before they confirm."),
            ("Week first, month on demand", "A full-month grid doesn't fit a 360 px screen. The week strip shows status at a glance and expands into a month view through a single handle."),
            ("One framework, two audiences", "Release 2 reused release 1's components and added a hub-and-spoke model for overtime: billing type, breaks and on-call each open their own sub-page. Reuse cut release 2's design time by about <b>40%</b>."),
        ],
        "shots": [
            ("https://framerusercontent.com/images/9qXuNAxqO7ypx4u55fba0EFqHZM.png?width=1200", "Final screens: regular timesheet", True),
            ("https://framerusercontent.com/images/8UvxL2jLQx8krAajyMWrIiD7YqU.png?width=1200", "Final screens: overtime timesheet", True),
            ("https://framerusercontent.com/images/bikvkehBoSXSoA5d89BIPR3OvQE.png?width=1000", "Interactive concept exploration in Axure", False),
        ],
        "reflection": "At this scale the best features were the ones that removed decisions. Most of the time savings came from good defaults rather than new functionality.",
    },
    {
        "slug": "ulstudio",
        "title": "UL Studio",
        "headline": "Giving Urban Ladder's art directors a virtual photo studio on iPad to launch products faster",
        "card_desc": "An iPad app that lets art directors stage furniture in a 3D studio, compose shots and push renders to approval without a physical photoshoot.",
        "company": "Urban Ladder",
        "platform": "Tablet · iPadOS",
        "timeline": "6 months",
        "role": "UX designer (NID graduation project)",
        "tags": ["0→1", "3D tooling", "Retail", "NID project"],
        "cover": cover_image("ulstudio.jpg"),
        "card_stats": [("20", "stakeholder interviews"), ("−64%", "image turnaround"), ("−55%", "cost per hero shot")],
        "problem": (
            "Product images drive furniture purchases online, and every new Urban Ladder product needed them before "
            "launch. Physical shoots meant booking studios, moving furniture and coordinating photographers. 3D renders "
            "depended on specialist artists and long feedback loops between eight teams. Image creation had become the "
            "slowest step in a product launch."
        ),
        "roles": [
            ("My role", "UX designer, researcher and visual designer. This was my M.Des graduation project at the National Institute of Design."),
            ("Team", "Reviewed weekly with the VP Product, VP Engineering and the then-CEO. Worked with 3D artists and art directors."),
            ("Scope", "MVP of Studio (scene setup and shot composition) and Assets (exports, approvals and comments)."),
        ],
        "impact": [
            ("−64", "%", "Image turnaround per product", "From ~14 days to 5 in the pilot, by removing studio booking and file hand-offs.", 64),
            ("−55", "%", "Cost per hero image", "Projected against the cost of a physical studio shoot, per category team's estimate.", 55),
            ("3 → 1", "", "Hand-offs per shot", "Art directors compose and submit directly instead of briefing a 3D artist.", 66),
            ("20", "", "Stakeholder interviews", "Across art direction, photography, 3D, product, category and marketing.", 100),
        ],
        "before": [
            "Physical shoots with studio booking and logistics",
            "Art directors briefed 3D artists through long email threads",
            "Files traded between 8 departments with no single source",
            "Feedback arrived after renders were done",
        ],
        "after": [
            "Art directors place products and lights in a virtual studio",
            "Scene setups saved, edited and exported for rendering",
            "Searchable asset library tied to each launch",
            "Comments and approvals on the image itself",
        ],
        "decisions": [
            ("Designed for art directors, not 3D artists", "Pro tools like Maya and 3ds Max expose hundreds of controls. I limited the studio to camera, lights, material and placement, and used photography language instead of 3D terms, so art directors could work without training."),
            ("Prototyped 3D interaction with real users", "Sketch couldn't prototype 3D, so I tested gestures in Set A Light Studio and recorded art directors moving cameras and lights. That fixed the orbit, pan and drop-in gestures before engineering started."),
            ("Moved steps to the back end", "Leadership reviews pushed for automation. Rendering, file naming and versioning happen on the server, which cut the flow from <b>11 steps to 6</b>."),
        ],
        "shots": [
            ("https://framerusercontent.com/images/H9aqZ2Xuw9PYMoyH4F5eZRfBs.png?width=1200", "Proof of concept: scene setup and shot composition", True),
            ("https://framerusercontent.com/images/ZHPw5qOET90XAVIBuYZxaqns.png?width=1200", "Tablet wireframes", True),
            ("https://framerusercontent.com/images/dpv34NqCC5xItzXYYT3Z60yu0.png?width=1200", "Information architecture", False),
        ],
        "reflection": "Working with a CEO who reviewed every week taught me to bring decisions, not options. The project also set the approach I still use from NID: understand the whole system before designing any single screen.",
    },
]

EXPERIENCE = [
    ("Feb 2024 — Now", "Senior Product Designer", "Brillio · Hyderabad", "Design lead on enterprise SaaS and AI products for global clients, including the Impakt IQ ESG platform. Own research, IA, interaction design and design systems from discovery to handoff."),
    ("Sep 2022 — Jul 2023", "UX Design Specialist", "Schneider Electric · Bengaluru", "Designed workflows for energy management and building automation software used by facility and operations teams."),
    ("Jul 2018 — Sep 2022", "UX Designer", "Tata Consultancy Services · Thane", "Designed employee-facing products on the Ultimatix platform, including the mobile timesheet used by 600,000+ employees, plus HR and intranet portals."),
    ("Jun 2016 — Jan 2017", "UX Design Intern", "Urban Ladder · Bengaluru", "Built UL Studio, an iPad virtual photo studio for art directors, as my NID graduation project."),
]

EDUCATION = [
    ("2014 — 2017", "M.Des, Interaction Design", "National Institute of Design (NID) · Bengaluru", "Two and a half years of studio-based training in interaction design, research and systems thinking at India's premier design school."),
    ("2009 — 2013", "B.E, Computer Science & Engineering", "Visvesvaraya Technological University (VTU) · Bengaluru", "Engineering foundation that still shapes how I work with developers and scope what can ship."),
]

PRINCIPLES = [
    ("eye", "Make it obvious", "Products that look good, read clearly and work without a manual."),
    ("cut", "Design by elimination", "I explore widely, then remove options until the strongest one is left."),
    ("spark", "Push the product forward", "I bring emerging patterns and tech to teams and stakeholders early."),
    ("grid", "Leave a clear trail", "Documented decisions and tracked work so teams know what changed and why."),
]


# --------------------------------------------------------------------------
# Partials
# --------------------------------------------------------------------------
def head(title: str, desc: str, root: str) -> str:
    return dedent(f"""\
    <!doctype html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta name="theme-color" content="#08090b">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:type" content="website">
    <link rel="icon" href="{root}favicon.ico" sizes="48x48">
    <link rel="icon" href="{root}assets/icons/favicon.svg" type="image/svg+xml">
    <link rel="icon" href="{root}assets/icons/favicon-32.png" type="image/png" sizes="32x32">
    <link rel="apple-touch-icon" href="{root}assets/icons/apple-touch-icon.png">
    {FONTS}
    <link rel="stylesheet" href="{root}assets/css/site.css">
    <script src="{root}assets/js/site.js" defer></script>
    </head>
    <body>
    <a class="skip" href="#main">Skip to content</a>
    """)


def nav(root: str, current: str) -> str:
    def link(href: str, label: str, key: str) -> str:
        cur = ' aria-current="page"' if key == current else ""
        return f'<a href="{root}{href}"{cur}>{label}</a>'

    return f"""
<header class="nav">
  <div class="wrap nav__inner">
    <a class="brand" href="{root}index.html" aria-label="{SITE['name']}, home">{SITE['name']}</a>
    <button class="nav__toggle" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav-links">{I['menu']}</button>
    <nav class="nav__links" id="nav-links" aria-label="Primary">
      {link("index.html#work", "Work", "work")}
      {link("about/index.html", "About", "about")}
      {link("index.html#education", "Education", "education")}
      <a class="btn btn--primary nav__cta" href="{root}index.html#contact">Get in touch</a>
    </nav>
  </div>
</header>"""


def footer(root: str) -> str:
    return f"""
<footer class="footer">
  <div class="wrap footer__inner">
    <p>© <span data-year>2026</span> {SITE['name']} · Interaction Design, National Institute of Design</p>
    <div class="footer__links">
      <a href="{SITE['dribbble']}" target="_blank" rel="noopener">Dribbble</a>
      <a href="{SITE['instagram']}" target="_blank" rel="noopener">Instagram</a>
      <a href="{SITE['goodreads']}" target="_blank" rel="noopener">Goodreads</a>
      <a href="{SITE['letterboxd']}" target="_blank" rel="noopener">Letterboxd</a>
    </div>
  </div>
</footer>
</body>
</html>
"""


def contact_panel() -> str:
    return f"""
<section class="section section--tight" id="contact">
  <div class="wrap">
    <div class="cta-panel reveal">
      <span class="eyebrow">Open to Lead &amp; Senior roles</span>
      <h2 class="grad">Let's build something people finish using.</h2>
      <p class="lede">I'm looking for senior and lead product design roles on complex enterprise and AI products. Based in Bengaluru, open to hybrid and remote.</p>
      <div class="email-row">
        <code>{SITE['email']}</code>
        <button class="btn" type="button" data-copy="{SITE['email']}">{I['copy']}<span>Copy email</span></button>
        <a class="btn btn--primary" href="mailto:{SITE['email']}">Write to me {I['arrow']}</a>
      </div>
    </div>
  </div>
</section>"""


def holo_cards() -> str:
    """Education badges: metallic medallions that tilt, catch light and spin on tap."""
    def badge(mod: str, label: str, core: str, kind: str, degree: str, field: str, inst: str, years: str, delay: str = "") -> str:
        return f"""
  <div class="reveal"{delay}>
    <div class="holo holo--{mod}" tabindex="0" role="button" aria-label="{label}. Press to spin the badge.">
      <div class="badge__stage">
        <div class="badge__medal">
          <div class="badge__front">
            <div class="badge__rim"></div>
            <div class="badge__core">{core}</div>
            <div class="badge__shine"></div>
          </div>
          <div class="badge__back"><span>{years.split(" · ")[0]}</span></div>
        </div>
        <div class="badge__shadow"></div>
      </div>
      <div class="badge__text">
        <span class="badge__kind">{kind}</span>
        <span class="badge__degree">{degree}</span>
        <span class="badge__field">{field}</span>
        <span class="badge__inst">{inst}</span>
      </div>
    </div>
    <p class="holo__hint mono">{years}</p>
  </div>"""

    nid = badge(
        "nid", "Master of Design in Interaction Design, National Institute of Design, 2014 to 2017",
        '<span class="badge__emboss"><i class="badge__logo badge__logo--nid"></i></span>',
        "Postgraduate", "M.Des", "Interaction Design", "National Institute of Design, Bengaluru",
        "2014 — 2017 · Bengaluru campus",
    )
    vtu = badge(
        "vtu", "Bachelor of Engineering in Computer Science, Visvesvaraya Technological University, 2009 to 2013",
        '<img class="badge__seal" src="/assets/img/vtu.png" alt="" decoding="async">',
        "Undergraduate", "B.E", "Computer Science &amp; Engineering", "Visvesvaraya Technological University",
        "2009 — 2013 · Bengaluru", ' data-delay="1"',
    )
    return f'<div class="creds">{nid}{vtu}\n</div>'


def work_card(c: dict, root: str, delay: int = 0) -> str:
    href = f"{root}case-studies/{c['slug']}/index.html"
    tags = "".join(f'<span class="tag">{t}</span>' for t in c["tags"])
    stats = "".join(f"<div><b>{n}</b><span>{l}</span></div>" for n, l in c["card_stats"])
    return f"""
<article class="work-card reveal" data-delay="{delay}">
  <div class="work-card__media">{c['cover']()}</div>
  <div class="work-card__body">
    <div>
      <div class="work-card__meta"><span class="tag">{c['company']}</span>{tags}</div>
      <h3 class="work-card__title">{c['headline']}</h3>
      <p class="work-card__desc">{c['card_desc']}</p>
      <span class="work-card__cta">Read case study {I['arrow']}</span>
    </div>
    <div class="work-card__stats">{stats}</div>
  </div>
  <a class="work-card__link" href="{href}" aria-label="Read the {c['title']} case study"></a>
</article>"""


def timeline_rows(items, edu=False) -> str:
    cls = "tl-row tl-row--edu" if edu else "tl-row"
    return "".join(
        f'<div class="{cls}"><span class="tl-row__when">{w}</span><div class="tl-row__role"><h3>{r}</h3><p>{o}</p></div><p class="tl-row__what">{d}</p></div>'
        for w, r, o, d in items
    )


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------
def page_home() -> str:
    root = ""
    cards = "".join(work_card(c, root, i % 3) for i, c in enumerate(CASES))
    principles = "".join(
        f'<div class="principle reveal" data-delay="{i}">{I[ic]}<h3>{t}</h3><p>{d}</p></div>'
        for i, (ic, t, d) in enumerate(PRINCIPLES)
    )
    return (
        head(f"{SITE['name']} · Product Designer", f"{SITE['name']} is a Senior Product Designer with {SITE['years']} years of experience and an M.Des in Interaction Design from the National Institute of Design (NID).", root)
        + nav(root, "")
        + f"""
<main id="main">
  <section class="hero">
    <div class="glow" aria-hidden="true"></div>
    <div class="grid-bg" aria-hidden="true"></div>
    <div class="wrap hero__inner">
      <a class="chip reveal" href="#education"><span class="chip__dot">NID</span>M.Des Interaction Design, National Institute of Design</a>
      <h1 class="grad reveal" data-delay="1">Calm, clear products for complex enterprise work.</h1>
      <p class="lede reveal" data-delay="2">I'm Chaya, a Senior Product Designer with {SITE['years']} years of experience shipping enterprise software across ESG, HR-tech, energy and retail. Trained at the National Institute of Design, I turn tangled workflows into products teams actually finish using.</p>
      <div class="hero__actions reveal" data-delay="3">
        <a class="btn btn--primary" href="#work">View selected work {I['arrow']}</a>
        <a class="btn" href="about/index.html">About me</a>
      </div>
      <div class="hero__meta reveal" data-delay="3">
        <span><i class="status-dot" aria-hidden="true"></i>Open to Lead / Senior roles</span>
        <span>Bengaluru, India</span>
        <span>Senior Product Designer at Brillio</span>
      </div>
    </div>
  </section>

  <section class="section--tight" aria-label="Career highlights">
    <div class="wrap">
      <div class="kpis reveal">
        <div class="kpi"><span class="kpi__num">{SITE['years']}<small>yrs</small></span><span class="kpi__label">Product &amp; UX design</span><span class="kpi__note">Since 2016 · NID-trained</span></div>
        <div class="kpi"><span class="kpi__num">600K<small>+</small></span><span class="kpi__label">Users on products I've shipped</span><span class="kpi__note">TCS Timesheet, 46 countries</span></div>
        <div class="kpi"><span class="kpi__num">2<small>×</small></span><span class="kpi__label">0→1 platforms led</span><span class="kpi__note">Impakt IQ · UL Studio</span></div>
        <div class="kpi"><span class="kpi__num">−76<small>%</small></span><span class="kpi__label">Time to log a workday</span><span class="kpi__note">Mobile vs web timesheet</span></div>
      </div>
      <div class="logos reveal" style="margin-top:40px" aria-label="Where I've worked and studied">
        <span>Brillio</span><span>Schneider Electric</span><span>Tata Consultancy Services</span><span>Urban Ladder</span><span>Impakt IQ</span><span class="is-nid">NID</span>
      </div>
    </div>
  </section>

  <section class="section" id="work">
    <div class="wrap">
      <div class="sec-head reveal">
        <span class="eyebrow">Selected work</span>
        <h2 class="h-section grad">Shipped products, measured outcomes.</h2>
        <p class="lede">Three projects across web, mobile and tablet. Each one starts with the problem, then shows the decisions and the numbers that moved.</p>
      </div>
      <div class="work">{cards}</div>
    </div>
  </section>

  <section class="section" id="education">
    <div class="wrap">
      <div class="sec-head reveal">
        <span class="eyebrow">Education</span>
        <h2 class="h-section grad">Engineer by training. Designer by NID.</h2>
        <p class="lede">A computer science degree taught me how software is built. The National Institute of Design taught me who it's for. Tilt the badges, or tap one to spin it.</p>
      </div>
      {holo_cards()}
      <div class="nid-band reveal" style="margin-top:clamp(40px,6vw,72px)">
        <div class="stack">
          <span class="eyebrow">National Institute of Design</span>
          <h2>India's premier design school, and where my practice began.</h2>
          <p class="muted">NID's studio method shapes how I work: start with people and context, make things to think, and critique in the open.</p>
        </div>
        <ul>
          <li>{I['check']}<span>M.Des in Interaction Design, 2014–2017</span></li>
          <li>{I['check']}<span>Graduation project with Urban Ladder became UL Studio</span></li>
          <li>{I['check']}<span>Studio training in research, systems thinking and prototyping</span></li>
          <li>{I['check']}<span>Engineering + NID: designs that respect how products get built</span></li>
        </ul>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="sec-head reveal">
        <span class="eyebrow">How I work</span>
        <h2 class="h-section grad">Four habits behind every project.</h2>
      </div>
      <div class="principles">{principles}</div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="sec-head sec-head--split reveal">
        <div class="stack"><span class="eyebrow">Experience</span><h2 class="h-section grad">{SITE['years']} years, four companies.</h2></div>
        <a class="btn" href="about/index.html">Full profile {I['arrow']}</a>
      </div>
      <div class="timeline reveal">{timeline_rows(EXPERIENCE)}{timeline_rows(EDUCATION[:1], edu=True)}</div>
    </div>
  </section>
  {contact_panel()}
</main>"""
        + footer(root)
    )


def page_about() -> str:
    root = "../"
    skills = [
        ("Product design", ["End-to-end product design", "Interaction design", "Information architecture", "Design systems", "Prototyping", "UI copy"]),
        ("Research &amp; strategy", ["User interviews", "Usability testing", "Stakeholder mapping", "Journey &amp; service maps", "RBAC &amp; workflow modelling", "Workshop facilitation"]),
        ("Tools", ["Figma", "Axure RP", "Adobe Creative Suite", "Cinema 4D", "Blender", "HTML / CSS"]),
    ]
    sk = "".join(
        f'<div class="skill-group reveal" data-delay="{i}"><h3>{t}</h3><div class="tags">{"".join(f"<span class=tag>{x}</span>" for x in xs)}</div></div>'
        for i, (t, xs) in enumerate(skills)
    )
    return (
        head(f"About · {SITE['name']}", f"About {SITE['name']}, Senior Product Designer and National Institute of Design alumnus.", root)
        + nav(root, "about")
        + f"""
<main id="main">
  <section class="hero">
    <div class="glow" aria-hidden="true"></div>
    <div class="wrap about-hero" style="position:relative;z-index:1">
      <div class="stack" style="gap:24px">
        <a class="chip reveal" href="#education"><span class="chip__dot">NID</span>Interaction Design alumnus</a>
        <h1 class="grad reveal" data-delay="1" style="font-size:var(--step-4)">From engineer to designer, {SITE['years']} years in.</h1>
        <p class="lede reveal" data-delay="2">I studied computer science at VTU, then Interaction Design at the National Institute of Design. Since then I've designed enterprise products at Tata Consultancy Services, Schneider Electric and Brillio, across HR, energy, ESG audit and retail technology.</p>
        <p class="lede reveal" data-delay="2">I'm at my best on products with many roles, rules and edge cases, where clear structure matters more than decoration. I work closely with engineers, and I like to leave teams with systems they can keep using after I've moved on.</p>
        <div class="hero__actions reveal" data-delay="3"><a class="btn btn--primary" href="../index.html#work">See the work {I['arrow']}</a><a class="btn" href="../index.html#contact">Contact</a></div>
      </div>
      <div class="portrait reveal" data-delay="2">
        <span class="portrait__mono" aria-hidden="true">CN</span>
        <img src="{SITE['portrait']}" alt="Portrait of {SITE['name']}" loading="lazy" onerror="this.remove()">
        <div class="portrait__tag"><span>{SITE['name']}</span><span class="muted">Bengaluru</span></div>
      </div>
    </div>
  </section>

  <section class="section--tight">
    <div class="wrap">
      <div class="kpis reveal">
        <div class="kpi"><span class="kpi__num">{SITE['years']}<small>yrs</small></span><span class="kpi__label">Industry experience</span></div>
        <div class="kpi"><span class="kpi__num">5</span><span class="kpi__label">Domains</span><span class="kpi__note">ESG · HR · Energy · Retail · Intranet</span></div>
        <div class="kpi"><span class="kpi__num">3</span><span class="kpi__label">States</span><span class="kpi__note">Karnataka · Maharashtra · Telangana</span></div>
        <div class="kpi"><span class="kpi__num">NID</span><span class="kpi__label">M.Des Interaction Design</span></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="sec-head reveal"><span class="eyebrow">Career</span><h2 class="h-section grad">Where I've worked.</h2></div>
      <div class="timeline reveal">{timeline_rows(EXPERIENCE)}</div>
    </div>
  </section>

  <section class="section" id="education">
    <div class="wrap">
      <div class="sec-head reveal"><span class="eyebrow">Education</span><h2 class="h-section grad">National Institute of Design, and an engineering degree before it.</h2></div>
      {holo_cards()}
      <div class="timeline reveal" style="margin-top:48px">{timeline_rows(EDUCATION, edu=True)}</div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="sec-head reveal"><span class="eyebrow">Capabilities</span><h2 class="h-section grad">What I bring to a team.</h2></div>
      <div class="skills">{sk}</div>
    </div>
  </section>
  {contact_panel()}
</main>"""
        + footer(root)
    )


def page_case(c: dict, idx: int) -> str:
    root = "../../"
    facts = "".join(
        f"<div><dt>{k}</dt><dd>{v}</dd></div>"
        for k, v in (("Company", c["company"]), ("Platform", c["platform"]), ("Timeline", c["timeline"]), ("Role", c["role"]))
    )
    roles = "".join(f"<div><h3>{t}</h3><p>{d}</p></div>" for t, d in c["roles"])
    impact = "".join(
        f'<div class="impact__item"><span class="impact__num">{n}<span class="unit">{u}</span></span>'
        f'<span class="impact__label">{l}</span><span class="impact__ctx">{ctx}</span>'
        f'<div class="impact__bar" aria-hidden="true"><i style="--w:{w}%"></i></div></div>'
        for n, u, l, ctx, w in c["impact"]
    )
    before = "".join(f"<li>{x}</li>" for x in c["before"])
    after = "".join(f"<li>{x}</li>" for x in c["after"])
    decisions = "".join(f'<div class="decision"><div><h3>{t}</h3><p>{d}</p></div></div>' for t, d in c["decisions"])
    shots = "".join(
        f'<figure class="shot{" shot--crop" if crop else ""}" data-alt="{cap}. Image unavailable.">'
        f'<img src="{src}" alt="{cap}" loading="lazy" decoding="async">'
        f'<figcaption><span>{cap}</span><span>{c["title"]}</span></figcaption></figure>'
        for src, cap, crop in c["shots"]
    )
    others = [o for o in CASES if o["slug"] != c["slug"]]
    nxt = "".join(
        f'<a href="{root}case-studies/{o["slug"]}/index.html"><small>{"Next" if i == 0 else "Also see"}</small><b>{o["title"]}</b><span class="muted">{o["company"]} · {o["platform"]}</span></a>'
        for i, o in enumerate(others)
    )
    toc = "".join(
        f'<a href="#{k}">{v}</a>'
        for k, v in (("overview", "Overview"), ("impact", "Impact"), ("shift", "What changed"), ("decisions", "Key decisions"), ("screens", "Screens"), ("reflection", "Reflection"))
    )
    nid_note = (
        '<p class="muted" style="font-size:14px">Design approach grounded in my Interaction Design training at the National Institute of Design (NID).</p>'
    )
    return (
        head(f"{c['title']} · {SITE['name']}", c["card_desc"], root)
        + nav(root, "work")
        + f"""
<main id="main">
  <section class="cs-hero">
    <div class="glow" aria-hidden="true"></div>
    <div class="wrap cs-hero__inner">
      <a class="cs-back" href="{root}index.html#work">{I['back']}All work</a>
      <span class="eyebrow">Case study · {c['title']}</span>
      <h1 class="grad">{c['headline']}</h1>
      <dl class="cs-facts">{facts}</dl>
      <div class="cs-cover">{c['cover']()}</div>
    </div>
  </section>

  <section class="section">
    <div class="wrap cs-layout">
      <nav class="cs-toc" aria-label="On this page">{toc}</nav>
      <div class="cs-body">
        <section class="cs-sec" id="overview">
          <span class="eyebrow">Overview</span>
          <h2>The problem</h2>
          <p>{c['problem']}</p>
          <div class="role-card">{roles}</div>
          {nid_note}
        </section>

        <section class="cs-sec" id="impact">
          <span class="eyebrow">Impact</span>
          <h2>What moved</h2>
          <div class="impact">{impact}</div>
        </section>

        <section class="cs-sec" id="shift">
          <span class="eyebrow">Before / after</span>
          <h2>What changed for users</h2>
          <div class="ba">
            <div class="ba__col"><h3>Before</h3><ul>{before}</ul></div>
            <div class="ba__col ba__col--after"><h3>After</h3><ul>{after}</ul></div>
          </div>
        </section>

        <section class="cs-sec" id="decisions">
          <span class="eyebrow">Key decisions</span>
          <h2>The calls that shaped it</h2>
          <div class="decisions">{decisions}</div>
        </section>

        <section class="cs-sec" id="screens">
          <span class="eyebrow">Screens</span>
          <h2>The work</h2>
          <div class="gallery">{shots}</div>
        </section>

        <section class="cs-sec" id="reflection">
          <span class="eyebrow">Reflection</span>
          <h2>What I took away</h2>
          <blockquote class="quote">{c['reflection']}<cite>{SITE['name']} · {c['role']}</cite></blockquote>
        </section>

        <div class="next-cs">{nxt}</div>
      </div>
    </div>
  </section>
  {contact_panel()}
</main>"""
        + footer(root)
    )


def write(path: str, html: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding="utf-8")
    print(f"  wrote {path}  ({len(html)/1024:.1f} KB)")


def main() -> None:
    print("Building site...")
    write("index.html", page_home())
    write("about/index.html", page_about())
    for i, c in enumerate(CASES):
        write(f"case-studies/{c['slug']}/index.html", page_case(c, i))
    # Keep the old /portfolio URL working
    write("portfolio/index.html", '<!doctype html><meta charset="utf-8"><title>Work · Chayananda Nagesh</title>'
          '<meta http-equiv="refresh" content="0; url=../index.html#work"><link rel="canonical" href="../index.html#work">'
          '<a href="../index.html#work">Selected work</a>')
    print("Done.")


if __name__ == "__main__":
    main()
