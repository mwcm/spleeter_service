from zipfile import ZipFile
from app import app
from app.utils import generate_random_filename
from flask import url_for, redirect
from spleeter.separator import Separator
from spleeter.audio.adapter import get_default_audio_adapter
from spleeter import SpleeterError
from spleeter.utils.configuration import load_configuration

from os.path import basename, join, splitext


class SimpleSeparator(Separator):
    def __init__(self, params_descriptor, MWF=False):
        """ Default constructor.
            :param params_descriptor: Descriptor for TF params to be used.
            :param MWF: (Optional) True if MWF should be used, False otherwise.
            """
        self._params = load_configuration(params_descriptor)
        self._sample_rate = self._params["sample_rate"]
        self._MWF = MWF
        self._predictor = None

    def separate_to_file(
        self,
        audio_descriptor,
        destination,
        audio_adapter=get_default_audio_adapter(),
        offset=0,
        duration=600.0,
        codec="wav",
        bitrate="128k",
        filename_format="{filename}/{instrument}.{codec}",
    ):
        """ Performs source separation and export result to file using
        given audio adapter.
        Filename format should be a Python formattable string that could use
        following parameters : {instrument}, {filename} and {codec}.
        :param audio_descriptor:    Describe song to separate, used by audio
                                    adapter to retrieve and load audio data,
                                    in case of file based audio adapter, such
                                    descriptor would be a file path.
        :param destination:         Target directory to write output to.
        :param audio_adapter:       (Optional) Audio adapter to use for I/O.
        :param offset:              (Optional) Offset of loaded song.
        :param duration:            (Optional) Duration of loaded song.
        :param codec:               (Optional) Export codec.
        :param bitrate:             (Optional) Export bitrate.
        :param filename_format:     (Optional) Filename format.
        """
        waveform, _ = audio_adapter.load(
            audio_descriptor,
            offset=offset,
            duration=duration,
            sample_rate=self._sample_rate,
        )
        sources = self.separate(waveform)
        filename = splitext(basename(audio_descriptor))[0]
        generated = []
        for instrument, data in sources.items():
            formatted_name = filename_format.format(
                filename=filename, instrument=instrument, codec=codec
            )
            path = join(destination, formatted_name,)
            if path in generated:
                raise SpleeterError(
                    (
                        f"Separated source path conflict : {path},"
                        "please check your filename format"
                    )
                )
            generated.append(path)
            audio_adapter.save(path, data, self._sample_rate, codec, bitrate)

        # TODO: set to something more descriptive later
        zip_path = generate_random_filename(destination, "zip")
        with ZipFile(zip_path, "w") as zip:
            for output_path in generated:
                zip.write(output_path, arcname=basename(output_path))
        with app.app_context():
            return url_for("processed_file", filename=basename(zip_path))
