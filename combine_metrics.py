import pandas as pd

def remove_false_positives(all_relevant): 
    # irrelevant clusters: 17, 21, 80, 82
    print(all_relevant.shape)
    truly_all_relevant = all_relevant.loc[~all_relevant['cluster_label'].isin([17, 21, 80, 82])]
    print(truly_all_relevant.shape)
    return truly_all_relevant

def get_score_for_domain(domain, bias_scores): 
    match = bias_scores[bias_scores["domain"] == domain]
    if match.shape[0] == 0: 
        return None
    score = match['score'].iloc[0]
    return score

def clean_stance(raw_output): 
    if raw_output is None: 
        return None
    elif raw_output in ["<NEUTRAL>", "<DEFENDING CRT>", "<ANTI-CRT>"]: 
        return raw_output
    elif "<ANTI-CRT>" in raw_output: 
        return "<ANTI-CRT>"
    elif "<NEUTRAL>" in raw_output: 
        return "<NEUTRAL>"
    elif "<DEFENDING CRT>" in raw_output: 
        return "<DEFENDING CRT>"
    else: 
        return None
    
def clean_actor(raw_output): 
    if raw_output is None: 
        return None
    elif raw_output in ["<POLITICAL INFLUENCER>", "<EDUCATIONAL PRACTITIONER>", 
                      "<NONE/OTHER>", "<IMPACTED ACTOR>"]: 
        return raw_output
    elif "<POLITICAL INFLUENCER>" in raw_output: 
        return "<POLITICAL INFLUENCER>"
    elif "<EDUCATIONAL PRACTITIONER>" in raw_output: 
        return "<EDUCATIONAL PRACTITIONER>"
    elif "<NONE/OTHER>" in raw_output: 
        return "<NONE/OTHER>"
    elif "<IMPACTED ACTOR>" in raw_output: 
        return "<IMPACTED ACTOR>"
    else: 
        return None

def get_label_for_headline(headline, labels, label_name): 
    match = labels[labels["title"] == headline]
    if match.shape[0] == 0: 
        print("missing", label_name, "label:", headline)
        return None
    assignment = match[label_name].iloc[0]
    return assignment

def main(): 
    # read in the raw results
    relevant_results = pd.read_csv("all_relevant.csv")
    headlines = relevant_results['title'].tolist()

    # assign cluster_label to each headline
    clusters = pd.read_csv("cluster_results.csv")
    assignments = []
    for h in headlines: 
        assignments.append(get_label_for_headline(h, clusters, 'cluster_label'))
    relevant_results['cluster_label'] = assignments

    # remove headlines in irrelevant clusters
    relevant_results = remove_false_positives(relevant_results)
    headlines = relevant_results['title'].tolist()

    # assign GPT-generated labels (stance and actor) to each headline
    GPT_stances = pd.read_csv("GPT_label_results/GPT_stances.csv")
    GPT_actors = pd.read_csv("GPT_label_results/GPT_actors.csv")
    stances = []
    actors = []
    for h in headlines: 
        stance = get_label_for_headline(h, GPT_stances, "gpt_label")
        stances.append(clean_stance(stance))

        actor = get_label_for_headline(h, GPT_actors, "gpt_label")
        actors.append(clean_actor(actor))
    
    relevant_results['stance'] = stances
    relevant_results['actor'] = actors

    # reorder columns
    count_columns = [c for c in list(relevant_results.columns.values) if c.endswith("_count")]
    count_columns.sort()
    col_order = ['title','url','seendate', "domain", "cluster_label", "stance", "actor"] + count_columns
    relevant_results = relevant_results.loc[:,col_order]

    # write output to csv
    relevant_results.to_excel("coverage_by_unique_headline.xlsx", index=False)

    ######### REPEAT FOR URL DATA #########

    # read in raw results by URL
    relevant_results_by_URL = pd.read_csv("all_relevant_by_URL.csv")
    headlines = relevant_results_by_URL['title'].tolist()

    # assign cluster_label to each headline
    clusters = pd.read_csv("cluster_results.csv")
    assignments = []
    for h in headlines: 
        assignments.append(get_label_for_headline(h, clusters, 'cluster_label'))
    relevant_results_by_URL['cluster_label'] = assignments

    # remove headlines in irrelevant clusters
    relevant_results_by_URL = remove_false_positives(relevant_results_by_URL)
    headlines = relevant_results_by_URL['title'].tolist()

    # get bias score
    bias_scores = pd.read_csv("bias_scores.csv")
    scores = []
    for d in list(relevant_results_by_URL['domain']): 
        scores.append(get_score_for_domain(d, bias_scores))
    relevant_results_by_URL['bias_score'] = scores

    # get reddit data
    reddit_posts = pd.read_json("reddit_post_data.json")
    relevant_results_by_URL = pd.merge(relevant_results_by_URL, reddit_posts, on="url", how="left")

    # write result to csv
    relevant_results_by_URL.to_json("coverage_by_unique_URL.json", orient="records")

main()