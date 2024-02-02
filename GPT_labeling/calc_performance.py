import numpy as np
from sklearn.metrics import f1_score
import pandas as pd
from collections import Counter

def clean_baseline_entry(entry): 
    if '<CLASS4>' in entry: 
        return '<CLASS4>'
    elif '<CLASS3>' in entry: 
        return '<CLASS3>'
    elif '<CLASS2>' in entry: 
        return '<CLASS2>'
    elif '<CLASS1>' in entry: 
        return '<CLASS1>'
    else: 
        print("Error! No class found")
        return None

def get_classwise_f1(inFile): 
    all_labels = pd.read_csv(inFile)

    # clean labels
    all_labels['actor_pred'] = [clean_baseline_entry(a) for a in all_labels['actor_pred']]
    all_labels['headline stance_pred'] = [clean_baseline_entry(a) for a in all_labels['headline stance_pred']]

    conversions = {
        # baseline trial items
        "<CLASS1>": 0,
        "<CLASS2>": 1,
        "<CLASS3>": 2,
        "<CLASS4>": 3,

        # actor
        "<EDUCATIONAL PRACTITIONER>": 0,
        "educational practitioners": 0,
        "<POLITICAL INFLUENCER>": 1,
        "political influencers": 1,
        "<IMPACTED ACTOR>": 2,
        "impacted actors": 2,
        "<NONE/OTHER>": 3,
        "none / other": 3,

        # action direction and headline stance
        "<ANTI-CRT>": 0, 
        "anti-CRT": 0, 
        "<DEFENDING CRT>": 1,
        "defending CRT": 1,
        "<NEUTRAL>": 2, 
        "neutral": 2
    }

    ##### ACTOR #####
    actor_true = [conversions[l] for l in all_labels['actor']]
    actor_pred = [conversions[l] for l in all_labels['actor_pred']]
    classwise_f1 = f1_score(actor_true, actor_pred, average=None)
    weighted_f1 = f1_score(actor_true, actor_pred, average="weighted")
    avg_f1 = f1_score(actor_true, actor_pred, average="macro")
    print("class-wise:", classwise_f1)
    print("weighted average:", weighted_f1)
    print("average (doesn't account for imbalance):", avg_f1)
    print("counts:", Counter(all_labels['actor']))

    ##### HEADLINE STANCE #####
    stance_true = [conversions[l] for l in all_labels['headline stance']]
    stance_pred = [conversions[l] for l in all_labels['headline stance_pred']]
    classwise_f1 = f1_score(stance_true, stance_pred, average=None)
    weighted_f1 = f1_score(stance_true, stance_pred, average="weighted")
    avg_f1 = f1_score(stance_true, stance_pred, average="macro")
    print("class-wise:", classwise_f1)
    print("weighted average:", weighted_f1)
    print("average (doesn't account for imbalance):", avg_f1)
    print("counts:", Counter(all_labels['headline stance']))
    

get_classwise_f1("baseline_approach/n=2_contested.csv")
get_classwise_f1("baseline_approach/n=2_uncontested.csv")
get_classwise_f1("baseline_approach/n=4.csv")
