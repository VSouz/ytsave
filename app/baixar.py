import os
import shutil
from moviepy.editor import *
from botocore.exceptions import NoCredentialsError
import yt_dlp
import boto3
import requests


s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name='sa-east-1'
)

bucket_name = 'ytsave-storage2'

def generate_presigned_url(bucket_name, object_name, expiration=3600):
    try:
        response = s3.generate_presigned_url('get_object',
                                             Params={'Bucket': bucket_name,
                                                     'Key': object_name},
                                             ExpiresIn=expiration)
    except Exception as e:
        print(e)
        return None
    return response


def upload_to_aws(local_file, bucket, s3_file):
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False



def clear_bucket(bucket):
    try:
        bucket_objects = s3.list_objects_v2(Bucket=bucket)
        if 'Contents' in bucket_objects:
            for obj in bucket_objects['Contents']:
                s3.delete_object(Bucket=bucket, Key=obj['Key'])
        print("Bucket cleared")
    except Exception as e:
        print(f"Error clearing bucket: {e}")


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
    
    if upload_to_aws(file_path, bucket_name, file_name):
        return f"s3://{bucket_name}/{file_name}"
    else:
        return None

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
