import numpy as np
from sklearn.metrics import f1_score
import pandas as pd
from collections import Counter

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
    print("class-wise:", classwise_f1)
    print("weighted average:", weighted_f1)
    print("counts:", Counter(all_labels['actor']))

    ##### ACTION #####
    action_true = [conversions[l] for l in all_labels['action']]
    action_pred = [conversions[l] for l in all_labels['action_pred']]
    classwise_f1 = f1_score(action_true, action_pred, average=None)
    weighted_f1 = f1_score(action_true, action_pred, average="weighted")
    print("class-wise:", classwise_f1)
    print("weighted average:", weighted_f1)
    print("counts:", Counter(all_labels['action']))

    ##### ACTION DIRECTION #####
    direction_true = [conversions[l] for l in all_labels['action direction']]
    direction_pred = [conversions[l] for l in all_labels['action direction_pred']]
    classwise_f1 = f1_score(direction_true, direction_pred, average=None)
    weighted_f1 = f1_score(direction_true, direction_pred, average="weighted")
    print("class-wise:", classwise_f1)
    print("weighted average:", weighted_f1)
    print("counts:", Counter(all_labels['action direction']))

    ##### HEADLINE STANCE #####
    stance_true = [conversions[l] for l in all_labels['headline stance']]
    stance_pred = [conversions[l] for l in all_labels['headline stance_pred']]
    classwise_f1 = f1_score(stance_true, stance_pred, average=None)
    weighted_f1 = f1_score(stance_true, stance_pred, average="weighted")
    print("class-wise:", classwise_f1)
    print("weighted average:", weighted_f1)
    print("counts:", Counter(all_labels['headline stance']))

get_classwise_f1()