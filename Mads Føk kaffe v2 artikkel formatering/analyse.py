PLOT_SAVE = True

import json
import datetime
import zoneinfo
import matplotlib.pyplot as plt

def to_datetime(unix_ms): return datetime.datetime.fromtimestamp(unix_ms // 1000, tz=zoneinfo.ZoneInfo("Europe/Copenhagen"))

font_default = 10
def set_font(size):
    plt.rcParams['font.size'] = size

plt.set_font = set_font

def font_saver(f):
    def inner():
        f()
        plt.rcParams['font.size'] = font_default
    return inner

if PLOT_SAVE:
    name = None
    def set_name(local_name):
        global name
        name = local_name
    plt.set_name = set_name

    # @font_saver
    def save():
        global name
        assert name is not None
        plt.savefig(f"plot_{name}.pgf", bbox_inches='tight')
        plt.clf()
        name = None
    plt.show = save

else:
    plt.set_name = plt.title
    # plt.show = font_saver(plt.show)

plt.rcParams['font.size'] = font_default



def add_labels(xs, int_values, offset, neg_offset=None, rotate=False):
    if neg_offset is None:
        neg_offset = offset
    kwargs = {"ha": "center"}
    if rotate:
        kwargs["rotation"] = 90
        kwargs["va"] = "center"
        kwargs["rotation_mode"] = "anchor"
    for x, c in zip(xs, int_values):
        if rotate:
            kwargs["ha"] = "left" if c >= 0 else "right"
        plt.text(x, c + offset if c >= 0 else c - neg_offset, c, **kwargs)


def year_range(dates):
    return f"{dates[-1].year}-{dates[0].year}"


def plot_weekday_analysis(dates, diff=None):
    name_tail = year_range(dates) + (f"_diff_{year_range(diff)}" if diff is not None else "")

    weekday_count = [0] * 7
    for date in dates:
        weekday_count[date.weekday()] += 1
    
    if diff is not None:
        for date in diff:
            weekday_count[date.weekday()] -= 1
        
        plt.axhline(y=0, color='black', linestyle='-')

    plt.bar(range(7), weekday_count, color="grey")
    weekday_names = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]
    plt.xticks(range(7), weekday_names, rotation=90, ha="right", va="center", rotation_mode="anchor")
    plt.ylabel("Antal pings", labelpad=10)
    add_labels(range(7), weekday_count, max(weekday_count) * 0.03)
    plt.tight_layout()
    plt.ylim(min(0, *weekday_count), max(weekday_count) * 1.13)
    plt.set_name(f"weekday_analysis_{name_tail}")
    plt.show()

    weekday_hour_count = [[0] * 24 for _ in range(7)]
    for date in dates:
        weekday_hour_count[date.weekday()][date.hour] += 1
    
    if diff is not None:
        for date in diff:
            weekday_hour_count[date.weekday()][date.hour] -= 1

    for i, day in enumerate(weekday_hour_count):
        off = 24 * i
        # plt.bar(range(off, off + 24), day, align='edge', width=1.0)
        plt.bar(range(off, off + 24), day, align='edge', color="grey", width=1.0)

    min_entry = 0 if diff is None else min(hour_count for day in weekday_hour_count for hour_count in day) - 4
    max_entry = max(hour_count for day in weekday_hour_count for hour_count in day) + 4
    for i in range(1, 7):
        plt.plot([i * 24, i * 24], [min_entry, max_entry], ":", color="black")

    if diff is not None:
        plt.axhline(y=0, color='black', linestyle='-')

    space = "\\hspace{3pt}"
    # space=""
    labels = [l for name in weekday_names for l in ["", space+"06\n", space+"12\n" + space+name, space+"18\n"]]
    plt.xticks(range(0, 24 * 7, 6), labels)
    plt.xlim([0, 24 * 7])
    plt.ylim([min_entry, max_entry])
    plt.xlabel("Klokkeslet \& Ugedag", labelpad=10)
    plt.ylabel("Antal pings", labelpad=10)
    plt.set_name(f"weekday_analysis_hour_{name_tail}")
    plt.show()


def plot_weeknumber_over_year_analysis(dates, diff=None):
    pings_pr_weeknumber = [0] * 53
    for date in dates:
        pings_pr_weeknumber[date.isocalendar().week] += 1
    
    if diff is not None:
        for date in diff:
            pings_pr_weeknumber[date.isocalendar().week] -= 1

    plt.bar(range(1, 53), pings_pr_weeknumber[1:], color="grey")
    plt.xlabel("Uge nummer")
    plt.ylabel("Antal pings", labelpad=10)
    # add_labels(range(7), weekday_count, 4, neg_offset=10)
    plt.tight_layout()
    # plt.set_name(f"weekday_analysis_{name_tail}")
    plt.show()


