# -*- coding: utf8 -*-
import requests
import bs4
import sys
import csv
import codecs

#download webpage - input = webpage link
#output requests.models.response object
def download(link):
    res = requests.get(link)
    print(type(res))
    try:
        res.raise_for_status()
    except Exception as e:
        print('issue: %s' %(e))
    return res

def getCategoryLinks(aCategoryList):
    result = []

    category_topics_all = aCategoryList.select('.category_topics_all')
    if not category_topics_all:
        #if category has no subcategories
        #print(aCategoryList.select('a')[0].get('href'))
        #leaving this out first - it goes to a completely diff site
        n=1
    else:
        linkObj = category_topics_all[0].select('ul > li > a')
        for i in range(len(linkObj)):
            #print('https://www.mumsnet.com/'+linkObj[i].get('href'))
            result.append('https://www.mumsnet.com/'+linkObj[i].get('href'))
    return result

def getMainPageLinks(link):
    res = download(link)
    mainPage = bs4.BeautifulSoup(res.text, 'html.parser')
    categoryList = mainPage.select('.category')
    for i in range(len(categoryList)):
        #get all links within a category
        listOfCategoryLinks = getCategoryLinks(categoryList[i])
        for x in range(len(listOfCategoryLinks)):
            print (listOfCategoryLinks[x])

