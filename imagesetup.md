# Arthur Image Setup

You can run our solution by following the readme and related guides. It takes a bit of effort, so we decided to share a ready made image as well, to get you started as fast as possible. You can download our ready made image for ISSPI. If you would like to roll your own, you can follow the simple guide below.

## Setup ISSPI image

Here are the steps to follow to reproduce the results we have at Raspberry Valley. You start by rolling your own Pi image.

* Setup a base image. We assume you would like to use a headless image. We have a full guide at the Raspberry Valley knowledge base: setup an [IoT Raspberry Pi Device](http://raspberry-valley.azurewebsites.net/IoT-Raspberry-Pi-Device/). We suggest to use the latest Raspbian base (Lite).
	* If you access the device from Windows for further development, ensure Samba is installed ([Samba guide](http://raspberry-valley.azurewebsites.net/Samba/))
	* Setting up a nice looking Hostname is a good idea (you will be accessing the IISPI from phone or PC)
	* \[alternative\] If you prefer Docker on your Pi, please start with our [Docker IoT Device guide](http://raspberry-valley.azurewebsites.net/IoT-Raspberry-Pi-Device-on-Docker/)
* The IoT guide mentions several Python dependencies. Our code is intended for Python 3, so you might want to duplicate the dependency installation for both versions available on the Pi image (2.x and 3.x). Specifically, you have to make sure the following pre-requisites are met:
	* pip
	* pip3
	* paho libraries for Python 2 and Python 3. 
* For convenience, make your Python 3 default. Check our guide [here](http://raspberry-valley.azurewebsites.net/Python-Default-Version/)
* Clone our code
* \[optional\] Modify the **launcher.py** file if needed. The launcher is built around this guide, so you are probably safe if you don't
* Setup your launcher to be launched at system startup. You can follow our [Autorun Python Script](http://raspberry-valley.azurewebsites.net/Autorun-Python-Script/) guide.