def plot_year_analysis(dates, diff=None, named=None, day_count_tests=[], label_height=4):
    name_tail = year_range(dates) + (f"_diff_{year_range(diff)}" if diff is not None else "")
    if named is not None: name_tail = named

    month_count = [0] * 12
    for date in dates:
        month_count[date.month - 1] += 1
    
    if diff is not None:
        for date in diff:
            month_count[date.month - 1] -= 1
        
        plt.axhline(y=0, color='black', linestyle='-')

    month_names = ["Januar", "Februar", "Marts", "April", "Maj", "Juni", "Juli", "August", "September", "Oktober", "November", "December"]
    plt.bar(range(12), month_count, color="grey")
    plt.xticks(range(12), month_names, rotation=90, ha="right", va="center", rotation_mode="anchor")
    add_labels(range(12), month_count, max(month_count) * 0.03)
    plt.ylabel("Antal pings", labelpad=10)
    plt.ylim(min(0, *month_count), max(month_count) * 1.13)
    plt.tight_layout()
    plt.set_name(f"month_analysis_{name_tail}")
    plt.show()
    
    days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_day_count = [[0] * days for days in days_in_month]
    for date in dates:
        month_day_count[date.month - 1][date.day - 1] += 1
    
    if diff is not None:
        for date in diff:
            month_day_count[date.month - 1][date.day - 1] -= 1
        
        plt.axhline(y=0, color='black', linestyle='-')

    for test in day_count_tests:
        print(f"Test {test}:")
        print([(day + 1, month_names[month], count) for month, days in enumerate(month_day_count) for day, count in enumerate(days) if test(count)])

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
    
    min_entry = 0 if diff is None else min(day_count for month in month_day_count for day_count in month) - 1
    max_entry = max(day_count for month in month_day_count for day_count in month) + 1
    
    plt.xticks(ticks, month_names, rotation=90, ha="right", va="center", rotation_mode="anchor")
    plt.xlim([0, sum(days_in_month)])
    plt.ylim([min_entry, max_entry])
    plt.ylabel("Antal pings", labelpad=10)
    plt.tight_layout()
    plt.set_name(f"year_analysis_{name_tail}")
    plt.show()


def plot_weekday_and_month_side_by_side(dates_1, dates_2):
    name_tail = year_range(dates_1) + "_" + year_range(dates_2)

    width = 0.4
    padding = 0.0

    weekday_counts = []
    for i, (dates, color) in enumerate([(dates_1, "gray"), (dates_2, "lightgray")]):
        weekday_count = [0] * 7
        for date in dates:
            weekday_count[date.weekday()] += 1
        
        offset = -width / 2 - padding / 2 + (width + padding) * i
        plt.bar([x + offset for x in range(7)], weekday_count, width, color=color)

        weekday_counts.append(weekday_count)
    
    max_count = max(*weekday_counts[0], max(*weekday_counts[1]))
    for i, weekday_count in enumerate(weekday_counts):
        offset = -width / 2 - padding / 2 + (width + padding) * i
        add_labels([x + offset for x in range(7)], weekday_count, max_count * 0.03)

    weekday_names = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]
    plt.xticks(range(7), weekday_names, rotation=90, ha="right", va="center", rotation_mode="anchor")
    plt.ylabel("Antal pings", labelpad=10)
    plt.tight_layout()
    plt.ylim(0, max_count * 1.13)
    plt.set_name(f"weekday_analysis_side_by_side_{name_tail}")
    plt.show()


    month_counts = []
    for i, (dates, color) in enumerate([(dates_1, "gray"), (dates_2, "lightgray")]):
        month_count = [0] * 12
        for date in dates:
            month_count[date.month - 1] += 1
        
        offset = -width / 2 - padding / 2 + (width + padding) * i
        plt.bar([x + offset for x in range(12)], month_count, width, color=color)

        month_counts.append(month_count)
    
    max_count = max(*month_counts[0], max(*month_counts[1]))
    for i, month_count in enumerate(month_counts):
        offset = -width / 2 - padding / 2 + (width + padding) * i
        add_labels([x + offset for x in range(12)], month_count, max_count * 0.03, rotate=True)

    month_names = ["Januar", "Februar", "Marts", "April", "Maj", "Juni", "Juli", "August", "September", "Oktober", "November", "December"]
    plt.xticks(range(12), month_names, rotation=90, ha="right", va="center", rotation_mode="anchor")
    plt.ylabel("Antal pings", labelpad=10)
    plt.tight_layout()
    plt.ylim(0, max_count * 1.13)
    plt.set_name(f"month_analysis_side_by_side_{name_tail}")
    plt.show()


