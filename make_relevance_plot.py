import plotly.graph_objects as go
import pandas as pd
import datetime
from IPython.display import display
import plotly.express as px

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

def plot_relevance(states_list, interval="daily"):
    print(interval)
    first_s = states_list[0]
    means = avg_by_date(f"relevant_results/{first_s}_labeled.csv",
                                   interval)
    fig = px.line(means, x='date', y='relevant')
    fig.data[0].name=first_s
    fig.update_traces(showlegend=True)
    
    for s in states_list[1:]:
        means = avg_by_date(f"relevant_results/{s}_labeled.csv",
                                       interval)
        fig.add_scatter(x=means['date'],
                        y=means['relevant'],
                        mode='lines',
                        name=s)
    fig.show()

def main():
    plot_relevance(["FL", "VA", "IL", "KS"], "bimonthly")

main()
