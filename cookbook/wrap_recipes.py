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

body = soup.body

new_body = []
current_section = None

for element in list(body.children):

    if getattr(element, "name", None) == "h2":

        if current_section:
            new_body.append(current_section)

        current_section = soup.new_tag("section")
        current_section["class"] = ["card", "recipe-card"]
        current_section.append(element)

    else:

        if current_section:
            current_section.append(element)
        else:
            new_body.append(element)

if current_section:
    new_body.append(current_section)

body.clear()

for item in new_body:
    body.append(item)

# overwrite the same file with formatted HTML
with open(file_path, "w", encoding="utf-8") as f:
    f.write(soup.prettify())

print("Finished. File updated:", file_path)
