import mimetypes
from app import app
from flask import render_template, request, send_file, send_from_directory
from app import baixar
import os

@app.route('/')
@app.route('/index')

def index():
    return render_template('home.html')

@app.route('/mp3')

def mp3():
    return render_template('mp3.html')

@app.route('/home')

def home():
    return render_template('home.html')

@app.route('/autenticarmp3', methods = ['GET'])

def autenticarmp3():
    link = request.args.get('link')

    if link:
        info = baixar.details(link)

        return render_template('autenticarmp3.html', info=info )
    else:
        return render_template('mp3.html')

@app.route('/autenticarmp4', methods = ['GET','POST'])

def autenticarmp4():

    link = request.args.get('link')

    if link:
        info = baixar.details(link)

        return render_template('autenticarmp4.html', info=info )
    else:
        return render_template('mp4.html')
    


@app.route('/baixarVideoBest', methods=['POST'])

def baixarVideoBest():
    link = request.form.get('video1080')
    baixado = baixar.baixarVideoBest(link)
    return send_file(baixado, as_attachment=True)


@app.route('/baixarVideo', methods=['POST'])

def baixarVideo():
    link = request.form.get('video360')
    baixar.baixar_video(link)
    # mime_type, _ = mimetypes.guess_type(baixado)
    return True


@app.route('/baixaraudio50', methods=['POST'])
def baixaraudio50():
    link = request.form.get('audio50')
    baixado = baixar.baixar_audio_50(link)
    return send_file(baixado, as_attachment=True)

@app.route('/baixaraudio70', methods=['POST'])
def baixaraudio70():
    link = request.form.get('audio70')
    baixado = baixar.baixar_audio_70(link)
    return send_file(baixado, as_attachment=True)

@app.route('/baixaraudio160', methods=['POST'])
def baixaraudio160():
    link = request.form.get('audio160')
    baixado = baixar.baixar_audio_160(link)
    return send_file(baixado, as_attachment=True)