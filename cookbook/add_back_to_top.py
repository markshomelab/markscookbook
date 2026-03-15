from bs4 import BeautifulSoup
from tkinter import Tk, filedialog

# open file picker
root = Tk()
root.withdraw()

file_path = filedialog.askopenfilename(
    title="Select HTML file",
    filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
)

if not file_path:
    print("No file selected.")
    exit()

# load HTML
with open(file_path, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# ensure body has id="top"
if soup.body and not soup.body.get("id"):
    soup.body["id"] = "top"
elif soup.body and soup.body.get("id") != "top":
    soup.body["id"] = "top"

# find all recipe cards
recipe_cards = soup.select("section.card.recipe-card")

added_count = 0
skipped_count = 0

for card in recipe_cards:
    existing = card.find("p", class_="back-top")
    if existing:
        skipped_count += 1
        continue

    back_p = soup.new_tag("p")
    back_p["class"] = "back-top"

    back_link = soup.new_tag("a", href="#top")
    back_link.string = "Back to top ↑"

    back_p.append(back_link)
    card.append(back_p)
    added_count += 1

# overwrite the same file with formatted HTML
with open(file_path, "w", encoding="utf-8") as f:
    f.write(soup.prettify())

print(f"Finished. File updated: {file_path}")
print(f"Back-to-top links added: {added_count}")
print(f"Skipped because already present: {skipped_count}")
