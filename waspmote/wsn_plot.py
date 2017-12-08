    #!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

import sys

import os
from pprint import pprint
import requests

'''

Ressources: https://stackoverflow.com/questions/21104592/json-to-pandas-dataframe
'''

def query(limit=100, offset=0, mote=None, sensor=None):
    '''
    Function to query the WSN database.
    :param limit: number of records to query. Ordered from most recent
    :param offset: number of most recent records to skip
    :param mote: Waspmote ID
    :param sensor: sensor tag
    :return: a json variable
    '''
    headers = {'Authorization': 'Token %s' % TOKEN}
    params = {'limit': limit, 'offset': offset, 'mote': mote, 'sensor': sensor}
    response = requests.get('http://hycamp.org/wsn/api/query/',
                            headers=headers, params=params)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    TOKEN = os.getenv('WSN_TOKEN')
    if not TOKEN:
        print("Define the WSN_TOKEN environment variable.")
    else:
        response = query(limit=100, mote=161398434909148276)


        #============================================
        # Convert json to pandas dataframe and plot
