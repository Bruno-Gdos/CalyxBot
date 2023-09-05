import pytube
from pytube import YouTube
import re 
from pytube.exceptions import VideoUnavailable
import requests

def download_link(video_link:str): 
    if re.match(r'^https:\/\/www\.youtube\.com\/watch\?v=', video_link):
        try:
            download = [None, None]
            video_url = YouTube(video_link)
            video = video_url.streams.get_highest_resolution().url
            download[0] = encurtar_link(video)
            download[1] = video_url.title
            return download
                
        except VideoUnavailable:
            return "O vídeo não está disponível."

        except Exception as e:
            return "Ocorreu um erro ao processar o vídeo."

    else:
        return "Por favor, insira um link válido de vídeo do YouTube."
    
def download_audio(video_link:str):
    if re.match(r'^https:\/\/www\.youtube\.com\/watch\?v=', video_link):
        try:
            download = [None, None]
            video_url = YouTube(video_link)
            video = video_url.streams.get_audio_only().url
            download[0] = encurtar_link(video)
            download[1] = video_url.title
            return download
                
        except VideoUnavailable:
            return "O vídeo não está disponível."

        except Exception as e:
            return "Ocorreu um erro ao processar o vídeo."

    else:
        return "Por favor, insira um link válido de vídeo do YouTube."
    

def encurtar_link(url):
    endpoint = 'http://tinyurl.com/api-create.php?url='
    response = requests.get(endpoint + url)
    if response.status_code == 200:
        return response.text
    return None
