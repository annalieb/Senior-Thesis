import os
import pandas as pd
import numpy as np

def count_unique_domains(): 
    '''Count the number of unique domains'''
    all_relev = pd.read_csv("all_relevant_with_2020.csv")
    unique = all_relev['domain'].unique()
    print("unique domains:", unique.shape)
    return unique.shape[0]


def count_total_headlines():

    '''Count the number of total headlines in the GDELT_results folder'''
    states = [("Alabama", "AL"), ("Alaska", "AK"), ("Arizona", "AZ"), ("Arkansas", "AK"),
              ("California", "CA"), ("Colorado", "CO"), ("Connecticut", "CT"),
              ("Delaware", "DE"), ("Florida", "FL"), ("Georgia", "GA"), ("Hawaii", "HI"),
              ("Idaho", "ID"), ("Illinois", "IL"), ("Indiana", "IN"), ("Iowa", "IA"),
              ("Kansas", "KS"), ("Kentucky", "KY"), ("Louisiana", "LA"), ("Maine", "ME"),
              ("Maryland", "MD"), ("Massachusetts", "MA"), ("Michigan", "MI"), ("Minnesota", "MN"),
              ("Mississippi", "MS"), ("Missouri", "MO"), ("Montana", "MT"), ("Nebraska", "NE"),
              ("Nevada", "NV"), ("New%20Hampshire", "NH"), ("New%20Jersey", "NJ"),
              ("New%20Mexico", "NM"), ("New%20York", "NY"), ("North%20Carolina", "NC"),
              ("North%20Dakota", "ND"), ("Ohio", "OH"), ("Oklahoma", "OK"), ("Oregon", "OR"),
              ("Pennsylvania", "PA"), ("Rhode%20Island", "RI"), ("South%20Carolina", "SC"),
              ("South%20Dakota", "SD"), ("Tennessee", "TN"), ("Texas", "TX"), ("Utah", "UT"),
              ("Vermont", "VT"), ("Virginia", "VA"), ("West%20Virginia", "WV"), ("Wisconsin", "WI"),
              ("Wyoming", "WY"), ("USA", "USA")]
    
    total = []

    for state, state_abrv in states:
        print("working on:", state) 
        file = f"relevant_results/{state_abrv}_labeled.csv"
        titles = pd.read_csv(file)['title']
        total.append(titles)
    
    total = np.concatenate(total)
    print("Total num headlines:", total.shape)
    total_df = pd.DataFrame(total, columns=["domain"])
    print("Total num unique headlines:", total_df['domain'].unique().shape)
    return total

count_total_headlines()
# count_unique_domains()