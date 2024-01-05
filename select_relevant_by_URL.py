import pandas as pd
from IPython.display import display
import os
from random import sample
from datetime import datetime
from collections import Counter

def get_unique(folder):
    '''Takes a folder of relevant results files.
    Returns a list of all unique titles in the results.'''
    all_URLs = []
    metadata = {}
    for f in os.listdir(folder):
        if f != ".DS_Store":
            relevant = get_relevant_titles(f) # df of only relevant results
            all_URLs = all_URLs + relevant['url'].tolist()
            metas = zip(relevant['title'].tolist(),
                        relevant['url'].tolist(),
                        relevant['seendate'].tolist(),
                        relevant['domain'].tolist())
            for title, url, date, domain in metas:
                metadata[url] = (title, date, domain)
    
    url_counter = Counter(all_URLs)
    unique_urls = url_counter.keys()
    total_urls = url_counter.values()
    
    return unique_urls, total_urls, metadata

def get_relevant_titles(state_f):
    '''Given a state file, reads the file and returns a dataframe
    of all relevant rows'''
    results = pd.read_csv(f"relevant_results/{state_f}")
    relevant = results[results["relevant"] == 1]
    return relevant
    
def main():
    folder = "relevant_results"

    # get a list of all unique URLs (these are our rows) 
    all_unique_urls, all_total_urls, metadata = get_unique(folder)
    nrows = len(all_unique_urls)
    print("total unique URLs (n):", nrows)

    # define columns, with a column for each state
    data = {'title': [None] * nrows, 
            'url': all_unique_urls,
            'seendate': [None] * nrows,
            'domain': [None] * nrows,
            'total_repeats': all_total_urls}
        
    print("columns:", data.keys())

    # match up metadata with unique articles
    # note that the metadata only matches one of the repeated URLs
    for i, t in enumerate(data['url']):
        data['title'][i] = metadata[t][0]
        data['seendate'][i] = metadata[t][1]
        data['domain'][i] = metadata[t][2]
    
    all_relevant_df = pd.DataFrame.from_dict(data)

    # convert the date string into datetime object
    all_relevant_df['seendate'] = all_relevant_df['seendate'].apply(lambda x:
                                                                    datetime.strptime(x, '%Y%m%dT%H%M%SZ'))
    all_relevant_df = all_relevant_df.sort_values(by=['seendate', 'title'])
            
    display(all_relevant_df)
    # write to CSV
    all_relevant_df.to_csv("all_relevant_by_URL.csv", index=False)

            
main()
