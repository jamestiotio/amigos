#!/usr/bin/python3
# -*- coding: utf-8 -*-

import seaborn as sns
from typing import Dict, List


def plot_groups(
    teams: Dict[str, Dict[str, List[int]]],
    course_option: str = "",
    outfile: str = "output.png",
):
    sns.set_theme(style="darkgrid")
    x = [
        len(j)
        for cohort in [i.items() for i in list(teams.values())]
        for _, j in cohort
    ]
    ax = sns.countplot(x=x, palette=sns.color_palette(palette="bright", n_colors=3))
    ax.set(xlabel="Number of team members", ylabel="Number of groups")
    ax.set(ylim=(0, 65))

    if course_option == "DESIGN":
        ax.set_title("Plot for 03.007 Introduction to Design", weight="bold")
    elif course_option == "DW":
        ax.set_title("Plot for 10.009 The Digital World", weight="bold")
    else:
        ax.set_title("Plot for xx.xxx Course Title/Name", weight="bold")

    ax.get_figure().savefig(outfile)