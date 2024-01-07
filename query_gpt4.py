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
@backoff.on_exception(backoff.expo, openai.RateLimitError)
def completions_with_backoff(**kwargs):
    return client.chat.completions.create(**kwargs)

def single_query(messages,stop="\n\n",maxTokens=128):

    # calculate absolute max tokens in context
    num_prompt_tokens = count_tokens_from_msgs(messages)
    maxTokens = 4096 - num_prompt_tokens 
    # alternatively, keep maxTokens at hard-coded value (500) to avoid buying excessive tokens

    response = {}

    try:
        response = completions_with_backoff(
            model="gpt-4-1106-preview", 
            messages=messages, # previous message history
            temperature=0, # default 1, ranges from 0 to 2, with 0 = more deterministic and 2 = more random
            max_tokens=maxTokens, # max num tokens to generate in completion
            n=1, # default 1, num completions to generate for each prompt
            frequency_penalty=0, # Positive val decreases the model's likelihood to repeat the same line verbatim.
            presence_penalty=0, # Positive val increases the model's likelihood to talk about new topics
            # don't need to specify stop token for chat
    )
    except openai.APIConnectionError as e:
        print(f"Failed to connect to OpenAI API: {e}")
        pass
    except openai.RateLimitError as e:
        # this shouldn't ever happen
        print("Uh oh... exponential backoff isn't working")
        print(f"OpenAI API request exceeded rate limit: {e}")
        pass
    except openai.APIError as e:
        print(f"OpenAI API returned an API Error: {e}")
        pass

    return response

def count_tokens_from_msgs(messages, model="gpt-4-1106-preview"):
    '''Returns the number of tokens in a ChatGPT message history (including system message). 
    Uses gpt-3.5-turbo tokenizer encoding. '''
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
    if len(sys.argv) < 2:
        print("Usage: python query_gpt4.py input")
        return
    result = single_query(sys.argv[1]) 
    print(result)

if __name__ == '__main__':
    main()

