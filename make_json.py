from urllib.request import urlopen
import json

with urlopen("https://meetings.siam.org/speakdex.cfm?CONFCODE=CSE23") as f:
    page = f.read().decode("utf-8")
page = page.split("<body")[1].split(">", 1)[1]
# page = page.split("<dl>")[1].split("</dl>")[0].split("<br />")

sessions = set()

for talk in page.split("<table")[1].split("<", 1)[1].split("<br />"):
    if "SESSIONCODE=" in talk and "Canceled" not in talk:
        sessions.add(talk.split("SESSIONCODE=")[1].split("\"")[0])

talks = {}

for id in sessions:
    print(id)
    url = f"https://meetings.siam.org/sess/dsp_programsess.cfm?SESSIONCODE={id}"
    with urlopen(url) as f:
        page = f.read().decode("utf-8")

    date = page.split("<h3>")[1].split("</h3>")[0]
    title = page.split("<h2>")[1].split("</h2>")[0].split("</br>")[1].strip()
    code = page.split("<h2>")[1].split("</h2>")[0].split("</br>")[0].strip()
    time = page.split("<p>")[1].split("<br />")[0].strip()
    room = page.split("Room:")[1].split("<")[0].strip() if "Room:" in page else None

    if "PD" in code:
        # panel discussion
        pass
    elif "dsp_talk.cfm" in page:
        # minisympsium talk
        talks[id] = {"type": "talk"}
    else:
        print("plenary")
        print(code)
        continue
        # plenary
        talks[id] = {"type": "plenary", "code": code, "date": date, "title": title, "time": time, }
        talks[id]["date"] = page.split("<h3>")[1].split("</h3>")
        talks[id]["title"] = page.split("<h2>")[1].split("</h2>")[0].split("</br>")[1].strip()
        talks[id]["sessioncode"] = page.split("<h2>")[1].split("</h2>")[0].split("</br>")[0].strip()
        talks[id]["time"] = page.split("<p>")[1].split("<br />")[0].strip()
        talks[id]["room"] = page.split("Room:")[1].split("<")[0].strip()
        break

with open("talks.json", "w") as f:
    json.dump(talks, f)
