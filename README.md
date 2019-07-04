# Flipdot Sign API

A simple http endpoint for pushing json serialized `numpy` arrays directly to the Hanover flipdot display. 

Uses `pyflidot` to interface with the sign. It is small, simple and the best python3 flipdot class.

## API

Endpoint: `/api/dots`

Post a json serialized `numpy` array directly to the endoint.

### Example Curl request

    curl -X POST -H "Content-Type: application/json" -d @nparray_test.json http://localhost:8080/api/dots


**That is it. That is the api.**


## Creating numpy arrays

You can create a numpy array represents all of the pixels of the flipdot display. It must be the same size as your flipdot display. For instance, if the flipdot display is 96x16, then the numpy array should be 96x16 as well. 

### Example code

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




