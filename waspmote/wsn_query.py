import datetime
import os, sys
import pprint
import requests
from pandas.io.json import json_normalize
import pandas as pd

URL = 'https://hycamp.org/wsn/api/query/v2/'
#URL = 'http://localhost:8000/wsn/api/query/v2/'
TOKEN = os.getenv('WSN_TOKEN')

def query(
    limit=100, # Pagination
    fields=None,         # Fields to return (all by default)
    tags=None,           # Tags to return (all by default)
    debug=False,         # Not sent to the API
    # Filters
    time__gte=None, time__lte=None, # Time is special
    **kw):
    '''

    :param limit: number of frame to download from now unitl limit
    :param fields: which frame field to return
    :param tags:
    :param debug:
    :param time__gte: start date to downlaod (in datetime format) (gte = great than equal)
    :param time__lte: end date to download (in datetime format)   (lte = less than equal)
    :param kw: orther query parameter such as serial (waspmote serial number)
    :return: a Json object containing the requested data to the server
    '''

    # Parameters
    if time__gte:
        time__gte = time__gte.timestamp()
    if time__lte:
        time__lte = time__lte.timestamp()

    params = {
        'limit': limit,               # Pagination
        'time__gte': time__gte, 'time__lte': time__lte, # Time filter
        'fields': fields,
        'tags': tags,
    }

    # Filter inside json
    for key, value in kw.items():
        if value is None:
            params[key] = None
            continue

        if type(value) is datetime.datetime:
            value = int(value.timestamp())

        if isinstance(value, int):
            key += ':int'

        params[key] = value

    # Query
    headers = {'Authorization': 'Token %s' % TOKEN}
    print(params)
    response = requests.get(URL, headers=headers, params=params)
    response.raise_for_status()
    json = response.json()

    # Debug
    if debug:
        pprint.pprint(params)
        pprint.pprint(json)
        print()

    return json

def get_token():
    try:
        token = os.environ['WSN_TOKEN']
        return token
    except KeyError:
        print("Please set the environment variable WSN_TOKEN in .bashrc as follow: \n\t export WSN_TOKEN=xxxxxxxxxxxxxxxxx ")
        sys.exit(1)

def query_df(
    limit=100, # Pagination
    fields=None,         # Fields to return (all by default)
    tags=None,           # Tags to return (all by default)
    debug=False,         # Not sent to the API
    # Filters
    time__gte=None, time__lte=None, # Time is special
    **kw):
    '''

    :param limit: number of frame to download from now unitl limit
    :param fields: which frame field to return
    :param tags:
    :param debug:
    :param time__gte: start date to downlaod (in datetime format) (gte = great than equal)
    :param time__lte: end date to download (in datetime format)   (lte = less than equal)
    :param kw: orther query parameter such as serial (waspmote serial number)
    :return: a Json object containing the requested data to the server
    '''

    # Parameters
    if time__gte:
        time__gte = time__gte.timestamp()
    if time__lte:
        time__lte = time__lte.timestamp()
    if time__gte and time__lte:
        limit = None

    params = {
        'limit': limit,               # Pagination
        'time__gte': time__gte, 'time__lte': time__lte, # Time filter
        'fields': fields,
        'tags': tags,
    }

    # Filter inside json
    for key, value in kw.items():
        if value is None:
            params[key] = None
            continue

        if type(value) is datetime.datetime:
            value = int(value.timestamp())

        if isinstance(value, int):
            key += ':int'

        params[key] = value

    # Query
    headers = {'Authorization': 'Token %s' % TOKEN}
    print(params)
    response = requests.get(URL, headers=headers, params=params)
    response.raise_for_status()
    json = response.json()

    # Debug
    if debug:
        pprint.pprint(params)
        pprint.pprint(json)
        print()

    df = json_normalize(json['results'])  # convert json object to pandas dataframe
    try:
        df['timestamp'] = pd.to_datetime(df.epoch, unit='s')
    except:
        print('WARNING: no epoch')
    return df
#
# def query_df(limit=100, serial=None, fields=None, tags=None, tst__gte=None, tst__lte=None, debug=False, **kw):
#
#     # Paramters
#     resp = query(
#         limit=limit, serial=serial,  fields=fields,  tags=tags,  debug=debug,  time__gte=tst__gte, time__lte=tst__lte)
#
#     df = json_normalize(resp['results'])  # convert json object to pandas dataframe
#     try:
#         df['timestamp'] = pd.to_datetime(df.epoch, unit='s')
#     except:
#         print('WARNING: no epoch')
#     return df


if __name__ == '__main__':
    # We need an authentication token
    TOKEN = os.getenv('WSN_TOKEN', 'dcff0c629050b5492362ec28173fa3e051648cb1')

    # Number of elements to return in every query
    limit = 2

    # Example 1: Get all the fields and tags of a given mote from a given time.
    # This is good to explore the data, but bad on performance.
    response = query(limit=limit,
        serial=0x1F566F057C105487,
        time__gte=datetime.datetime(2017, 11, 15),
        debug=True,
    )

    # Example 2: Get the RSSI of an Xbee module identified by its address
    print('==============================================')
    response = query(limit=limit,
        source_addr_long=0x0013A2004105D4B6,
        fields=['rssi'],
        debug=True,
    )

    # Example 3: Get the battery and internal temperature from all motes,
    # include the serial tag to tell them apart.
    # Frames that don't have at least one of the fields we ask for will not be
    # included.
    print('==============================================')
    response = query(limit=limit,
        fields=['bat', 'in_temp'],
        tags=['serial'],
        debug=True,
    )

    # Example 4: Get the time the frame was received by the Pi
    print('==============================================')
    response = query(limit=limit,
        serial=408520806,
        fields=['received'],
        debug=True,
)