def plot_weekday_hour_on_top(dates_1, dates_2):
    name_tail = year_range(dates_1) + "_" + year_range(dates_2)

    min_entry = float("inf")
    max_entry = -float("inf")

    for dates, sign in (dates_1, 1), (dates_2, -1):
        weekday_hour_count = [[0] * 24 for _ in range(7)]
        for date in dates:
            weekday_hour_count[date.weekday()][date.hour] += 1

        for i, day in enumerate(weekday_hour_count):
            off = 24 * i
            day_data = [h * sign for h in day]
            plt.bar(range(off, off + 24), day_data, align='edge', color="grey", width=1.0)

            min_entry = min(min_entry, *day_data)
            max_entry = max(max_entry, *day_data)

    min_entry -= 4
    max_entry += 4

    for i in range(1, 7):
        plt.plot([i * 24, i * 24], [min_entry, max_entry], ":", color="black")
    
    plt.axhline(y=0, color='black', linestyle='-')

    # space = "\\hspace{3pt}"
    space=""
    weekday_names = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]
    labels = [l for name in weekday_names for l in ["", space+"06\n", space+"12\n" + space+name, space+"18\n"]]
    plt.xticks(range(0, 24 * 7, 6), labels)
    plt.xlim([0, 24 * 7])
    plt.xlabel("Klokkeslet \& Ugedag", labelpad=10)

    plt.ylim([min_entry, max_entry])
    plt.ylabel("Antal pings", labelpad=40)
    plt.gca().yaxis.set_major_formatter(lambda y, p: int(abs(y)))
    sec = plt.gca().secondary_yaxis(location=0)
    sec.set_yticks([max_entry / 2, min_entry / 2], ["Periode 1\n\n", "Periode 2\n\n"], rotation=90)
    sec.tick_params('y', length=0)

    plt.set_name(f"weekday_analysis_hour_over_{name_tail}")
    plt.show()


def plot_weekday_hour_super_imposed(dates_1, dates_2):
    weekday_hour_counts = []
    for dates in dates_1, dates_2:
        weekday_hour_count = [[0] * 24 for _ in range(7)]
        for date in dates:
            weekday_hour_count[date.weekday()][date.hour] += 1
        weekday_hour_counts.append(weekday_hour_count)

    for i, (day_1, day_2) in enumerate(zip(*weekday_hour_counts)):
        off = 24 * i
        
        # day_1_min_data = [h1 if h1 < h2 else 0 for h1, h2 in zip(day_1, day_2)]
        # day_1_max_data = [h1 if h1 > h2 else 0 for h1, h2 in zip(day_1, day_2)]
        # day_2_min_data = [h2 if h1 > h2 else 0 for h1, h2 in zip(day_1, day_2)]
        # day_2_max_data = [h2 if h1 < h2 else 0 for h1, h2 in zip(day_1, day_2)]
        # day_equal_data = [h1 if h1 == h2 else 0 for h1, h2 in zip(day_1, day_2)]
        
        # plt.bar(range(off, off + 24), day_1_max_data, align='edge', color="grey", width=1.0)
        # plt.bar(range(off, off + 24), day_2_max_data, align='edge', color="lightgrey", width=1.0)
        # # plt.bar(range(off, off + 24), day_1_min_data, align='edge', color="grey", width=1.0)
        # # plt.bar(range(off, off + 24), day_1_min_data, align='edge', color="white", width=1.0)
        # plt.bar(range(off, off + 24), day_1_min_data, align='edge', color="darkgrey", width=1.0)
        # # plt.bar(range(off, off + 24), day_2_min_data, align='edge', color="lightgrey", width=1.0)
        # # plt.bar(range(off, off + 24), day_2_min_data, align='edge', color="white", width=1.0)
        # plt.bar(range(off, off + 24), day_2_min_data, align='edge', color="darkgrey", width=1.0)
        # plt.bar(range(off, off + 24), day_equal_data, align='edge', color="darkgrey", width=1.0)

        day_min = [min(h1, h2) for h1, h2 in zip(day_1, day_2)]
        
        plt.bar(range(off, off + 24), day_1, align='edge', color="grey", width=1.0)
        plt.bar(range(off, off + 24), day_2, align='edge', color="lightgrey", width=1.0)
        plt.bar(range(off, off + 24), day_min, align='edge', color="darkgrey", width=1.0)

    max_entry = max(h for count in weekday_hour_counts for day in count for h in day) + 4
    for i in range(1, 7):
        plt.plot([i * 24, i * 24], [0, max_entry], ":", color="black")

    space = "\\hspace{3pt}"
    # space=""
    weekday_names = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]
    labels = [l for name in weekday_names for l in ["", space+"06\n", space+"12\n" + space+name, space+"18\n"]]
    plt.xticks(range(0, 24 * 7, 6), labels)
    plt.xlim([0, 24 * 7])
    plt.xlabel("Klokkeslet \& Ugedag", labelpad=10)

    plt.ylim([0, max_entry])
    plt.ylabel("Antal pings", labelpad=10)
    name_tail = year_range(dates_1) + "_" + year_range(dates_2)
    plt.set_name(f"weekday_analysis_hour_imposed_{name_tail}")
    plt.show()


