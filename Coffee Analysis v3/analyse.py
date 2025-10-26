PLOT_SAVE = True

import json
import datetime
import zoneinfo
import matplotlib.pyplot as plt
from collections import defaultdict


if PLOT_SAVE:
    name = None
    def set_name(local_name):
        global name
        name = local_name
    plt.set_name = set_name

    def save():
        global name
        assert name is not None
        plt.savefig(f"plot_{name}.pgf")
        plt.clf()
        name = None
    plt.show = save

else:
    plt.set_name = plt.title

plt.rcParams['font.size'] = 10


# Help functions
def to_datetime(unix_ms): return datetime.datetime.fromtimestamp(unix_ms // 1000, tz=zoneinfo.ZoneInfo("Europe/Copenhagen"))

def year_range(dates):
    return f"{dates[0].year}-{dates[-1].year}"

def add_labels(xs, int_values, offset, neg_offset=None, rotated=False):
    if neg_offset is None:
        neg_offset = offset
    for x, c in zip(xs, int_values):
        y = c + offset if c >= 0 else c - neg_offset
        if rotated:
            plt.text(x, y, c, rotation=90, ha="left", va="center", rotation_mode="anchor")
        else:
            plt.text(x, y, c, ha="center")

def days_in_month_for_years(*in_years):
    # This is hardcoded to only handle leap year 2024
    if 2024 in in_years:
        return [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# Constants
WEEKDAY_NAMES = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]
MONTH_NAMES = ["Januar", "Februar", "Marts", "April", "Maj", "Juni", "Juli", "August", "September", "Oktober", "November", "December"]

GROUP_TIME_DELTA = 5 * 60 * 1000  # Five minutes in unix


# Standart

def plot_weekday_analysis(dates):
    weekday_count = [0] * 7
    for date in dates:
        weekday_count[date.weekday()] += 1

    plt.bar(range(7), weekday_count, color="grey")
    
    plt.xticks(range(7), WEEKDAY_NAMES, rotation=90, ha="right", va="center", rotation_mode="anchor")
    plt.ylabel("Antal pings", labelpad=10)
    add_labels(range(7), weekday_count, max(weekday_count) * 0.03)
    plt.tight_layout()
    plt.ylim(0, max(weekday_count) * 1.13)
    plt.set_name(f"weekday_analysis_{year_range(dates)}")
    plt.show()


def plot_weekday_analysis_multi(multi_dates):
    assert len(multi_dates) <= 3

    colors = ["darkgray", "gray", "lightgray"]
    width = 0.3

    base_offset = -width * len(multi_dates) / 2 + width / 2

    weekday_counts = []
    for i, (dates, color) in enumerate(zip(multi_dates, colors)):
        weekday_count = [0] * 7
        for date in dates:
            weekday_count[date.weekday()] += 1
        
        offset = base_offset + width * i
        plt.bar([x + offset for x in range(7)], weekday_count, width, color=color)

        weekday_counts.append(weekday_count)
    
    max_count = max(max(count) for count in weekday_counts)
    for i, weekday_count in enumerate(weekday_counts):
        offset = base_offset + width * i
        add_labels([x + offset for x in range(7)], weekday_count, max_count * 0.01, rotated=True)
    
    plt.xticks(range(7), WEEKDAY_NAMES, rotation=90, ha="right", va="center", rotation_mode="anchor")
    plt.ylabel("Antal pings", labelpad=10)
    plt.tight_layout()
    plt.ylim(0, max_count * 1.13)
    plt.set_name(f"weekday_analysis_multi_{'_'.join(year_range(dates) for dates in multi_dates)}")
    plt.show()


def plot_weekday_by_hour_analysis(dates, append_name=None):
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
    # space = ""
    labels = [l for name in WEEKDAY_NAMES for l in ["", space+"06\n", space+"12\n" + space+name, space+"18\n"]]
    plt.xticks(range(0, 24 * 7, 6), labels)
    plt.xlim([0, 24 * 7])
    plt.ylim([0, max_entry])
    plt.xlabel("Klokkeslet \& Ugedag", labelpad=10)
    plt.ylabel("Antal pings", labelpad=10)
    name = f"weekday_by_hour_analysis_{year_range(dates)}"
    if append_name is not None:
        name += "_" + append_name
    plt.set_name(name)
    plt.show()


def plot_weekday_by_hour_single_weekday_analysis(dates, weekday):
    weekday_hour_count = [[0] * 24 for _ in range(53)]
    for date in dates:
        if date.weekday() == weekday:
            weekday_hour_count[date.isocalendar().week][date.hour] += 1
    
    print(f"    {', '.join([f'{t:2d}' for t in range(24)])}")
    for weeknum, pings in enumerate(weekday_hour_count):
        print(f"{weeknum:2d}: {', '.join([f'{c:2d}' for c in pings])}")

    for i, day in enumerate(weekday_hour_count):
        off = 24 * i
        # plt.bar(range(off, off + 24), day, align='edge', width=1.0)
        plt.bar(range(off, off + 24), day, align='edge', color="grey", width=1.0)

    max_entry = max(hour_count for day in weekday_hour_count for hour_count in day) + 4
    # for i in range(1, 7):
    #     plt.plot([i * 24, i * 24], [0, max_entry], ":", color="black")

    space = "\\hspace{3pt}"
    # space = ""
    labels = [l for weeknum in range(53) for l in ["", space+"06\n", space+"12\n" + space+str(weeknum), space+"18\n"]]
    plt.xticks(range(0, 24 * 53, 6), labels)
    plt.xlim([0, 24 * 53])
    plt.ylim([0, max_entry])
    plt.xlabel("Klokkeslet \& Ugenummer", labelpad=10)
    plt.ylabel("Antal pings", labelpad=10)
    name = f"weekday_by_hour_weekday_{weekday}_analysis_{year_range(dates)}"
    plt.set_name(name)
    plt.show()


def plot_month_analysis(dates):
    month_count = [0] * 12
    for date in dates:
        month_count[date.month - 1] += 1

    plt.bar(range(12), month_count, color="grey")
    plt.xticks(range(12), MONTH_NAMES, rotation=90, ha="right", va="center", rotation_mode="anchor")
    add_labels(range(12), month_count, max(month_count) * 0.03)
    plt.ylabel("Antal pings", labelpad=10)
    plt.ylim(0, max(month_count) * 1.13)
    plt.tight_layout()
    plt.set_name(f"month_analysis_{year_range(dates)}")
    plt.show()


def plot_month_analysis_multi(multi_dates):
    assert len(multi_dates) <= 3

    colors = ["darkgray", "gray", "lightgray"]
    width = 0.27

    base_offset = -width * len(multi_dates) / 2 + width / 2

    month_counts = []
    for i, (dates, color) in enumerate(zip(multi_dates, colors)):
        month_count = [0] * 12
        for date in dates:
            month_count[date.month - 1] += 1
        
        offset = base_offset + width * i
        plt.bar([x + offset for x in range(12)], month_count, width, color=color)

        month_counts.append(month_count)
    
    max_count = max(max(count) for count in month_counts)
    for i, month_count in enumerate(month_counts):
        offset = base_offset + width * i
        add_labels([x + offset for x in range(12)], month_count, max_count * 0.01, rotated=True)
    
    plt.xticks(range(12), MONTH_NAMES, rotation=90, ha="right", va="center", rotation_mode="anchor")
    plt.ylabel("Antal pings", labelpad=10)
    plt.tight_layout()
    plt.ylim(0, max_count * 1.13)
    plt.set_name(f"month_analysis_multi_{'_'.join(year_range(dates) for dates in multi_dates)}")
    plt.show()


def plot_year_by_date_analysis(dates, day_count_tests=[]):
    days_in_month = days_in_month_for_years(*{date.year for date in dates})

    month_day_count = [[0] * days for days in days_in_month]
    for date in dates:
        month_day_count[date.month - 1][date.day - 1] += 1

    for test in day_count_tests:
        print(f"Test {test}:")
        print([(day + 1, MONTH_NAMES[month], count) for month, days in enumerate(month_day_count) for day, count in enumerate(days) if test(count)])

    off = 0
    colors = ["lightgrey", "grey"]
    c = 0
    for month, days in zip(month_day_count, days_in_month):
        plt.bar(range(off, off + days), month, align='edge', color=colors[c], width=1.0)
        c = 1 - c
        off += days

    off = 0
    ticks = []
    for days in days_in_month:
        ticks.append(off + days / 2)
        off += days

    max_entry = max(day_count for month in month_day_count for day_count in month) + 1
    plt.xticks(ticks, MONTH_NAMES, rotation=90, ha="right", va="center", rotation_mode="anchor")
    plt.xlim([0, sum(days_in_month)])
    plt.ylim([0, max_entry])
    plt.ylabel("Antal pings", labelpad=10)
    plt.tight_layout()
    plt.set_name(f"year_analysis_{year_range(dates)}")
    plt.show()



# Other plots

def plot_pings_per_day_normal_distribution(dates, ignore_zero_days=False):
    # TODO: hardcoded
    all_dates = [
        (year, month, day)
        for year in [2022, 2023, 2024, 2025]
        for month, count in enumerate(days_in_month_for_years(year), start=1)
        for day in range(1, count + 1)
    ]

    # TODO: hardcoded
    observe_dates = all_dates[261:-104]

    # print(dates[-1], dates[0])
    # print(observe_dates[0], observe_dates[-1])

    from collections import defaultdict
    observations = defaultdict(lambda: 0)
    for date in dates:
        observations[date.year, date.month, date.day] += 1

    max_count = max(observations.values())
    count_count = [0] * (max_count + 1)
    for date in observe_dates:
        count_count[observations[date]] += 1

    total = sum(count_count)
    assert total == len(observations)

    xs = list(range(max_count + 1))

    if ignore_zero_days:
        print(f"Ignoring {count_count[0]} zero days, which is {count_count[0] / total * 100} %")
        total -= count_count[0]
        count_count.pop(0)
        xs.pop(0)

    plt.bar(xs, [c / total for c in count_count], color="gray")
    plt.ylabel("Procent af alle dage", labelpad=10)
    plt.xlabel("Antal pings per dag")

    import matplotlib.ticker as mtick
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))

    full_data = [v for v, c in enumerate(count_count, start=int(ignore_zero_days)) for _ in range(c)]
    assert len(full_data) == total
    median = full_data[len(full_data) // 2]
    average = sum(full_data) / len(full_data)
    variance = sum((x - average)**2 for x in full_data) / len(full_data)
    sd = variance**.5
    print("Median:", median)
    print("Average:", average)
    print("Variance:", variance)
    print("SD:", sd)

    import numpy as np
    import scipy.stats as stats
    import math

    mu = average
    sigma = math.sqrt(variance)
    x = np.linspace(int(ignore_zero_days), max_count, 100)
    norm = stats.norm.pdf(x, mu, sigma)
    scale = 1
    plt.plot(x, scale * norm, color="black")
    plt.tight_layout()
    plt.set_name("days_count_distribution" + ("_ignore_zero_days" if ignore_zero_days else ""))
    plt.show()


def plot_cummulative_year_analysis(dates, named=None):
    # TODO: hardcoded
    all_dates = [
        (year, month, day)
        for year in [2022, 2023, 2024, 2025]
        for month, count in enumerate(days_in_month_for_years(year), start=1)
        for day in range(1, count + 1)
    ]

    # TODO: hardcoded
    observe_dates = all_dates[261:-104]

    print(dates[0], dates[-1])
    print(observe_dates[0], observe_dates[-1])

    from collections import defaultdict
    observations = defaultdict(lambda: 0)
    for date in dates:
        observations[date.year, date.month, date.day] += 1
    
    total = 0
    data_line = []
    for date in observe_dates:
        total += observations[date]
        data_line.append(total)
    
    plt.plot(range(len(observe_dates)), data_line, "-", color="black")
    plt.plot([0, len(observe_dates) - 1], [0, len(dates)], ":", color="gray")
    plt.ylabel("Antal pings", labelpad=10)

    month_ticks = []
    for i, (year, month, day) in enumerate(observe_dates):
        if (days_in_month_for_years(year)[month - 1]) // 2 == day:
            month_ticks.append((i, f"{MONTH_NAMES[month - 1]}"))
    plt.xticks(*zip(*month_ticks), rotation=90, ha="right", va="center", rotation_mode="anchor")

    year_ticks = []
    for y in [2022, 2023, 2024, 2025]:
        iss = [i for i, (year, _, _) in enumerate(observe_dates) if year == y]
        min_i = min(iss)
        max_i = max(iss)
        year_ticks.append(((min_i + max_i) / 2, f"\n\n\n\n{y}"))
    sec = plt.gca().secondary_xaxis(location=0)
    sec.set_xticks(*zip(*year_ticks))
    sec.tick_params('x', length=0)

    sec2 = plt.gca().secondary_xaxis(location=0)
    sep = []
    for y1, y2 in [(2022, 2023), (2023, 2024), (2024, 2025)]:
        a = max(i for i, (y, _, _) in enumerate(observe_dates) if y == y1)
        b = min(i for i, (y, _, _) in enumerate(observe_dates) if y == y2)
        sep.append((a + b) / 2)
    sec2.set_xticks(sep, labels=[])
    sec2.tick_params('x', length=80, width=1)

    name = "cummulative_sum_vs_average"
    if named is not None: name += "_" + named
    plt.set_name(name)
    plt.tight_layout()
    plt.show()


# Group

def get_named_groups_no_duplicates(unix_pings_with_sender, remove_single_groups=False, return_group_unix=False):
    last_time = -float("inf")
    groups = []
    groups_time = []
    for unix_time, person in unix_pings_with_sender:
        if unix_time - last_time > GROUP_TIME_DELTA:
            groups.append([])
            groups_time.append(unix_time)
        last_time = unix_time
        if person not in groups[-1]:
            groups[-1].append(person)

    if remove_single_groups:
        assert return_group_unix == False
        groups = [g for g in groups if len(g) > 1]

    if return_group_unix:
        return groups, groups_time
    
    return groups


def plot_group_sizes(unix_pings_with_sender, justified=False):
    groups = get_named_groups_no_duplicates(unix_pings_with_sender)
    sizes = [len(b) for b in groups]
    max_size = max(sizes)
    size_count = [0] * (max_size + 1)
    for s in sizes:
        size_count[s] += 1

    if justified:
        size_count = [s * i for i, s in enumerate(size_count)]

    xs = list(range(1, len(size_count)))
    size_count = size_count[1:]
    plt.bar(xs, size_count, color="grey")
    add_labels(xs, size_count, 4)
    plt.xlabel("Gruppestørrlse", labelpad=10)
    plt.ylabel("Antal ture", labelpad=10)
    plt.tight_layout()
    plt.show()

def plot_group_sizes_expected(unix_pings_with_sender, for_person):
    groups = get_named_groups_no_duplicates(unix_pings_with_sender)
    max_size = max(map(len, groups))
    size_count = [0] * (max_size + 1)
    for group in groups:
        if for_person in group:
            size_count[len(group)] += 1

    xs = list(range(1, len(size_count)))
    size_count = size_count[1:]
    plt.bar(xs, size_count, color="grey")
    add_labels(xs, size_count, 4)
    plt.xlabel("Gruppestørrlse", labelpad=10)
    plt.ylabel("Antal ture", labelpad=10)
    plt.tight_layout()
    plt.show()

def plot_group_sizes_expected_for_all(unix_pings_with_sender):
    from collections import defaultdict

    groups = get_named_groups_no_duplicates(unix_pings_with_sender)
    max_size = max(map(len, groups))
    size_count_for_person = defaultdict(lambda: [0] * (max_size + 1))
    for group in groups:
        for person in group:
            size_count_for_person[person][len(group)] += 1

    for person, size_count in size_count_for_person.items():
        xs = list(range(1, len(size_count)))
        size_count = size_count[1:]
        plt.bar(xs, size_count, color="grey")
        add_labels(xs, size_count, 4)
        plt.xlabel("Gruppestørrlse", labelpad=10)
        plt.ylabel("Antal ture", labelpad=10)
        plt.tight_layout()
        plt.set_name(person)
        plt.show()


def plot_group_size_per_hour(unix_pings_with_sender, justified=False, hour_range=None):
    groups, groups_time = get_named_groups_no_duplicates(unix_pings_with_sender, return_group_unix=True)

    sizes = [len(b) for b in groups]
    group_dates = to_dates(groups_time)

    hour_groups_sizes = [[0, 0, 0, 0] for _ in range(24)]

    for size, date in zip(sizes, group_dates):
        inc = size if justified else 1
        hour_groups_sizes[date.hour][min(size, 3)] += inc
    
    xs = list(range(24))
    if hour_range is not None:
        hour_groups_sizes = hour_groups_sizes[hour_range[0]:hour_range[1]+1]
        xs = xs[hour_range[0]:hour_range[1]+1]

    colors = ["darkgray", "gray", "lightgray"]
    width = 0.27
    base_offset = -width * 3 / 2 + width / 2

    group_hour_sizes = list(zip(*hour_groups_sizes))
    max_count = max(max(count) for count in group_hour_sizes)
    for size, (counts, color) in enumerate(zip(group_hour_sizes[1:], colors)):
        offset = base_offset + width * size
        plt.bar([x + offset for x in xs], counts, width, color=color)
        add_labels([x + offset for x in xs], counts, max_count * 0.01, rotated=True)
    
    # plt.xticks(xs, xs, rotation=90, ha="right", va="center", rotation_mode="anchor")
    plt.xticks(xs, xs)
    plt.xlabel("Klokkeslet", labelpad=10)
    plt.ylabel("Antal personer" if justified else "Antal grupper", labelpad=10)
    plt.tight_layout()
    plt.ylim(0, max_count * 1.13)
    plt.set_name("groups_per_hour")
    plt.show()



def social_credit_scores(unix_pings_with_sender, ignore_single_groups=False):
    groups = get_named_groups_no_duplicates(unix_pings_with_sender, remove_single_groups=ignore_single_groups)

    credit_score = defaultdict(lambda: 0)
    for group in groups:
        for idx, person in enumerate(group):
            # credit_score[person] += (len(group) - idx) * (1 / 2**idx)
            # credit_score[person] += 1 + (len(group) - 1 - idx) * (1 / 2**idx)
            # credit_score[person] += (len(group) - 1 - idx) * (1 / 2**idx)
            credit_score[person] += (len(group) - idx - 1)
    
    print("Raw credit scores:")
    print(*sorted(credit_score.items(), key=lambda t: t[-1], reverse=True), sep="\n")
    print()

    contained_in_group = defaultdict(lambda: 0)
    for group in groups:
        for person in group:
            contained_in_group[person] += 1
    
    assert credit_score.keys() == contained_in_group.keys()
    people = credit_score.keys()

    normalized_score = {person: credit_score[person] / contained_in_group[person] for person in people}
    
    print("Normalized credit scores:")
    print(*sorted(normalized_score.items(), key=lambda t: t[-1], reverse=True), sep="\n")
    print()


def elo_rating_scores(unix_pings_with_sender, initial_elo=100, K=32, can_loose=True):
    groups = get_named_groups_no_duplicates(unix_pings_with_sender)

    rating = defaultdict(lambda: initial_elo)

    for g in groups:
        chances = defaultdict(lambda: 0)
        
        for i, a in enumerate(g):
            for b in g[i+1:]:
                rating_a = rating[a]
                rating_b = rating[b]
                prop_a = 1.0 / (1 + pow(10, (rating_a - rating_b) / 400))
                prop_b = 1.0 / (1 + pow(10, (rating_b - rating_a) / 400))
                chances[a] += K * (1 - prop_a)
                if can_loose:
                    chances[b] -= K * prop_b
        
        for person, delta in chances.items():
            rating[person] += delta
    
    print(*sorted(rating.items(), key=lambda t: t[-1], reverse=True), sep="\n")



# Read the data
with open("message_1.json") as f:
    data1 = json.load(f)
with open("message_2.json") as f:
    data2 = json.load(f)


coffee_emoji_original = "\u00e2\u0098\u0095\u00ef\u00b8\u008f"

coffee_emoji_all_variants = {
    "\u00e2\u0098\u0095",
    "\u00e2\u0098\u0095\u00ef\u00b8\u0080",
    "\u00e2\u0098\u0095\u00ef\u00b8\u0081",
    "\u00e2\u0098\u0095\u00ef\u00b8\u0082",
    "\u00e2\u0098\u0095\u00ef\u00b8\u0083",
    "\u00e2\u0098\u0095\u00ef\u00b8\u0084",
    "\u00e2\u0098\u0095\u00ef\u00b8\u0085",
    "\u00e2\u0098\u0095\u00ef\u00b8\u0086",
    "\u00e2\u0098\u0095\u00ef\u00b8\u0087",
    "\u00e2\u0098\u0095\u00ef\u00b8\u0088",
    "\u00e2\u0098\u0095\u00ef\u00b8\u0089",
    "\u00e2\u0098\u0095\u00ef\u00b8\u008a",
    "\u00e2\u0098\u0095\u00ef\u00b8\u008b",
    "\u00e2\u0098\u0095\u00ef\u00b8\u008c",
    "\u00e2\u0098\u0095\u00ef\u00b8\u008d",
    "\u00e2\u0098\u0095\u00ef\u00b8\u008e",
    "\u00e2\u0098\u0095\u00ef\u00b8\u008f",
}

cuts = [datetime.datetime(year, 9, 19, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Copenhagen")) for year in [2022, 2023, 2024, 2025] ]

coffee_pings = [
    message
    for data in [data1, data2]
    for message in data["messages"]
    if "content" in message and \
        message["content"] in coffee_emoji_all_variants and \
        cuts[0] <= to_datetime(message["timestamp_ms"]) < cuts[3]
]

coffee_pings.sort(key=lambda message: message["timestamp_ms"])

coffee_pings_years = [
    [message for message in coffee_pings if cuts[0] <= to_datetime(message["timestamp_ms"]) < cuts[1]],
    [message for message in coffee_pings if cuts[1] <= to_datetime(message["timestamp_ms"]) < cuts[2]],
    [message for message in coffee_pings if cuts[2] <= to_datetime(message["timestamp_ms"]) < cuts[3]]
]

print(len(coffee_pings))
print(len(data1["messages"]) + len(data2["messages"]))
pings_per_year = [len(p) for p in coffee_pings_years]
days_per_year = [sum(days_in_month_for_years(y)) for y in [2023, 2024, 2025]]
print(pings_per_year)
print(days_per_year)
print([round(p / d, 2) for p, d in zip(pings_per_year, days_per_year)])
print(round(sum(pings_per_year) / sum(days_per_year), 2))


to_unix_times = lambda pings: [
    message["timestamp_ms"]
    for message in pings
]

unix_pings = to_unix_times(coffee_pings)
unix_pings_years = list(map(to_unix_times, coffee_pings_years))


to_unix_times_with_sender = lambda pings: [
    (message["timestamp_ms"], message["sender_name"])
    for message in pings
]

unix_pings_with_sender = to_unix_times_with_sender(coffee_pings)
unix_pings_with_sender_years = list(map(to_unix_times_with_sender, coffee_pings_years))



to_dates = lambda times: [
    to_datetime(unix)
    for unix in times
]

dates_pings = to_dates(unix_pings)
dates_pings_years = list(map(to_dates, unix_pings_years))

print(min(dates_pings))
print(max(dates_pings))
print()


# Top k pingers
if False:
    count_per_person = defaultdict(lambda: 0)
    for message in coffee_pings:
        count_per_person[message["sender_name"]] += 1

    person_ping_count = sorted(count_per_person.items(), key=lambda t: t[-1], reverse=True)
    print(*person_ping_count, sep="\n")

    k = 5
    top_k_pingers = {person for person, _ in person_ping_count[:k]}
    print(top_k_pingers)


# Tea ping analysis
if False:
    tea = "\u00F0\u009F\u008D\u00B5"
    tea_pings = [
        message
        for data in [data1, data2]
        for message in data["messages"]
        if "content" in message and tea in message["content"]
    ]

    print(*tea_pings, sep="\n")

    exit(0)


# Weird pings analysis
if False:
    from collections import Counter

    coffee_pings_weird = [
        message
        for data in [data1, data2]
        for message in data["messages"]
        if "content" in message and \
            message["content"] in coffee_emoji_all_variants and message["content"] != coffee_emoji_original and \
            cuts[0] <= to_datetime(message["timestamp_ms"]) < cuts[3]
    ]
    print(len(coffee_pings_weird))
    
    pings_content = [bytes(message["content"], "utf-8") for message in coffee_pings_weird]
    print(Counter(pings_content))

    senders = [message["sender_name"] for message in coffee_pings_weird]
    print(Counter(senders))

    coffee_pings_weird.sort(key=lambda m: m["timestamp_ms"])

    a, b, c = 26, 20, 30
    print(f"{'Day':<{a}s}|{'Person':<{b}s}|{'Message':<{c}s}")
    print(f"{'-'*a}+{'-'*b}+{'-'*c}")

    for message in coffee_pings_weird:
        day, = to_dates([message["timestamp_ms"]])
        person = message["sender_name"]
        raw_message = str(bytes(message["content"], "utf-8"))
        print(f"{str(day):<{a}s}|{person[:b]:<{b}s}|{raw_message:<{c}s}")

    switch_message = "\u00e2\u0098\u0095: \u00e2\u0098\u0095: \u00e2\u0098\u0095: \u00e2\u0098\u0095: \u00e2\u0098\u0095: \u00e2\u0098\u0095 har indstillet den hurtige reaktion til \u00e2\u0098\u0095."
    the_switch = [
        message
        for data in [data1, data2]
        for message in data["messages"]
        if "content" in message and message["content"] == switch_message
    ]
    assert len(the_switch) == 1
    print(to_dates([m["timestamp_ms"] for m in the_switch]))

    exit(0)


# Pings per person per year
if False:
    from collections import defaultdict

    count = defaultdict(lambda: [0, 0, 0])

    for year_idx, pings in enumerate(coffee_pings_years):
        for message in pings:
            count[message["sender_name"]][year_idx] += 1

    print(*sorted(count.items()), sep="\n")

    exit(0)


# Test plot all tuesdays
if False:
    plot_weekday_by_hour_single_weekday_analysis(dates_pings_years[-1], 1)



# Basis plots
if False:
    plot_weekday_analysis(dates_pings)
    plot_weekday_analysis(dates_pings_years[-1])

    plot_weekday_by_hour_analysis(dates_pings)
    plot_weekday_by_hour_analysis(dates_pings_years[-1])

    plot_month_analysis(dates_pings)
    plot_month_analysis(dates_pings_years[-1])

    plot_year_by_date_analysis(dates_pings, day_count_tests=[lambda count: count == 0])
    plot_year_by_date_analysis(dates_pings_years[-1], day_count_tests=[lambda count: count >= 25])

# Combined plots
if True:
    plot_weekday_analysis_multi(dates_pings_years)
    plot_month_analysis_multi(dates_pings_years)


# Great many pings on the 30th july
if False:
    from_date = datetime.datetime(2025, 7, 29, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Copenhagen"))
    to_date = datetime.datetime(2025, 8, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Copenhagen"))
    mega_pings = [
        (str(*to_dates([message["timestamp_ms"]])), message["sender_name"])
        for message in coffee_pings
        if from_date <= to_dates([message["timestamp_ms"]])[0] < to_date
    ]
    print(*mega_pings, sep="\n")

    exit(0)


# Other plots
if False:
    plot_cummulative_year_analysis(dates_pings)
    plot_pings_per_day_normal_distribution(dates_pings)
    plot_pings_per_day_normal_distribution(dates_pings, ignore_zero_days=True)


# Try the group sizes again
if False:
    plot_group_sizes(unix_pings_with_sender)
    plot_group_sizes(unix_pings_with_sender, justified=True)
    plot_group_sizes_expected(unix_pings_with_sender, "Casper Rysgaard")

    plot_group_sizes(unix_pings_with_sender_years[-1])
    plot_group_sizes(unix_pings_with_sender_years[-1], justified=True)
    plot_group_sizes_expected(unix_pings_with_sender_years[-1], "Casper Rysgaard")

    plot_group_sizes_expected_for_all(unix_pings_with_sender)


# Group sizes by hour
if False:
    plot_group_size_per_hour(unix_pings_with_sender)
    plot_group_size_per_hour(unix_pings_with_sender, justified=True)
    plot_group_size_per_hour(unix_pings_with_sender, justified=True, hour_range=(7, 18))

# Group analysis
if False:
    print("Groups:")
    print(len(get_named_groups_no_duplicates(unix_pings_with_sender, remove_single_groups=False)))
    print(len(get_named_groups_no_duplicates(unix_pings_with_sender, remove_single_groups=True)))
    print()

# Social credit scores
if False:
    social_credit_scores(unix_pings_with_sender, ignore_single_groups=False)
    # social_credit_scores(unix_pings_with_sender, ignore_single_groups=True)


# Elo rating
if False:
    # elo_rating_scores(unix_pings_with_sender_years[0], initial_elo=5000, K=16)
    # print()
    # elo_rating_scores(unix_pings_with_sender_years[1], initial_elo=5000, K=16)
    # print()
    # elo_rating_scores(unix_pings_with_sender_years[2], initial_elo=5000, K=16)
    # print()
    # elo_rating_scores(unix_pings_with_sender, initial_elo=5000, K=16)

    elo_rating_scores(unix_pings_with_sender, initial_elo=1200, K=16)
    print()
    elo_rating_scores(unix_pings_with_sender, initial_elo=0, K=16, can_loose=False)

# Analysis just om me
if False:
    casper_dates_last = to_dates(to_unix_times([message for message in coffee_pings_years[-1] if message["sender_name"] == "Casper Rysgaard"]))
    plot_weekday_by_hour_analysis(casper_dates_last)

    from_date = datetime.datetime(2025, 7, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Copenhagen"))
    to_date = datetime.datetime(2025, 8, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Copenhagen"))
    casper_dates_last_juli = [
        date for date in casper_dates_last
        if from_date <= date < to_date
    ]
    plot_weekday_by_hour_analysis(casper_dates_last_juli)


# Analyze each person last year
if False:
    people = {message["sender_name"] for message in coffee_pings_years[-1]}
    for person in people:
        person_dates = to_dates(to_unix_times([message for message in coffee_pings_years[-1] if message["sender_name"] == person]))
        plot_weekday_by_hour_analysis(person_dates, append_name=person)
