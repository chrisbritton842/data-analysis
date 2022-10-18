import csv
from datetime import datetime

import matplotlib.pyplot as plt

filename = 'data/spy.csv'

with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)

    dates, closes, volumes = [], [], []
    for row in reader:
        current_date = datetime.strptime(row[0], '%m/%d/%Y')
        try:
            close = float(row[4])
            volume = int(row[5].replace(',', '')) / 1000000
        except ValueError:
            print(f"Missing data")
        else:
            dates.append(current_date)
            closes.append(close)
            volumes.append(volume)

plt.style.use('seaborn')
fig, ax = plt.subplots()
ax.plot(dates, closes, c='red')
ax.plot(dates, volumes, c='blue')

ax.set_title("SPY Closing Prices and Volume", fontsize=24)
ax.set_xlabel('', fontsize=16)
fig.autofmt_xdate()
ax.set_ylabel('', fontsize=16)
ax.tick_params(axis='both', which='major', labelsize=16)

plt.show()
