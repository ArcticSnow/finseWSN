#!/usr/bin/env python2.7
'''
Script to download webcam images from Finse
Simon Filhol, November 2016

1. webcam @ the research station:
    'http://www.finse.uio.no/news/webcam/'
2. webcam @ the train station:
    'http://www.bt.no/tv/#!/video/100521/finse-stasjon'
'''
import urllib2
from bs4 import BeautifulSoup
from urllib import urlretrieve
import urlparse
import datetime

def download_finse_train_station_cam(path):
    '''
    downlaod image from finse train station webcam.
    :param path: path where to save the images
    :return:
    '''
    url = 'http://www.webcams.travel/webcam/fullscreen/1235134756'

    html = urllib2.urlopen(url)
    soup = BeautifulSoup(html, 'html')
    img = soup.findAll("img")[4]
    img_url = urlparse.urljoin(url, img['src'])
    file_name = 'finse_train_' + str(datetime.datetime.now())[0:10] + \
                       	'_' + str(datetime.datetime.now())[11:13] + '.jpg'
    urlretrieve(img_url, path+file_name)


def download_finse_research_station_cam(path):
    '''
    Downlaod image from finse research station webcam.
        picture taken every hour between  6am and 6pm

    :param path: path where to save the images
    :return:
    '''

    url = 'http://www.finse.uio.no/news/webcam/'

    if datetime.datetime.now().hour>=6 and datetime.datetime.now().hour<=18:
        html = urllib2.urlopen(url)
        soup = BeautifulSoup(html, 'html')
        img=soup.findAll("img")[0]
        img_url = urlparse.urljoin(url, img['src'])
        file_name = 'finse_research' + str(datetime.datetime.now())[0:10] + \
                    '_' + str(datetime.datetime.now())[11:13] + '.jpg'
        urlretrieve(img_url, path+file_name)
