import json
import datetime
import zoneinfo
import matplotlib.pyplot as plt

# import tikzplotlib

# plot_num = 0
# def save():
#     tikzplotlib.save(f"plot{plot_num}.tex")
#     plot_num += 1

# plt.show = save

plot_num = 0
def save():
    global plot_num
    plt.savefig(f"plot{plot_num}.pgf")
    plt.clf()
    plot_num += 1

plt.show = save

plt.rcParams['font.size'] = 15


with open("message_1.json") as f:
    data = json.load(f)


coffee_emoji = "\u00e2\u0098\u0095\u00ef\u00b8\u008f"
assert data["messages"][0]["content"] == coffee_emoji

coffee_pings = [
    message
    for message in data["messages"]
    if "content" in message and message["content"] == coffee_emoji
]

unix_times = [
    message["timestamp_ms"]
    for message in coffee_pings
]

def to_datetime(unix_ms): return datetime.datetime.fromtimestamp(unix_ms // 1000, tz=zoneinfo.ZoneInfo("Europe/Copenhagen"))

dates = [
    to_datetime(unix)
    for unix in unix_times
]

print(min(dates))
print(max(dates))


def add_labels(xs, int_values, offset):
    for x, c in zip(xs, int_values):
        plt.text(x, c + offset, c, ha="center")


def plot_weekday_analysis():
    weekday_count = [0] * 7
    for date in dates:
        weekday_count[date.weekday()] += 1

    plt.bar(range(7), weekday_count, color="grey")
    weekday_names = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]
    plt.xticks(range(7), weekday_names, rotation=90)
    plt.ylabel("Antal pings", labelpad=10)
    add_labels(range(7), weekday_count, 4)
    plt.tight_layout()
    plt.show()

    weekday_hour_count = [[0] * 24 for _ in range(7)]
    for date in dates:
        weekday_hour_count[date.weekday()][date.hour] += 1

    for i, day in enumerate(weekday_hour_count):
        off = 24 * i
        # plt.bar(range(off, off + 24), day, align='edge', width=1.0)
        plt.bar(range(off, off + 24), day, align='edge', color="grey", width=1.0)

    max_entry = max(hour_count for day in weekday_hour_count for hour_count in day) + 4
    for i in range(1, 7):
        plt.plot([i * 24, i * 24], [0, max_entry], ":", color="black")

    space = "\\hspace{3pt}"
    labels = [l for name in weekday_names for l in ["", space+"06\n", space+"12\n" + space+name, space+"18\n"]]
    plt.xticks(range(0, 24 * 7, 6), labels)
    plt.xlim([0, 24 * 7])
    plt.ylim([0, max_entry])
    plt.xlabel("Klokkeslet \& Ugedag", labelpad=10)
    plt.ylabel("Antal pings", labelpad=10)
    plt.show()


def plot_year_analysis():
    month_count = [0] * 12
    for date in dates:
        month_count[date.month - 1] += 1

    month_names = ["Januar", "Februar", "Marts", "April", "Maj", "Juni", "Juli", "August", "September", "Oktober", "November", "December"]
    plt.bar(range(12), month_count, color="grey")
    plt.xticks(range(12), month_names, rotation=90, ha="right", va="center", rotation_mode="anchor")
    add_labels(range(12), month_count, 4)
    plt.ylabel("Antal pings", labelpad=10)
    plt.tight_layout()
    plt.show()

    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_day_count = [[0] * days for days in days_in_month]
    for date in dates:
        month_day_count[date.month - 1][date.day - 1] += 1

    print([(day + 1, month_names[month], count) for month, days in enumerate(month_day_count) for day, count in enumerate(days) if count >= 20])

    off = 0
    colors = ["lightgrey", "grey"]
    c = 0
    for month, days in zip(month_day_count, days_in_month):
        # plt.bar(range(off, off + days), month, align='edge', width=1.0)
        plt.bar(range(off, off + days), month, align='edge', color=colors[c], width=1.0)
        c = 1 - c
        off += days

    max_entry = max(day_count for month in month_day_count for day_count in month) + 1
    # off = 0
    # for days in days_in_month[:-1]:
    #     off += days
    #     plt.plot([off, off], [0, max_entry], "--", color="black", linewidth=1)

    off = 0
    ticks = []
    for days in days_in_month:
        ticks.append(off + days / 2)
        off += days
    
    plt.xticks(ticks, month_names, rotation=90, ha="right", va="center", rotation_mode="anchor")
    plt.xlim([0, sum(days_in_month)])
    plt.ylim([0, max_entry])
    plt.ylabel("Antal pings", labelpad=10)
    plt.tight_layout()
    plt.show()


def plot_group_sizes():
    # Two minutes
    time_within = 5 * 60 * 1000

    sorted_time = sorted(unix_times)
    buckets = [[sorted_time[0]]]
    for t in sorted_time[1:]:
        if t - buckets[-1][-1] > time_within:
            buckets.append([])
        buckets[-1].append(t)

    sizes = [len(b) for b in buckets]
    max_size = max(sizes)
    size_count = [0] * (max_size + 1)
    for s in sizes:
        size_count[s] += 1

    xs = list(range(1, len(size_count)))
    size_count = size_count[1:]
    plt.bar(xs, size_count, color="grey")
    add_labels(xs, size_count, 4)
    plt.xlabel("Gruppestørrlse", labelpad=10)
    plt.ylabel("Antal ture", labelpad=10)
    plt.tight_layout()
    plt.show()


def plot_people_count():
    # People count
    from collections import Counter
    people = [
        message["sender_name"]
        for message in coffee_pings
    ]

    count_tuples = sorted(Counter(people).items(), key=lambda t: t[1])

    count = [c for _, c in count_tuples]
    labels = [l for l, _ in count_tuples]
    xs = list(range(len(count_tuples)))

    plt.bar(xs, count, color="grey")
    add_labels(xs, count, 3)

    # plt.xticks(xs, labels, rotation=60, ha="right", va="center", rotation_mode="anchor")
    # plt.xticks(xs, xs)
    plt.xticks([], [])
    plt.ylabel("Antal pings", labelpad=10)
    plt.tight_layout()
    plt.show()


def plot_people_count_time_sensitive():
    from collections import defaultdict

    people_pings = defaultdict(lambda: [])
    for message in coffee_pings:
        people_pings[message["sender_name"]].append(to_datetime(message["timestamp_ms"]))
    
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    dates = [
        (year, month, day)
        for year in [2022, 2023]
        for month, count in enumerate(days_in_month, start=1)
        for day in range(1, count + 1)
    ]

    dates = dates[261:-104]

    for person, pings in people_pings.items():
        date_count = defaultdict(lambda: 0)
        for t in pings:
            date_count[(t.year, t.month, t.day)] += 1
        
        data_line = []
        c = 0
        for d in dates:
            c += date_count[d]
            data_line.append(c)
        
        plt.plot(range(len(dates)), data_line, "-", label=person)

    i = 20
    plt.xticks(range(0, len(dates), i), dates[::i], rotation=90, ha="right", va="center", rotation_mode="anchor")
    plt.legend()
    plt.tight_layout()
    plt.show()


# plot_people_count_time_sensitive()
# exit(0)


print("Total pings:", len(coffee_pings))

plot_weekday_analysis()
plot_year_analysis()
plot_group_sizes()
plot_people_count()
