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


def pad2(n):
    n = str(n)
    while len(n) < 2:
        n = "0" + n
    return n


with open(os.path.join(dir, "talks.json")) as f:
    talks_json = f.read()
with open(os.path.join(dir, "order.json")) as f:
    order_json = f.read()

talks = json.loads(talks_json)
order = json.loads(order_json)

talks_list = []
for i, n in enumerate(order):
    try:
        t = talks[n]
    except KeyError:
        continue
    timestamp = "2022-"
    timestamp += "02" if "February" in t["date"] else "03"
    timestamp += "-" + pad2(t["date"].split(" ")[-1])
    timestamp += " "
    if "AM" in t["time"][0]:
        timestamp += pad2(t["time"][0].split(":")[0])
    else:
        timestamp += pad2(int(t["time"][0].split(":")[0]) + 12)
    timestamp += ":"
    timestamp += t["time"][0].split(":")[1].split(" ")[0]

    talks_html = f"<div id='talk{i}' style='display:none'>"
    talks_html += f"<a href='javascript:toggle_star({i})' class='star'><span class='star{i}'>&star;</span></a> "
    talks_html += f"<b>{t['time'][0]}&ndash;{t['time'][1]}"
    if t["room"] is not None:
        talks_html += f" ({t['room']})"
    talks_html += "</b> "
    if t["type"] == "panel":
        talks_html += to_html(f"{', '.join([' '.join(i) for i in t['panel']])} {t['title']}")
    else:
        talks_html += to_html(f"{t['speaker'][0]} {t['speaker'][1]}, {t['title']}")
    talks_html += "</div>"

    talks_list.append((timestamp, talks_html))

talks_list.sort(key=lambda x: x[0])
talks_list_html = ""
for day, date in [
    ("Monday", "2022-02-27"),
    ("Tuesday", "2022-02-28"),
    ("Wednesday", "2022-03-01"),
    ("Thursday", "2022-03-02"),
    ("Friday", "2022-03-03"),
]:
    talks_list_html += f"<h2>{day}</h2>"
    talks_list_html += "\n".join([i[1] for i in talks_list if date in i[0]])

speakers = []
for i, t in talks.items():
    if "speaker" in t:
        speakers.append([unidecode(", ".join(t["speaker"][::-1])).upper(), " ".join(t["speaker"]), order.index(i)])
    elif "panel" in t:
        for person in t["panel"]:
            speakers.append([unidecode(", ".join(person[::-1])).upper(), " ".join(person), order.index(i)])

speakers.sort(key=lambda x: x[0])

list_speakers = "<br />".join([
    f"<a href='javascript:toggle_star({s[2]})' class='star'><span class='star{s[2]}'>&star;</span></a> {to_html(s[1])}"
    for s in speakers
    if "ANNOUNCED" not in s[0]
])

titles = []
for i, t in talks.items():
    titles.append([t["title"].upper(), t["title"], order.index(i)])

titles.sort(key=lambda x: x[0])

list_titles = "<br />".join([
    f"<a href='javascript:toggle_star({t[2]})' class='star'><span class='star{t[2]}'>&star;</span></a> {to_html(t[1])}"
    for t in titles
])

replacements = {}


def replace(content):
    content = content.replace("{{list-speakers}}", list_speakers)
    content = content.replace("{{list-titles}}", list_titles)
    content = content.replace("{{talks-list}}", talks_list_html)
    content = content.replace("{{talks.json}}", talks_json)
    content = content.replace("{{order.json}}", order_json)
    content = content.replace("{{order.length}}", f"{len(order)}")
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
