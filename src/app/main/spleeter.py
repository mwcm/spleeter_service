from app import app

from spleeter.audio.adapter import get_default_audio_adapter
from spleeter.separator import Separator


def spleeter_setup():
    separators = dict()
    for model in ["2stems", "4stems", "5stems"]:
        separators[int(model[0])] = Separator(f"spleeter:{model}")
    audio_loader = get_default_audio_adapter()
    return separators, audio_loader
