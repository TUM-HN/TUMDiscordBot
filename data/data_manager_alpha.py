"""
Alpha version of the data manager, currently is not automated.

:copyright: (c) 2023-present Ivan Parmacli
:license: MIT, see LICENSE for more details.
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

very_easy = "Very Easy"
very_hard = "Very Hard"


def plot_intermediate_exam_difficulty_results():
    very_easy_entries = 0
    easy_entries = 0
    medium_entries = 0
    hard_entries = 0
    very_hard_entries = 0
    labels = []
    sizes = []
    sutdents_percentage = 0

    with open(
        file="./data/exercise_feedback/FileName.csv",
        mode="r",
        newline="",
    ) as csvfile:
        lines = csvfile.readlines()
        for line in lines:
            if very_easy in line:
                very_easy_entries += 1
            if "Easy" in line and very_easy not in line:
                easy_entries += 1
            if "Medium" in line:
                medium_entries += 1
            if "Hard" in line and very_hard not in line:
                hard_entries += 1
            if very_hard in line:
                very_hard_entries += 1

    if very_easy_entries != 0:
        sizes.append(round(float(very_easy_entries / sutdents_percentage), 2))
        labels.append(very_easy)
    if easy_entries != 0:
        sizes.append(round(float(easy_entries / sutdents_percentage), 2))
        labels.append("Easy")
    if medium_entries != 0:
        sizes.append(round(float(medium_entries / sutdents_percentage), 2))
        labels.append("Medium")
    if hard_entries != 0:
        sizes.append(round(float(hard_entries / sutdents_percentage), 2))
        labels.append("Hard")
    if very_hard_entries != 0:
        sizes.append(round(float(very_hard_entries / sutdents_percentage), 2))
        labels.append(very_hard)

    fig, ax1 = plt.subplots(figsize=(9, 7), layout="constrained")
    fig.canvas.manager.set_window_title("Intermediate Exam Survey")

    ax1.set_xlabel("Percentage of Students")

    test_names = labels
    percentiles = sizes

    rects = ax1.barh(test_names, percentiles, align="center", height=0.5)
    ax1.bar_label(
        rects,
        sizes,
        padding=5,
        color="black",
        fontweight="bold",
    )

    ax1.set_xlim([0, 50])
    ax1.set_xticks(
        [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
        ["0%", "5%", "10%", "15%", "20%", "25%", "30%", "35%", "40%", "45%", "50%"],
    )
    ax1.xaxis.grid(True, linestyle="--", which="major", color="grey", alpha=0.25)
    ax1.axvline(50, color="grey", alpha=0.25)  # median position


def plot_intermediate_exam_score_results():
    score_40 = 0
    score_60 = 0
    score_80 = 0
    score_100 = 0
    labels = []
    sizes = []
    sutdents_percentage = 0

    with open(
        file="./data/exercise_feedback/FileName.csv",
        mode="r",
        newline="",
    ) as csvfile:
        lines = csvfile.readlines()
        for line in lines:
            if "40%" in line:
                score_40 += 1
            if "60%" in line:
                score_60 += 1
            if "80%" in line:
                score_80 += 1
            if "100" in line:
                score_100 += 1

    if score_40 != 0:
        sizes.append(round(float(score_40 / sutdents_percentage), 2))
        labels.append("40-60")
    if score_60 != 0:
        sizes.append(round(float(score_60 / sutdents_percentage), 2))
        labels.append("60-80")
    if score_80 != 0:
        sizes.append(round(float(score_80 / sutdents_percentage), 2))
        labels.append("80-100")
    if score_100 != 0:
        sizes.append(round(float(score_100 / sutdents_percentage), 2))
        labels.append("100")

    fig, ax1 = plt.subplots(figsize=(9, 7), layout="constrained")
    fig.canvas.manager.set_window_title("Intermediate Exam Survey Score")

    ax1.set_xlabel("Percentage of Students")

    test_names = labels
    percentiles = sizes

    rects = ax1.barh(test_names, percentiles, align="center", height=0.5)
    ax1.bar_label(
        rects,
        sizes,
        padding=5,
        color="black",
        fontweight="bold",
    )

    ax1.set_xlim([0, 46])
    ax1.set_xticks(
        [0, 5, 10, 15, 20, 25, 30, 35, 40, 45],
        ["0%", "5%", "10%", "15%", "20%", "25%", "30%", "35%", "40%", "45%"],
    )
    ax1.xaxis.grid(True, linestyle="--", which="major", color="grey", alpha=0.25)
    ax1.axvline(50, color="grey", alpha=0.25)  # median position


def plot_lectures_results():
    very_easy_entries = [0] * 10
    easy_entries = [0] * 10
    medium_entries = [0] * 10
    hard_entries = [0] * 10
    very_hard_entries = [0] * 10
    files_list = [
        "./data/exercise_feedback/FileName.csv",
        "./data/exercise_feedback/FileName.csv",
        "./data/exercise_feedback/FileName.csv",
        "./data/exercise_feedback/FileName.csv",
        "./data/exercise_feedback/FileName.csv",
        "./data/exercise_feedback/FileName.csv",
        "./data/exercise_feedback/FileName.csv",
        "./data/exercise_feedback/FileName.csv",
        "./data/exercise_feedback/FileName.csv",
        "./data/exercise_feedback/FileName.csv",
    ]
    sizes = [[], [], [], [], [], [], [], [], [], []]
    difficulties = (very_easy, "Easy", "Medium", "Hard", very_hard)
    difficulty_dict = {}

    i = 0
    while i < 10:
        with open(
            file=files_list[i],
            mode="r",
            newline="",
        ) as csvfile:
            lines = csvfile.readlines()
            for line in lines:
                if very_easy in line:
                    very_easy_entries[i] += 1
                if "Easy" in line and very_easy not in line:
                    easy_entries[i] += 1
                if "Medium" in line:
                    medium_entries[i] += 1
                if "Hard" in line and very_hard not in line:
                    hard_entries[i] += 1
                if very_hard in line:
                    very_hard_entries[i] += 1

        sizes[i].append(very_easy_entries[i])
        sizes[i].append(easy_entries[i])
        sizes[i].append(medium_entries[i])
        sizes[i].append(hard_entries[i])
        sizes[i].append(very_hard_entries[i])
        difficulty_dict.update(
            {
                "Lecture "
                + str(i): (
                    sizes[i][0],
                    sizes[i][1],
                    sizes[i][2],
                    sizes[i][3],
                    sizes[i][4],
                )
            }
        )
        i += 1

    x = np.array([6, 12, 18, 24, 30])  # the label locations
    width = 0.5  # the width of the bars
    multiplier = -2.5

    fig, ax = plt.subplots()

    for label, measurement in difficulty_dict.items():
        rects = ax.bar(x + multiplier, measurement, width, label=label)
        # ax.bar_label(rects, padding=3)
        multiplier += 0.5

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel("Number of Students")
    ax.set_xlabel("Difficulty")
    ax.legend(
        [
            "Lecture 1",
            "Lecture 2",
            "Lecture 3",
            "Lecture 4",
            "Lecture 5",
            "Lecture 6",
            "Lecture 7",
            "Lecture 8",
            "Lecture 9",
            "Lecture 10",
        ]
    )
    ax.set_xticks(x, difficulties)
    ax.set_ylim(0, 20)
    ax.set_xlim(0, 35)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))


def plot_quiz_results():
    very_easy_entries = [0] * 10
    easy_entries = [0] * 10
    medium_entries = [0] * 10
    hard_entries = [0] * 10
    very_hard_entries = [0] * 10
    files_list = [
        "./data/exercise_feedback/FileName.csv",
        "./data/exercise_feedback/FileName.csv",
        "./data/exercise_feedback/FileName.csv",
        "./data/exercise_feedback/FileName.csv",
        "./data/exercise_feedback/FileName.csv",
        "./data/exercise_feedback/FileName.csv",
        "./data/exercise_feedback/FileName.csv",
        "./data/exercise_feedback/FileName.csv",
        "./data/exercise_feedback/FileName.csv",
        "./data/exercise_feedback/FileName.csv",
    ]
    sizes = [[], [], [], [], [], [], [], [], [], []]
    difficulties = (very_easy, "Easy", "Medium", "Hard", very_hard)
    difficulty_dict = {}

    i = 0
    while i < 10:
        with open(
            file=files_list[i],
            mode="r",
            newline="",
        ) as csvfile:
            lines = csvfile.readlines()
            for line in lines:
                if very_easy in line:
                    very_easy_entries[i] += 1
                if "Easy" in line and very_easy not in line:
                    easy_entries[i] += 1
                if "Medium" in line:
                    medium_entries[i] += 1
                if "Hard" in line and very_hard not in line:
                    hard_entries[i] += 1
                if very_hard in line:
                    very_hard_entries[i] += 1

        sizes[i].append(very_easy_entries[i])
        sizes[i].append(easy_entries[i])
        sizes[i].append(medium_entries[i])
        sizes[i].append(hard_entries[i])
        sizes[i].append(very_hard_entries[i])
        difficulty_dict.update(
            {
                "Lecture "
                + str(i): (
                    sizes[i][0],
                    sizes[i][1],
                    sizes[i][2],
                    sizes[i][3],
                    sizes[i][4],
                )
            }
        )
        i += 1

    x = np.array([6, 12, 18, 24, 30])  # the label locations
    width = 0.5  # the width of the bars
    multiplier = -2.5

    fig, ax = plt.subplots()

    for label, measurement in difficulty_dict.items():
        rects = ax.bar(x + multiplier, measurement, width, label=label)
        # ax.bar_label(rects, padding=3)
        multiplier += 0.5

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel("Number of Students")
    ax.set_xlabel("Difficulty")
    ax.legend(
        [
            "Quiz 1",
            "Quiz 2",
            "Quiz 3",
            "Quiz 4",
            "Quiz 5",
            "Quiz 6",
            "Quiz 7",
            "Quiz 8",
            "Quiz 9",
            "Quiz 10",
        ]
    )
    ax.set_xticks(x, difficulties)
    ax.set_ylim(0, 20)
    ax.set_xlim(0, 35)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))


def plot_real_exam_results():
    score_100 = 0
    score_80_100 = 0
    score_60_80 = 0
    score_40_60 = 0
    score_lower_than_40 = 0
    number_of_students_percentage = 0
    labels = []
    percentage_of_students = []

    with open(
        file="./data/exercise_feedback/FileName.csv",
        mode="r",
        newline="",
    ) as csvfile:
        lines = csvfile.readlines()
        for line in lines:
            if line.split(",")[1] == "Overall Exam Points\r\n":
                continue
            points = float(line.split(",")[1].replace("\r\n", ""))
            if points == 100:
                score_100 += 1
            else:
                if points > 80 or points == 80:
                    score_80_100 += 1
                else:
                    if points > 60 or points == 60:
                        score_60_80 += 1
                    else:
                        if points > 40 or points == 40:
                            score_40_60 += 1
                        else:
                            score_lower_than_40 += 1

    if score_100 != 0:
        labels.append("100")
        percentage_of_students.append(
            round(float(score_100 / number_of_students_percentage), 2)
        )
    if score_80_100 != 0:
        labels.append("80-100")
        percentage_of_students.append(
            round(float(score_80_100 / number_of_students_percentage), 2)
        )
    if score_60_80 != 0:
        labels.append("60-80")
        percentage_of_students.append(
            round(float(score_60_80 / number_of_students_percentage), 2)
        )
    if score_40_60 != 0:
        labels.append("40-60")
        percentage_of_students.append(
            round(float(score_40_60 / number_of_students_percentage), 2)
        )
    if score_lower_than_40 != 0:
        labels.append("<40")
        percentage_of_students.append(
            round(float(score_lower_than_40 / number_of_students_percentage), 2)
        )

    labels.reverse()
    percentage_of_students.reverse()

    fig, ax1 = plt.subplots(figsize=(9, 7), layout="constrained")
    fig.canvas.manager.set_window_title("Intermediate Exam Real Results")

    ax1.set_xlabel("Percentage of Students")
    ax1.set_ylabel("Overall Exam Points")

    rects = ax1.barh(labels, percentage_of_students, align="center", height=0.5)
    ax1.bar_label(
        rects,
        percentage_of_students,
        padding=5,
        color="black",
        fontweight="bold",
    )

    ax1.set_xlim([0, 35])
    ax1.set_xticks([0, 5, 10, 15, 20, 30], ["0%", "5%", "10%", "15%", "20%", "30%"])
    ax1.xaxis.grid(True, linestyle="--", which="major", color="grey", alpha=0.25)
    ax1.axvline(50, color="grey", alpha=0.25)  # median position


# plot_intermediate_exam_difficulty_results()
# plot_intermediate_exam_score_results()
# plot_lectures_results()
# plot_quiz_results()
# plot_real_exam_results()
# plt.ylabel("Expected Score", fontsize=15)
# plt.xlabel("Percentage of Students", fontsize=15)
plt.yticks(fontsize=15)
plt.xticks(fontsize=15)
plt.show()
