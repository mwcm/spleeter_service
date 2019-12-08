import os
import redis
from uuid import uuid4
from app import app


from app.main.seperator import SimpleSeparator
from rq import Queue, Connection


def allowed_extensions(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


def generate_random_filename(upload_directory, extension):
    filename = str(uuid4())
    filename = os.path.join(upload_directory, filename + "." + extension)
    return filename


def separate_helper(filename, n):
    allowed_n = ["2", "4", "5"]
    if n not in allowed_n:
        n = "2"
    separator = SimpleSeparator(f"spleeter:{n}stems")
    with Connection(redis.from_url(app.config["REDIS_URL"])):
        q = Queue()
        task = q.enqueue(
            separator.separate_to_file,
            f'{app.config["SPLEETER_IN"]}{filename}',
            destination=f'{app.config["SPLEETER_OUT"]}',
            filename_format="{instrument}.{codec}",
        )
    response_object = {"status": "success", "data": {"task_id": task.get_id()}}
    return response_object
