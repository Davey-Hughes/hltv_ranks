# Plots HLTV world rankings over time
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

import matplotlib.pyplot as plt
import pandas as pd


def main():
    df = pd.read_pickle("../data/data.pkl")
    teams = list(df.columns.values)
    dates = list(df.index.values)

    # plot dimensions
    plt.figure(figsize=(40, 40))

    # remove frame lines
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    # show ticklines at left and bottom only
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    # plot axis limits
    plt.ylim(0, 1000)
    plt.xlim(df.first_valid_index(), df.last_valid_index())

    plt.yticks(range(0, 910, 100), [str(x) for x in range(0, 910, 100)], fontsize=28)
    plt.xticks(fontsize=28)

    plt.tick_params(axis="both", which="both", bottom=False, top=False,
                    labelbottom=True, left=False, right=True, labelleft=True)

    for i, team in enumerate(teams):
        ys = list(map(int, (df[team].fillna(0).values)))
        plt.plot(dates, ys, lw=2.5, color='#000000')

    plt.savefig('../plots/plot.png')


if __name__ == '__main__':
    main()
