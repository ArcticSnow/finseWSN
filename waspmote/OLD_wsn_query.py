import datetime
import os
import pprint
import requests
from pandas.io.json import json_normalize

'''
Example script to query data from hycamp.org WSN database.
'''


URL = 'http://hycamp.org/wsn/api/query/'


def query(limit=100, offset=0, mote=None, sensor=None, tst__gte=None, tst__lte=None):
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
        'sensor': sensor,
        'tst__gte': tst__gte,
        'tst__lte': tst__lte,
    }

    # Query
    headers = {'Authorization': 'Token %s' % TOKEN}
    response = requests.get(URL, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def query_df(limit=100, offset=0, mote=None, sensor=None, tst__gte=None, tst__lte=None):
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
    # Paramters
    if tst__gte:
        tst__gte = tst__gte.strftime('%Y-%m-%dT%H:%M:%S+00:00')
    if tst__lte:
        tst__lte = tst__lte.strftime('%Y-%m-%dT%H:%M:%S+00:00')

    params = {
        'limit': limit,
        'offset': offset,
        'mote': mote,
        'sensor': sensor,
        'tst__gte': tst__gte,
        'tst__lte': tst__lte,
    }

    # Query
    headers = {'Authorization': 'Token %s' % TOKEN}
    response = requests.get(URL, headers=headers, params=params)
    response.raise_for_status()
    resp = response.json()

    return json_normalize(resp['results'])


if __name__ == '__main__':
    TOKEN = os.getenv('WSN_TOKEN')
    if not TOKEN:
        print("Define the WSN_TOKEN environment variable.")
    else:
        response = query_df(
            limit=100,
            mote=161398434909148276,
            tst__gte=datetime.datetime(2017, 12, 1)
        )
        pprint.pprint(response)


a =query(limit=1000, mote=3390197892757083161)