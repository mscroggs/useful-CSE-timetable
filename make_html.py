import os
import sys

dir = os.path.dirname(os.path.realpath(__file__))
source_dir = os.path.join(dir, "html")

if len(sys.argv) == 2:
    target_dir = sys.argv[1]
else:
    assert len(sys.argv) == 1
    target_dir = os.path.join(dir, "_html")

with open(os.path.join(dir, "talks.json")) as f:
    talks_json = f.read()
with open(os.path.join(dir, "order.json")) as f:
    order_json = f.read()

if not os.path.isdir(target_dir):
    os.mkdir(target_dir)

for file in os.listdir(source_dir):
    if not file.startswith("."):
        with open(os.path.join(source_dir, file)) as f:
            content = f.read()

        content = content.replace("{{talks.json}}", talks_json)
        content = content.replace("{{order.json}}", order_json)

        with open(os.path.join(target_dir, file), "w") as f:
            f.write(content)
