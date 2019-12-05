from gevent import monkey

monkey.patch_all()
from app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=7000, gevent=100, threaded=True)
