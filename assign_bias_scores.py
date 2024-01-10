import pandas as pd

def get_score_for_domain(domain, bias_scores): 
    match = bias_scores[bias_scores["domain"] == domain]
    if match.shape[0] == 0: 
        return None
    score = match['score'].iloc[0]
    return score

def main(): 
    all_relev = pd.read_csv("all_relevant_by_URL_with_2020.csv")
    bias_scores = pd.read_csv("bias_scores.csv")
    scores = []
    for d in list(all_relev['domain']): 
        scores.append(get_score_for_domain(d, bias_scores))
    all_relev['score'] = scores
    all_relev.to_csv("matched_bias_scores.csv", index=False)

main()
    