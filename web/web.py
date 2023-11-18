import time
import typing
import os
import re

import sqlalchemy.exc
from flask import Flask, request, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
import yt_dlp

from web.models import db, Queue, Movie
import movieparser

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
        pt = movie.parsed_text
        prettied_text = ''
        for line in pt.split('\n'):
            if not line:
                continue
            timestamp = re.match(r'(\d+:\d+:\d+)', line).group()
            players = line.removeprefix(timestamp).strip()
            h, m, s = map(int, timestamp.split(':'))
            timestamp_second = h * 3600 + m * 60 + s
            link = f"https://www.youtube.com/watch?v={movie.movie_id}&t={timestamp_second}s"
            prettied_text += f'<a href="{link}">{timestamp}</a> {players}<br>'
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


def execute_queue():
    while True:
        process_queue()
        time.sleep(1)


def process_queue():
    with app.app_context():
        queue = db.session.query(Queue).order_by(Queue.id).limit(5).all()
        if not queue:
            return

        for q in queue:
            try:
                if db.session.query(Movie).filter(Movie.movie_id == q.movie_id).first():
                    db.session.delete(q)
                    db.session.commit()
                    continue

                movie_id = q.movie_id
                u = f"https://www.youtube.com/watch?v={movie_id}"
                ydl_opts = {
                    'outtmpl': 'tmp/%(id)s.%(ext)s',
                }
                # Update queue status to processing
                print(f"Processing start {movie_id}")
                q.status = 'processing (downloading)'
                db.session.commit()
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([u])
                    info_dict = ydl.extract_info(u, download=False)
                    video_title = info_dict.get('title', None)
                    file_path = f'tmp/{movie_id}.mp4'
                    print(f"Downloaded {video_title}")

                    q.status = 'processing (parsing)'
                    db.session.commit()

                    flop_time_list = movieparser.parse_movie(file_path)
                    comment = movieparser.get_timestamp_comment_from_list(flop_time_list)
                    print(f"Parsed {video_title}")
                    print(comment)

                    db.session.add(Movie(movie_id=movie_id, title=video_title, parsed_text=comment))
                    db.session.delete(q)
                    db.session.commit()

                    # Remove tmp file
                    os.remove(file_path)
            except (yt_dlp.utils.YoutubeDLError, sqlalchemy.exc.SQLAlchemyError) as e:
                print(e)
                q.status = 'error {e}'
                db.session.commit()
                continue
