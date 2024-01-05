import query_gpt35
import sys

def get_gpt_response(prompt):
    print("API input: \n", prompt)
    
    # query model
    response = query_gpt35.single_query(prompt)
    # print(response)
    completion = response["choices"][0]["message"]["content"]
    print("GPT response:", completion)
    print("GPT finish reason:", response["choices"][0]["finish_reason"])
    return completion

def main():
    test_message = [
        {"role": "user", "content": "Hello!"}
        ]
    gpt_resp = get_gpt_response(test_message)
    return gpt_resp

main()