def plot_count_days_with_certain_pings(dates):
    days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    all_dates = [
        (year, month, day)
        for year in [2022, 2023, 2024]
        for month, count in enumerate(days_in_month, start=1)
        for day in range(1, count + 1 - int(year != 2024 and month == 2))
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

    # plt.bar(range(max_count + 1), count_count, color="gray")
    plt.bar(range(max_count + 1), [c / total for c in count_count], color="gray")
    # add_labels(range(max_count + 1), count_count, max(count_count) * 0.03)
    # plt.ylim(0, max(count_count) * 1.13)
    # plt.ylabel("Number of days", labelpad=10)
    plt.ylabel("Procent af alle dage", labelpad=10)
    plt.xlabel("Antal pings per dag")

    # plt.gca().set_yticklabels([f'{x*100:.0f}%' for x in plt.gca().get_yticks()]) 

    import matplotlib.ticker as mtick
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))

    full_data = [v for v, c in enumerate(count_count) for _ in range(c)]
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
    x = np.linspace(0, max_count, 100)
    norm = stats.norm.pdf(x, mu, sigma)
    # scale = max(count_count) / max(norm)
    scale = 1
    plt.plot(x, scale * norm, color="black")

    # ysec = plt.gca().secondary_yaxis('right', functions=(lambda y: y/scale, lambda y: y/scale))
    # ysec.set_ylabel("Sandsynlighed", labelpad=10)

    plt.set_name("days_count_distribution")
    plt.show()


def plot_cummulative_year_analysis(dates, named=None):
    # TODO: hardcoded
    days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    all_dates = [
        (year, month, day)
        for year in [2022, 2023, 2024]
        for month, count in enumerate(days_in_month, start=1)
        for day in range(1, count + 1 - int(year != 2024 and month == 2))
    ]

    # TODO: hardcoded
    observe_dates = all_dates[261:-104]

    # print(dates[-1], dates[0])
    # print(observe_dates[0], observe_dates[-1])

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

    month_names = ["Januar", "Februar", "Marts", "April", "Maj", "Juni", "Juli", "August", "September", "Oktober", "November", "December"]
    month_ticks = []
    for i, (year, month, day) in enumerate(observe_dates):
        if (days_in_month[month - 1] - int(year != 2024 and month == 2)) // 2 == day:
            month_ticks.append((i, f"{month_names[month - 1]}"))
    plt.xticks(*zip(*month_ticks), rotation=90, ha="right", va="center", rotation_mode="anchor")

    year_ticks = []
    for y in [2022, 2023, 2024]:
        iss = [i for i, (year, _, _) in enumerate(observe_dates) if year == y]
        min_i = min(iss)
        max_i = max(iss)
        year_ticks.append(((min_i + max_i) / 2, f"\n\n\n\n{y}"))
    sec = plt.gca().secondary_xaxis(location=0)
    sec.set_xticks(*zip(*year_ticks))
    sec.tick_params('x', length=0)

    sec2 = plt.gca().secondary_xaxis(location=0)
    sep = []
    for y1, y2 in [(2022, 2023), (2023, 2024)]:
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


