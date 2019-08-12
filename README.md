# galaxest

**galaxest** is a CLI (Command Line Interface) software to help developer/tester to run automation test through any device farms agnostically.

## Installation & Setup

### Requirements
 - Mac OS / Linux Debian based
 - Python 2.7
 - Python PIP
 - ADB properly setup

### Installation
You must have all of the requirements installed first. Then you can simply install via Python PIP:
```
pip install galaxest
```

### Setup
You have to setup your app after the installation success. type command below if this is your first setup:
```
galaxest
```
or you can type below command if you want to re-setup your configuration:
```
galaxest --reset-config
```
It will show a dialogue to prompt you about the setup. Choose **Yes** if you are ready to do the setup.

You'll be asked to choose the device farm sources available for your project. You can choose more than one device farm source if you have it. You have to type <kbd>&#8594;</kbd> for each options you choose until the indicator shows **X** while **O** means you are not choosing the option.

### OpenSTF Device Farm Setup
You'll need **host**,**api key**, and **adb public key** of the OpenSTF to make your app works with OpenSTF Device Farm.
1. Please put your OpenSTF host address completely like example :
```
http://mystf.com:7100
```
2. Then you have to generate your OpenSTF API Key from your OpenSTF Dashboard and put the API Key to the setup dialogue.
3. Last, you need to register your ADB Public Key to your OpenSTF account in order to do remote connect and do some adb commands through the device.
4. It will check if the app is able to connect to the OpenSTF Device Farm.

Next, You'll be asked to choose one automation tool that you use in your computer.

### Katalon Automation Tool Setup
There are some questions to make galaxest working perfectly with your Katalon.
1. The Katalon Application Path
2. Your Automation Project
3. The project file

## Features

### Help
```
galaxest --help
```

### Connect
If you want to connect randomly to a device:
```
galaxest -c
```
Or if you want to connect to a desired device:
```
galaxest -c <serial_id>
```

### Disconnect
```
galaxest -d <serial_id>
```

### Run a Test
```
galaxest -r <test_suite_name> --by <parallel_type> --opts <additional run options>
```

## License

See [LICENSE](LICENSE).

Copyright © 2019 The galaxest Project. All Rights Reserved.

[contact-link]: mailto:pancaprima8@gmail.com
