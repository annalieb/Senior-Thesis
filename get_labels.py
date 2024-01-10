import query_gpt4
import pandas as pd
import csv

def get_gpt_response(prompt):
    # print("API input: \n", prompt)
    
    # query model
    response = query_gpt4.single_query(prompt)
    # print(response)
    completion = response.choices[0].message
    if response.model != "gpt-4-1106-preview": 
        print("GPT model version:", response.model)
    # print("GPT response:", completion)
    if response.choices[0].finish_reason != "stop": 
        print("GPT finish reason:", response.choices[0].finish_reason)
    return completion

def get_one_actor(headline): 
    actor_prompt = f'''News article headlines can shape the ways that people perceive current events and understand the world around them. Therefore, nuances in the headline's language and word choice can be very important. The goal of this task is to identify the main actor (ie. a person or organization) in a news headline. 
    
    You will be given a news headline related to critical race theory (CRT). Your response should identify the main actor in the headline. Your response must be one of the following predefined labels: <EDUCATIONAL PRACTITIONER>, <POLITICAL INFLUENCER>, <IMPACTED ACTOR>, or <NONE/OTHER>. 
    
    Please carefully consider the following label definitions: 
    <EDUCATIONAL PRACTITIONER> - This actor's primary role is to deliver instruction to students. Some examples include schools, universities, school districts, teachers, professors, and school administrations. 
    <POLITICAL INFLUENCER> - This actor's primary role is to represent the political interests and/or policy preferences of people. Some examples include governors, school boards, political commentators, pundits, the president, and political figures.
    <IMPACTED ACTOR> - This actor participates in the school system without direct influence over policies or educational practices. Some examples may include students, parents, and voters. 
    <NONE/OTHER> - There is no actor in the headline, or the main actor does not fit any of the other categories above.

    Your interpretations of the headline should be guided by the main ideas that stand out in the headline. Consider that the headline might belong to one of the categories implicitly, without direct reference to exact words provided in the label definition.

    Please consider the following headline: "{headline}"
    What is the main actor in this headline? Please respond with exactly one of the following predefined labels that best describes the main actor in this headline: <EDUCATIONAL PRACTITIONER>, <POLITICAL INFLUENCER>, <IMPACTED ACTOR>, or <NONE/OTHER>. '''

    message = [
        {"role": "user", "content": actor_prompt}
    ]

    completion = get_gpt_response(message)
    return completion

def get_one_action(headline): 
    action_prompt = f'''News article headlines can shape the ways that people perceive current events and understand the world around them. Therefore, nuances in the headline's language and word choice can be very important. The goal of this task is to identify the main action taking place in a news headline. 

    You will be given a news headline related to critical race theory (CRT). Your response should identify the main action in the headline. Your response must be one of the following predefined labels: <PROTEST / SPEAKING OUT>, <POLICY / LEGAL / ELECTIONS>, <THREATS / EXTENT>, or <NONE/OTHER>. 

    Please carefully consider the following label definitions: 
    <PROTEST / SPEAKING OUT> - The primary action in the headline involves an act of protest or speaking out. Some examples include people voicing concerns, protesting, public demonstrations, and debate at public meetings
    <POLICY / LEGAL / ELECTIONS> - The primary action in the headline involves policies, legal action, or an election. Some examples include imposing bans, passing legislation, implementing a school/district/state policy, filing a lawsuit, school curriculum policy, elections, campaigns, and voting. 
    <THREATS / EXTENT> - The primary action in the headline involves CRT posing a threat or the extent of CRT itself. Some examples may include teaching CRT, learning CRT, spread of CRT in schools, influencing the quality of education, posing a cultural/social/moral threat, and limiting personal rights or civil liberties. 
    <NONE/OTHER> - There is no clear action taking place in the headline, or the main action in the headline does not fit any of the other categories above.

    Your interpretations of the headline should be guided by the main ideas that stand out in the headline. Consider that the headline might belong to one of the categories implicitly, without direct reference to exact words provided in the label definition.

    Please consider the following headline: "{headline}"
    What is the main action in this headline? Please respond with exactly one of the following predefined labels that best describes the main action in this headline: <PROTEST / SPEAKING OUT>, <POLICY / LEGAL / ELECTIONS>, <THREATS / EXTENT>, or <NONE/OTHER>. 
    '''

    message = [
        {"role": "user", "content": action_prompt}
    ]

    completion = get_gpt_response(message)
    return completion

