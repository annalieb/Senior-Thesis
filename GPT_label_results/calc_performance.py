import numpy as np
from sklearn.metrics import f1_score
import pandas as pd

def get_classwise_f1(): 
    all_labels = pd.read_csv("all_preds.csv")

    conversions = {
        # actor
        "<EDUCATIONAL PRACTITIONER>": 0,
        "educational practitioners": 0,
        "<POLITICAL INFLUENCER>": 1,
        "political influencers": 1,
        "<IMPACTED ACTOR>": 2,
        "impacted actors": 2,
        "<NONE/OTHER>": 3,
        "none / other": 3,
        # action
        "<PROTEST / SPEAKING OUT>": 0, 
        "protest / speaking out": 0,
        "<POLICY / LEGAL / ELECTIONS>": 1, 
        "policy & legal": 1, 
        "elections": 1,
        "<THREATS / EXTENT>": 2, 
        "threats/extent": 2,
        "<NONE/OTHER>": 3,
        "none/other": 3, 
        # action direction
        # headline stance
    }

    ##### ACTOR #####
    actor_true = [conversions[l] for l in all_labels['actor']]
    actor_pred = [conversions[l] for l in all_labels['actor_pred']]
    classwise_f1 = f1_score(actor_true, actor_pred, average=None)
    print(classwise_f1)

    ##### ACTION #####
    action_true = [conversions[l] for l in all_labels['action']]
    action_pred = [conversions[l] for l in all_labels['action_pred']]
    classwise_f1 = f1_score(action_true, action_pred, average=None)
    print(classwise_f1)

    ##### ACTION DIRECTION #####

get_classwise_f1()