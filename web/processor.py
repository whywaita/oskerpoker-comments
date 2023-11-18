import os
import time

import sqlalchemy.exc
import yt_dlp

from web.models import db, Queue, Movie
from web import app

import movieparser


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
