import datetime
import os, sys
import pprint
import requests
from pandas.io.json import json_normalize
import pandas as pd

URL = 'https://hycamp.org/wsn/api/query/v2/'
#URL = 'http://localhost:8000/wsn/api/query/v2/'

def query(
    limit=100, offset=0, # Pagination
    fields=None,         # Fields to return (all by default)
    tags=None,           # Tags to return (all by default)
    debug=False,         # Not sent to the API
    # Filters
    time__gte=None, time__lte=None, # Time is special
    **kw):

    # Parameters
    if time__gte:
        time__gte = time__gte.timestamp()
    if time__lte:
        time__lte = time__lte.timestamp()

    params = {
        'limit': limit, 'offset': offset,               # Pagination
        'time__gte': time__gte, 'time__lte': time__lte, # Time filter
        'fields': fields,
        'tags': tags,
    }

    # Filter inside json
    for key, value in kw.items():
        if value is None:
            params[key] = None
            continue

<<<<<<< HEAD
        if type(value) is datetime.datetime:
            value = int(value.timestamp())

        if isinstance(value, int):
            key += ':int'

        params[key] = value
=======
def get_token():
    try:
        token = os.environ['WSN_TOKEN']
        return token
    except KeyError:
        print "Please set the environment variable WSN_TOKEN in .bashrc as follow: \n\t export WSN_TOKEN=xxxxxxxxxxxxxxxxx "
        sys.exit(1)


def query(limit=100, offset=0, mote=None, xbee=None, sensor=None, tst__gte=None, tst__lte=None, debug=False):
    '''
    Function to query the WSN database and return a Json object
    :param limit: number of records to query. Ordered from most recent
    :param offset: number of most recent records to skip
    :param mote: Waspmote ID
    :param sensor: sensor tag
    :param tst__gte: timestamp with the following format: '%Y-%m-%dT%H:%M:%S+00:00'
    :param tst__lte: timestamp with the following format: '%Y-%m-%dT%H:%M:%S+00:00'
    :return:  a json variable
    '''
    # Paramters
    if tst__gte:
        tst__gte = tst__gte.strftime('%Y-%m-%dT%H:%M:%S+00:00')
    if tst__lte:
        tst__lte = tst__lte.strftime('%Y-%m-%dT%H:%M:%S+00:00')

    params = {
        'limit': limit,
        'offset': offset,
        'mote': mote,
        'xbee': xbee,
        'sensor': sensor,
        'tst__gte': tst__gte,
        'tst__lte': tst__lte,
    }
>>>>>>> 1ccee17b00daaa01ee6b2d2a36112e5712f7f3ad

    # Query
    headers = {'Authorization': 'Token %s' % get_token()}
    response = requests.get(URL, headers=headers, params=params)
    response.raise_for_status()
<<<<<<< HEAD
    json = response.json()
=======
    myjson = response.json()

    # Debug
    if debug:
        pprint.pprint(params)
        pprint.pprint(myjson)
        print()

    return myjson
>>>>>>> 1ccee17b00daaa01ee6b2d2a36112e5712f7f3ad

    # Debug
    if debug:
        pprint.pprint(params)
        pprint.pprint(json)
        print()

<<<<<<< HEAD
    return json


def query_df(limit=100, offset=0, serial=None, fields=None, tags=None, tst__gte=None, tst__lte=None, debug=False):
=======
def query_df(limit=100, offset=0, mote=None, xbee=None, sensor=None, tst__gte=None, tst__lte=None, debug=False):
>>>>>>> 1ccee17b00daaa01ee6b2d2a36112e5712f7f3ad
    '''
    Function to query the WSN database and return data as a Pandas dataframe
    :param limit: number of records to query. Ordered from most recent
    :param offset: number of most recent records to skip
    :param mote: Waspmote ID
    :param sensor: sensor tag
    :param tst__gte: timestamp with the following format: '%Y-%m-%dT%H:%M:%S+00:00'
    :param tst__lte: timestamp with the following format: '%Y-%m-%dT%H:%M:%S+00:00'
    :return:  a json variable
    '''
<<<<<<< HEAD
    # Paramters
    resp = query(
        limit=limit, offset=offset, serial=serial,  fields=fields,  tags=tags,  debug=debug,  time__gte=tst__gte, time__lte=tst__lte)
=======

    resp = query(limit, offset, mote, xbee, sensor, tst__gte, tst__lte, debug)

>>>>>>> 1ccee17b00daaa01ee6b2d2a36112e5712f7f3ad

    df = json_normalize(resp['results'])  # convert json object to pandas dataframe
    try:
        df['timestamp'] = pd.to_datetime(df.epoch, unit='s')
    except:
        print('WARNING: no epoch')
    return df


def query2csv(filepath, sep=',', ret=False, limit=100, offset=0, mote=None, xbee=None, sensor=None, tst__gte=None, tst__lte=None):
    '''
    Function to query hycamp.org for WSN database and save data into a csv file to a specified path and filename

    :param filepath: path and filename
    :param sep: csv separator type (see documentation of pandas to_csv()
    :param ret: boolean for returning a data frame object or not
    :param limit: number of records to query. Ordered from most recent
    :param offset: number of most recent records to skip
    :param mote: Waspmote ID
    :param sensor: sensor tag
    :param tst__gte: timestamp with the following format: '%Y-%m-%dT%H:%M:%S+00:00'
    :param tst__lte: timestamp with the following format: '%Y-%m-%dT%H:%M:%S+00:00'
    :return:
    '''
    try:
        df = query_df(limit=limit, offset=offset, mote=mote, xbee=xbee, sensor=sensor, tst__gte=tst__gte, tst__lte=tst__lte, debug=False)
        df.to_csv(filepath, sep=sep)
        print('=========')
        print('Data saved to ' + filepath)

        if ret:
            return df

    except:
        print('ERROR: query2csv() not successful')


<<<<<<< HEAD
=======
if __name__ == '__main__':
    TOKEN = os.getenv('WSN_TOKEN')
    if not TOKEN:
        print("Define the WSN_TOKEN environment variable.")
    else:
        response = query_df(
            limit=10000,
            #mote=161398434909148276,
            #tst__gte=datetime.datetime(2017, 12, 1)
        )
        pprint.pprint(response)
        response.to_csv('waspmote_test.csv')

>>>>>>> 1ccee17b00daaa01ee6b2d2a36112e5712f7f3ad


a =query_df(limit=1000, serial=3390197892757083161)

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