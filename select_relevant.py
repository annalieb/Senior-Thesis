import pandas as pd
from IPython.display import display
import os
from random import sample
from collections import Counter

def get_unique(folder):
    '''Takes a folder of relevant results files.
    Returns a list of all unique titles in the results.'''
    all_titles = []
    metadata = {}
    for f in os.listdir(folder):
        if f != ".DS_Store":
            relevant = get_relevant_titles(f) # df of only relevant results
            all_titles = all_titles + relevant['title'].tolist()
            metas = zip(relevant['title'].tolist(),
                        relevant['url'].tolist(),
                        relevant['seendate'].tolist(),
                        relevant['domain'].tolist())
            for title, url, date, domain in metas:
                metadata[title] = (url, date, domain)
    
    title_counter = Counter(all_titles)
    unique_titles = title_counter.keys()
    total_counts = title_counter.values()
    
    return unique_titles, total_counts, metadata

def get_relevant_titles(state_f):
    '''Given a state file, reads the file and returns a dataframe
    of all relevant rows'''
    results = pd.read_csv(f"relevant_results/{state_f}")
    relevant = results[results["relevant"] == 1]
    return relevant

def update_df(df, headline_pairs):
    '''Takes tuples of headline, state count pairs (for example: ("Breaking news", "MA_count"))
    and updates the full dataframe of state counts'''
    for p in headline_pairs:
        headline = p[0]
        col = p[1] + "_count"
        # increment count by 1
        df.loc[df.title == headline, col] += 1
    
def main():
    folder = "relevant_results"

    # get a list of all unique headlines (these are our rows) 
    all_unique_titles, all_total_counts, metadata = get_unique(folder)
    nrows = len(all_unique_titles)
    print("total unique titles (n):", nrows)

    # define columns, with a column for each state
    data = {'title': all_unique_titles, 
            'url': [None] * nrows,
            'seendate': [None] * nrows,
            'domain': [None] * nrows,
            'total_repeats': all_total_counts,}
    
    count_cols = [s[0:s.find("_l")]+"_count" for s in os.listdir(folder)]
    for c in count_cols:
        data[c] = [0] * nrows
        
    print("columns:", data.keys())

    # match up metadata with unique articles
    # note that the metadata only matches one of the repeated articles
    for i, t in enumerate(data['title']):
        data['url'][i] = metadata[t][0]
        data['seendate'][i] = metadata[t][1]
        data['domain'][i] = metadata[t][2]
    
    all_relevant_df = pd.DataFrame.from_dict(data)

    for f in os.listdir(folder):
        if f != ".DS_Store":
            print("Updating relevance for", f)
            
            df = get_relevant_titles(f)
            # create pairs of headlines and state code
            code = f[0:f.find("_l")]
            pairs = zip(df['title'], [code] * df.shape[0])
            update_df(all_relevant_df, pairs)
            
    display(all_relevant_df)
    all_relevant_df.to_csv("all_relevant.csv", index=False)
            
# main()
    
def remove_false_positives(): 
    # irrelevant cluster #: 17, 21, 80, 82
    clusters = pd.read_csv("cluster_results.csv")
    print(clusters.shape)
    irr = clusters.loc[clusters['cluster_label'].isin([17, 21, 80, 82])]
    print(irr.shape)
    
    all_relevant = pd.read_csv("all_relevant.csv")
    print(all_relevant.shape)
    truly_all_relevant = all_relevant.loc[~all_relevant['title'].isin(irr["sentence"])]
    print(truly_all_relevant.shape)
    truly_all_relevant.to_csv("all_relevant.csv")

remove_false_positives()