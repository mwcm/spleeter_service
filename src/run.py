from gevent import monkey

monkey.patch_all()
from api.views import app

app = Flask(__name__)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=7000, gevent=100, threaded=True)
