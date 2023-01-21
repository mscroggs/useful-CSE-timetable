import os
import sys
import json
from unidecode import unidecode

dir = os.path.dirname(os.path.realpath(__file__))
source_dir = os.path.join(dir, "html")

if len(sys.argv) == 2:
    target_dir = sys.argv[1]
else:
    assert len(sys.argv) == 1
    target_dir = os.path.join(dir, "_html")


def to_html(txt):
    return txt.encode('ascii', 'xmlcharrefreplace').decode("utf-8")


with open(os.path.join(dir, "talks.json")) as f:
    talks_json = f.read()
with open(os.path.join(dir, "order.json")) as f:
    order_json = f.read()

talks = json.loads(talks_json)
order = json.loads(order_json)

speakers = []
for i, t in talks.items():
    if "speaker" in t:
        speakers.append([unidecode(", ".join(t["speaker"][::-1])).upper(), " ".join(t["speaker"]), order.index(i)])
    elif "panel" in t:
        for person in t["panel"]:
            speakers.append([unidecode(", ".join(person[::-1])).upper(), " ".join(person), order.index(i)])

speakers.sort(key=lambda x: x[0])

list_speakers = "<br />".join([
    f"<a href='javascript:toggle_star({s[2]})'><span class='star{s[2]}'>&star;</span></a> {to_html(s[1])}"
    for s in speakers
    if "ANNOUNCED" not in s[0]
])

titles = []
for i, t in talks.items():
    titles.append([t["title"].upper(), t["title"], order.index(i)])

titles.sort(key=lambda x: x[0])

list_titles = "<br />".join([
    f"<a href='javascript:toggle_star({t[2]})'><span class='star{t[2]}'>&star;</span></a> {to_html(t[1])}"
    for t in titles
])

replacements = {}


def replace(content):
    content = content.replace("{{list-speakers}}", list_speakers)
    content = content.replace("{{list-titles}}", list_titles)
    content = content.replace("{{talks.json}}", talks_json)
    content = content.replace("{{order.json}}", order_json)
    for i, j in replacements.items():
        content = content.replace("{{" + i + "}}", j)
    return content


for file in os.listdir(source_dir):
    if file.startswith("_"):
        with open(os.path.join(source_dir, file)) as f:
            replacements[file] = replace(f.read())

if not os.path.isdir(target_dir):
    os.mkdir(target_dir)

for file in os.listdir(source_dir):
    if not file.startswith(".") and not file.startswith("_"):
        with open(os.path.join(source_dir, file)) as f:
            content = replace(f.read())

        with open(os.path.join(target_dir, file), "w") as f:
            f.write(content)