def plot_double_cummulative_year_analysis(dates, single_dates, named):
    # TODO: hardcoded
    days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    all_dates = [
        (year, month, day)
        for year in [2022, 2023, 2024]
        for month, count in enumerate(days_in_month, start=1)
        for day in range(1, count + 1 - int(year != 2024 and month == 2))
    ]

    # TODO: hardcoded
    observe_dates = all_dates[261:-104]

    data = []
    for dates in dates, single_dates:
        from collections import defaultdict
        observations = defaultdict(lambda: 0)
        for date in dates:
            observations[date.year, date.month, date.day] += 1
        
        total = 0
        data_line = []
        for date in observe_dates:
            total += observations[date]
            data_line.append(total)
        
        data.append(data_line)
    
    scale = data[0][-1] / data[1][-1]
    plt.plot([0, len(observe_dates) - 1], [0, data[0][-1]], ":", color="lightgray")
    plt.plot(range(len(observe_dates)), data[0], "-", color="black")
    plt.plot(range(len(observe_dates)), [d * scale for d in data[1]], "-", color="gray")

    plt.xlim([-1, len(observe_dates)])
    plt.ylim([-1, data[0][-1] + 1])

    plt.ylabel("Antal pings", labelpad=10)
    ysec = plt.gca().secondary_yaxis('right', functions=(lambda y: y/scale, lambda y: y/scale))
    ysec.set_ylabel("Steffan antal pings", labelpad=0)

    month_names = ["Januar", "Februar", "Marts", "April", "Maj", "Juni", "Juli", "August", "September", "Oktober", "November", "December"]
    month_ticks = []
    for i, (year, month, day) in enumerate(observe_dates):
        if (days_in_month[month - 1] - int(year != 2024 and month == 2)) // 2 == day:
            month_ticks.append((i, f"{month_names[month - 1]}"))
    plt.xticks(*zip(*month_ticks), rotation=90, ha="right", va="center", rotation_mode="anchor")

    year_ticks = []
    for y in [2022, 2023, 2024]:
        iss = [i for i, (year, _, _) in enumerate(observe_dates) if year == y]
        min_i = min(iss)
        max_i = max(iss)
        year_ticks.append(((min_i + max_i) / 2, f"\n\n\n\n\n{y}"))
        # year_ticks.append(((min_i + max_i) / 2, f"\n\n\n\n\n\n{y}"))
    sec = plt.gca().secondary_xaxis(location=0)
    sec.set_xticks(*zip(*year_ticks))
    sec.tick_params('x', length=0)

    sec2 = plt.gca().secondary_xaxis(location=0)
    sep = []
    for y1, y2 in [(2022, 2023), (2023, 2024)]:
        a = max(i for i, (y, _, _) in enumerate(observe_dates) if y == y1)
        b = min(i for i, (y, _, _) in enumerate(observe_dates) if y == y2)
        sep.append((a + b) / 2)
    sec2.set_xticks(sep, labels=[])
    sec2.tick_params('x', length=60, width=1)
    # sec2.tick_params('x', length=95, width=1)

    name = "double_cummulative_sum_vs_average_with_" + named
    plt.set_name(name)
    plt.tight_layout()
    plt.show()


def plot_group_sizes():
    # Five minutes
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


