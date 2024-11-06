import gradio as gr
import requests
import json


def process_query(message, history):
    
    fp = open('config.json')
    config = json.load(fp)
    fp.close()

    myobj = {'question': message}

    x = requests.post(config['api_url'], json = myobj)

    return json.loads(x.text)['response']

gr.ChatInterface(process_query, 
                    type="messages",
                    title="Specialist in Brazilian Literature 🤓",
                    description="Ask any question and I will try my best to help you!",
                    theme="citrus",
                    examples=[{"text": "Quem é capitu?"}, {"text": "Em qual cidade se passa a história de O Cortiço?"}],
                ).launch()

