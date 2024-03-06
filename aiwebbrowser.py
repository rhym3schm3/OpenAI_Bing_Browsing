from openai import OpenAI

import os
import requests
bing_api_key = os.getenv('BING_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

def search_bing(query):
    headers = {"Ocp-Apim-Subscription-Key": bing_api_key}
    params = {"q": query, "textDecorations": True, "textFormat": "HTML"}
    search_url = "https://api.bing.microsoft.com/v7.0/search"
    response = requests.get(search_url, headers=headers, params=params)
    return response.json()

def summarize_with_openai(text):
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # Make sure to use the correct and latest model
        messages=[{
                "role": "user",
                "content":  f"Summarize the following: {text}"
            }],
        temperature=0.7,
        max_tokens=300)
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
user_query = input("Please enter your question: ")
search_results = search_bing(user_query)

# Assuming search_results is properly structured and contains the necessary data
if 'webPages' in search_results and 'value' in search_results['webPages']:
    text_to_summarize = " ".join([result['snippet'] for result in search_results['webPages']['value']])
    summary_response = summarize_with_openai(text_to_summarize)
    if summary_response:
        print(summary_response.choices[0].message.content)
