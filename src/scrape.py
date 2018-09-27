# Scrapes HLTV rankings
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

import datetime as dt
import subprocess
import pandas as pd
from bs4 import BeautifulSoup

base_url = 'https://www.hltv.org/ranking/teams/'
dates = []
teams = dict()

# human readable mapping from aligned dates to actual dates in hltv
dates_map = {
    '2015-09-28': '2015-10-01',
    '2015-11-02': '2015-11-03',
    '2015-11-23': '2015-11-24',
    '2015-11-30': '2015-12-01',
}

# mapping in the datetime format
fix_dates = {
        dt.datetime.fromisoformat(k): dt.datetime.fromisoformat(dates_map[k])
        for k in dates_map
}


def process_page(date, soup):
    names = soup.find_all(class_='name')
    points = soup.find_all(class_='points')

    new_names = []
    new_points = []

    for name in names:
        new_names.append(name.text)

    for point in points:
        new_points.append(point.text.replace('(', '').replace(' points)', ''))

    dates.append(date)

    for i, name in enumerate(new_names):
        if name not in teams:
            teams[name] = dict()

        teams[name][date] = new_points[i]


def get_page_soup(date):
    print('Getting data for %s' % (date))
    url = base_url + str(date.year) + '/' + date.strftime("%B").lower() + '/' + str(date.day)

    p = subprocess.run(['curl', url], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    page = p.stdout
    soup = BeautifulSoup(page, 'html.parser')

    return soup


def make_df():
    df = pd.DataFrame(index=dates, columns=[k for k in teams])

    for i, date in enumerate(dates):
        for team in teams:
            if date in teams[team]:
                df.at[date, team] = teams[team][date]

    return df


def write_file(df):
    df.to_pickle('../data/data.pkl')
    df.to_csv('../data/data.csv')


def main():
    prev = dt.datetime.fromisoformat('2015-09-28')
    # end = datetime.datetime.fromisoformat('2018-09-24')
    end = dt.datetime.fromisoformat('2015-12-01')

    # d = dict()

    while (prev <= end):
        adjust_date = prev

        if prev in fix_dates:
            adjust_date = fix_dates[prev]

        soup = get_page_soup(adjust_date)
        process_page(adjust_date, soup)

        week_after = prev + dt.timedelta(days=7)
        prev = week_after

    df = make_df()
    write_file(df)


if __name__ == '__main__':
    main()
