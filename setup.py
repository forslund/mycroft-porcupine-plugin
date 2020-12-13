#!/usr/bin/env python3
from setuptools import setup

PLUGIN_ENTRY_POINT = ('porcupine_wakeword_plug = '
                      'mycroft_porcupine_plugin:PorcupineWakeword')

setup(
    name='mycroft-porcupine-plugin',
    version='1',
    description='A Wakeword plugin for mycroft',
    author='Åke Forslund',
    author_email='ake.forslund@gmail.com',
    packages=['mycroft_porcupine_plugin'],
    keywords='mycroft plugin tts',
    entry_points={'mycroft.plugin.wake_word': PLUGIN_ENTRY_POINT},
    install_requires=['pvporcupine']
)
