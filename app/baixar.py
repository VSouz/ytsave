import os
import shutil
from moviepy.editor import *
import yt_dlp
import cloudconvert
import requests



def convert_seconds(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h:d}:{m:02d}:{s:02d}"

def details(url):
    ydl_opts = {
        'format': 'best',
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)

    duration = convert_seconds(info_dict['duration'])

    def get_audio_size(format_id):
        audio_stream = next((f for f in info_dict['formats'] if f['format_id'] == format_id), None)
        if audio_stream:
            return f"{audio_stream['filesize'] // (1024 * 1024)} Mb" if 'filesize' in audio_stream else "N/A"
        return "N/A"

    stream_fast = next((f for f in info_dict['formats'] if f['ext'] == 'mp4'), None)
    file_fast = f"{stream_fast['filesize'] // (1024 * 1024)} Mb" if stream_fast and 'filesize' in stream_fast else "N/A"

    stream_best = next((f for f in info_dict['formats'] if f['ext'] == 'mp4'), None)
    file_best = f"{stream_best['filesize'] // (1024 * 1024)} Mb" if stream_best and 'filesize' in stream_best else "N/A"

    audio70size = get_audio_size('140')
    audio160size = get_audio_size('251')
    audio50size = get_audio_size('139')

    info = {
        "img": info_dict.get('thumbnail'),
        "title": info_dict.get('title'),
        "SizeFast": file_fast,
        "SizeBest": file_best,
        "duration": duration,
        "url": url,
        "audio70": audio70size,
        "audio160": audio160size,
        "audio50": audio50size
    }

    return info

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def baixarVideoBest(url):
    pasta = 'videos'

    if os.path.isdir(pasta):
        shutil.rmtree(pasta)

    os.mkdir(pasta)  

    video_temp_path = os.path.join(pasta, 'temp_video.mp4')
    audio_temp_path = os.path.join(pasta, 'temp_audio.mp4')

    ydl_opts_video = {
        'format': 'bestvideo[ext=mp4]',
        'outtmpl': video_temp_path
    }

    ydl_opts_audio = {
        'format': 'bestaudio[abr<=160k][ext=mp4]',
        'outtmpl': audio_temp_path
    }

    with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
        ydl.download([url])

    with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
        ydl.download([url])

    final_path = os.path.join(pasta, 'final_video.mp4')

    
    return final_path


def baixar_video(url):

    pasta = 'videos'  

    if os.path.isdir(pasta):
        shutil.rmtree(pasta)

    os.mkdir(pasta)

    ydl_opts = {
        'noplaylist': True,
        'outtmpl': '\\videos\\%(title)s.%(ext)s'  
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_title = info_dict.get('title', None)
        video_ext = info_dict.get('ext', 'mp4')  
    
   
    file_name = f"{video_title}.{video_ext}"
    file_path = os.path.join('..\\videos', file_name)  
    
    return file_path

def baixar_audio(url, bitrate):

    pasta = 'audios'  

    if os.path.isdir(pasta):
        shutil.rmtree(pasta)

    os.mkdir(pasta)


    ydl_opts = {
        'format': f'bestaudio[abr<={bitrate}]',
        'noplaylist': True,
        'outtmpl': '\\audios\\%(title)s.%(ext)s'
    }


    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        audio_title = info_dict.get('title', None)
        audio_ext = info_dict.get('ext', 'mp4')

    file_name = f"{audio_title}.{audio_ext}"
    file_path = os.path.join('..\\audios', file_name)
    
    
    return file_path

def baixar_audio_70(url):
    return baixar_audio(url, 70)

def baixar_audio_160(url):
    return baixar_audio(url, 160)

def baixar_audio_50(url):
    return baixar_audio(url, 50)
