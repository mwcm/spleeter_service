from app import app
import redis
from rq import Connection, Worker


def run_worker():
    redis_connection = redis.from_url(app.config["REDIS_URL"])
    with Connection(redis_connection):
        worker = Worker(app.config["REDIS_QUEUES"])
        worker.work()


if __name__ == "__main__":
    run_worker()
