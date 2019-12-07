from gevent import monkey

monkey.patch_all()
from app import app


# ty https://github.com/jqueguiner/spleeter-as-a-service/blob/master/src/app.py
if __name__ == "__main__":

    separators = dict()

    app.run(
        host="0.0.0.0",
        debug=app.config["DEBUG"],
        port=app.config["PORT"],
        gevent=100,
        threaded=True,
    )
