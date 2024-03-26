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

def avg_by_date(inFile, metric="median", interval="monthly"):
    '''Reads in a csv file and returns a dataframe with only date and average score.'''
    raw_results = pd.read_csv(inFile)
    raw_dates = [d[0:8] for d in raw_results['seendate'].tolist()]
    
    if interval == "monthly":
        dates = get_monthly(raw_dates)
    elif interval == "bimonthly":
        dates = get_bimonthly(raw_dates)
    else:
        dates = get_daily(raw_dates)

    scores = raw_results['score'].tolist()
    scores_by_date = pd.DataFrame(list(zip(dates, scores)),
                                  columns =['date', 'score'])
    if metric == "mean": 
        means = scores_by_date.groupby('date').mean()
    elif metric == "median": 
        means = scores_by_date.groupby('date').median()
    means = means.reset_index()
    return means

def plot_bias(interval, metric):
    print(interval)
    means = avg_by_date("matched_bias_scores.csv", metric, interval)
    # means.to_excel("visualization/PAB_over_time.xlsx", index=False)
    labels = {"date": "Date",
              "score": "Median partisan audience bias score"}
    fig = px.line(means, x='date', y='score', labels=labels, 
                  title=f"{metric} Partisan Audience Bias score (monthly)")
    fig.show()

def main():
    plot_bias("monthly", "median")
    # plot_bias("monthly", "mean")
    # could also do another plot with two lines: 
    # "liberal" (score < 0) and "conservative" (score > 0) sources
    

main()
