from collections import defaultdict

import json
from datetime import datetime
import matplotlib.pyplot as plt

from utils import prompt_select

with open("eva-data.json", "r", encoding="utf-8") as file:
    eva_data = json.load(file)

records = []
country_eva_durs: defaultdict[str, float] = defaultdict(float)

for eva in eva_data:
    date_text = eva.get("date")
    duration_text = eva.get("duration")

    if not duration_text:
        continue

    hours, minutes = map(int, duration_text.split(":"))
    duration_hours = hours + minutes / 60

    if (country := eva.get("country")) is not None:
        country_eva_durs[country] += duration_hours

    if date_text:
        date = datetime.fromisoformat(date_text)
        records.append((date, duration_hours))


chosen_country = prompt_select(
    sorted(country_eva_durs.keys()),
    prompt="Select country to view EVA duration for",
)
print(f"Total EVA duration for {chosen_country}: {country_eva_durs[chosen_country]:.2f} hrs")

records.sort(key=lambda record: record[0])

dates = []
cumulative_hours = []
total_hours = 0

for date, duration_hours in records:
    total_hours += duration_hours
    dates.append(date)
    cumulative_hours.append(total_hours)

plt.plot(dates, cumulative_hours)
plt.xlabel("Year")
plt.ylabel("Cumulative EVA duration (hours)")
plt.tight_layout()
plt.savefig("cumulative_duration.png")
plt.show()
