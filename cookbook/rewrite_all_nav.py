from bs4 import BeautifulSoup
from pathlib import Path

NAV = [
    ("index.html", "Home"),
    ("1breakfast.html", "Breakfast"),
    ("2entrees.html", "Entrées"),
    ("3grains.html", "Pasta, Noodles & Grains"),
    ("4sides.html", "Appetizers, Salads & Sides"),
    ("5sauces.html", "Sauces, Dressings & Condiments"),
    ("6seasonings.html", "Spice Blends & Seasonings"),
    ("7breads.html", "Breads"),
    ("8desserts.html", "Desserts"),
]

CHAPTER_FILES = {
    "1breakfast.html",
    "2entrees.html",
    "3grains.html",
    "4sides.html",
    "5sauces.html",
    "6seasonings.html",
    "7breads.html",
    "8desserts.html",
}

base_dir = Path(__file__).resolve().parent

updated = 0
skipped = 0

for filename in CHAPTER_FILES:
    path = base_dir / filename

    if not path.exists():
        print(f"Skipped {filename}: file not found.")
        skipped += 1
        continue

    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    body = soup.body
    if body is None:
        print(f"Skipped {filename}: no <body> found.")
        skipped += 1
        continue

    h1 = body.find("h1")
    if h1 is None:
        print(f"Skipped {filename}: no <h1> found.")
        skipped += 1
        continue

    old_nav = body.find("nav", class_="site-nav")
    if old_nav:
        old_nav.decompose()

    nav = soup.new_tag("nav")
    nav["class"] = "site-nav"

    for i, (href, label) in enumerate(NAV):
        if href == filename:
            el = soup.new_tag("span")
            el["class"] = "current"
            el.string = label
        else:
            el = soup.new_tag("a", href=href)
            el.string = label

        nav.append(el)

        if i < len(NAV) - 1:
            nav.append("\n  ·\n  ")

    h1.insert_after("\n")
    h1.insert_after(nav)

    with open(path, "w", encoding="utf-8") as f:
        f.write(soup.prettify())

    print(f"Updated {filename}")
    updated += 1

print(f"\nDone. Updated {updated} file(s).")
print(f"Skipped {skipped} file(s).")

input("\nPress Enter to close...")
