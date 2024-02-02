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

def get_examples(example_type):
    if example_type == "uncontested_actor": 
        return '''The headline: "Teachers Unions Push CRT in Schools"
        The CLASS of the headline: <CLASS1>

        The headline: "No new teachers in Glen Ellyn sign pledge on Oct . 19 to teach Critical Race Theory"
        The CLASS of the headline: <CLASS1>

        The headline: "Critical Race Theory Is a Potent Issue in the Virginia Governor Race"
        The CLASS of the headline: <CLASS2>

        The headline: "Wisconsin assembly passes bill banning critical race theory in the classroom"
        The CLASS of the headline: <CLASS2>

        The headline: "WATCH : Parents , Activists Protest CRT at Texas School Board Meeting"
        The CLASS of the headline: <CLASS3>

        The headline: "Local Parents Speak Out Against Critical Race Theory | News Radio 101 . 9 Big WAAX"
        The CLASS of the headline: <CLASS3>

        The headline: "What Is Critical Race Theory Anyway ?"
        The CLASS of the headline: <CLASS4>

        The headline: "COMMENTARY : The truth about CRT"
        The CLASS of the headline: <CLASS4>'''
    elif example_type == "contested_actor": 
        return '''The headline: "Department of Education wisely retreats from critical race theory"
        The CLASS of the headline: <CLASS1>

        The headline: "Racist CRT Lessons in Public School Classrooms"
        The CLASS of the headline: <CLASS1>

        The headline: "CRT is dividing Democrats and rallying Republicans"
        The CLASS of the headline: <CLASS2>

        The headline: "UCLA database reveals well - funded push for critical race theory , argues Cornell law professor"
        The CLASS of the headline: <CLASS2>

        The headline: "Critical Race Theory Aims to Turn Students Into  Red Guards , Chinese American Warns By Terri Wu"
        The CLASS of the headline: <CLASS3>

        The headline: "Fears about CRT , masks turned local races into battlegrounds"
        The CLASS of the headline: <CLASS3>

        The headline: "Critical race theory : The education trap"
        The CLASS of the headline: <CLASS4>

        The headline: "Critical Race Theory : What Christians Need to Know"
        The CLASS of the headline: <CLASS4> '''
    elif example_type == "all_actor": 
        return '''The headline: "Teachers Unions Push CRT in Schools"
        The CLASS of the headline: <CLASS1>

        The headline: "No new teachers in Glen Ellyn sign pledge on Oct . 19 to teach Critical Race Theory"
        The CLASS of the headline: <CLASS1>

        The headline: "Department of Education wisely retreats from critical race theory"
        The CLASS of the headline: <CLASS1>

        The headline: "Racist CRT Lessons in Public School Classrooms"
        The CLASS of the headline: <CLASS1>

        The headline: "Critical Race Theory Is a Potent Issue in the Virginia Governor Race"
        The CLASS of the headline: <CLASS2>

        The headline: "Wisconsin assembly passes bill banning critical race theory in the classroom"
        The CLASS of the headline: <CLASS2>

        The headline: "CRT is dividing Democrats and rallying Republicans"
        The CLASS of the headline: <CLASS2>

        The headline: "UCLA database reveals well - funded push for critical race theory , argues Cornell law professor"
        The CLASS of the headline: <CLASS2>

        The headline: "WATCH : Parents , Activists Protest CRT at Texas School Board Meeting"
        The CLASS of the headline: <CLASS3>

        The headline: "Local Parents Speak Out Against Critical Race Theory | News Radio 101 . 9 Big WAAX"
        The CLASS of the headline: <CLASS3>

        The headline: "Critical Race Theory Aims to Turn Students Into  Red Guards , Chinese American Warns By Terri Wu"
        The CLASS of the headline: <CLASS3>

        The headline: "Fears about CRT , masks turned local races into battlegrounds"
        The CLASS of the headline: <CLASS3>

        The headline: "What Is Critical Race Theory Anyway ?"
        The CLASS of the headline: <CLASS4>

        The headline: "COMMENTARY : The truth about CRT"
        The CLASS of the headline: <CLASS4>
        
        The headline: "Critical race theory : The education trap"
        The CLASS of the headline: <CLASS4>

        The headline: "Critical Race Theory : What Christians Need to Know"
        The CLASS of the headline: <CLASS4>'''
    
    elif example_type == "uncontested_stance": 
        return '''The headline: "Ted Cruz Says Critical Race Theory Is  Every Bit As Racist As The Klansmen In White Sheets"
        The CLASS of the headline: <CLASS1>

        The headline: "The Left Assault on  Racist  Math Continues : DeSantis Rejects CRT - Riddled Textbooks"
        The CLASS of the headline: <CLASS1>

        The headline: "The librarians uniting to battle school book ban laws"
        The CLASS of the headline: <CLASS2>

        The headline: "Guest commentary : Legislation on critical race theory isn't a good idea"
        The CLASS of the headline: <CLASS2>

        The headline: "Where Are Black Parent Voices on Critical Race Theory ?"
        The CLASS of the headline: <CLASS3>

        The headline: "Critical race theory bill gets first vote from Kentucky lawmakers"
        The CLASS of the headline: <CLASS3>'''
    elif example_type == "contested_stance": 
        return '''The headline: "GOP : The Fight Against Critical Race Theory Has Only Just Begun"
        The CLASS of the headline: <CLASS1>

        The headline: "CURRICULUM CONTROVERSY : District responds to claims it will implement CRT , gender identity lessons"
        The CLASS of the headline: <CLASS1>

        The headline: "Demonizing Critical Race Theory | History News Network"
        The CLASS of the headline: <CLASS2>

        The headline: "Biden signs Emmett Till Antilynching Act as CRT bans restrict talk of race"
        The CLASS of the headline: <CLASS2>

        The headline: "North Hunterdon librarian who fought LGBTQ book ban honored"
        The CLASS of the headline: <CLASS3>

        The headline: "General Milley is clueless on critical race theory"
        The CLASS of the headline: <CLASS3>'''
    elif example_type == "all_stance": 
        return '''The headline: "Ted Cruz Says Critical Race Theory Is  Every Bit As Racist As The Klansmen In White Sheets"
        The CLASS of the headline: <CLASS1>

        The headline: "The Left Assault on  Racist  Math Continues : DeSantis Rejects CRT - Riddled Textbooks"
        The CLASS of the headline: <CLASS1>

        The headline: "GOP : The Fight Against Critical Race Theory Has Only Just Begun"
        The CLASS of the headline: <CLASS1>

        The headline: "CURRICULUM CONTROVERSY : District responds to claims it will implement CRT , gender identity lessons"
        The CLASS of the headline: <CLASS1>

        The headline: "The librarians uniting to battle school book ban laws"
        The CLASS of the headline: <CLASS2>

        The headline: "Guest commentary : Legislation on critical race theory isn't a good idea"
        The CLASS of the headline: <CLASS2>

        The headline: "Demonizing Critical Race Theory | History News Network"
        The CLASS of the headline: <CLASS2>

        The headline: "Biden signs Emmett Till Antilynching Act as CRT bans restrict talk of race"
        The CLASS of the headline: <CLASS2>

        The headline: "Where Are Black Parent Voices on Critical Race Theory ?"
        The CLASS of the headline: <CLASS3>

        The headline: "Critical race theory bill gets first vote from Kentucky lawmakers"
        The CLASS of the headline: <CLASS3>
        
        The headline: "North Hunterdon librarian who fought LGBTQ book ban honored"
        The CLASS of the headline: <CLASS3>

        The headline: "General Milley is clueless on critical race theory"
        The CLASS of the headline: <CLASS3>'''
    else: 
        return None

