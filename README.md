# SwagScanner

SwagScanner is a device that can scan your small/medium-sized objects into the virtual world. All hardware is designed and built from the ground up. I designed the software pipeline to be extensible, robust, and fast. Compatible with any depth camera--just verify its minimum scanning distance and acquire the correct mounting hardware and API and you're good to go. You can find more information about the design process and challenges on [my website](https://www.seanngpack.com/swagscanner/).

## Getting Started

These instructions will guide you through the process of setting up Swag Scanner on your local machine. Complete BOM for the hardware coming soon.

### Prerequisites

Currently MacOS and Linux are the only supported platforms due to non-universal Bluetooth low-energy libraries. Let's get started with installing non-pip libraries:


```
# Installing pyrealsense2
$ git clone https://github.com/IntelRealSense/librealsense
$ cd librealsense
$ mkdir build
$ cd build
$ cmake ../ -DBUILD_PYTHON_BINDINGS=bool:true
$ make -j4
$ sudo make install
$ export PYTHONPATH=$PYTHONPATH:/usr/local/lib or add that to your .bashrc
```



### Installing

Let's setup your Swag Scanner environment


```
$ git clone https://github.com/seanngpack/swag-scanner/
$ cd swag-scanner
$ virtualenv venv
$ source venv/bin/activate
$ (venv) pip install -r requirements.txt
$ (venv) pip install -e .
```
```
# Installing Adafruit's bluetooth library

$ (venv) git clone https://github.com/adafruit/Adafruit_Python_BluefruitLE
$ (venv) cd Adafruit_Python_BluefruitLE
$ (venv) python setup.py install
```

## Authors

* **Sean Ng Pack** - *literally everything* - [seanngpack.com](https://www.seanngpack.com)


## License

This project is licensed under the MIT License
