import io
import itertools
import time
import zipfile
from datetime import datetime

import pandas as pd

from timer import measure


def custom_date_parser(x):
    return datetime.strptime(x, '%Y-%m-%d %H:%M:%S')


start = time.time()
TABLE_BETS = pd.read_csv(io.StringIO(zipfile.ZipFile('data.zip', 'r').read('data.csv').decode('utf-8')), parse_dates=['starts', 'timestamp'], date_parser=custom_date_parser)
print(f"Data successfully loaded in {time.time() - start} seconds.")


@measure
def get_max_starts():
    """ Returns starts of the latest fixture """

    return TABLE_BETS['starts'].max()


@measure
def get_total_bets():
    """ Returns total number of bets """

    return TABLE_BETS['id'].count()


@measure
def get_unique_sports():
    """ Returns a set of distinct sports """

    return set(TABLE_BETS['sport'].unique())


@measure
def get_unique_books():
    """ Returns a set of distinct books """

    return set(TABLE_BETS['book'].unique())


@measure
def get_unique_countries():
    """ Returns a set of distinct countries """

    return set(TABLE_BETS['country'].unique())


@measure
def get_unique_leagues():
    """ Returns a set of distinct leagues """

    return set(TABLE_BETS['league'].unique())


@measure
def get_bets(min_val: float, odds_range: list, books: list, sports: list, countries: list, leagues: list):
    """ Returns all bets """

    return TABLE_BETS[(TABLE_BETS['value'] >= min_val) & (TABLE_BETS['odds'] >= odds_range[0]) & (TABLE_BETS['odds'] <= odds_range[1]) & (TABLE_BETS['book'].isin(books)) & (TABLE_BETS['sport'].isin(sports)) & (TABLE_BETS['country'].isin(countries)) & (TABLE_BETS['league'].isin(leagues))].to_records(index=False)


@measure
def get_monthly_stats(year: int, month: int, min_val: float, odds_range: list, books: list, sports: list, countries: list, leagues: list):
    """ Returns cumulative data for the specified year and month """

    subset = TABLE_BETS[(TABLE_BETS['starts'].dt.year == year) & (TABLE_BETS['starts'].dt.month == month) & (TABLE_BETS['value'] >= min_val) & (TABLE_BETS['odds'] >= odds_range[0]) & (TABLE_BETS['odds'] <= odds_range[1]) & (TABLE_BETS['book'].isin(books)) & (TABLE_BETS['sport'].isin(sports)) & (TABLE_BETS['country'].isin(countries)) & (TABLE_BETS['league'].isin(leagues))]
    return subset['id'].count(), subset['odds'].mean(), subset['profit'].sum(), subset['clv'].mean()


@measure
def get_total_averages(min_val: float, odds_range: list, books: list, sports: list, countries: list, leagues: list):
    """ Returns total cumulative data """

    subset = TABLE_BETS[(TABLE_BETS['value'] >= min_val) & (TABLE_BETS['odds'] >= odds_range[0]) & (TABLE_BETS['odds'] <= odds_range[1]) & (TABLE_BETS['book'].isin(books)) & (TABLE_BETS['sport'].isin(sports)) & (TABLE_BETS['country'].isin(countries)) & (TABLE_BETS['league'].isin(leagues))]
    return subset['odds'].mean(), subset['clv'].mean()


@measure
def get_accumulated_profits(min_val: float, odds_range: list, books: list, sports: list, countries: list, leagues: list):
    """ Returns accumulated profit for each bet as a list in chronological order """

    profits, clvs = list(), list()
    subset = TABLE_BETS[(TABLE_BETS['value'] >= min_val) & (TABLE_BETS['odds'] >= odds_range[0]) & (TABLE_BETS['odds'] <= odds_range[1]) & (TABLE_BETS['book'].isin(books)) & (TABLE_BETS['sport'].isin(sports)) & (TABLE_BETS['country'].isin(countries)) & (TABLE_BETS['league'].isin(leagues))]
    for data in zip(subset['profit'].tolist(), subset['clv'].tolist()):
        profits.append(data[0]) if data[0] is not None else profits.append(0)
        clvs.append(data[1]) if data[1] is not None else profits.append(0)

    accumulated_data = list()
    for profit, clv in zip(list(itertools.accumulate(profits)), list(itertools.accumulate(clvs))):
        accumulated_data.append([profit, clv])

    return accumulated_data
