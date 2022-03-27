from flask import render_template, request, redirect

from app import app
from sensors import sensors


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Erik'}
    posts = [
        {
            'author': {'username': 'Emanuel'},
            'body': 'Sonniges Wetter in Dresden!'
        },
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/value')
def value():
    return request.args.get('value')


@app.route('/temp')
def temp():
    return str(sensors.get_temp_indoor())


@app.route('/remote')
def remote():
    functions = ["Aussenlicht",
                 "Finnhuette",
                 "Pool Pumpe",
                 "Pool Licht",
                 "LED Licht",
                 "Party Licht",
                 "Vitrine",
                 "3D Drucker",
                 "Wasserboiler",
                 "Rolladen"]
    return render_template('remote.html', title='Remote', functions=functions)


@app.route('/old')
def old():
    return render_template('old.html', title='[OLD] Remote')
