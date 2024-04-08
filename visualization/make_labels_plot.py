import plotly.graph_objects as go
import pandas as pd
import datetime
from IPython.display import display
import plotly.express as px
from collections import Counter

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

def count_by_date(inFile, frame, interval="monthly"):
    '''Reads in a csv file and returns a dataframe with only date and average score.'''
    raw_results = pd.read_csv(inFile)
    raw_dates = [d[0:8] for d in raw_results['seendate'].tolist()]
    
    if interval == "monthly":
        dates = get_monthly(raw_dates)
    elif interval == "bimonthly":
        dates = get_bimonthly(raw_dates)
    else:
        dates = get_daily(raw_dates)

    labels = raw_results[frame].tolist()
    scores_by_date = pd.DataFrame(list(zip(dates, labels)),
                                  columns =['date', frame])

    by_date = scores_by_date.groupby('date')
    time_range = by_date.groups.keys() # all of the unique dates 

    # create results df for stance or actor
    if frame=="stance": 
        labels = ['<DEFENDING CRT>', '<ANTI-CRT>', '<NEUTRAL>']
    elif frame == "actor": 
        labels = ['<POLITICAL INFLUENCER>', '<EDUCATIONAL PRACTITIONER>', 
                  '<IMPACTED ACTOR>', '<NONE/OTHER>']
        
    results = pd.DataFrame(columns=(['date'] + labels))
    for date in time_range: 
        # make a label counter for each date range
        this_group = by_date.get_group(date)
        labels_counter = dict(Counter(list(this_group[frame])))
        labels_counter['date'] = date
        results = pd.concat([results, pd.DataFrame([labels_counter])], ignore_index=True)

    # add column for total number of articles in the time period
    results['total_count'] = results.loc[:, results.columns != 'date'].sum(axis=1)
    print(results.columns)

    # use for getting percentage (instead of count)
    prop_results = results[labels].div(results['total_count'], axis=0)
    prop_results = pd.concat([results['date'], prop_results], axis=1)

    print(prop_results.shape)
    display(prop_results)
    prop_results.to_excel("stances_over_time.xlsx", index=False)

    prop_results = prop_results.fillna(0)
    
    # return results for count instead of proportion
    return prop_results

def plot_labels(interval):
    print(interval)
    counts = count_by_date("../coverage_by_unique_headline.csv", "stance", interval)
    # switch out <DEFENDING CRT> or <POLITICAL INFLUENCER>
    fig = px.line(counts, x='date', y='<DEFENDING CRT>', labels={"date": "Date", 
                                                                 "<DEFENDING CRT>":"Label proportion"},
                  title=f"Stance labels over time")
    for label in counts.columns[1:4]: # 1:4 for stance, 1:5 for actor
        fig.add_scatter(x=counts['date'],
                        y=counts[label],
                        mode='lines',
                        name=label)
    fig.show()

def main():
    plot_labels("monthly")
    # plot_bias("monthly", "mean")
    # could also do another plot with two lines: 
    # "liberal" (score < 0) and "conservative" (score > 0) sources
    

main()
