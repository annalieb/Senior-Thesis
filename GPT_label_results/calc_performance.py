import numpy as np
from sklearn.metrics import f1_score
import pandas as pd

def get_classwise_f1(): 
    all_labels = pd.read_csv("actor_preds.csv")

    conversions = {
        "<EDUCATIONAL PRACTITIONER>": 0,
        "educational practitioners": 0,
        "<POLITICAL INFLUENCER>": 1,
        "political influencers": 1,
        "<IMPACTED ACTOR>": 2,
        "impacted actors": 2,
        "<NONE/OTHER>": 3,
        "none / other": 3,
    }

    actor_true = [conversions[l] for l in all_labels['actor']]
    actor_pred = [conversions[l] for l in all_labels['actor_pred']]
    classwise_f1 = f1_score(actor_true, actor_pred, average=None)
    print(classwise_f1)

get_classwise_f1()