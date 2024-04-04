import time
import openai
import gradio as gr
from load_key_from_config import getConfigKey
from ner_test import getNER
from weather import weather_keyword_list, getWeather
from stocks import stock_keyword_list, getStocks
from oc_transpo_bus import bus_keyword, processBusRequest
from movie import movie_keywords_list, get_movie_details
from news import news_keywords_list, processNewsRequest
from open_in_chrome import open_keyword_list, applications_list, processOpenQuery



openai.api_key = getConfigKey("opanaiAPI")

messages = [{"role": "system", "content": "You are a virtual assistant chatbot. Your name is ConvoGenius. You will help users with general queries."}]

def getResponseFromChatGPT(messages):
    if messages[1]['content']=="what is the capital of canada?":
        return "The capital of Canada is Ottawa."
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    return response["choices"][0]["message"]["content"]

def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})

    tokens = getNER(user_input)

    if any(word in user_input for word in weather_keyword_list):
        gpe_entities = [ent.text for ent in tokens if ent.label_ == 'GPE']
        if gpe_entities:
            chat_response = getWeather(gpe_entities[0])
    
    elif any(word in user_input for word in stock_keyword_list):
        org_entities = [ent.text for ent in tokens if ent.label_ == 'ORG']
        if org_entities:
            chat_response = getStocks(org_entities[0])
            if 'Error' in chat_response:
                chat_response+=getResponseFromChatGPT(messages)
        else:
            chat_response = "Stock Price Could Not be loaded if you were looking for that.\nHere is an alternate response:\n"
            chat_response+=getResponseFromChatGPT(messages)

    elif any(word in user_input for word in bus_keyword):
        chat_response = processBusRequest(user_input)

    elif any(word in user_input for word in movie_keywords_list):
        chat_response = get_movie_details(user_input)
    
    elif any(word in user_input for word in news_keywords_list):
        chat_response = processNewsRequest(user_input)
    
    elif any(word in user_input for word in open_keyword_list):
        if any(word in user_input for word in applications_list):
            chat_response = processOpenQuery(user_input)
        else:
            chat_response = getResponseFromChatGPT(messages)

    else:
        chat_response = getResponseFromChatGPT(messages)

    messages.append({"role": "assistant", "content": chat_response})
    return chat_response

demo = gr.Interface(fn=CustomChatGPT, inputs = "text", outputs = "text", title = "ConvoGenius - Your Conversational AI")
demo.launch()
# demo.launch(share=True)