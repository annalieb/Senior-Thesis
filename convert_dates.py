import pandas as pd
from datetime import datetime

def main():
    data = pd.read_csv("all_relevant.csv")
    data['seendate'] = data['seendate'].apply(lambda x:
                                              datetime.strptime(x, '%Y%m%dT%H%M%SZ'))
    data = data[["title", "url", "seendate", "domain"]]
    data = data.sort_values(by=['seendate', 'title'])
    data.to_csv('all_relevant_subset.csv', index=False)

main()
