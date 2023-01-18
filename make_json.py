from urllib.request import urlopen
import json
import sys
import os
import re

test = "test" in sys.argv
if test:
    cache_dir = letter_dir = os.path.join(
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

for talk in page.split("<table")[1].split("<", 1)[1].split("<br />"):
    if "SESSIONCODE=" in talk and "Canceled" not in talk:
        sessions.add(talk.split("SESSIONCODE=")[1].split("\"")[0])

talks = {}

sessions = sorted(list(sessions))

for id in sessions:
    print(f"{sessions.index[id] + 1}/{len(sessions)}")
    url = f"https://meetings.siam.org/sess/dsp_programsess.cfm?SESSIONCODE={id}"
    page = load_page(url)

    date = page.split("<h3>")[1].split("</h3>")[0]
    title = page.split("<h2>")[1].split("</h2>")[0].split("</br>")[1].strip()
    code = page.split("<h2>")[1].split("</h2>")[0].split("</br>")[0].strip()
    time = page.split("<p>")[1].split("<br />")[0].strip()
    start, end = time.split(" - ")
    room = page.split("Room:")[1].split("<")[0].strip() if "Room:" in page else None

    if "PD" in code:
        # panel discussion
        talks[id] = {"type": "panel", "date": date, "code": code, "time": (start, end), "room": room, "title": title}
        talks[id]["panel"] = [
            p.split("</strong>")[0].strip()
            for p in page.split("<strong>")[1:]]
    elif "SP" in code:
        # S? plenary
        speaker = page.split("<b>")[1].split("</b>")[0].strip()
        talks[id] = {"type": "prize", "date": date, "code": code, "time": (start, end), "room": room, "title": title, "speaker": speaker}
    elif "IP" in code:
        # I? plenary
        speaker = page.split("<b>")[1].split("</b>")[0].strip()
        talks[id] = {"type": "plenary", "date": date, "code": code, "time": (start, end), "room": room, "title": title, "speaker": speaker}
    elif "CANCELLED" not in page:
        assert "dsp_talk.cfm" in page
        # minisympsium talks
        for talk in page.split("<dt>")[1:]:
            if "Cancelled" not in talk:
                talk_id = talk.split("<a href=\"dsp_talk.cfm?p=")[1].split("\"")[0]
                speaker = talk.split("<dd>")[1].split("<em>")[1].split("</EM>")[0].strip()
                title = talk.split("<strong>")[1].split("</strong>")[0].strip()
                if title.startswith("-"):
                    title = title[1:].strip()
                talks[talk_id] = {"type": "talk", "date": date, "code": code, "time": (start, end), "room": room, "speaker": speaker, "title": title}

with open("talks.json", "w") as f:
    json.dump(talks, f)