def plot_group_graf_relation(unix_time_with_sender, line_ticks=20, anonymous=False):
    plt.rcParams['font.size'] = 20

    # Five minutes
    time_within = 5 * 60 * 1000

    sorted_time_sender = sorted(unix_time_with_sender)
    buckets = [([sorted_time_sender[0][0]], [sorted_time_sender[0][1]])]
    for t, s in sorted_time_sender[1:]:
        if t - buckets[-1][0][-1] > time_within:
            buckets.append(([], []))
        buckets[-1][0].append(t)
        buckets[-1][1].append(s)
    
    new_buckets = [b for b in buckets if len(b[0]) >= 2]
    print("Solo groups =", len(buckets) - len(new_buckets))
    buckets = new_buckets

    # Detect double pings
    double_count = 0
    for bts, bss in buckets:
        if len(bss) > len(set(bss)):
            double_count += 1
            # print("!!!", to_datetime(bts[0]), to_datetime(bts[-1]), bss)
            if len(set(bts)) == 1:
                assert False
    print("Counting groups:")
    print(f"{double_count = }")
    print("Total count =", len(buckets))

    all_persons = {s for _, s in unix_time_with_sender}
    person_weight = {p: 0 for p in all_persons}
    pair_weights = {(a, b): 0 for a in all_persons for b in all_persons if a < b}

    for _, group in buckets:
        group = set(group)
        for a in group:
            person_weight[a] += 1
            for b in group:
                if a < b:
                    pair_weights[a, b] += 1
    
    weights = sorted([(w, a, b) for (a, b), w in pair_weights.items()])
    # print(*weights, sep="\n")

    from math import sin, cos, pi
    turn = 2 * pi / len(all_persons)
    polar_to_xy = lambda dis, i: (dis * cos(turn * i), dis * sin(turn * i))
    people_ordered = sorted(all_persons)
    person_to_location = {p: polar_to_xy(10, i) for i, p in enumerate(people_ordered)}
    

    def annotate():
        # greek = [r"$ \alpha $", r"$ \beta $", r"$ \gamma $", r"$ \delta $", r"$ \epsilon $", r"$ \zeta $", r"$ \eta $", r"$ \theta $", r"$ \iota $", r"$ \kappa $", r"$ \lambda $", r"$ \mu $", r"$ \nu $", r"$ \xi $", "$o$", r"$ \pi $", r"$ \rho $", r"$ \sigma $", r"$ \tau $", r"$ \upsilon $", r"$ \phi $", r"$ \chi $", r"$ \psi $", r"$ \omega $"]
        greek = [r"$ \alpha $", r"$ \beta $", r"$ \gamma $", r"$ \delta $", r"$ \zeta $", r"$ \eta $", r"$ \theta $", r"$ \iota $", r"$ \kappa $", r"$ \lambda $", r"$ \nu $", r"$ \xi $", "$o$", r"$ \pi $", r"$ \rho $", r"$ \sigma $", r"$ \tau $", r"$ \upsilon $", r"$ \phi $", r"$ \chi $", r"$ \psi $", r"$ \omega $"]
        for i, p in enumerate(people_ordered):
            plt.plot(*polar_to_xy(10, i), "o", color="black")
            if not anonymous:
                plt.annotate(p, polar_to_xy(10, i),
                            xytext=polar_to_xy(14 + (i == 6 or i == 17), i), ha='center',
                            arrowprops=dict(arrowstyle="->"))
            else:
                plt.annotate(greek[i], polar_to_xy(10, i), xytext=polar_to_xy(11.5, i), ha='center')


    max_weight = max(pair_weights.values())
    for w, a, b in weights:
        points = [person_to_location[a], person_to_location[b]]
        plt.plot(*zip(*points), "-", color=str(1-(w/max_weight)))
    
    annotate()

    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')
    plt.tight_layout()
    plt.set_name("pair_relation_norm_by_max_pair_weight")
    plt.show()

    max_person_group_weight = {
        p: max(pair_weights[(p, a) if p < a else (a, p)] for a in all_persons if a != p)
        for p in all_persons
    }

    for normalizer, plot_name in [(person_weight, "pair_relation_norm_by_person_group_count"), (max_person_group_weight, "pair_relation_norm_by_person_max_pair_count")]:
        line_to_plot = []
        for w, a, b in weights:
            xa, ya = person_to_location[a]
            xb, yb = person_to_location[b]
            a_col = 1 - (w / normalizer[a]) if normalizer[a] != 0 else 1
            b_col = 1 - (w / normalizer[b]) if normalizer[b] != 0 else 1
            # cutoff = 0.4
            # if a_col > cutoff or b_col > cutoff: continue
            dx = (xb - xa) / line_ticks
            dy = (yb - ya) / line_ticks
            dc = (b_col - a_col) / line_ticks
            for i in range(line_ticks):
                line_to_plot.append((a_col + (i + 0.5) * dc, [xa + i * dx, xa + (i + 1) * dx],[ya + i * dy, ya + (i + 1) * dy]))
        
        line_to_plot.sort(reverse=True)
        print(f"Had {len(line_to_plot)} lines")
        cutoff = 0.95
        line_to_plot = [(c / cutoff, xs, ys) for c, xs, ys in line_to_plot if c <= cutoff]
        print(f"Decrease to {len(line_to_plot)} lines")
        for c, xs, ys in line_to_plot:
            plt.plot(xs, ys, "-", color=str(c))

        annotate()

        plt.gca().set_aspect('equal', adjustable='box')
        plt.axis('off')
        plt.tight_layout()
        plt.set_name(plot_name)
        plt.show()
    
    plt.rcParams['font.size'] = font_default


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

    plt.xticks(xs, labels, rotation=60, ha="right", va="center", rotation_mode="anchor")
    # plt.xticks(xs, xs)
    # plt.xticks([], [])
    plt.ylabel("Antal pings", labelpad=10)
    plt.tight_layout()
    plt.show()


