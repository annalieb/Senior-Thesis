import plotly.graph_objects as go
import pandas as pd
import datetime
from IPython.display import display
import plotly.express as px
import scipy

from scipy import signal

def get_daily(raw_dates):
    '''Convert a list of raw dates to datetime dates
    accurate to the day'''
    dates = []
    for d in raw_dates:
        year, month, day = (d[0:4], d[4:6], d[6:8])
        date = datetime.date(int(year), int(month), int(day))
        dates.append(date)
    return dates

def get_bimonthly(raw_dates):
    '''Convert a list of raw dates to datetime dates
    accurate to the day'''
    dates = []
    for d in raw_dates:
        year, month, day = (d[0:4], d[4:6], d[6:8])
        if int(day) < 15: 
            date = datetime.date(int(year), int(month), 1)
        else:
            date = datetime.date(int(year), int(month), 15)
        dates.append(date)
    return dates

def get_monthly(raw_dates):
    '''Convert a list of raw dates to datetime dates
    accurate to the month'''
    dates = []
    for d in raw_dates:
        year, month = (d[0:4], d[4:6])
        date = datetime.date(int(year), int(month), 1)
        dates.append(date)
    return dates

def avg_by_date(inFile, interval="daily"):
    '''Reads in a file from relevant_results folder
    and returns a dataframe with only date and relevance labels.'''
    raw_results = pd.read_csv(inFile)
    raw_dates = [d[0:8] for d in raw_results['seendate'].tolist()]
    
    if interval == "monthly":
        dates = get_monthly(raw_dates)
    elif interval == "bimonthly":
        dates = get_bimonthly(raw_dates)
    else:
        dates = get_daily(raw_dates)

    relevance_labels = raw_results['relevant'].tolist()
    relevance_by_date = pd.DataFrame(list(zip(dates, relevance_labels)),
                                     columns =['date', 'relevant'])
    means = relevance_by_date.groupby('date').mean()
    means = means.reset_index()
    return means

def plot_relevance(states_list, interval="daily", smoothing=False):
    print(interval)
    first_s = states_list[0]
    means = avg_by_date(f"relevant_results/{first_s}_labeled.csv",
                                   interval)
    # means.to_csv("related_term_daily.csv", index=False)
    labels = {"date": "Date",
              "relevant": "Relevance (proportion of state coverage)"}
    if smoothing:
        # https://plotly.com/python/smoothing/
        fig = px.line(means, x='date', y=signal.savgol_filter(means['relevant'],
                                                          53, # window size used for filtering
                                                          5)) # order of fitted polynomial'relevant', labels=labels)
    else: 
        fig = px.line(means, x='date', y='relevant') # order of fitted polynomial'relevant', labels=labels)
    fig.data[0].name=first_s
    fig.update_traces(showlegend=True)
    
    for s in states_list[1:]:
        means = avg_by_date(f"relevant_results/{s}_labeled.csv",
                                       interval)
        means.to_csv("related_term_daily_2.csv", index=False)
        n_intervals = len(means['relevant'])
        trimester = (n_intervals // 3)
        if max(means['relevant'][trimester*2: trimester*3] > 0.04):
            print(f"Warning: {s} has high coverage {means['date'][trimester*2]} through {means['date'][trimester*3]}")
            print(f"max:{max(means['relevant'][trimester*2:(trimester*3)])}")
        if smoothing: 
            fig.add_scatter(x=means['date'],
                            y=signal.savgol_filter(means['relevant'],
                                                   53, # window size used for filtering
                                                   5),
                            mode='lines',
                            name=s)
        else: 
            fig.add_scatter(x=means['date'],
                            y=means['relevant'],
                            mode='lines',
                            name=s)
    fig.show()

def main():
    # plot_relevance(["USA"], "bimonthly")
    # plot_relevance(["FL", "OK", "VA", "ID", "MT"], "bimonthly") # first movers
    # plot_relevance(["FL", "OK", "VA", "MS", "SD"], "bimonthly") # second wave
    
    # plot_relevance(["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL",
    #                 "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA",
    #                 "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE",
    #                 "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
    #                 "OR", "PA", "SC", "RI", "SD", "TN", "TX", "UT", "VT",
    #                 "VA", "WV", "WI", "WY"],
    #                "bimonthly")
    # plot_relevance(["FL", "OK", "TX", "VA", "USA"], "bimonthly")
    # plot_relevance(["USA", "USA_woke", "USA_masking", "USA_trans"], "bimonthly", False)
    plot_relevance(["USA", "USA_woke", "USA_trans"], "daily", False)
    # plot_relevance(["FL", "FL_woke", "FL_covid", "FL_trans"], "bimonthly", False)

    

main()
