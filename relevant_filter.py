# Filter out relevant articles
import pandas as pd
import os
import string
from IPython.display import display

# test for florida
def read_results(state_abrv):
    '''Takes the state_abrv (ie. NJ) and returns a pandas dataframe
    with all articles collected from that state'''
    results = pd.read_csv(f"gdelt_results/{state_abrv}/" + os.listdir(f"gdelt_results/{state_abrv}")[0])
    for f in [f for f in os.listdir(f"gdelt_results/{state_abrv}") if f != ".DS_Store"]:
        print(f"gdelt_results/{state_abrv}/{f}")
        temp = pd.read_csv(f"gdelt_results/{state_abrv}/{f}")
        results = pd.concat([results, temp])

    return results

def get_unique(title_list):
    '''Takes a list of article titles and eliminates repeated titles in the list.
    Returns a list of only unique titles.'''
    unique_titles = list(set(title_list))
    print(len(unique_titles))
    return unique_titles

def get_relevant(titles_list):
    labels = []
    for t in titles_list: 
        if type(t) != str:
            labels.append(0)
        else: 
            t = t.lower()
            t = t.split()
            if (("race" in t and ("critical" in t or "theory" in t)) or
                ("crt" in t)): 
                labels.append(1)
            else: 
                labels.append(0)
    print(len(labels)) 
    print("Relevant count:", sum(labels)) # number of matches
    print("Relevant %:", sum(labels) / len(labels)) # percent relevant
    return labels

def write_relevant_csv(df, relevance_labels, state_abrv):
    '''Takes a dataframe, a list of relevance labels, and the state_abrv.
    Returns a dataframe with a new column for the labels
    ("relevant") and writes it to csv.'''
    df['relevant'] = relevance_labels
    df.to_csv(f"relevant_results/{state_abrv}_labeled.csv", index=False)
    return df

def get_relevance_for(state_abrv):
    '''Reads from gdelt results file, labels article titles as relevant or not,
    and writes the results to a new file in the relevant_results folder'''
    results = read_results(state_abrv)
    # display(results) # see dataframe
    titles = results['title'].tolist()
    # unique_titles = get_unique(titles)
    labels = get_relevant(titles)
    results = write_relevant_csv(results, labels, state_abrv)

def main():
    for state in ["NY"]:
        if state != ".DS_Store":
            try:
                print(f"Getting relevance labels for {state}")
                get_relevance_for(state)
            except:
                print(f"error getting relevance labels for {state}")
            
    
##    relevant_results = results[results['rule_label'] == 1]
##    relevant_results.to_csv("FL_relevant_sample.csv", index=False)

main()