def plot_people_count_time_sensitive():
    from collections import defaultdict

    people_pings = defaultdict(lambda: [])
    for message in coffee_pings:
        people_pings[message["sender_name"]].append(to_datetime(message["timestamp_ms"]))
    
    days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    dates = [
        (year, month, day)
        for year in [2022, 2023]
        for month, count in enumerate(days_in_month, start=1)
        for day in range(1, count + 1)
    ]

    # TODO: HARDCODED
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


with open("message_1.json") as f:
    data = json.load(f)


coffee_emoji = "\u00e2\u0098\u0095\u00ef\u00b8\u008f"
coffee_emoji_steffan = "\u00e2\u0098\u0095\u00ef\u00b8\u008e"
coffee_emoji_no_tail = "\u00e2\u0098\u0095"
assert data["messages"][0]["content"] == coffee_emoji
assert all(not ("content" in message and message["content"] == coffee_emoji_steffan) for message in data["messages"])

Steffan = "Steffan Christ S\u00c3\u00b8lvsten"
Lasse = "Lasse Letager Hansen"
Casper = "Casper Rysgaard"
Louise = "Louise Dohn"
Andreas = "Andreas Hesselholt H\u00c3\u00b8j Hansen"

coffee_pings = [
    message
    for message in data["messages"]
    if "content" in message and message["content"] in [coffee_emoji, coffee_emoji_no_tail]
]

