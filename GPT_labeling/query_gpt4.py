import sys
import os
import openai
import backoff 
from openai import OpenAI
import tiktoken

# API reference: https://platform.openai.com/docs/api-reference/chat/create?lang=python
# overview of models: https://platform.openai.com/docs/models/gpt-3-5
# token pricing: https://openai.com/pricing

# properties of gpt-3.5-turbo: 
# Max tokens / max context length: 4096 
# Cost per 1k tokens: $0.002 

client = OpenAI()

# handle rate limit error with exponential backoff
# @backoff.on_exception(backoff.expo, openai.RateLimitError)
# def completions_with_backoff(**kwargs):
#     return client.chat.completions.create(**kwargs)

def single_query(messages,stop="\n\n",maxTokens=256):

    # calculate absolute max tokens in context
    # num_prompt_tokens = count_tokens_from_msgs(messages)
    # maxTokens = 4096 - num_prompt_tokens 
    # alternatively, keep maxTokens at hard-coded value (500) to avoid buying excessive tokens

    response = {}

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview", 
            messages=messages, # previous message history
            temperature=0, # default 1, ranges from 0 to 2, with 0 = more deterministic and 2 = more random
            max_tokens=maxTokens, # max num tokens to generate in completion
            n=1, # default 1, num completions to generate for each prompt
            frequency_penalty=0, # Positive val decreases the model's likelihood to repeat the same line verbatim.
            presence_penalty=0, # Positive val increases the model's likelihood to talk about new topics
    )
    except openai.APIConnectionError as e:
        print(f"Failed to connect to OpenAI API: {e}")
        pass
    except openai.RateLimitError as e:
        # this shouldn't ever happen if exponential backoff is being used 
        print("Uh oh... exponential backoff isn't working")
        print(f"OpenAI API request exceeded rate limit: {e}")
        pass
    except openai.APIError as e:
        print(f"OpenAI API returned an API Error: {e}")
        pass

    return response

def count_tokens_from_msgs(messages, model="gpt-4-1106-preview"):
    '''Returns the number of tokens in a ChatGPT message history (including system message). 
    Uses gpt-4-turbo tokenizer encoding. '''
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens

def main():
    print("input tokens per request", count_tokens_from_msgs([
        {"role": "user", "content": '''News article headlines can shape the ways that people perceive current events and understand the world around them. Therefore, nuances in the headline's language and word choice can be very important. The goal of this task is to identify the stance or bias of a news headline. 

    You will be given a news headline related to critical race theory (CRT). Your response should identify the stance of the headline. Your response must be one of the following predefined labels: <ANTI-CRT>, <DEFENDING CRT>, or <NEUTRAL>. 

    Please carefully consider the following label definitions: 
    <ANTI-CRT> - The headline favors an anti-CRT viewpoint. Its viewpoint appears to oppose CRT, support CRT bans, or make alarmist claims about threats posed by CRT. It has an anti-CRT stance. 
    <DEFENDING CRT> - The headline favors a viewpoint that defends CRT. Its viewpoint appears to support CRT, oppose CRT bans, or minimize the threat posed by CRT-related curricula. It has a stance that defends CRT. 
    <NEUTRAL> - The headline does not have a strong viewpoint. It is neutral or impartial. It reports on news events without favoring one viewpoint or the other (neither anti-CRT nor defending CRT). 

    Note that the impact of the event in the headline is different from the headline stance or bias. For example, consider the following headline: "Florida bans critical race theory from classrooms." For this headline, the action taking place has an anti-CRT impact because the ban would prevent teaching CRT in classrooms. However, in this case, the headline stance is neutral because the headline does not reveal a strong journalistic bias for or against CRT. Therefore, this headline stance would have the <NEUTRAL> label.

    Your interpretations of the headline should be guided by polarizing terms that stand out in the headline, which may indicate the headline's stance. Consider that the headline stance might belong to one of the categories implicitly, without direct reference to exact words or examples provided in the label definition.

    Please consider the following headline: "this is a test"
    Consider any biased framing in the headline. What is the headline's stance? Please respond with exactly one of the following predefined labels that best describes the stance in this headline: <ANTI-CRT>, <DEFENDING CRT>, or <NEUTRAL>. '''
    }
    ]))

    print("output tokens per request", count_tokens_from_msgs([
        {"role": "assistant", "content": '''<NEUTRAL>'''
    }
    ]))

    # if len(sys.argv) < 2:
    #     print("Usage: python query_gpt4.py input")
    #     return
    # result = single_query(sys.argv[1]) 
    # print(result)

if __name__ == '__main__':
    main()

