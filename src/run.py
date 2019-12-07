from gevent import monkey

monkey.patch_all()
from app import app, store

# from spleeter.audio.adapter import get_default_audio_adapter
# from spleeter.separator import Separator

if __name__ == "__main__":

    # try:
    # separators = dict()
    # for model in ["2stems", "4stems", "5stems"]:
    # separators[int(model[0])] = Separator(f"spleeter:{model}")
    # audio_loader = get_default_audio_adapter()
    # except Exception as e:
    # print(f"EXCEPTION {e}")
    # raise e

    # from app.main.spleeter import spleeter_setup

    # seperators, audio_loader = spleeter_setup(store)

    app.run(
        host="0.0.0.0",
        debug=app.config["DEBUG"],
        port=app.config["PORT"],
        gevent=100,
        threaded=True,
    )
