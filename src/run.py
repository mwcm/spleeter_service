from gevent import monkey

monkey.patch_all()

from app import app

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=app.config["DEBUG"],
        port=app.config["PORT"],
        gevent=100,
        threaded=True,
    )
