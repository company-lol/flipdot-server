# Flipdot Sign API

A simple http endpoint for pushing json serialized `numpy` arrays directly to the Hanover flipdot display. 

Uses `pyflidot` to interface with the sign. It is small, simple and the best python3 flipdot class.

## API

Endpoint: `/api/dots`

Post a json serialized `numpy` array directly to the endoint.

### Example Curl request

    curl -X POST -H "Content-Type: application/json" -d @nparray_test.json http://localhost:8080/api/dots


**That is it. That is the api.**

## Getting Started

I am assuming you are on linux. It sohuld work under osx, but I cannot promise anything. 

### Checkout sourcecode

Check out this repo:

    git clone https://github.com/company-lol/flipdot-server.git
    flipdot-server.git

Edit the config file

    cp config.ini.example config.ini
    vi config.ini

You will want to make sure that the config file has all the right items in it and that they match your install:

    ; config.ini
    [SERVER]
    HOST = 0.0.0.0
    PORT = 8080

    [FLIPDOTSIGN]
    COLUMNS = 96
    ROWS = 16
    ADDRESS = 1
    USB = "/dev/ttyUSB0"
    SIMULATOR = True


### Run server

Build the app, cp the config example to config.ini, and run the server:

    pip3 install -r requirements.txt
    python3 app.py

Should output something like: 

    DEBUG:asyncio:Using selector: KqueueSelector
    INFO:__main__:Instantiating server
    INFO:__main__:Creating web app
    INFO:__main__:Starting background tasks

### Use Docker

Docker should be pretty straight forward. 

    docker-compose build
    docker-compose up

If you want to have it connect to your USB serial adapter you will need to edit the `docker-compose.yml` file and un-comment out the following:

    #devices:
    #  - "/dev/ttyUSB0:/dev/ttyUSB0"

to 

    devices:
      - "/dev/ttyUSB0:/dev/ttyUSB0"

## Using the API

If you are testing or getting started, you should go ahead and enable the simulator. This allows you to see what would be pushed through to the flipdot display without actually having the display hooked up. A nice way to debug.  You can ensure that the simlulator is enabled by making sure the `SIMULATOR = True` in the `config.ini`.

Once you have everything configured and it works - you can change the `config.ini` to `SIMULATOR = False` and edit the `docker-compose.yml` to enable the USB device to be passed through.

### Creating numpy arrays

You can create a numpy array represents all of the pixels of the flipdot display. It must be the same size as your flipdot display. For instance, if the flipdot display is 96x16, then the numpy array should be 96x16 as well. 

#### Example code

    import numpy
    import requests
    import json

    sign_columns = 96
    sign_rows = 16

    image_array = numpy.full((sign_rows, sign_columns), False)
    image_array[0][0] = True
    image_array[sign_rows-1][sign_columns-1] = True

    url = "http://localhost:8080/api/dots"

    headers = {'Content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(image_array.tolist()), headers=headers)

This will push a numpy array to your api endpoint that has a pixel in the top left and a pixel in the bottom right.

## Utilities

I will create some utility scripts that can use this API. I am thinking about making: 

* Clock - A simple clock that is cron based that pings the API on the minute to display a clock
* MQTT Text renderer - a simple mqtt listener that posts a payload to the sign
* Image renderer - a way to render images

## Help out

I would love a solid code review of the server `app.py` and some help making sure my async code works. ;) 



