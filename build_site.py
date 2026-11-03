"""Build a static portfolio from site_content.json and templates/."""
from datetime import date
from html import escape
from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "site"
DATA = json.loads((ROOT / "site_content.json").read_text(encoding="utf-8"))

def esc(value):
    return escape(str(value), quote=True)

def fill(template_name, **values):
    text = (ROOT / "templates" / template_name).read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", str(value))
    return text

def card(item, href=None):
    inside = f'<small>{esc(item.get("category", "Project"))} · {esc(item.get("year", ""))}</small><h3>{esc(item["title"])}</h3><p class="muted">{esc(item.get("description", ""))}</p>'
    return f'<a class="card" href="{esc(href)}">{inside}</a>' if href else f'<article class="card">{inside}</article>'

def save_page(filename, title, description, content, prefix=""):
    html = fill("base.html", title=esc(title + " · " + DATA["name"]), description=esc(description), prefix=prefix,
                short=esc(DATA["short_name"]), name=esc(DATA["name"]), year=date.today().year, content=content)
    target = OUT / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")

def build():
    OUT.mkdir(exist_ok=True)
    (OUT / "assets").mkdir(exist_ok=True)
    (OUT / "assets" / "site.css").write_text((ROOT / "assets" / "site.css").read_text(encoding="utf-8"), encoding="utf-8")
    parts = DATA["tagline"].split(".", 1)
    line1 = esc(parts[0] + ("." if len(parts) > 1 else ""))
    line2 = esc(parts[1].strip() if len(parts) > 1 else "Make useful things")
    project_cards = []
    for index, project in enumerate(DATA["projects"], 1):
        slug = re.sub(r"[^a-z0-9]+", "-", project["title"].lower()).strip("-") or f"project-{index}"
        project["slug"] = slug
        project_cards.append(card(project, f"projects/{slug}.html"))
    content = fill("home.html", name=esc(DATA["name"]), role=esc(DATA["role"]), line1=line1, line2=line2,
                   intro=esc(DATA["intro"]), project_cards="".join(project_cards),
                   about="".join(f"<p>{esc(p)}</p>" for p in DATA["about"]),
                   tags="".join(f'<span class="tag">{esc(x)}</span>' for x in DATA["interests"]),
                   work="".join(f'<div class="row"><h3>{esc(x["title"])}</h3><p class="muted">{esc(x.get("description", ""))}</p></div>' for x in DATA["other_work"]),
                   contact_copy=esc(DATA["contact_copy"]), email=esc(DATA["email"]))
    save_page("index.html", "Home", DATA["intro"], content)
    about = '<section class="hero wrap"><div class="hero-inner"><div class="eyebrow">About</div><h1>Curious by nature.<br><span>Builder by habit.</span></h1><p class="intro">' + esc(DATA["intro"]) + '</p></div></section><section class="section"><article class="wrap copy">' + "".join(f"<p>{esc(p)}</p>" for p in DATA["about"]) + "</article></section>"
    save_page("about.html", "About", "About " + DATA["name"], about)
    listing_cards = []
    for project in DATA["projects"]:
        listing_cards.append(card(project, "projects/" + project["slug"] + ".html"))
        detail = fill("detail.html", category=esc(project.get("category", "Project")), year=esc(project.get("year", "")),
                      heading=esc(project["title"]), summary=esc(project.get("description", "")), url=esc(project.get("url", "#")),
                      details="".join(f"<p>{esc(p)}</p>" for p in project.get("details", ["Project details coming soon."])))
        save_page("projects/" + project["slug"] + ".html", project["title"], project.get("description", ""), detail, "../")
    projects = fill("listing.html", kicker="Selected work", heading="Projects.", intro="Projects, experiments, and useful things I have made.", cards="".join(listing_cards))
    save_page("projects.html", "Projects", "Projects by " + DATA["name"], projects)
    note_cards = "".join(card({"title": n["title"], "category": n.get("date", "Note"), "description": n.get("summary", "")}) for n in DATA["notes"])
    if not note_cards:
        note_cards = '<article class="card"><h3>Notes coming soon</h3><p class="muted">Add notes in site_content.json and rebuild to publish.</p></article>'
    notes = fill("listing.html", kicker="Writing & notes", heading="Things I’m thinking about.", intro="Short notes, ideas, and lessons from what I’m learning.", cards=note_cards)
    save_page("notes.html", "Notes", "Notes by " + DATA["name"], notes)
    socials = "".join(card({"title": item["label"], "description": item["url"], "category": "Find me online"}, item["url"]) for item in DATA["social"])
    contact = '<section class="hero wrap"><div class="hero-inner"><div class="eyebrow">Contact</div><h1>Let’s talk.</h1><p class="intro">' + esc(DATA["contact_copy"]) + '</p><div class="actions"><a class="button primary" href="mailto:' + esc(DATA["email"]) + '">Email me ↗</a></div></div></section><section class="section"><div class="wrap grid">' + socials + "</div></section>"
    save_page("contact.html", "Contact", "Contact " + DATA["name"], contact)
    (ROOT / "site_content.json").write_text(json.dumps(DATA, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Built {len(list(OUT.rglob('*.html')))} pages in {OUT}")

if __name__ == "__main__":
    build()
