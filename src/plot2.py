import os
import sys

import pandas as pd
import plotly as py
import plotly.graph_objs as go
from plotly.offline import plot


# globals
plot_type = None
plot_file = None
df_file = None
layout = None


def main():
    if len(sys.argv) < 2:
        print('Must specify whether plotting points or rank')
        return

    plot_type = sys.argv[1]
    # default values are for points
    if sys.argv[1] == 'points':
        plot_file = '../plots/plot_points.html'
        df_file = '../data/data_points.pkl'
    elif sys.argv[1] == 'ranks':
        plot_file = '../plots/plot_ranks.html'
        df_file = '../data/data_ranks.pkl'

    script_path = os.path.abspath(os.path.dirname(__file__))
    df = pd.read_pickle(os.path.join(script_path, df_file))

    teams = list(df.columns.values)
    dates = pd.DatetimeIndex(list(df.index.values))

    data = []

    for team in teams:
        ys = list(df[team].values)
        team_plot = go.Scatter(
            x=dates,
            y=ys,
            name=team
        )

        data.append(team_plot)

    if plot_type == 'points':
        layout = go.Layout()
    elif plot_type == 'ranks':
        layout = go.Layout(
            yaxis=dict(
                autorange='reversed'
            )
        )

    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename=plot_file)


if __name__ == '__main__':
    main()
