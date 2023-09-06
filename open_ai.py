# -*- coding: utf-8 -*-

import requests
import os

APIKEY = os.getenv('OPEN_AI_TOKEN')

def get_response(prompt):
    headers = {"Authorization": f"Bearer {APIKEY}", "Content-Type": "application/json"}
    id_modelo = "gpt-3.5-turbo"
    link = "https://api.openai.com/v1/chat/completions"
    mensagem = None

    body = {
            "model": id_modelo,
    
            "messages": [
                {"role": "assistant", "content": prompt + "\n\n Responda de forma direta, em um parágrafo curto."},
            ]
            
        }
    try:
        
        response = requests.post(link, headers=headers, json=body)
        response.raise_for_status()
        resposta = response.json()

        if resposta['choices'][0]['message']['content'] == '':
            mensagem = 'Não entendi o que você disse.'
        else:
            mensagem = resposta['choices'][0]['message']['content']
    
    except requests.exceptions.HTTPError as err:
        print(err)
        mensagem = 'Ocorreu um erro ao processar a sua mensagem.'

    return mensagem

def genereate_image(prompt):
    link = "https://api.openai.com/v1/images/generations"

    body = {
            "prompt": prompt,
            "n": 1,
            "size": "512x512",
            "response_format": 'b64_json'
        }
    try:

        headers = {"Authorization": f"Bearer {APIKEY}", "Content-Type": "application/json"}
        response = requests.post(link, headers=headers, json=body)
        response.raise_for_status()
        resposta = response.json()

        if resposta['data'][0]['b64_json'] == '':
            mensagem = 'Ocorreu um erro ao processar a sua mensagem.'
        else:
            mensagem = resposta['data'][0]['b64_json']

    except requests.exceptions.HTTPError as err:
        print(err)
        mensagem = 'Ocorreu um erro ao processar a sua mensagem.'

    return mensagem






if __name__ == "__main__":
   # print(get_response(' como passar na entrevista de emprego?'))
    print(genereate_image('A imagem de um gato'))