def get_one_actor(headline, examples): 
    actor_prompt = f'''You will be given a news headline related to critical race theory (CRT). Your response should identify the CLASS of the headline. Your response must be one of the following predefined labels: <CLASS1>, <CLASS2>, <CLASS3>, or <CLASS4>. 

    Here are some examples of correct classification responses. 

    {examples}

    Please consider the following headline: "{headline}"
    What is the CLASS in this headline? Please respond with exactly one of the following predefined labels that best describes the CLASS in this headline: <CLASS1>, <CLASS2>, <CLASS3>, or <CLASS4>. '''

    message = [
        {"role": "user", "content": actor_prompt}
    ]

    completion = get_gpt_response(message)
    return completion

def get_one_stance(headline, examples): 
    stance_prompt = f'''You will be given a news headline related to critical race theory (CRT). Your response should identify the CLASS of the headline. Your response must be one of the following predefined labels: <CLASS1>, <CLASS2>, or <CLASS3>. 

    Here are some examples of correct classification responses. 

    {examples}

    Please consider the following headline: "{headline}"
    What is the CLASS in this headline? Please respond with exactly one of the following predefined labels that best describes the CLASS in this headline: <CLASS1>, <CLASS2>, or <CLASS3>. '''

    message = [
        {"role": "user", "content": stance_prompt}
    ]

    completion = get_gpt_response(message)
    return completion

def get_many_labels(val, label_type, example_type, outF): 
    '''params: 
    val - validation set
    label_type - one of "actor", "action", "action direction", or "headline stance"'''
    headlines = list(val['Title'])

    # set examples
    e = get_examples(example_type)
    
    # get actor labels
    preds = []
    labels = list(val[label_type])
    for h, label in zip(headlines, labels): 
        if label_type == "actor": 
            resp = get_one_actor(h, e)
        elif label_type == "headline stance": 
            resp = get_one_stance(h, e)
        else: 
            print(f"ERROR: no label_type {label_type}")
            return None
        pred = resp.content
        preds.append(pred)
        print(f"headline: {h}")
        print(f"predicted: {pred}")
        print(f"actual: {label}")

    val.insert(2, f"{label_type}_pred", preds)
    val.to_csv(outF)


def main():
    # read in test data
    val = pd.read_csv("GPT_validation_data.csv")
    print(val.shape)

    # get actor labels for validation dataset
    # get_many_labels(val, "actor", "uncontested_actor", "baseline_approach/n=2_uncontested/actor_preds.csv")
    # get_many_labels(val, "actor", "contested_actor", "baseline_approach/n=2_contested/actor_preds.csv")
    # get_many_labels(val, "actor", "all_actor", "baseline_approach/n=4/actor_preds.csv")

    # get headline stance labels for validation dataset
    # get_many_labels(val, "headline stance", "uncontested_stance", "baseline_approach/n=2_uncontested/stance_preds.csv")
    # get_many_labels(val, "headline stance", "contested_stance", "baseline_approach/n=2_contested/stance_preds.csv")
    # get_many_labels(val, "headline stance", "all_stance", "baseline_approach/n=4/stance_preds.csv")
    


main()