def get_one_action_direction(headline): 
    action_direction_prompt = f'''News article headlines can shape the ways that people perceive current events and understand the world around them. Therefore, nuances in the headline's language and word choice can be very important. The goal of this task is to identify the impact of an action or event taking place in a news headline. 

    You will be given a news headline related to critical race theory (CRT). Your response should identify the action direction in the headline. Your response must be one of the following predefined labels: <ANTI-CRT>, <DEFENDING CRT>, or <NEUTRAL>. 

    Please carefully consider the following label definitions: 
    <ANTI-CRT> - The headline reports on anti-CRT actions that restrict teaching CRT, actions taken to speak out against CRT, or any other anti-CRT actions taken to counter CRT. 
    <DEFENDING CRT> - The headline reports on actions that defend teaching CRT, actions taken to speak out in support of CRT, or any other actions taken to counter anti-CRT efforts.
    <NEUTRAL> - The headline does not clearly identify an action, or the action does not make change in either direction (neither for or against CRT). 

    Note that the impact of the event in the headline is different from the headline stance or bias. For example, consider the following headline: "Florida bans critical race theory from classrooms." For this headline, the headline stance is neutral because the headline does not reveal a strong journalistic bias for or against CRT. However, the action taking place has an anti-CRT impact because the ban would prevent teaching CRT in classrooms. Therefore, this headline stance would have the <ANTI-CRT> label.

    Your interpretations of the headline should be guided by the main actions or events that stand out in the headline. Consider that the headline action might belong to one of the categories implicitly, without direct reference to exact words or examples provided in the label definition.

    Please consider the following headline: "{headline}"
    Consider the main action taking place in the headline. What is the action's impact? Please respond with exactly one of the following predefined labels that best describes the action direction in this headline: <ANTI-CRT>, <DEFENDING CRT>, or <NEUTRAL>. 
    '''

    message = [
        {"role": "user", "content": action_direction_prompt}
    ]

    completion = get_gpt_response(message)
    return completion

def get_one_stance(headline): 
    action_direction_prompt = f'''News article headlines can shape the ways that people perceive current events and understand the world around them. Therefore, nuances in the headline's language and word choice can be very important. The goal of this task is to identify the stance or bias of a news headline. 

    You will be given a news headline related to critical race theory (CRT). Your response should identify the stance of the headline. Your response must be one of the following predefined labels: <ANTI-CRT>, <DEFENDING CRT>, or <NEUTRAL>. 

    Please carefully consider the following label definitions: 
    <ANTI-CRT> - The headline favors an anti-CRT viewpoint. Its viewpoint appears to oppose CRT, support CRT bans, or make alarmist claims about threats posed by CRT. It has an anti-CRT stance. 
    <DEFENDING CRT> - The headline favors a viewpoint that defends CRT. Its viewpoint appears to support CRT, oppose CRT bans, or minimize the threat posed by CRT-related curricula. It has a stance that defends CRT. 
    <NEUTRAL> - The headline does not have a strong viewpoint. It is neutral or impartial. It reports on news events without favoring one viewpoint or the other (neither anti-CRT nor defending CRT). 

    Note that the impact of the event in the headline is different from the headline stance or bias. For example, consider the following headline: "Florida bans critical race theory from classrooms." For this headline, the action taking place has an anti-CRT impact because the ban would prevent teaching CRT in classrooms. However, in this case, the headline stance is neutral because the headline does not reveal a strong journalistic bias for or against CRT. Therefore, this headline stance would have the <NEUTRAL> label.

    Your interpretations of the headline should be guided by polarizing terms that stand out in the headline, which may indicate the headline's stance. Consider that the headline stance might belong to one of the categories implicitly, without direct reference to exact words or examples provided in the label definition.

    Please consider the following headline: "{headline}"
    Consider any biased framing in the headline. What is the headline's stance? Please respond with exactly one of the following predefined labels that best describes the stance in this headline: <ANTI-CRT>, <DEFENDING CRT>, or <NEUTRAL>. 
    '''

    message = [
        {"role": "user", "content": action_direction_prompt}
    ]

    completion = get_gpt_response(message)
    return completion

def get_many_labels(val, label_type): 
    '''params: 
    val - validation set
    label_type - one of "actor", "action", "action direction", or "headline stance"'''
    headlines = list(val['Title'])

    # get actor labels
    preds = []
    labels = list(val[label_type])
    for h, label in zip(headlines, labels): 
        if label_type == "action": 
            resp = get_one_action(h)
        elif label_type == "actor": 
            resp = get_one_actor(h)
        elif label_type == "action direction": 
            resp = get_one_action_direction(h)
        elif label_type == "headline stance": 
            resp = get_one_stance(h)
        else: 
            print(f"ERROR: no label_type {label_type}")
            return None
        pred = resp.content
        preds.append(pred)
        print(f"headline: {h}")
        print(f"predicted: {pred}")
        print(f"actual: {label}")

    val.insert(2, f"{label_type}_pred", preds)
    val.to_csv("GPT_label_results/actor_35_preds.csv")

def get_gpt_labels_from_ind(start_ind, title_list): 
    generated_rows = []
    for i, t in enumerate(list(title_list)[start_ind:]): 
        pred = get_one_actor(t).content
        # print(pred, t) # uncomment for verbose version (see every headline and label)
        generated_rows.append([t, pred]) # title, gpt_label
        if i % 25 == 0:
            print("processed 25 headlines, writing to file.")
            with open("GPT_label_results/GPT_actors.csv", 'a', newline='\n') as f:
                writer = csv.writer(f)
                writer.writerows(generated_rows)
            generated_rows = []


def main():
    # read in test data
    val = pd.read_csv("coding/complete_consensus_coding.csv")
    all_data = pd.read_csv("all_relevant.csv")

    # get actor labels for validation dataset
    # get_many_labels(val, "actor")

    # get action labels for validation dataset
    # get_many_labels(val, "action")

    # get action direction labels for validation dataset
    # get_many_labels(val, "action direction")

    # get headline stance labels for validation dataset
    # get_many_labels(val, "headline stance")

    get_gpt_labels_from_ind(8020, all_data['title'])


main()

