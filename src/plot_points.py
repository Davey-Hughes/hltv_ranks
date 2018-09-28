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

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# globals
fontsize = 56


def main():
    script_path = os.path.abspath(os.path.dirname(__file__))
    df = pd.read_pickle(os.path.join(script_path, '../data/data.pkl'))

    teams = list(df.columns.values)
    dates = list(df.index.values)

    # plot dimensions
    plt.figure(figsize=(200, 80), dpi=100)

    # remove frame lines
    ax = plt.subplot(111)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # show ticklines at left and bottom only
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    # plot axis limits
    plt.ylim(0, 1000)
    plt.xlim(df.first_valid_index(), df.last_valid_index())

    first = df.first_valid_index()
    last = df.last_valid_index()

    date_range = pd.date_range(first, last)

    for y in range(0, 1100, 100):
        plt.plot(date_range, [y] * len(date_range),
                 '--', lw=5, color='black', alpha=0.3)

    # y axis ticks
    plt.yticks(range(100, 1100, 100),
               [str(x) for x in range(100, 1100, 100)],
               fontsize=fontsize)
    plt.xticks(fontsize=fontsize)

    plt.tick_params(axis='both', which='both', bottom=False, top=False,
                    labelbottom=True, left=False, right=True, labelleft=True)

    # draw lines for each team
    for i, team in enumerate(teams):
        ys = list(map(int, (df[team].fillna(0).values)))
        plt.plot(dates, ys, lw=5)

        y_pos = int(df[team].fillna(0).values[-1])
        plt.text(dates[-1] + np.timedelta64(2, 'D'),
                 y_pos,
                 team,
                 fontsize=fontsize)

    plt.savefig(os.path.join(script_path, '../plots/plot_points.png'),
                bbox_inches='tight',
                pad_inches=2.5)


if __name__ == '__main__':
    main()
