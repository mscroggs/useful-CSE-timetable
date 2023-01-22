from urllib.request import urlopen
import json
import sys
import os
import re

test = "test" in sys.argv
if test:
    cache_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "_cache")
    if not os.path.isdir(cache_dir):
        os.mkdir(cache_dir)


def load_page(url):
    if test:
        fname = re.sub(r"[^A-Za-z0-9_]", "_", url)
        if os.path.isfile(os.path.join(cache_dir, fname)):
            with open(os.path.join(cache_dir, fname)) as f:
                return f.read()

        with urlopen(url) as f:
            page = f.read().decode("utf-8")
        with open(os.path.join(cache_dir, fname), "w") as f:
            f.write(page)
        return page

    with urlopen(url) as f:
        return f.read().decode("utf-8")


page = load_page("https://meetings.siam.org/speakdex.cfm?CONFCODE=CSE23")
page = page.split("<body")[1].split(">", 1)[1]

sessions = set()
names = {}

for talk in page.split("<table")[1].split("<", 1)[1].split("<br />"):
    if "SESSIONCODE=" in talk and "Canceled" not in talk:
        sessions.add(talk.split("SESSIONCODE=")[1].split("\"")[0])
        surname, forename = talk.split(":")[0].split(">")[-1].strip().split(", ")
        names[forename + " " + surname] = (forename, surname)

sessions = sorted(list(sessions))


def name_split(name):
    if name in names:
        return names[name]
    if ". " in name:
        nsp = name.split(". ")
        return ". ".join(nsp[:-1]) + ".", nsp[-1]
    nsp = name.split(" ")
    if len(nsp) == 2:
        return nsp
    return name


talks = {}

for id in sessions:
    url = f"https://meetings.siam.org/sess/dsp_programsess.cfm?SESSIONCODE={id}"
    print(f"{sessions.index(id) + 1}/{len(sessions)} {url}")
    page = load_page(url)

    date = page.split("<h3>")[1].split("</h3>")[0]
    title = page.split("<h2>")[1].split("</h2>")[0].split("</br>")[1].strip()
    code = page.split("<h2>")[1].split("</h2>")[0].split("</br>")[0].strip()
    time = page.split("<p>")[1].split("<br")[0].strip()
    start, end = time.split(" - ")
    room = page.split("Room:")[1].split("<")[0].strip() if "Room:" in page else None

    if "PD" in code:
        # panel discussion
        talks[id] = {"type": "panel", "date": date, "code": code, "time": (start, end), "room": room, "title": title, "url": url}
        talks[id]["panel"] = [
            name_split(p.split("</strong>")[0].strip())
            for p in page.split("<strong>")[1:]]
    elif "SP" in code:
        # S? plenary
        speaker = page.split("<b>")[1].split("</b>")[0].strip()
        talks[id] = {"type": "prize", "date": date, "code": code, "time": (start, end), "room": room, "title": title, "speaker": name_split(speaker), "url": url}
    elif "IP" in code:
        # I? plenary
        speaker = page.split("<b>")[1].split("</b>")[0].strip()
        talks[id] = {"type": "plenary", "date": date, "code": code, "time": (start, end), "room": room, "title": title, "speaker": name_split(speaker), "url": url}
    elif "PP" in code:
        # Poster session
        for talk in page.split("<dt>")[1:]:
            if "Cancelled" not in talk:
                talk_id = talk.split("<a href=\"dsp_talk.cfm?p=")[1].split("\"")[0]
                try:
                    speaker = talk.split("<dd>")[1].split("<em>")[1].split("</EM>")[0].strip()
                except:
                    speaker = talk.split("<dd>")[1].split(",")[0].split(">")[-1].strip()
                title = talk.split("<strong>")[1].split("</strong>")[0].strip()
                if title.startswith("-"):
                    title = title[1:].strip()
                talks[talk_id] = {"type": "poster", "date": date, "code": code, "time": (start, end), "room": room, "speaker": name_split(speaker), "title": title, "url": url}
    elif "CANCELLED" not in page:
        assert "dsp_talk.cfm" in page
        # minisympsium talks
        talkn = 1
        for talk in page.split("<dt>")[1:]:
            if "Cancelled" not in talk:
                talk_id = talk.split("<a href=\"dsp_talk.cfm?p=")[1].split("\"")[0]
                try:
                    speaker = talk.split("<dd>")[1].split("<em>")[1].split("</EM>")[0].strip()
                except:
                    speaker = talk.split("<dd>")[1].split(",")[0].split(">")[-1].strip()
                title = talk.split("<strong>")[1].split("</strong>")[0].strip()
                if title.startswith("-"):
                    title = title[1:].strip()
                talks[talk_id] = {"type": "talk", "date": date, "code": code, "time": (start, end), "room": room, "speaker": name_split(speaker), "title": title, "url": url, "n": talkn}
                talkn += 1
with open("talks.json", "w") as f:
    json.dump(talks, f)

with urlopen("https://raw.githubusercontent.com/mscroggs/useful-CSE-timetable/json/order.json") as f:
    order = json.loads(f.read().decode("utf-8"))

for i in talks.keys():
    if i not in order:
        order.append(i)

with open("order.json", "w") as f:
    json.dump(order, f)
