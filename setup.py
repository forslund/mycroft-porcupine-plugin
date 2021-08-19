#!/usr/bin/env python3
from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

PLUGIN_ENTRY_POINT = ('porcupine_wakeword_plug = '
                      'mycroft_porcupine_plugin:PorcupineWakeword')

setup(
    name='mycroft-porcupine-plugin',
    version='0.2.0',
    description='A Porcupine wakeword plugin for mycroft',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Åke Forslund',
    author_email='ake.forslund@gmail.com',
    packages=['mycroft_porcupine_plugin'],
    keywords='mycroft plugin wakeword',
    entry_points={'mycroft.plugin.wake_word': PLUGIN_ENTRY_POINT},
    install_requires=['pvporcupine>=1.9']
)
