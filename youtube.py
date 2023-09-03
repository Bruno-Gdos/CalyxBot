import pytube
from pytube import YouTube
import re 
from pytube.exceptions import VideoUnavailable

def download_link(video_link:str):
    if re.match(r'^https:\/\/www\.youtube\.com\/watch\?v=', video_link):
        try:
            video_url = YouTube(video_link)
            video = video_url.streams.get_highest_resolution()
            download_link = video.url
            return download_link
                
        except VideoUnavailable:
            return "O vídeo não está disponível."

        except Exception as e:
            return "Ocorreu um erro ao processar o vídeo."

    else:
        return "Por favor, insira um link válido de vídeo do YouTube."
