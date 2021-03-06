# Scrapes HLTV world rankings
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

import datetime
import subprocess
import queue
import threading
import os

import pandas as pd
from bs4 import BeautifulSoup


# globals
num_threads = 8

base_url = 'https://www.hltv.org/ranking/teams/'
dates = []
teams = dict()
teams_lock = threading.Lock()

dates_queue = queue.Queue()
queue_lock = threading.Lock()


# human readable mapping from aligned dates to actual dates in hltv
dates_map = {
    '2015-09-28': '2015-10-01',
    '2015-11-02': '2015-11-03',
    '2015-11-23': '2015-11-24',
    '2015-11-30': '2015-12-01',
    '2015-12-07': '2015-12-08',
    '2016-01-04': '2016-01-05',
    '2016-02-08': '2016-02-09',
    '2016-02-29': '2016-03-01',
    '2016-04-04': '2016-04-05',
    '2016-04-17': '2016-04-18',
    '2016-05-16': '2016-05-17',
    '2016-05-30': '2016-06-01',
    '2016-06-20': '2016-06-21',
    '2016-07-18': '2016-07-19',
    '2016-07-25': '2016-07-26',
    '2016-10-31': '2016-11-01',
    '2018-01-15': '2018-01-16',
    '2018-01-22': '2018-01-23',
}

# mapping in the datetime format
fix_dates = {
        datetime.datetime.fromisoformat(k): datetime.datetime.fromisoformat(dates_map[k])
        for k in dates_map
}


class MyThread(threading.Thread):
    def __init__(self, threadid):
        threading.Thread.__init__(self)
        self.threadid = threadid

    def run(self):
        threadWork()


# task for each thread
def threadWork():
    while True:
        queue_lock.acquire()
        try:
            date = dates_queue.get(timeout=.001)
        except:
            queue_lock.release()
            break

        queue_lock.release()

        soup = get_page_soup(date)
        process_page(date, soup)


# parse page for team name, rank, and points
def process_page(date, soup):
    names = soup.find_all(class_='name')
    points = soup.find_all(class_='points')

    new_names = []
    new_points = []

    for name in names:
        new_names.append(name.text)

    for point in points:
        new_points.append(int(point.text.replace('(', '').replace(' points)', '')))

    teams_lock.acquire()
    for i, name in enumerate(new_names):
        if name not in teams:
            teams[name] = dict()

        teams[name][date] = [i + 1, new_points[i]]
    teams_lock.release()


# fetch page source for a given date
def get_page_soup(date):
    print('Getting data for %s-%s-%s' % (date.year, date.month, date.day))
    url = base_url + str(date.year) + '/' + date.strftime("%B").lower() + '/' + str(date.day)

    p = subprocess.run(['curl', url],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.DEVNULL)

    page = p.stdout
    soup = BeautifulSoup(page, 'html.parser')

    return soup


# make dataframe from scraped data
def make_df():
    # lock not required here because all threads have been joined by this point
    df_points = pd.DataFrame(index=dates, columns=[k for k in teams])
    df_ranks = pd.DataFrame(index=dates, columns=[k for k in teams])

    for i, date in enumerate(dates):
        for team in teams:
            if date in teams[team]:
                df_points.at[date, team] = teams[team][date][1]
                df_ranks.at[date, team] = teams[team][date][0]

    return df_points, df_ranks


# write dataframes to file
def write_file(df_p, df_r):
    script_path = os.path.abspath(os.path.dirname(__file__))

    df_p.to_pickle(os.path.join(script_path, '../data/data_points.pkl'))
    df_p.to_csv(os.path.join(script_path, '../data/data_points.csv'))

    df_r.to_pickle(os.path.join(script_path, '../data/data_ranks.pkl'))
    df_r.to_csv(os.path.join(script_path, '../data/data.ranks.csv'))


def main():
    threads = []
    fin_threads = []

    prev = datetime.datetime.fromisoformat('2015-09-28')
    end = datetime.datetime.now()

    # generate all dates
    while (prev <= end):
        adjust_date = prev
        if prev in fix_dates:
            adjust_date = fix_dates[prev]

        dates.append(adjust_date)

        week_after = prev + datetime.timedelta(days=7)
        prev = week_after

    # create queue of dates we want to scrape
    for date in dates:
        dates_queue.put(date)

    # launch threads
    for i in range(num_threads):
        thread = MyThread(i)
        thread.start()
        threads.append(thread)

    # wait for threads
    for t in threads:
        queue_lock.acquire()
        if dates_queue.empty():
            try:
                queue_lock.release()
                t.join(timeout=20)
                fin_threads.append(t)
            except:
                pass
        else:
            queue_lock.release()
            t.join()
            fin_threads.append(t)

    # make sure threads have all exited
    for t in threads:
        if t not in fin_threads:
            print("Warning, the following threads haven't exited:")
            for t in threads:
                if t not in fin_threads:
                    print(t.threadid)
            break

    # make and write dataframe
    df_p, df_r = make_df()
    write_file(df_p, df_r)


if __name__ == '__main__':
    main()
