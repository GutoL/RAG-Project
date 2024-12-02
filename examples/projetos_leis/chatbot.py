import gradio as gr
import requests
import json


def process_query(message, history):
    
    fp = open('config.json')
    config = json.load(fp)
    fp.close()

    myobj = {'question': message}

    x = requests.post(config['api_url'], json = myobj)

    print(x)
    return json.loads(x.text)['response']

gr.ChatInterface(process_query, 
                    type="messages",
                    title="Estou aqui para te ajudar a entender o que os nossos políticos estão pensando para nós 🤓",
                    description="Me pergunte qualquer coisa que eu vou tentar te ajudar!",
                    theme="citrus",
                    examples=[{"text": "Quais são os ultimos projetos de lei que foram criados?"}, 
                              {"text": "Qual é o projeto de lei mais recente que está sendo analisado no momento?"}],
                ).launch()

