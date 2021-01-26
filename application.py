import os
import subprocess
import re
import glob
from random import choice
from flask import Flask, request, redirect, render_template, url_for


app = Flask(__name__)
MEDIA_FOLDER = "/home/daoudi/Projects/ytd/static/media"


def valid_url(url):
    return re.search("^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com))\/watch\?v=[a-zA-Z0-9\_-]+(&list=[a-zA-Z0-9\_-]+)?(&index=[0-9]+)?$", url)


def make_files():
    list_of_files = {}
    for filename in os.listdir(MEDIA_FOLDER):
        list_of_files[filename] = "http://127.0.0.1:5000/static/media/"+filename
    return list_of_files


@app.route('/', methods=['GET', 'POST'])
def ytd():
    if request.method == 'POST':
        url = request.form['url']
        if valid_url(url):
            subprocess.call(['youtube-dl', '--extract-audio', '--audio-format', 'mp3', '-o', '{}/%(title)s.%(ext)s'.format(MEDIA_FOLDER), url])
            return redirect(url_for('ytd'))
    return render_template('home.html', list_of_files=make_files())


@app.route('/clear_storage', methods=['GET', 'POST'])
def clear_storage():
    if request.method == 'POST':
        files = glob.glob('{}/*'.format(MEDIA_FOLDER))
        for f in files:
            os.remove(f)
    return redirect(url_for('ytd')) 
