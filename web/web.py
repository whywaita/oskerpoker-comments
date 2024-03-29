import json
import typing
import os
import re
import logging

import sqlalchemy.exc
from flask import Flask, request, redirect, url_for, render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import yt_dlp

from web.models import db, Queue, Movie

app = Flask(__name__)
secret_key = os.environ.get('SECRET_KEY')
if not secret_key:
    raise Exception('SECRET_KEY is not set')
app.secret_key = secret_key

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL', 'sqlite:///queue.db')
# app.config["SQLALCHEMY_ECHO"] = True
db.init_app(app)


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    queue = db.session.query(Queue).order_by(Queue.id).limit(5).all()
    movie = db.session.query(Movie).order_by(Movie.id.desc()).limit(5).all()
    movie = pretty_text(movie)

    return render_template('index.html', queue=queue, movie=movie)


def pretty_text(ms: typing.List[Movie]) -> typing.List[Movie]:
    for movie in ms:
        try:
            pt = movie.parsed_text
            prettied_text = ''
            for line in pt.split('\n'):
                if not line:
                    continue
                match = re.match(r'(\d+:\d+:\d+)', line)
                if match:
                    timestamp = match.group()
                else:
                    timestamp = '00:00:00'

                players = line.removeprefix(timestamp).strip()
                h, m, s = map(int, timestamp.split(':'))
                timestamp_second = h * 3600 + m * 60 + s
                link = f"https://www.youtube.com/watch?v={movie.movie_id}&t={timestamp_second}s"
                prettied_text += f'<a href="{link}">{timestamp}</a> {players}<br>'
        except AttributeError or ValueError or TypeError as e:
            logging.warning(f'Failed to parse {movie.title}: {e}')
            prettied_text = movie.parsed_text
        movie.parsed_text = prettied_text
    return ms


@app.route('/enqueue', methods=['POST'])
def enqueue():
    oskerpoker_channel_id = "UC_gAHSMwNCSj0U10fpxc8SQ"

    if request.method != 'POST':
        return 'Invalid method'

    movie_id = request.form['movie_id']
    if not movie_id:
        flash('Movie ID is required', 'error')
        return redirect(url_for('index'))
    u = f"https://www.youtube.com/watch?v={movie_id}"

    with yt_dlp.YoutubeDL({}) as ydl:
        try:
            info_dict = ydl.extract_info(u, download=False)
            video_title = info_dict.get('title', None)
            channel_id = info_dict.get('channel_id', None)
            channel_name = info_dict.get('uploader', None)
            if channel_id != oskerpoker_channel_id:
                flash(f'{channel_name} is invalid channel', 'error')
                return redirect(url_for('index'))
            db_enqueue(db, movie_id)
            flash(f'Enqueued {video_title}', 'success')
            print(f"Enqueued {video_title} {movie_id}")
        except yt_dlp.utils.YoutubeDLError:
            flash(f'{movie_id} is invalid movie id', 'error')
        except sqlalchemy.exc.SQLAlchemyError as e:
            flash(f'DB Error: {e}', 'error')

        return redirect(url_for('index'))


def db_enqueue(db_session: SQLAlchemy, movie_id: str):
    if db_session.session.query(Queue).filter(Queue.movie_id == movie_id).first():
        raise sqlalchemy.exc.SQLAlchemyError('Already enqueued')
    if db_session.session.query(Movie).filter(Movie.movie_id == movie_id).first():
        raise sqlalchemy.exc.SQLAlchemyError('Already parsed')

    db_session.session.add(Queue(movie_id=movie_id))
    db_session.session.commit()


@app.route('/movies')
def movies():
    ms = db.session.query(Movie).order_by(Movie.uploaded_at.desc()).all()
    ms = pretty_text(ms)
    return render_template('movies.html', movie=ms)


@app.route('/api/movie')
def api_movies():
    ms = db.session.query(Movie).order_by(Movie.uploaded_at.desc()).all()
    return jsonify([m.to_dict() for m in ms])


@app.route('/api/queue')
def api_queue():
    qs = db.session.query(Queue).order_by(Queue.id).all()
    return jsonify([q.to_dict() for q in qs])