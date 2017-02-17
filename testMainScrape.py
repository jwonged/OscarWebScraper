# -*- coding: utf8 -*-
import requests
import bs4
import sys
import csv
import codecs
import mainPageScrape

link = 'https://www.mumsnet.com/Talk'
mainPageScrape.getMainPageLinks(link)