cuts = [datetime.datetime(year, 9, 19, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Copenhagen")) for year in [2022, 2023, 2024] ]

coffee_pings_1 = [message for message in coffee_pings if cuts[0] <= to_datetime(message["timestamp_ms"]) < cuts[1]]
coffee_pings_2 = [message for message in coffee_pings if cuts[1] <= to_datetime(message["timestamp_ms"]) < cuts[2]]

coffee_pings_1_missing = [message for message in coffee_pings if message["content"] == coffee_emoji_no_tail and cuts[0] <= to_datetime(message["timestamp_ms"]) < cuts[1]]
# print(len(coffee_pings_1_missing))
# print(len(coffee_pings_1) - len(coffee_pings_1_missing))

coffee_pings_1_steffan_missing = [
    message
    for message in coffee_pings
    if message["content"] == coffee_emoji_no_tail and
       message["sender_name"] == Steffan and
       cuts[0] <= to_datetime(message["timestamp_ms"]) < cuts[1]
]
coffee_pings_1_steffan_not_missing = [
    message
    for message in coffee_pings
    if message["content"] == coffee_emoji and
       message["sender_name"] == Steffan and
       cuts[0] <= to_datetime(message["timestamp_ms"]) < cuts[1]
]
steffan_pings = [message for message in coffee_pings if message["sender_name"] == Steffan]
lasse_pings = [message for message in coffee_pings if message["sender_name"] == Lasse]
casper_pings = [message for message in coffee_pings if message["sender_name"] == Casper]
louise_pings = [message for message in coffee_pings if message["sender_name"] == Louise]
andreas_pings = [message for message in coffee_pings if message["sender_name"] == Andreas]

to_unix_times = lambda pings: [
    message["timestamp_ms"]
    for message in pings
]

unix_times = to_unix_times(coffee_pings)
unix_times_1 = to_unix_times(coffee_pings_1)
unix_times_2 = to_unix_times(coffee_pings_2)

unix_time_with_sender = [(message["timestamp_ms"], message["sender_name"]) for message in coffee_pings]

to_dates = lambda times: [
    to_datetime(unix)
    for unix in times
]

dates = to_dates(unix_times)
dates_1 = to_dates(unix_times_1)
dates_2 = to_dates(unix_times_2)
dates_1_missing = to_dates(to_unix_times(coffee_pings_1_missing))
dates_1_steffan_missing = to_dates(to_unix_times(coffee_pings_1_steffan_missing))
dates_1_steffan_not_missing = to_dates(to_unix_times(coffee_pings_1_steffan_not_missing))
dates_steffan = to_dates(to_unix_times(steffan_pings))
dates_lasse = to_dates(to_unix_times(lasse_pings))
dates_casper = to_dates(to_unix_times(casper_pings))
dates_louise = to_dates(to_unix_times(louise_pings))
dates_andreas = to_dates(to_unix_times(andreas_pings))

print(min(dates))
print(max(dates))

print("Total pings:", len(coffee_pings))
print("Year 1 pings:", len(coffee_pings_1))
print("Year 2 pings:", len(coffee_pings_2))

# w = sum(date.weekday() >= 5 or date.hour < 7 or date.hour >= 17 for date in dates)
# print("Total outside work hours", w, w / len(dates))
# persons = {message["sender_name"] for message in coffee_pings}
# data = []
# for person in persons:
#     d = to_dates(to_unix_times(message for message in coffee_pings if message["sender_name"] == person))
#     a = sum(date.weekday() >= 5 or date.hour < 7 or date.hour >= 17 for date in d)
#     data.append((person, len(d), a, a / len(d)))
# data = sorted(data, key=lambda t: t[-1])
# print(*data, sep="\n")

# plt.plot([0, len(data) - 1], [w/len(dates)]*2, ":", color="blue")
# plt.plot([0, len(data) - 1], [data[len(data) // 2][-1]]*2, ":", color="red")
# plt.plot(range(len(data)), [d[-1] for d in data], "-", color="black")
# plt.xticks(range(len(data)), [d[0] for d in data], rotation=90, ha="right", va="center", rotation_mode="anchor")
# plt.tight_layout()
# plt.show()


# from collections import Counter
# print("Missing:", Counter(message["sender_name"] for message in coffee_pings_1_missing))

plot_weekday_analysis(dates)
# plot_weekday_analysis(dates_1)
# plot_weekday_analysis(dates_2)
# plot_weekday_analysis(dates_2, diff=dates_1)

# plot_weeknumber_over_year_analysis(dates)
# plot_weeknumber_over_year_analysis(dates_2, diff=dates_1)

plot_year_analysis(dates, day_count_tests=[lambda c: c == 0])

# days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
# all_dates = [
#     (year, month, day)
#     for year in [2022, 2023, 2024]
#     for month, count in enumerate(days_in_month, start=1)
#     for day in range(1, count + 1 - int(year != 2024 and month == 2))
# ]
# observe_dates = all_dates[261:-104]
# buckets = {}
# for y, m, d in observe_dates:
#     if (m, d) not in buckets:
#         buckets[m, d] = []
#     buckets[m, d].append(y)
# for (m, d), ys in buckets.items():
#     if len(ys) == 1:
#         assert (m, d) == (1, 29)
#         continue
#     y1, y2 = ys
#     d1 = datetime.datetime(y1, m, d)
#     d2 = datetime.datetime(y2, m, d)
#     if d1.weekday() >= 5 and d2.weekday() >= 5:
#         print(m, d, y1, y2, d1.weekday(), d2.weekday())

# plot_year_analysis(dates_1, day_count_tests=[lambda c: c >= 20])
# plot_year_analysis(dates_2, day_count_tests=[lambda c: c >= 20])
# plot_year_analysis(dates_2, diff=dates_1)

# plot_year_analysis(dates_1_missing, named="2022-2023_missing")
# plot_year_analysis(dates_1_steffan_missing, named="2022-2023_steffan_missing")
# plot_year_analysis(dates_1_steffan_not_missing, named="2022-2023_steffan_not_missing")
# plot_year_analysis(dates_1_steffan_not_missing, diff=dates_1_steffan_missing, named="2022-2023_steffan_diff")

# plot_year_analysis(dates_lasse)

plot_weekday_and_month_side_by_side(dates_1, dates_2)
# plot_weekday_hour_on_top(dates_1, dates_2)
plot_weekday_hour_super_imposed(dates_1, dates_2)

plot_count_days_with_certain_pings(dates)

# plot_cummulative_year_analysis(dates)
# plot_cummulative_year_analysis(dates_steffan, named="Steffan")
plot_double_cummulative_year_analysis(dates, dates_steffan, "Steffan")
# steffan_count = len(dates_steffan)
# year_dates = 365 + 366
# was_gone = 17 + 30 + 31 + 30 + 31 + 1
# pings_pr_present_day = steffan_count / (year_dates - was_gone)
# missing_pings = pings_pr_present_day * was_gone
# print(steffan_count, pings_pr_present_day, was_gone, missing_pings)
# plot_cummulative_year_analysis(dates_lasse, named=Lasse)
# plot_cummulative_year_analysis(dates_casper, named=Casper)
# plot_cummulative_year_analysis(dates_louise, named=Louise)
# plot_cummulative_year_analysis(dates_andreas, named=Andreas)

# plot_group_graf_relation(unix_time_with_sender, anonymous=False)
plot_group_graf_relation(unix_time_with_sender, anonymous=True)

# plot_group_sizes()
# plot_people_count()
# plot_people_count_time_sensitive()
