# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Picovoice Porcupine wakeword plugin for Mycroft Core."""
from os.path import expanduser
import struct

from ovos_plugin_manager.templates.hotwords import HotWordEngine
from ovos_utils.log import LOG


class PorcupineWakeword(HotWordEngine):
    """Hotword engine using picovoice's Porcupine hot word engine."""
    def __init__(self, key_phrase="hey mycroft", config=None, lang="en-us"):
        super().__init__(key_phrase, config, lang)
        keyword_file_paths = [expanduser(x.strip()) for x in self.config.get(
            "keyword_file_path", "hey_mycroft.ppn").split(',')]
        sensitivities = self.config.get("sensitivities", 0.5)
        access_key = self.config.get("access_key", None)

        try:
            import pvporcupine
            from pvporcupine.util import (pv_library_path,
                                          pv_model_path)
        except ImportError as err:
            raise Exception(
                "Python bindings for Porcupine not found. "
                "Please run \"mycroft-pip install pvporcupine\"") from err

        if isinstance(sensitivities, float):
            sensitivities = [sensitivities] * len(keyword_file_paths)
        else:
            sensitivities = [float(x) for x in sensitivities.split(',')]

        self.audio_buffer = []
        self.has_found = False
        self.num_keywords = len(keyword_file_paths)


        LOG.info(
            'Loading Porcupine using keyword path {} and sensitivities {}'
            .format(keyword_file_paths, sensitivities))
        self.porcupine = pvporcupine.create(
            access_key,
            keyword_paths=keyword_file_paths,
            sensitivities=sensitivities)

        LOG.info('Loaded Porcupine')

    def update(self, chunk):
        """Update detection state from a chunk of audio data.

        Arguments:
            chunk (bytes): Audio data to parse
        """
        pcm = struct.unpack_from("h" * (len(chunk)//2), chunk)
        self.audio_buffer += pcm
        while True:
            if len(self.audio_buffer) >= self.porcupine.frame_length:
                result = self.porcupine.process(
                    self.audio_buffer[0:self.porcupine.frame_length])
                # result will be the index of the found keyword or -1 if
                # nothing has been found.
                self.has_found |= result >= 0
                self.audio_buffer = self.audio_buffer[
                    self.porcupine.frame_length:]
            else:
                return

    def found_wake_word(self, frame_data):
        """Check if wakeword has been found.

        Returns:
            (bool) True if wakeword was found otherwise False.
        """
        if self.has_found:
            self.has_found = False
            return True
        return False

    def stop(self):
        """Stop the hotword engine.

        Clean up Porcupine library.
        """
        if self.porcupine is not None:
            self.porcupine.delete()
