## Picovoice Porcupine Wakeword plugin for Mycroft

This plugins allows using [Porcupine](https://github.com/Picovoice/porcupine) wakewords together with Mycroft.

## Configuration
To activate the plugin edit the mycroft config using the `mycroft-config edit user` command and add a hotword section if it doesn't already exist

```
[...]
  "hotwords": {

  }
```

Then insert a new hotword into the `hotwords` section

```
    "blueberry": {
      "module": "porcupine_wakeword_plug",
      "keyword_file_path": "~/.mycroft/blueberry_linux.ppn",
      "sensitivity": 0.5
    }
```

Above is using the _blueberry_ model provided by picovoice stored in the location `~/.mycroft/blueberry_linux.ppn` and a sensitivity of 0.5.

## Models
Some models are available without charge from the [picovoice repo](https://github.com/Picovoice/porcupine/tree/master/resources/keyword_files), you can also generate models using the [Picovoice console](https://console.picovoice.ai/)

## Supported platforms

Porcupine ships precompiled binaries for several common platforms (x86 amd64, raspberry Pi, and several more) but may not work on your platform. Check their repo for more details.

## Credits

The original Mycroft bindings for Porcupine was written by @Tanel.Alumae, this plugin is based upon their initial work with some updates for newer Porcupine releases.
