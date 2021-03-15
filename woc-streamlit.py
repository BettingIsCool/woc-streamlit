import calendar

import pandas as pd
import streamlit as st

import db
from increments import ODDS_INCREMENTS

# Title
st.title('The Wisdom Of The Crowd')
st.markdown("""
by Joseph Buchdahl [@12Xpert](https://twitter.com/12xpert?lang=en)
* This web app illustrates the performance of the #WisdomOfTheCrowd betting strategy applied to 50+ bookmakers and multiple sports.
* The Wisdom Of The Crowd is a robust method in order to gain long-term betting profits and was first introduced by Joseph Buchdahl [@12Xpert](https://twitter.com/12xpert?lang=en)
* The method is built on the idea of efficient market hypothesis which is commonly used in financial economics.
* Sports betting analyst Joseph Buchdahl did a fantastic 20-page article explaining the approach in detail here https://www.football-data.co.uk/The_Wisdom_of_the_Crowd_updated.pdf
* **This app shows historical bets only.** Bets can be received in real-time (via e-mail). If you're interested please visit https://bettingiscool.com/the-wisdom-of-the-crowd/ and contact me at **contact@bettingiscool.com**
""")

# Filters
st.sidebar.header('User Input Features')

min_val = st.sidebar.slider(label='Minimum Value', min_value=0.00, max_value=0.25, value=0.05, step=0.01, format='%f')
odds_range = st.sidebar.select_slider(label='Odds Range', options=ODDS_INCREMENTS, value=[1.01, 1000])

unique_books = list(db.get_unique_books())
selected_books = st.sidebar.multiselect(label='Books', options=sorted(unique_books), default='BET365')
unique_sports = list(db.get_unique_sports())
selected_sports = st.sidebar.multiselect(label='Sports', options=sorted(unique_sports), default=unique_sports)
unique_countries = list(db.get_unique_countries())
selected_countries = st.sidebar.multiselect(label='Countries', options=sorted(unique_countries), default=unique_countries)
unique_leagues = list(db.get_unique_leagues())
selected_leagues = st.sidebar.multiselect(label='Leagues', options=sorted(unique_leagues), default=unique_leagues)

if len(selected_sports) > 0 and len(selected_books) > 0 and len(selected_countries) > 0 and len(selected_leagues) > 0:

    # Display monthly stats

    st.header('Performance by month')
    data = dict()
    data.update({'YEAR': list()})
    data.update({'MONTH': list()})
    data.update({'BETS': list()})
    data.update({'AVG_ODDS': list()})
    data.update({'PROFIT': list()})
    data.update({'ROI': list()})
    data.update({'CLV': list()})

    for year in (2021, ):
        for month in range(1, 4):
            bets, avg_odds, profit, clv = db.get_monthly_stats(year=year, month=month, min_val=min_val, odds_range=odds_range, books=selected_books, sports=selected_sports, countries=selected_countries, leagues=selected_leagues)

            if bets and bets is not None and avg_odds and profit and clv:
                data['YEAR'].append(year)
                data['MONTH'].append(calendar.month_name[month])
                data['BETS'].append(bets)
                data['AVG_ODDS'].append(avg_odds)
                data['PROFIT'].append(profit)
                data['ROI'].append(profit / bets)
                data['CLV'].append(clv)

    avg_odds, clv = db.get_total_averages(min_val=min_val, odds_range=odds_range, books=selected_books, sports=selected_sports, countries=selected_countries, leagues=selected_leagues)
    if data['BETS']:
        data['YEAR'].append('ALL YEARS')
        data['MONTH'].append('ALL MONTHS')
        data['BETS'].append(sum(data['BETS']))
        data['AVG_ODDS'].append(avg_odds)
        data['PROFIT'].append(sum(data['PROFIT']))
        data['ROI'].append(sum(data['PROFIT']) / sum(data['BETS']))
        data['CLV'].append(clv)

        df_monthly = pd.DataFrame(data=data)
        st.dataframe(df_monthly.style.format({'AVG_ODDS': "{:.2f}", 'PROFIT': "{:.2f}", 'ROI': "{:.2%}", 'CLV': "{:.2%}"}))

    # Display accumulated Profits (Chart)
    st.header('Expected Profits vs Actual Profits')
    accumulated_data = db.get_accumulated_profits(min_val=min_val, odds_range=odds_range, books=selected_books, sports=selected_sports, countries=selected_countries, leagues=selected_leagues)
    chart_data = pd.DataFrame(data=accumulated_data, columns=['ACTUAL PROFITS', 'EXPECTED PROFITS'])
    st.line_chart(chart_data)

    if st.button('Selections'):
        # Display log
        data = dict()
        data.update({'STARTS': list()})
        data.update({'SPORT': list()})
        data.update({'COUNTRY': list()})
        data.update({'LEAGUE': list()})
        data.update({'RUNNER_HOME': list()})
        data.update({'RUNNER_AWAY': list()})
        data.update({'SELECTION': list()})
        data.update({'BOOK': list()})
        data.update({'ODDS_TAKEN': list()})
        data.update({'ODDS_FAIR': list()})
        data.update({'VALUE': list()})
        data.update({'BET_ADVISED': list()})
        data.update({'SCORE_HOME': list()})
        data.update({'SCORE_AWAY': list()})
        data.update({'STATUS': list()})
        data.update({'PROFIT': list()})
        data.update({'TRUE_CLS': list()})
        data.update({'CLV': list()})

        for bet in db.get_bets(min_val=min_val, odds_range=odds_range, books=selected_books, sports=selected_sports, countries=selected_countries, leagues=selected_leagues):
            db_id, fixture_id, starts, sport, country, league, runner_home, runner_away, selection, book, odds, fair_odds, value, timestamp, score_home, score_away, status, profit, true_cls, clv = bet
            data['STARTS'].append(starts)
            data['SPORT'].append(sport)
            data['COUNTRY'].append(country)
            data['LEAGUE'].append(league)
            data['RUNNER_HOME'].append(runner_home)
            data['RUNNER_AWAY'].append(runner_away)
            data['SELECTION'].append(selection)
            data['BOOK'].append(book)
            data['ODDS_TAKEN'].append(odds)
            data['ODDS_FAIR'].append(fair_odds)
            data['VALUE'].append(value)
            data['BET_ADVISED'].append(timestamp)
            data['SCORE_HOME'].append(score_home)
            data['SCORE_AWAY'].append(score_away)
            data['STATUS'].append(status)
            data['PROFIT'].append(profit)
            data['TRUE_CLS'].append(true_cls)
            data['CLV'].append(clv)

        df_bets = pd.DataFrame(data=data)
        df_bets = df_bets.sort_values(by=['STARTS'], ascending=True)
        st.dataframe(df_bets)

st.text(f"Updated on {db.get_max_starts()}, {db.get_total_bets()} bets in the database.")
