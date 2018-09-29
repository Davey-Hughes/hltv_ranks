# HLTV World Rankings Plotter

<img src="https://media.githubusercontent.com/media/Davey-Hughes/hltv_ranks_pandas/master/plots/plot_ranks.png" width="1000"/>

## Depreciation
This repo will be reimplemented by storing the data scraped from HLTV in a
database. This should make performing analysis on information besides the world
rankings much easier once a local database has been built.

## Usage
```
python3 src/scrape.py
```
will scrape the world rankings data from HLTV and store the output in both a
csv and pickled pandas data frame in the data directory. They will overwrite
the data files currently in the data directory.

```
python3 src/plot.py plot_type
```
plot\_type can be either 'points' or 'ranks'. 'points' graphs each team's rank
from the points system HLTV uses to derive the ranking. 'ranks' will graph the
top 30 teams.

## Limitations
### Data Culling
Because of the amount of data and the fact that many teams have come into the
HLTV top rankings for only brief periods at a time, the current plotting method
culls a lot of the data. For the points plot, this means that only teams who
have appeared in at least 1/2 of HLTVs world rankings will be plotted. For the
ranks plot, only teams who have at least made the top 5 will be displayed.

### Team Continuity
Often is the case in Counter Strike where the core (or entirety) of a team
changes their team name or moves to a different organization. It would be
reasonable, then, for the lines from these two teams to be connected, however
currently this is not the case. A mapping from a previous team name to the
current team name could be constructed manually, as would be the case for TSM
-> ? -> Astralis, however since in many cases it is important to know the date
the team members changed (LG -> SK -> MiBR), this would also have to be taken
into account.

## Data Display
Currently the colors are random, and only the teams who are in the most recent
HLTV top rankings (and who pass the culling parameters) will be labeled.
Ideally the lines should be the same as the team's primary color (or the line
could have a stroke with the team's secondary color), but that will come with
either a manual mapping or another scraping tool that gets information from the
team's logos stored on HLTV.

### Future
Ideally this kind of plot would be somewhat interactive so that it could be
more easy to follow particular lines when exploring with the mouse. This would
make it much easier to read exact values and follow the path of a particular
team over time. The likely solution to this is to use plotly instead of
Matplotlib, which currently is slated for future development.

Further, an option to simply update the current data files rather than re-scrape
the entirety of HLTVs rankings should be added. This, in addition to being able
to scrape regional rankings as well should not be too difficult to add.
