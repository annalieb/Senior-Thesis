import query_gpt35
import pandas as pd

def get_gpt_response(prompt):
    # print("API input: \n", prompt)
    
    # query model
    response = query_gpt35.single_query(prompt)
    # print(response)
    completion = response.choices[0].message
    print("GPT model version:", response.model)
    print("GPT response:", completion)
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
        else: 
            print(f"ERROR: no label_type {label_type}")
            return None
        pred = resp.content
        preds.append(pred)
        print(f"headline: {h}")
        print(f"predicted: {pred}")
        print(f"actual: {label}")

    val.insert(3, f"{label_type}_pred", preds)
    val.to_csv("GPT_label_results/action_preds.csv")


def main():
    # test_message = [
    #     {"role": "user", "content": "What day did Russia invade Ukraine in 2022?"}
    #     ]
    # gpt_resp = get_gpt_response(test_message)

    # read in test data
    val = pd.read_csv("coding/complete_consensus_coding.csv")

    # get actor labels for validation dataset
    # get_many_labels(val, "actor")

    # get action labels for validation dataset
    get_many_labels(val, "action")


main()
