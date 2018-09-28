# Plots HLTV world rankings (by points) over time
# Copyright (C) 2018  David Hughes

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# globals
fontsize = 56
max_rank = 31

plot_type = None
y_max = None
y_iter = None
plot_file = None
df_file = None


def main():
    if len(sys.argv) < 2:
        print('Must specify whether plotting points or rank')
        return

    plot_type = sys.argv[1]
    # default values are for points
    if sys.argv[1] == 'points':
        y_max = 1100
        y_iter = 100
        plot_file = '../plots/plot_points.png'
        df_file = '../data/data_points.pkl'
    elif sys.argv[1] == 'ranks':
        y_max = max_rank
        y_iter = 1
        plot_file = '../plots/plot_ranks.png'
        df_file = '../data/data_ranks.pkl'

    script_path = os.path.abspath(os.path.dirname(__file__))
    df = pd.read_pickle(os.path.join(script_path, df_file))

    teams = list(df.columns.values)
    dates = pd.DatetimeIndex(list(df.index.values))

    # plot dimensions
    plt.figure(figsize=(400, 80), dpi=40)

    # remove frame lines
    ax = plt.subplot(111)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # show ticklines at left and bottom only
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    first = df.first_valid_index()
    last = df.last_valid_index()

    # plot axis limits
    plt.ylim(0, y_max - y_iter)
    plt.xlim(first, last)

    date_range = pd.date_range(first, last)
    # date_range_month = pd.date_range(first, last, freq='MS')
    date_range_month = [d for i, d in enumerate(dates) if not i % 4]

    for y in range(y_iter, y_max, y_iter):
        plt.plot(date_range, [y] * len(date_range),
                 '--', lw=5, color='black', alpha=0.3)

    # y-axis ticks
    plt.yticks(range(y_iter, y_max, y_iter),
               [str(x) for x in range(y_iter, y_max, y_iter)],
               fontsize=fontsize)
    plt.xticks(date_range_month,
               ['%s-%s-%d' % (t.year, t.month, t.day) for t in date_range_month],
               fontsize=fontsize, rotation='vertical')

    plt.tick_params(axis='both', which='both', bottom=False, top=False,
                    labelbottom=True, left=False, right=True, labelleft=True)

    # add padding for tick labels
    if plot_type == 'points':
        plt.tick_params(axis='y', pad=25)
    elif plot_type == 'ranks':
        plt.tick_params(axis='both', pad=25)

    # draw lines for each team
    for i, team in enumerate(teams):
        # cull teams that have showed up for less than half of the hltv
        # rankings history
        if plot_type == 'points' and len(df[team].dropna()) < len(dates) / 2:
            continue
        elif plot_type == 'ranks' and min(df[team].dropna()) > 5:
            continue

        ys = list(df[team].values)
        plt.plot(dates, ys, lw=5)

        # only show team names if they have a position at the end of the graph
        y_pos = df[team].fillna(0).values[-1]
        if y_pos > 0:
            plt.text(dates[-1] + np.timedelta64(2, 'D'),
                     y_pos,
                     team,
                     fontsize=fontsize)

    # put #1 ranking at top of y axis
    if plot_type == 'ranks':
        plt.gca().invert_yaxis()

    # export plot
    plt.savefig(os.path.join(script_path, plot_file),
                bbox_inches='tight',
                pad_inches=2.5)


if __name__ == '__main__':
    main()
