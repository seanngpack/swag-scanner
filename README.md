# SwagScanner

SwagScanner is a device that can scan your small/medium-sized objects into the virtual world. All hardware is designed and built from the ground up. I designed the software pipeline to be extensible, robust, and fast. Compatible with any depth camera--just verify its minimum scanning distance and acquire the correct mounting hardware and API and you're good to go. You can find more information about the design process and challenges on [my website](https://www.seanngpack.com/swagscanner/).

## Getting Started

These instructions will guide you through the process of setting up Swag Scanner on your local machine. Complete BOM for the hardware coming soon.

### Prerequisites

Currently MacOS and Linux are the only supported platforms due to non-universal Bluetooth low-energy libraries. The setup process is kind of painful, but I have painstakingly found good, working solutions that you can easily follow along.


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
# Installing basic requirements

$ git clone https://github.com/seanngpack/swag-scanner/
$ cd swag-scanner
$ virtualenv venv
$ source venv/bin/activate
$ (venv) pip install -r requirements.txt
$ (venv) pip install -e .
```

```
# Installing pcl and python-pcl
# cd to some random folder

$ git clone https://github.com/PointCloudLibrary/pcl 
$ mkdir build
$ cd build
$ cmake .. 
$ make
$ sudo make install

# Now we can install python-pcl
# cd to some random folder and have your virtual environment activated

$ (venv) git clone https://github.com/strawlab/python-pcl.git
$ (venv) cd python-pcl
# go into setup.py, change line 710 to the version of vtk that's installed in your system, and change all instances of 'c++11' to 'c++14'
$ (venv) sudo python setup.py clean
$ (venv) sudo make clean
$ (venv) sudo make all
$ (venv) sudo python setup.py install
```

```
# Installing Adafruit's bluetooth library
# cd to some random folder

$ (venv) git clone https://github.com/adafruit/Adafruit_Python_BluefruitLE
$ (venv) cd Adafruit_Python_BluefruitLE
$ (venv) python setup.py install
```

## Authors

* **Sean Ng Pack** - [seanngpack.com](https://www.seanngpack.com)


## License

This project is licensed under the MIT License
