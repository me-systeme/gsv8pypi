# gsv8pypi

## Content
Filename | 	Description
--- | ---
gsv8.py | GSV-8 Lib; include this file **only** in your own python script
gsv8.html | GSV-8 Lib documentation (german only)
example_config.py | explains how to config the GSV-8 via the python GSV-8 Lib
example_record.py | explains how to record measure-data and how to get the DIO-Pin level

Filename | 	associated files
--- | ---
gsv8.py | CSVwriter.py, GSV_BasicMeasurement.py, GSV_Exceptions.py, GSV6_AnfrageCodes.py, GSV6_BasicFrameType.py, GSV6_ErrorCodes.py, GSV6_FrameRouter.py, GSV6_MessFrameHandler.py, GSV6_Protocol.py, GSV6_SeriallLib.py, GSV6_UnitCodes.py, ThreadSafeVar.py
gsv8.html | _static folder
example_config.py | GSV-8 Lib (gsv8.py)
example_record.py | GSV-8 Lib (gsv8.py)

## How to run

You will need to have the following installed on the RPi to run the project: 

* Python 2.7
* PySerial

### install
#### pip
	cd ~/downloads
	wget https://bootstrap.pypa.io/get-pip.py
	python get-pip.py
	
#### PySerial
	pip install pyserial
	
### run example_config.py
first check wich serial port to be used and alter the follwing line

    dev1 = gsv8(21, 115200)
    
**Note:** for windows use com-port numbers like 0 for COM1 or 21 for COM22 or use an string like "COM22"

now it's time tu execute the example pythn script

    python example_config.py
    
**Note:** the gsv8 lib is written in **Python 2.7**