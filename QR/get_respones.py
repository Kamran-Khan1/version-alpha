import random

file = open("FOP1.csv")
lines = file.readlines()
file.close()

lines.pop(0)

names = []
for line in lines:
    name = line.strip().split(",")[1]
    names.append(name)

random.shuffle(names)

tasks = 5
group_size = round(len(names) / tasks)
groups = []
x = 0

for i in range(tasks):
    if i == tasks - 1:
        group = names[x:]
    else:
        group = names[x:x + group_size]
        x += group_size
    groups.append(group)

cards = ""
colors = ["#4F46E5", "#0891B2", "#059669", "#D97706", "#DC2626",
          "#7C3AED", "#DB2777", "#65A30D", "#EA580C", "#0284C7"]

for i, group in enumerate(groups):
    color = colors[i % len(colors)]
    members = "".join(f"<li>{name}</li>" for name in group)
    cards += f"""
    <div class="card" style="border-top: 5px solid {color}">
        <h2 style="color: {color}">Group {i+1}</h2>
        <ul>{members}</ul>
    </div>"""

html = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f1f5f9; padding: 30px; }}
        h1 {{ text-align: center; color: #1e293b; }}
        .grid {{ display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; }}
        .card {{ background: white; border-radius: 12px; padding: 20px 25px;
                 width: 200px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
        .card h2 {{ margin: 0 0 12px 0; font-size: 1.1rem; }}
        ul {{ margin: 0; padding-left: 18px; color: #374151; line-height: 1.8; }}
    </style>
</head>
<body>
    <h1>Random Groups</h1>
    <div class="grid">{cards}</div>
</body>
</html>"""

with open("groups.html", "w") as f:
    f.write(html)

print("Saved! Open groups.html in your browser.")