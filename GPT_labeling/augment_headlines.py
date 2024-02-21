import query_gpt4
import pandas as pd
import csv

def get_gpt_response(prompt):
    # print("API input: \n", prompt)
    
    # query model
    response = query_gpt4.single_query(prompt)
    # print(response)
    completion = response.choices[0].message
    if response.model != "gpt-4-0125-preview": 
        print("GPT model version:", response.model)
    # print("GPT response:", completion)
    if response.choices[0].finish_reason != "stop": 
        print("GPT finish reason:", response.choices[0].finish_reason)
    return completion

def get_actor_blurb(headline): 
    actor_prompt = f'''What type of actor is the primary actor in this headline? "{headline}" 
    Briefly describe the primary actor. If the headline doesn't reference an actor, say so. You don't need to include the headline in your response. '''

    message = [
        {"role": "user", "content": actor_prompt}
    ]

    completion = get_gpt_response(message)
    return completion

def get_stance_blurb(headline): 
    actor_prompt = f'''Here is a headline about critical race theory (CRT): "{headline}" 
    What is the headline's stance on CRT? Please be concise. You don't need to include the headline in your response. '''

    message = [
        {"role": "user", "content": actor_prompt}
    ]

    completion = get_gpt_response(message)
    return completion

def get_gpt_from_ind(start_ind, title_list, query_type): 
    generated_rows = []
    for i, t in enumerate(list(title_list)[start_ind:]): 
        if query_type == "actor": 
            pred = get_actor_blurb(t).content
        elif query_type == "stance": 
            pred = get_stance_blurb(t).content
        # print(pred, t) # uncomment for verbose version (see every headline and label)
        generated_rows.append([t, pred]) # title, gpt_label
        if i % 2 == 0:
            with open("augmentation_approach/GPT_actor_blurbs.csv", 'a', newline='\n') as f:
                writer = csv.writer(f)
                writer.writerows(generated_rows)
            generated_rows = []
            print(f"processed headlines up to index {start_ind + i}, wrote to file.")

def main(): 
    # read in all headlines
    headlines = pd.read_csv("../coverage_by_unique_headline.csv")
    print(headlines.shape)

    get_gpt_from_ind(11685, headlines['title'], "actor") # started with Anna API key at ind 11464

main()